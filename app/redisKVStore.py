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

def append_item(key, item):

    value, _ = store[key]
    value.append(item)
    return len(value)
