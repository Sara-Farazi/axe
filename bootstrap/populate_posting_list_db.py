import re
import sqlite3


DB_FILE_NAME = "db.sqlite3"
KEYWORDS_TABLE_NAME = "KEYWORDS"
IMAGES_TABLE_NAME = "IMAGE"


def create_connection():
    conn = sqlite3.connect(DB_FILE_NAME)
    return conn


def create_table(cursor, table_name):

    command = "CREATE TABLE IF NOT EXISTS {} (" \
              "TOKENS TEXT NOT NULL," \
              "IMAGE INT NOT NULL)".format(table_name)

    cursor.execute(command)


def populate_keywords_db(cursor):
    regex = re.compile("(\w+)")
    command = "SELECT ID, TOKENS from {}".format(IMAGES_TABLE_NAME)
    cursor.execute(command)
    results = cursor.fetchall()
    for row in results:
        tokens = regex.findall(row[1])
        id = row[0]
        for token in tokens:
            command = "INSERT INTO {} VALUES({}, \"{}\")".format(KEYWORDS_TABLE_NAME, id, token)
            cursor.execute(command)


def main():
    conn = create_connection()
    cursor = conn.cursor()
    create_table(cursor, KEYWORDS_TABLE_NAME)
    populate_keywords_db(cursor)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
