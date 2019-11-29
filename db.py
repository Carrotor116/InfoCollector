import sqlite3

conn = sqlite3.connect('test.db')


def _get_table_name(obj):
    cls = obj if isinstance(obj, type) else type(obj)
    return cls.__name__.upper()


def _get_primary_key(obj):
    if not hasattr(obj, '_TABLE_KEY'):
        return None, None
    key = getattr(obj, '_TABLE_KEY')
    if not hasattr(obj, key):
        return key, None
    value = getattr(obj, key)
    return key, value


def _get_cols2value(obj):
    if isinstance(obj, type):
        obj = obj()
    if not hasattr(obj, '__dict__'):
        return dict()
    dic = obj.__dict__
    attr = [i for i in dic.keys() if not i.startswith('_')]
    attr = sorted([i for i in attr if not callable(getattr(obj, i))])
    return {k: dic[k] for k in attr}


def create_table(cls) -> bool:
    table_name = _get_table_name(cls)
    cols = sorted(list(_get_cols2value(cls).keys()))
    primary_key, value = _get_primary_key(cls)

    if primary_key is not None:
        assert primary_key in cols
        cols.remove(primary_key)
        cols = '{} TEXT PRIMARY KEY NOT NULL, '.format(primary_key) + ', '.join(['{} TEXT'.format(i) for i in cols])
    else:
        cols = ', '.join(['{} TEXT'.format(i) for i in cols])
    sql = """CREATE TABLE IF NOT EXISTS {} ({});"""
    sql = sql.format(table_name, cols)
    try:
        conn.cursor().execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print(e)
    return False


def insert(obj) -> bool:
    table_name = _get_table_name(obj)
    cols2value = _get_cols2value(obj)
    cols = sorted(list(cols2value.keys()))
    value = [cols2value[c] for c in cols]
    sql = """INSERT INTO {} ({}) VALUES ({});"""
    sql = sql.format(table_name, ','.join(cols), ','.join(["'{}'".format(v) for v in value]))
    try:
        conn.cursor().execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True


def select_all(cls):
    table_name = _get_table_name(cls)
    cols = list(_get_cols2value(cls).keys())
    sql = """SELECT {} FROM {};"""
    sql = sql.format(', '.join(cols), table_name)
    res = []
    try:
        cursor = conn.execute(sql)
        for row in cursor:
            obj = cls()
            for col, value in zip(cols, row):
                setattr(obj, col, value)
            res.append(obj)
    except Exception as e:
        print(e)
    return res


def select_by_key(cls, key):
    table_name = _get_table_name(cls)
    pri_key, _ = _get_primary_key(cls)
    cols = list(_get_cols2value(cls).keys())

    sql = """SELECT {} FROM {} WHERE {};"""
    sql = sql.format(', '.join(cols), table_name, "{}='{}'".format(pri_key, key))
    try:
        cursor = conn.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            obj = cls()
            for col, value in zip(cols, row):
                setattr(obj, col, value)
            return obj
    except Exception as e:
        print(e)
    return None


def update(obj) -> bool:
    assert not isinstance(obj, type)
    table_name = _get_table_name(obj)
    pri_key, pri_value = _get_primary_key(obj)
    cols2value = _get_cols2value(obj)

    sql = """UPDATE {} SET {} WHERE {};"""
    sql = sql.format(table_name,
                     ','.join(["{}='{}'".format(c, v) for c, v in cols2value.items()]),
                     "{}='{}'".format(pri_key, pri_value))
    try:
        conn.cursor().execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print(e)
    return False


def delete(obj) -> bool:
    assert not isinstance(obj, type)
    pri_key, pri_val = _get_primary_key(obj)
    table_name = _get_table_name(obj)
    sql = """DELETE FROM {} WHERE {}='{}';"""
    sql = sql.format(table_name, pri_key, pri_val)
    try:
        conn.cursor().execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print(e)
    return False


if __name__ == '__main__':
    from bean import Info

    create_table(Info)
    print(insert(Info(ip='1232131')))

    infos = select_all(Info)
    for i in infos:
        print(i)
    print(update(Info('gpu1', ' 666')))
    print(select_by_key(Info, 'gpu1'))
