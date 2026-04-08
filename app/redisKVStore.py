import time

store = {}  # key -> (value, expiry_timestamp or None)

def set_key(key, value, px=None):
    expiry = None
    if px is not None:
        expiry = time.time() + (px / 1000)  # px is in milliseconds
    store[key] = (value, expiry)

def get_key(key):
    if key not in store:
        return None
    value, expiry = store[key]
    if expiry is not None and time.time() > expiry:
        del store[key]  # lazy delete
        return None
    return value

def append_items(key, items):

    value, _ = store[key]
    for item in items:
        value.append(item)
    return len(value)

def get_items(key, start, stop):

    value, _ = get_key(key)
    try:
        if (value == None or start > stop or start > len(value)-1):
            return []
        else:
            return value[start:min(stop+1, len(value)-1)]
    except:
        return []