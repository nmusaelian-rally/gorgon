import psycopg2
import datetime
from helpers.chronuti import TimeStamp


TABLE_NAME = "installation"


def getConnection(dburl):
    if '/cloudsql/' in dburl:
        temp, dbhost   = dburl.split('?host=', 1)
        dbtype, other  = temp.split('://')
        uspw, dbname   = other.split('@/')
        dbuser, dbpswd = uspw.split(':')
    else:
        temp, dbhostname = dburl.split('@', 1)
        dbhost, dbname   = dbhostname.split('/')
        throwaway, uspw  = temp.split("://")
        dbuser, dbpswd   = uspw.split(':')

    details = "dbname=%s user=%s password=%s host=%s" % (dbname, dbuser, dbpswd, dbhost.split(':')[0])
    connection = psycopg2.connect(details)
    connection.autocommit = True
    return connection

# def _queryForHitCount(cursor, install_id):
#     sql_query = "SELECT hit_count FROM {table_name} WHERE install_id={install_id}"
#     cursor.execute(sql_query.format(table_name=TABLE_NAME, install_id=install_id))
#     result = cursor.fetchone()
#     return result[0]

def _query(cursor, install_id):
    sql_query = "SELECT hit_count, api_key FROM {table_name} WHERE install_id={install_id}"
    cursor.execute(sql_query.format(table_name=TABLE_NAME, install_id=install_id))
    result = cursor.fetchone()
    return result

def update(dbconn, install_id):
    """
        update the hit_count for the record in our DB, and return back the associated APIKey to be
        used when accessing Rally for the purposes of create/update of the PullRequest item
    """
    cursor = dbconn.cursor()
    result = _query(cursor, install_id)
    hit_count = result[0]
    api_key   = result[1]
    if not hit_count:
        hit_count = 0
    hit_count += 1
    timestamp = TimeStamp.now().asISOString()
    #update_stmt = "UPDATE table {table_name} set hit_count = {hit_count}, last_used = '{timestamp}' where install_id = {install_id}"
    update_stmt = "UPDATE {table_name} set hit_count = {hit_count}, last_used = '{timestamp}' where install_id = {install_id}"
    sql_update = update_stmt.format(table_name=TABLE_NAME, hit_count=hit_count, timestamp=timestamp, install_id=install_id)
    cursor.execute(sql_update)
    return api_key

