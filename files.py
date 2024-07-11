def readfacts(path):
    with open(path, encoding="utf-8") as facts_txt:
        facts = list(facts_txt.readline().split(", "))
        facts_txt.close()

    return facts


def readrules(path):
    with open(path, encoding="utf-8") as rules_txt:
        rules = list(rules_txt.read().split("\n"))
        sortedrules = sortrules(rules)
        rules_txt.close()

    return sortedrules


# organize and return rules
def sortrules(rules):
    sorted_rules = []
    for rule in rules:
        parts, whole = rule.split(" = ")
        parts = parts.split(" + ")
        sorted_rules.append((whole, parts))

    return sorted_rules
