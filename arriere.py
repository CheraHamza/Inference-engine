def get_reaching_rules(rules, but):
    reaching_rules = []
    for rule in rules:
        if rule[0] == but:
            reaching_rules.append(rule)
    return reaching_rules


# return index of selected reaching rules (based on premise count then order)
def select_rules(reachable_rules):
    selected_rules = []
    if len(reachable_rules) < 1:
        return selected_rules
    nbr_premises = len(reachable_rules[0][1])
    for rule in reachable_rules:
        if len(rule[1]) > nbr_premises:
            reachable_rules.remove(rule)
            reachable_rules.insert(0, rule)
        else:
            if len(rule[1]) < nbr_premises:
                continue
        nbr_premises = len(rule[1])
    selected_rules = reachable_rules.copy()
    return selected_rules
