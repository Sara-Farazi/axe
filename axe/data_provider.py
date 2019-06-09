import redis
import sqlite3

redis_client = redis.Redis(host='localhost', port=6379, db=0)

DB_FILE_NAME = "db.sqlite3"
KEYWORDS_TABLE_NAME = "KEYWORDS"


def create_connection():
    conn = sqlite3.connect(DB_FILE_NAME)
    return conn


def add_term_entry(cursor, term):
    command = "SELECT TOKENS FROM {} WHERE IMAGE = '{}'".format(KEYWORDS_TABLE_NAME, term)
    results = cursor.execute(command).fetchall()
    for image in results:
        redis_client.sadd(term, image[0])


def get_keyword_results(keywords):
    conn = create_connection()
    cursor = conn.cursor()
    for keyword in keywords:
        # if the data for this keyword has not been cached yet
        # load it into redis
        if redis_client.smembers(keyword) == set():
            add_term_entry(cursor, keyword)

    results = redis_client.sinter(keywords)
    return list(results)

