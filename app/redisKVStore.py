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

def prepend_items(key, items):

    value, _ = store[key]
    value = items[::-1] + value
    print(value)
    return len(value)

def get_items(key, start, stop):

    value = get_key(key)
    try:
        start = recalibrate(start, len(value))
        stop = recalibrate(stop, len(value))
        if (value == None or start > stop or start > len(value)-1):
            return []
        else:
            return value[start:min(stop+1, len(value))]
    except:
        return []
    

def recalibrate(index, length):

    if (index < 0 and index >= -1*length):
        index += length
    elif(index < -1*length):
        index = 0
    else:
        pass
    return index