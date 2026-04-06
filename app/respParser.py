
def parser(request):

    reqItems = request.split("\r\n")
    itemIndex = 4
    echoItems = []
    while (itemIndex < len(reqItems)):
        echoItems.append(reqItems[itemIndex])
        itemIndex += 2
    return (reqItems[2].lower(), echoItems)

def formBulkString(item):

    return f"${len(item)}\r\n{item}\r\n"


