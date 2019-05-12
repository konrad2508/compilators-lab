def recursive_map(f, operand):
    return list(map(lambda x: f(x) if not isinstance(x, list) else recursive_map(f, x), operand))
