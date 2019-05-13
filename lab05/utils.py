def recursive_map(f, operand):
    return list(map(lambda x: f(x) if not isinstance(x, list) else recursive_map(f, x), operand))


def recursive_modify(obj, inds, new_val):
    obj[inds[0]] = new_val if len(inds) == 1 else recursive_modify(obj[inds[0]], inds[1:], new_val)
    return obj
