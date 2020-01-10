import database_common
import bcrypt


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def get_line(cursor, user_name):
    cursor.execute('''
                    SELECT user_name,password FROM users
                    WHERE user_name = %(user_name)s
    
    ''',    {'user_name':user_name})
    line = cursor.fetchall()
    return line


@database_common.connection_handler
def check_username(cursor,user_name):
    cursor.execute('''
                SELECT count(*) as num  FROM users
                WHERE user_name = %(user_name)s    
    
    ''',   {"user_name": user_name})

    result = cursor.fetchall()
    return result



@database_common.connection_handler
def save_user_data(cursor, user_name, password):
    cursor.execute('''
                INSERT INTO users (user_name, password)
                VALUES (%(user_name)s, %(password)s)

    ''',
                   {"user_name": user_name, "password": password})


@database_common.connection_handler
def get_five_question(cursor):
    cursor.execute('''
    SELECT * FROM question
    ORDER BY id DESC 
    LIMIT 5
     ''')
    question = cursor.fetchall()
    return question




