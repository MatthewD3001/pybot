import sqlite3

def init_db():
    conn = sqlite3.connect('data/users/swap.db')
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS users;
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE users(
            user_id int,
            letter text,
            submit text,
            banned int,
            santa_id int,
            PRIMARY KEY(user_id)
        );
    """)
    conn.commit()

    cur.execute(f"""
        INSERT INTO users VALUES (
            123,
            'example letter',
            '',
            0,
            0
        );
    """)
    conn.commit()

    cur.execute(f"""
        INSERT INTO users VALUES (
            321,
            'example letter',
            '',
            0,
            0
        );
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int, letter: str):
    conn = sqlite3.connect('data/users/swap.db')
    cur = conn.cursor()

    cur.execute(f"""
        INSERT INTO users VALUES (
            {user_id},
            '{letter}',
            '',
            0,
            0
        );
    """)

    conn.commit()
    conn.close()

def in_db(user_id: int) -> bool:
    conn = sqlite3.connect('data/users/swap.db')
    cur = conn.cursor()

    cur.execute(f"""
        SELECT rowid
        FROM users
        WHERE user_id = {user_id}
    """)
    result = cur.fetchall()
    if len(result) != 0:
        return True
    else:
        return False

    conn.commit()
    conn.close()

def get_letter(user_id: int) -> str:
    conn = sqlite3.connect('data/users/swap.db')
    cur = conn.cursor()

    cur.execute(f"""
        SELECT letter
        FROM users
        WHERE user_id = {user_id}
    """)
    letter = str(cur.fetchone())
    letter = letter[2 : len(letter) - 3]
    print(f'\n\n{letter}\n\n')

    conn.commit()
    conn.close()
    return letter

def list_users():
    conn = sqlite3.connect('data/users/swap.db')
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM users; 
    """)
    
    items = cur.fetchall()
    for item in items:
        print(item)

    conn.commit()
    conn.close()

#init_db()
#add_user(123456789, 'bananas')
#list_users()
#in_db(123456789)
