def list(this, options, items):
    result = []
    for thing in items:
        result.extend(options['fn'](thing))
    return result
