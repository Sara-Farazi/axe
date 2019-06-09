import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

KEYWORDS_TABLE_NAME = "KEYWORDS"


def add_term_entry(cursor, term):
    command = "SELECT * FROM {} WHERE TOKENS = {}".format(term)
    results = cursor.execute(command).fetchall()
    for image in results:
        redis_client.sadd(term, image)


def get_keyword_results(keywords):
    for keyword in keywords:
        # if the data for this keyword has not been cached yet
        # load it into redis
        if redis_client.smembers(keyword) == set():
            add_term_entry(keyword)

        redis_client.sinter(keywords)
