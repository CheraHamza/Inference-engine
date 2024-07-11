# evaluate rules and return applicable ones
def evaluate_rules(rules, facts):
    applicable_rules = rules.copy()
    for rule in rules:
        for premise in rule[1]:
            if premise not in facts:
                applicable_rules.remove(rule)
                break

    return applicable_rules


# return selected rules from evaluated rules (based on premise count then order)
def select_rules(applicable_rules):
    selected_rules = []
    if len(applicable_rules) < 1:
        return selected_rules
    premise_count = len(applicable_rules[0][1])
    for rule in applicable_rules:
        if len(rule[1]) > premise_count:
            selected_rules.clear()
        else:
            if len(rule[1]) < premise_count:
                continue
        premise_count = len(rule[1])
        selected_rules.append(rule)

    return selected_rules


# add new facts to BF
def apply_rules(rules, facts):
    fact = rules[0][0]  # le fait à ajouter
    if fact not in facts:
        facts.append(fact)
    return rules[0], facts
