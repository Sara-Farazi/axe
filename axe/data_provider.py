import redis
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))
redis_client = redis.Redis(host='localhost', port=6379, db=0)

DB_FILE_NAME = "db.sqlite3"
KEYWORDS_TABLE_NAME = "KEYWORDS"


def create_connection():
    conn = sqlite3.connect(DB_FILE_NAME)
    return conn


def add_term_entry(cursor, term):
    command = "SELECT IMAGE FROM {} WHERE TOKEN = '{}'".format(KEYWORDS_TABLE_NAME, term)
    results = cursor.execute(command).fetchall()
    for image in results:
        redis_client.sadd(term, image[0])


def get_keywords(query):
    tokens = []
    for token in word_tokenize(query):
        if token not in stop_words and token.isalnum():
            tokens.append(token)

    return tokens


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


def filter_by_size(min_size, max_size, keyword_results):
    if min_size == "" and max_size == "":
        return keyword_results
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    results = []
    min_size = int(min_size) * 1000
    max_size = int(max_size) * 1000

    for id in keyword_results:
        query = "SELECT SIZE FROM IMAGE WHERE ID = {}; ".format(int(id))
        size = cursor.execute(query).fetchall()[0][0]
        if min_size == "":
            if size < max_size:
                results.append(id)
        elif max_size == "":
            if size > min_size:
                results.append(id)
        else:
            if min_size < size < max_size:
                results.append(id)

    conn.close()
    return results


def get_query_results(query, min_size, max_size):
    keywords = get_keywords(query)
    query_key = ""
    for word in keywords:
        query_key = query_key + word + "+"
    query_key = query_key + min_size + "+" + max_size

    if redis_client.exists(query_key):
        length = redis_client.llen(query_key)
        return redis_client.lrange(query_key, 0, length)

    keywords_results = get_keyword_results(keywords)
    final_results = filter_by_size(min_size, max_size, keywords_results)

    for item in final_results:
        redis_client.lpush(query_key, item)
    return final_results
