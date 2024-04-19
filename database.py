import sqlite3
import random

def init_db():
    global conn
    global cur
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
            in_swap int,
            banned int,
            giftee_id int,
            PRIMARY KEY(user_id)
        );
    """)
    conn.commit()
    
    add_user(477096301364903936, "toby's letter")
    add_user(105365884951863296, "noon's letter")

def close_db():
    conn.close()


def get_user_ids_in_swap() -> list:
    cur.execute("""
        SELECT user_id
        FROM users
        WHERE in_swap = 1
    """)
    user_ids = cur.fetchall()
    for index in range(len(user_ids)):
        user_ids[index] = user_ids[index][0]
    return user_ids

def get_user_id_in_swap() -> int:
    cur.execute("""
        SELECT user_id
        FROM users
        WHERE in_swap = 1
        LIMIT 1
    """)
    return cur.fetchone()[0]


def start_swap():
    santa_ids = get_user_ids_in_swap()
    random.shuffle(santa_ids)
    for index in range(len(santa_ids) - 1):
        set_giftee(santa_ids[index], santa_ids[index + 1])
    set_giftee(santa_ids[len(santa_ids) - 1], santa_ids[0])

    list_users()


def get_giftee(santa_id: int):    
    cur.execute(f"""
        SELECT giftee_id
        FROM users
        WHERE user_id = {santa_id}
    """)
    return cur.fetchone()[0]


def set_giftee(user_id: int, giftee_id: int):
    cur.execute(f"""
        UPDATE users
        SET giftee_id = {giftee_id}
        WHERE user_id = {user_id}
    """)
    conn.commit()


def add_user(user_id: int, letter: str=''):
    cur.execute(f"""
        INSERT INTO users VALUES (
            {user_id},
            "{letter}",
            '',
            1,
            0,
            0
        );
    """)
    conn.commit()
    list_users()    

def remove_user(user_id: int):
    cur.execute(f"""
        DELETE FROM users
        WHERE user_id = {user_id}
    """)
    conn.commit()
    list_users()    


def get_in_swap(user_id: int) -> bool:
    cur.execute(f"""
        SELECT in_swap
        FROM users
        WHERE user_id = {user_id}
    """)
    result = cur.fetchone()[0]
    print(f'result: {result}')
    if result == 1:
        return True
    else:
        return False


def set_in_swap(user_id: int, in_swap: int):
    cur.execute(f"""
        UPDATE users
        SET in_swap = {in_swap}
        WHERE user_id = {user_id}
    """)
    conn.commit()

def set_ban(user_id: int, ban_status: int):
    cur.execute(f"""
        UPDATE users
        SET banned = {ban_status}
        WHERE user_id = {user_id}
    """)
    conn.commit()
    if ban_status == 1:
        set_in_swap(user_id, 0)
    list_users()    


def in_db(user_id: int) -> bool:
    cur.execute(f"""
        SELECT rowid
        FROM users
        WHERE user_id = {user_id}
    """)
    result = cur.fetchone()
    if result != None:
        return True
    else:
        return False


def is_banned(user_id: int) -> bool:
    cur.execute(f"""
        SELECT banned
        FROM users
        WHERE user_id = {user_id}
    """)
    result = cur.fetchone()[0]
    if result == 1:
        return True
    else:
        return False


def get_letter(user_id: int) -> str:
    cur.execute(f"""
        SELECT letter
        FROM users
        WHERE user_id = {user_id}
    """)
    letter = cur.fetchone()[0]
    #letter = letter[2 : len(letter) - 3]

    return letter

def edit_letter(user_id: int, letter: str):
    cur.execute(f"""
        UPDATE users
        SET letter = "{letter}"
        WHERE user_id = {user_id}
    """)
    conn.commit()
    list_users()    

def list_users():
    cur.execute("""
        SELECT * FROM users; 
    """)
    
    items = cur.fetchall()
    print()
    for item in items:
        print(item) 


#init_db()
#add_user(123456789, 'bananas')
#list_users()
#in_db(123456789)
