"""
Create database and tables in pgAdmin (after creating database click it then query tool again):

CREATE DATABASE "ASET";

CREATE TABLE city (
    id       UUID PRIMARY KEY,
    name     TEXT NOT NULL,
    country  TEXT NOT NULL
);

CREATE TABLE location (
    id       UUID PRIMARY KEY,
    city_id  UUID NOT NULL REFERENCES city (id),
    address  TEXT NOT NULL
);

CREATE TABLE product (
    id                    UUID PRIMARY KEY,
    location_id           UUID NOT NULL REFERENCES location (id),
    product_type          TEXT NOT NULL,
    furnish_type          TEXT NOT NULL,
    size                  NUMERIC(6,2) NOT NULL,
    floor_number          INTEGER,
    number_of_rooms       INTEGER,
    number_of_floors      INTEGER,
    year_of_construction  INTEGER
);

CREATE TABLE product_history (
    id          UUID PRIMARY KEY,
    product_id  UUID NOT NULL REFERENCES product (id),
    price       NUMERIC(11,2) NOT NULL,
    currency    TEXT NOT NULL,
    day         DATE NOT NULL
);

CREATE TABLE product_prediction (
    id               UUID PRIMARY KEY,
    product_id       UUID NOT NULL REFERENCES product (id),
    predicted_price  NUMERIC(11,2) NOT NULL,
    currency         TEXT NOT NULL,
    day              DATE NOT NULL
);
"""
import psycopg2

db_connection = None


def get_connection():
    global db_connection
    if db_connection is None:
        create_connection()
    return db_connection


def create_connection():
    global db_connection
    db_connection = psycopg2.connect(
        host="localhost",
        database="ASET",
        user="postgres",
        password="rainbow87")


def insert_csv_data():
    city_path = '..\\..\\Data\\city.csv'
    location_path = '..\\..\\Data\\locations.csv'
    product_path = '..\\..\\Data\\products.csv'
    history_path = '..\\..\\Data\\history.csv'

    conn = get_connection()
    cursor = conn.cursor()

    # insert cities
    with open(city_path) as cities:
        cities = cities.readlines()
        city_list = [line.split() for line in cities]
        for city in city_list:
            city = city[0].split(',')
            cursor.execute("INSERT INTO city VALUES (%s, %s, %s)", (city[0], city[1], city[2]))

    # insert locations
    with open(location_path) as locations:
        locations.readline()
        line = locations.readline()
        while line:
            line = line.split(",")
            cursor.execute("INSERT INTO location VALUES (%s, %s, %s)", (line[1], line[2][:-1], line[0]))
            line = locations.readline()

    # insert products
    with open(product_path) as products:
        products = products.readlines()[1:]
        product_list = [line.split() for line in products]
        for product in product_list:
            product = product[0].split(',')
            floor_number = product[5] if product[5] != 'NULL' else None
            nr_of_rooms = product[8] if product[8] != 'NULL' else None
            nr_of_floors = product[6] if product[6] != 'NULL' else None
            year_of_construction = product[7] if product[7] != 'NULL' else None
            cursor.execute("INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (product[0], product[2], product[3], product[4], product[1],
                            floor_number, nr_of_rooms, nr_of_floors, year_of_construction))

    # insert product history
    with open(history_path) as history_:
        history_ = history_.readlines()[1:]
        history_list = [line.split() for line in history_]
        for history in history_list:
            history = history[0].split(',')
            cursor.execute("INSERT INTO product_history VALUES (%s, %s, %s, %s, %s)",
                           (history[0], history[1], history[3], history[4], history[2]))

    # commit everything to database
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    insert_csv_data()
    db_connection.close()
