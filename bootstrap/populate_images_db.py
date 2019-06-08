import csv
import os
import sqlite3

from PIL import Image
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

DB_FILE_NAME = "db.sqlite3"


def create_connection():
    conn = sqlite3.connect(DB_FILE_NAME)
    return conn


DATA_DIR = "data"
DATA_FILE_NAME = "results.csv"
IMAGES_DIR = "images"
stop_words = set(stopwords.words("english"))
IMAGES_TABLE_NAME = "IMAGE"


def create_table(cursor, table_name):

    command = "CREATE TABLE IF NOT EXISTS {} (" \
              "ID INT PRIMARY KEY NOT NULL," \
              "TOKENS TEXT NOT NULL," \
              "SIZE INT NOT NULL," \
              "HEIGHT INT NOT NULL," \
              "WIDTH INT NOT NULL);".format(table_name)

    cursor.execute(command)


def get_file_name(image_id):
    return "{}/{}/{}".format(DATA_DIR, IMAGES_DIR, image_id)


def get_file_size(filename):
    return os.stat(filename).st_size


def get_file_dims(filename):
    return Image.open(filename).size


def add_to_database(cursor, image_id, comments):
    file_name = get_file_name(image_id)
    file_size = get_file_size(file_name)
    image_width, image_height = get_file_dims(file_name)
    id = int(image_id.split(".jpg")[0])

    tokens = []
    for comment in comments:
        for token in word_tokenize(comment):
            if token not in stop_words and token.isalnum():
                tokens.append(token)

    comments_string = " ".join(tokens)

    command = "INSERT INTO {} VALUES ({}, \"{}\", {}, {}, {});".format(IMAGES_TABLE_NAME,
                                                                       id,
                                                                       comments_string,
                                                                       file_size,
                                                                       image_height,
                                                                       image_width)

    cursor.execute(command)


def populate_db(cursor):
    data_file_path = "{}/{}".format(DATA_DIR, DATA_FILE_NAME)
    with open(data_file_path) as datafile:
        csv_reader = csv.reader(datafile, delimiter="|")
        current_batch = []
        current_id = None
        for line in csv_reader:
            try:

                image_id = line[0].strip()
                comment = line[2].strip()

                # if image_id != current_id previous batch has been completed
                if image_id != current_id:
                    # if it's the first batch of the entire data
                    if current_id:
                        add_to_database(cursor, current_id, current_batch)

                    current_id = image_id
                    current_batch = []

                current_batch.append(comment.lower())

            except Exception as e:
                print("Error processing line\n{}\n{}\n".format(line, str(e)))


def main():
    conn = create_connection()
    cursor = conn.cursor()
    create_table(cursor, IMAGES_TABLE_NAME)
    populate_db(cursor)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
