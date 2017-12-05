

def cursor_to_list(cursor):
    res = []
    snl = 0

    for row in cursor:
        snl = snl + 1
        row['_id'] = str(row['_id'])
        res.append(row)

    return res