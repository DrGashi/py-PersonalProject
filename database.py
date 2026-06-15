import sqlite3

def get_db_connection():
    conn = sqlite3.connect('cars.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            year INTEGER,
            issue TEXT,
            mechanic_id INTEGER,
            FOREIGN KEY (mechanic_id) REFERENCES mechanics(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mechanics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    conn.commit()
    return conn, cursor


def insert_mechanics(mechanics, cursor):
    mechanic_ids = {}

    for mechanic in mechanics:
        cursor.execute('''
            INSERT OR IGNORE INTO mechanics (name)
            VALUES (?)
        ''', (mechanic,))
        cursor.execute('SELECT id FROM mechanics WHERE name = ?', (mechanic,))
        row = cursor.fetchone()
        if row:
            mechanic_ids[mechanic] = row[0]

    return mechanic_ids


def insert_cars(car_dict, mechanic_ids, cursor):
    for (make, mechanic), info in car_dict.items():
        cursor.execute('''
            INSERT INTO cars (make, model, year, issue, mechanic_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            make,
            info['model'],
            info['year'],
            info['issue'],
            mechanic_ids[mechanic],
        ))


def insert_data(cars_dict, mechanics):
    conn, cursor = create_database()
    mechanic_ids = insert_mechanics(mechanics, cursor)
    insert_cars(cars_dict, mechanic_ids, cursor)

    conn.commit()
    conn.close()