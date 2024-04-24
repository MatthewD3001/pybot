import sqlite3
import random



def init_db():
    global conn
    global cur
    conn = sqlite3.connect('data/users/swap.db')
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS Users;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Swap;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS SwapStatus;
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE Users(
            uid INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            letter TEXT,
            in_swap INTEGER,
            banned INTEGER,
            reason TEXT
        );
    """)
    cur.execute("""
        CREATE TABLE Swap(
            uid INTEGER PRIMARY KEY,
            santa_id TEXT NOT NULL,
            giftee_id TEXT NOT NULL,
            submit TEXT,
            CONSTRAINT fk_santas
                FOREIGN KEY(santa_id)
                REFERENCES Users(user_id)
                ON DELETE CASCADE,
            CONSTRAINT fk_giftees
                FOREIGN KEY(giftee_id)
                REFERENCES Users(user_id)
                ON DELETE CASCADE
        );
    """)
    cur.execute("""
        CREATE TABLE SwapStatus(
            swap_started INTEGER
        );
    """)
    conn.commit()
    cur.execute("""
        INSERT INTO SwapStatus VALUES(
            0
        );
    """)
    conn.commit()
    
    add_user(477096301364903936, "toby's letter")
    add_user(105365884951863296, "noon's letter")
    add_user(439139492427988992, "cobra's letter")
    add_user(687300286066458653, "qb's letter")
    add_user(66207186417627136, "Something abt lolis")
    add_user(160763614888722433, "cirix's letter")
    add_user(316084228943249413, "scar's letter")

def close_db() -> None:
    conn.close()


def get_user_ids_in_swap() -> set:
    cur.execute("""
        SELECT santa_id
        FROM Swap
    """)
    santa_ids = cur.fetchall()
    user_ids = set()
    for index in range(len(santa_ids)):
        user_ids.add(int(santa_ids[index][0]))
    return user_ids

def get_user_id_in_swap() -> int:
    cur.execute("""
        SELECT user_id
        FROM Users
        WHERE in_swap = 1
        LIMIT 1
    """)
    return int(cur.fetchone()[0])


def start_swap() -> None:
    cur.execute("""
        SELECT user_id
        FROM Users
        WHERE in_swap = 1
    """)
    tmp_ids = cur.fetchall()
    santa_ids = []
    for id in tmp_ids:
        santa_ids.append(id[0])
    random.shuffle(santa_ids)
    for index in range(len(santa_ids) - 1):
        add_giftee(santa_ids[index], santa_ids[index + 1])
    add_giftee(santa_ids[len(santa_ids) - 1], santa_ids[0])
    cur.execute("""
        UPDATE SwapStatus
        SET swap_started = 1
    """)

    list_users()


def swap_started() -> bool:
    cur.execute("""
        SELECT swap_started
        FROM SwapStatus
        LIMIT 1
    """)
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False


def get_giftee(santa_id: int) -> int:    
    cur.execute(f"""
        SELECT giftee_id
        FROM Swap
        WHERE santa_id = '{santa_id}'
    """)
    return int(cur.fetchone()[0])


def add_giftee(user_id: int, giftee_id: int) -> None:
    cur.execute(f"""
        INSERT INTO Swap VALUES (
            NULL,
            '{user_id}',
            '{giftee_id}',
            ''
        );
    """)
    conn.commit()


def add_user(user_id: int, letter: str='') -> None:
    cur.execute(f"""
        INSERT INTO Users VALUES (
            NULL,
            '{user_id}',
            "{letter}",
            1,
            0,
            ''
        );
    """)
    conn.commit()
    list_users()    


def remove_user(user_id: int) -> None:
    cur.execute(f"""
        DELETE FROM Users
        WHERE user_id = '{user_id}'
    """)
    conn.commit()
    list_users()    


def get_in_swap(user_id: int) -> bool:
    cur.execute(f"""
        SELECT in_swap
        FROM Users
        WHERE user_id = '{user_id}'
    """)
    result = cur.fetchone()[0]
    if result == 1:
        return True
    else:
        return False


def leave_swap(user_id: int) -> None:
    if swap_started():
        set_ban(user_id, 1)
        # TODO: Make sure to reassign giftee
        
    else:
        set_in_swap(user_id, 0)
    list_users()    


def set_in_swap(user_id: int, in_swap: int) -> None:
    cur.execute(f"""
        UPDATE Users
        SET in_swap = {in_swap}
        WHERE user_id = '{user_id}'
    """)
    conn.commit()


def set_ban(user_id: int, ban_status: int) -> None:
    cur.execute(f"""
        UPDATE Users
        SET banned = {ban_status}
        WHERE user_id = '{user_id}'
    """)
    conn.commit()
    cur.execute(f"""
        SELECT in_swap
        FROM Users
        WHERE user_id = '{user_id}'
    """)
    if cur.fetchone()[0] == 1 and ban_status == 1:
        set_in_swap(user_id, 0)


def in_db(user_id: int) -> bool:
    cur.execute(f"""
        SELECT uid
        FROM Users
        WHERE user_id = '{user_id}'
    """)
    result = cur.fetchone()
    if result != None:
        return True
    else:
        return False


def is_banned(user_id: int) -> bool:
    cur.execute(f"""
        SELECT banned
        FROM Users
        WHERE user_id = '{user_id}'
    """)
    result = cur.fetchone()[0]
    if result == 1:
        return True
    else:
        return False


def get_letter(user_id: int) -> str:
    cur.execute(f"""
        SELECT letter
        FROM Users
        WHERE user_id = '{user_id}'
    """)
    letter = cur.fetchone()[0]

    return letter


def edit_letter(user_id: int, letter: str) -> None:
    cur.execute(f"""
        UPDATE Users
        SET letter = "{letter}"
        WHERE user_id = '{user_id}'
    """)
    conn.commit()
    list_users()    


def list_users() -> None:
    cur.execute("""
        SELECT * FROM Users; 
    """)
    
    items = cur.fetchall()
    print('\nUsers:')
    for item in items:
        print(item) 

    cur.execute("""
        SELECT * FROM Swap;
    """)

    items = cur.fetchall()
    print('Swap:')
    for item in items:
        print(item) 


#init_db()
#add_user(123456789, 'bananas')
#list_users()
#in_db(123456789)
