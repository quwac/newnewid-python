def nodoc(f):
    """No documentation for this function."""

    def wrapper(*args, **keywords):
        return f(*args, **keywords)

    return wrapper
