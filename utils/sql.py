from django.db import connection


def dictfetchall(cursor):
    """
    Returns all rows from a cursor as a dict.
    """
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_dictfetchall_sql(sql, where_params=[]):
    """
    Executes the sql and returns the data as dict.
    """
    cursor = connection.cursor()
    cursor.execute(sql, where_params)
    return dictfetchall(cursor)