import re
import collections


# simple parser

# tokens are re.Regexes in a dict
# rules are lists of:
#   strings: UPPERCASE means tokens, lower_case means rules
#   lists  : grouping of strings, last string in list is specifier:
#              ? optional
#              + at least one, maybe more
#              * optional and maybe more


class ParseError(Exception):
    def __init__(self, msg, at=0):
        Exception.__init__(self, msg)
        self.at = at


def pull(input_str, pattern, pattern_table):
    m = pattern_table[pattern].match(input_str)
    if m:
        content = input_str[:m.end()]
        return [input_str[m.end():], content]
    else:
        return None


def greedy(input_str, pattern_table):
    longest_pattern = [0, None]
    for pattern in pattern_table:
        m = pattern_table[pattern].match(input_str)
        if m:
            length = m.end()
            if longest_pattern[0] < length:
                longest_pattern = [length, pattern]
    return longest_pattern


def throw_parse_error(original, pos, text):
    line = 1
    char = 0
    for i in original[:pos]:
        char += 1
        if i == "\n":
            line += 1
            char = 0
    errmsg = "Parse error on line {} at column {}:\n{}".format(line, char, text)
    raise ParseError(errmsg, pos)


def lex(input_str, token_types):
    original_input = input_str[:]
    tokens = []
    pos = 0
    while True:
        if input_str == "":
            break
        length, pattern_type = greedy(input_str, token_types)
        if length == 0: throw_parse_error(original_input, pos, "Invalid token")
        pos += length
        input_str, content = pull(input_str, pattern_type, token_types)
        tokens.append((pattern_type, content, pos - length))
    return tokens


def postlex(tokens):
    new_tokens = []
    for token in tokens:
        if token[0].startswith("%"):
            continue
        new_tokens.append(token)
    return new_tokens


def is_keyword(token):
    return token.sub("", token.pattern.strip("\\"), count=1) == ""


def rule_instance(rulename, token_types, parsetree):
    inst = (rulename, [])
    for value in parsetree:
        if value[0] in token_types:
            if is_keyword(token_types[value[0]]):
                continue
        inst[1].append(value)
    return inst


def rule_is_recursive(rulename, ruletexts):
    return any(x[0] == rulename for x in ruletexts)


def parse_rulename(input_str, rulename, rules, tokens, at, token_types, is_start=False):
    if not rule_is_recursive(rulename, rules[rulename]):
        full_rule = rules[rulename]
        stored_error = []
        for ruletext in full_rule:
            try:
                return consume_rule(input_str, rulename, ruletext, tokens, at, rules, token_types, is_start=is_start)
            except ParseError as e:
                stored_error.append(e)
                continue
        raise ParseError(str(max(stored_error, key=lambda x: x.at)), at=at)
    else:
        current_biggest = None
        full_rule = rules[rulename]
        stored_error = []
        for ruletext in full_rule:
            if ruletext[0] == rulename: continue
            try:
                at, current_biggest = consume_rule(input_str, rulename, ruletext, tokens, at, rules, token_types, is_start=is_start)
                break
            except ParseError as e:
                stored_error.append(e)
                continue
        if current_biggest is None:
            throw_parse_error(input_str, tokens[at][2],
                              "Failed to parse {}: {}".format(rulename, "\n".join((str(err) for err in stored_error))))
        done = False
        while not done:
            done = True
            for ruletext in full_rule:
                try:
                    at, current_biggest = consume_rule(input_str, rulename, ruletext, tokens, at, rules, token_types, recurse_start=current_biggest, is_start=is_start)
                    done = False
                except ParseError as e:
                    continue
        return at, current_biggest


def consume_bare_rulesegment(input_str, rulesegment, tokens, at, rules, token_types):
    result = None
    head = tokens[at]
    if rulesegment.isupper():
        if head[0] == rulesegment:
            result = head
            at += 1
        else:
            throw_parse_error(input_str, head[2],
                              "Unexpected token: expected {}, got {}".format(rulesegment, head[0]))
    else:
        at, inst = parse_rulename(input_str, rulesegment, rules, tokens, tokens.index(head), token_types)
        result = inst
    return at, result


def consume_rule(input_str, name, rule, tokens, at, rules, token_types, recurse_start=None, is_start=False):
    childs = []
    if recurse_start is not None:
        childs.append(recurse_start)
    if recurse_start is not None and len(rule) == 1:
        throw_parse_error(input_str, tokens[at][2], '''Parse error: attempted to recursively parse a rule with only 1 
        segment''')

    stored_error = []

    for rulesegment in rule[(1 if recurse_start is not None else 0):]:
        if type(rulesegment) is str:
            at, inst = consume_bare_rulesegment(input_str, rulesegment, tokens, at, rules, token_types)
            childs.append(inst)
        elif type(rulesegment) in (list, tuple):
            identifier = rulesegment[-1]
            if identifier not in ("?", "+", "*"):
                raise ParseError('''Grammar error: rule {} contains an invalid identifier in a group: {}'''.format(name, identifier))
            elif identifier == "?":
                new_at = at
                instances = []
                try:
                    for it in rulesegment[:-1]:
                        new_at, inst = consume_bare_rulesegment(input_str, it, tokens, new_at, rules, token_types)
                        instances.append(inst)
                except ParseError as e:
                    stored_error.append(e)
                else:
                    at = new_at
                    childs.extend(instances)
            elif identifier == "+":
                for it in rulesegment[:-1]:
                    at, inst = consume_bare_rulesegment(input_str, it, tokens, at, rules, token_types)
                    childs.append(inst)
            if identifier in ("+", "*"):
                while True:
                    new_at = at
                    instances = []
                    try:
                        for it in rulesegment[:-1]:
                            new_at, inst = consume_bare_rulesegment(input_str, it, tokens, new_at, rules, token_types)
                            instances.append(inst)
                    except ParseError as e:
                        stored_error.append(e)
                        break
                    else:
                        at = new_at
                        childs.extend(instances)
        else:
            raise ParseError('''Grammar error: rule {} contains an invalid representation: {}'''.format(name, rulesegment))

    inst = rule_instance(name, token_types, childs)
    if len(inst[1]) == 0:
        throw_parse_error(input_str, tokens[at][2], '''Parse error: when parsing a {}, the resulting instance was empty 
        and invalid'''.format(name))
    if is_start and at != len(tokens) - 1:
        if len(stored_error) > 0:
            raise ParseError(str(max(stored_error, key=lambda x: x.at)), at=at)
    return at, inst


def postparse(treenode):
    if len(treenode[1]) == 1 and treenode[1][0][0].islower():
            return postparse((treenode[1][0][0], treenode[1][0][1]))
    else:
        result = (treenode[0], [])
        for child in treenode[1]:
            if child[0].isupper():
                result[1].append(child)
            else:
                result[1].append(postparse(child))
        return result


def parse(input_str, token_types, rules, start="root", postlex=postlex, postparse=postparse):
    tokens = lex(input_str, token_types)
    tokens = postlex(tokens)
    tokens.append(("EOF", "", tokens[-1][2]))
    at, treenode = parse_rulename(input_str, start, rules, tokens, 0, token_types, is_start=True)
    if at != len(tokens) - 1:
        throw_parse_error(input_str, at, '''Parse error: got to end of token stream without parsing everything''')
    return postparse(treenode)

