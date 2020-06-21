def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3:
        return y
    else:
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + '.' + p