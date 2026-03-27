'''

'''

def dbprint(enabled, *args, **kwargs):
    if enabled:
        print(*args, **kwargs)
    else:
        pass