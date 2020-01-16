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
    
    ''', {'user_name': user_name})
    line = cursor.fetchall()
    return line


@database_common.connection_handler
def check_username(cursor, user_name):
    cursor.execute('''
                SELECT count(*) as num  FROM users
                WHERE user_name = %(user_name)s    
    
    ''', {"user_name": user_name})

    result = cursor.fetchall()
    return result


@database_common.connection_handler
def save_user_data(cursor, user_name, password):
    cursor.execute('''
                INSERT INTO users (user_name, password, reputation)
                VALUES (%(user_name)s, %(password)s, 0)

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


@database_common.connection_handler
def get_all_question(cursor, column="id", direction="DESC"):
    cursor.execute(f"""
    SELECT * FROM question
    ORDER BY {column} {direction}
     """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def add_new_question(cursor, new_question):
    cursor.execute('''
    INSERT into question(view_number,vote_number,title,message,submission_time,user_name) VALUES %(new_question)s

    ''', {"new_question": new_question})


@database_common.connection_handler
def get_user_id(cursor, user_name):
    cursor.execute('''
                    SELECT user_id FROM users
                    where user_name = %(user_name)s
    
    ''', {"user_name": user_name})
    user_id = cursor.fetchall()
    return user_id

@database_common.connection_handler
def get_user_name_by_question_id(cursor, question_id):
    cursor.execute('''
                    SELECT user_name FROM question
                    WHERE id = %(question_id)s
    ''',
                   {"question_id": question_id})
    user_id = cursor.fetchall()
    return user_id


@database_common.connection_handler
def get_user_name_by_answer_id(cursor, answer_id):
    cursor.execute('''
                    SELECT user_name FROM answer
                    WHERE id = %(answer_id)s
    ''',
                   {"answer_id": answer_id})
    user_id = cursor.fetchall()
    return user_id


@database_common.connection_handler
def get_question(cursor, q_id):
    cursor.execute('''
    SELECT * FROM question 
    WHERE id = %(q_id)s
     ''',
                   {"q_id": q_id})
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_answers(cursor, q_id):
    cursor.execute('''
    SELECT * FROM answer 
    WHERE question_id = %(q_id)s
    ORDER BY submission_time
     ''',
                   {"q_id": q_id})

    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def add_new_answer(cursor, new_answer):
    cursor.execute('''
    INSERT into answer(vote_number,question_id, message,submission_time, user_name, accepted) VALUES %(new_answer)s

    ''', {"new_answer": new_answer})


@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute('''
    DELETE from question
    WHERE id = %(question_id)s
    ''',
                   {"question_id": question_id})


@database_common.connection_handler
def delete_all_answer(cursor, question_id):
    cursor.execute('''
    DELETE from answer
    WHERE question_id = %(question_id)s
    ''',
                   {"question_id": question_id})


@database_common.connection_handler
def write_edited_question(cursor, new_title, new_message, question_id):
    cursor.execute('''
    UPDATE question
    SET title = %(new_title)s, message= %(new_message)s
    WHERE id= %(question_id)s
    ''',
                   {"new_title": new_title, "new_message": new_message, "question_id": question_id})


@database_common.connection_handler
def delete_one_answer(cursor, answer_id):
    cursor.execute('''
    DELETE from answer
    WHERE id = %(answer_id)s
    ''',
                   {"answer_id": answer_id})


@database_common.connection_handler
def question_vote_up(cursor, question_id):
    cursor.execute('''
    UPDATE question 
    SET vote_number = vote_number+1
    WHERE id = %(question_id)s
    ''',
                   {"question_id": question_id})


@database_common.connection_handler
def question_vote_down(cursor, question_id):
    cursor.execute('''
    UPDATE question 
    SET vote_number = vote_number-1
    WHERE id = %(question_id)s
    ''',
                   {"question_id": question_id})


@database_common.connection_handler
def answer_vote_up(cursor, answer_id):
    cursor.execute('''
    UPDATE answer 
    SET vote_number = vote_number+1
    WHERE id = %(answer_id)s
    ''',
                   {"answer_id": answer_id})


@database_common.connection_handler
def answer_vote_down(cursor, answer_id):
    cursor.execute('''
    UPDATE answer 
    SET vote_number = vote_number-1
    WHERE id = %(answer_id)s
    ''',
                   {"answer_id": answer_id})


@database_common.connection_handler
def get_question_id(cursor, answer_id):
    cursor.execute('''
                    SELECT question_id FROM answer
                    where id = %(answer_id)s

    ''', {"answer_id": answer_id})
    question_id = cursor.fetchall()
    return question_id


@database_common.connection_handler
def edit_answer(cursor, new_message, answer_id):
    cursor.execute('''
    UPDATE answer
    SET message = %(new_message)s
    WHERE id= %(answer_id)s
    ''',
                   {"new_message": new_message, "answer_id": answer_id})


@database_common.connection_handler
def get_one_answer(cursor, answer_id):
    cursor.execute('''
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s
    
    ''',
                   {"answer_id": answer_id})
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def get_result_q(cursor, search_phrase):
    cursor.execute('''
                    SELECT * FROM question
    
                    WHERE upper(title) like upper(%(search_phrase)s) or lower(message) like lower(%(search_phrase)s)
    
    ''', {"search_phrase": search_phrase})
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_result_a(cursor, search_phrase):
    cursor.execute('''
                    SELECT * FROM answer

                    WHERE lower(message) like lower(%(search_phrase)s)

    ''', {"search_phrase": search_phrase})
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def add_question_comment(cursor, comment):
    cursor.execute(''' 
                    INSERT INTO comment(question_id, message, submission_time, user_name)
                    VALUES %(comment)s
                    
    ''', {"comment": comment})


@database_common.connection_handler
def get_one_comment(cursor, comment_id):
    cursor.execute('''
                    SELECT * FROM comment
                    WHERE id = %(comment_id)s
    
    ''',    {"comment_id":comment_id})
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def get_question_comments(cursor, question_id):
    cursor.execute('''
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s

    ''',    {"question_id":question_id})
    comment = cursor.fetchall()
    return comment



@database_common.connection_handler
def get_answer_comments(cursor, answer_id):
    cursor.execute('''
                    SELECT * FROM comment
                    WHERE question_id = %(answer_id)s

    ''',       {"answer_id":answer_id})
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def delete_question_comments(cursor, comment_id):
    cursor.execute('''
                        DELETE from comment
                        WHERE id = %(comment_id)s
  
                

    ''',     {"comment_id":comment_id})



@database_common.connection_handler
def edit_question_comments(cursor, comment_id):
    cursor.execute('''


    ''', {"comment_id": comment_id})
    comment = cursor.fetchall()
    return comment



@database_common.connection_handler
def edit_comment(cursor, new_comment, comment_id):
        cursor.execute('''
        UPDATE comment
        SET message = %(new_comment)s
        WHERE id= %(comment_id)s
        ''',
                       {"new_comment": new_comment, "comment_id": comment_id})


@database_common.connection_handler
def my_profile(cursor, name):
    cursor.execute('''
                    SELECT * FROM users
                    WHERE user_name = %(name)s

    ''',
                   {"name": name})
    profile = cursor.fetchall()
    return profile


@database_common.connection_handler
def get_all_user(cursor):
    cursor.execute('''
                    SELECT * FROM users

    ''')
    users = cursor.fetchall()
    return users





@database_common.connection_handler
def get_my_questions(cursor, name):
    cursor.execute('''
                    SELECT * FROM question
                    WHERE user_name = %(name)s
    ''',     {"name": name})
    my_data = cursor.fetchall()
    return my_data


@database_common.connection_handler
def get_my_answers(cursor, name):
    cursor.execute('''
                    SELECT * FROM answer
                    WHERE user_name = %(name)s
    ''',     {"name": name})
    my_data = cursor.fetchall()
    return my_data


@database_common.connection_handler
def get_my_comments(cursor, name):
    cursor.execute('''
                    SELECT * FROM comment
                    WHERE user_name = %(name)s
    ''', {"name": name})
    my_data = cursor.fetchall()
    return my_data


@database_common.connection_handler
def add_answer_comment(cursor, comment):
    cursor.execute('''
                INSERT INTO comment (question_id, answer_id, message, submission_time, user_name)
                VALUES %(comment)s
    ''', {'comment':comment})


@database_common.connection_handler
def delete_all_comment(cursor, question_id):
    cursor.execute('''
    DELETE from comment
    WHERE question_id = %(question_id)s
    ''',
                   {"question_id": question_id})




@database_common.connection_handler
def reputation_handler(cursor,user_name, value):
    cursor.execute('''
                    UPDATE users
                    SET reputation = reputation + %(value)s
                    WHERE user_name = %(user_name)s
    
    
    ''', {"user_name":user_name, "value":value})


@database_common.connection_handler
def set_answered(cursor, answer_id):
    cursor.execute('''
                    UPDATE answer
                    SET accepted = accepted + 1
                    WHERE id = %(answer_id)s


    ''', {"answer_id":answer_id})




@database_common.connection_handler
def save_tag(cursor, new_tag):
    cursor.execute('''
                INSERT INTO question_tag (question_id, tag_id)
                VALUES %(new_tag)s
    
    ''',      {"new_tag":new_tag})


@database_common.connection_handler
def get_max_question_id(cursor):
    cursor.execute('''
                    SELECT MAX(id) FROM question
    
    ''')
    max_id = cursor.fetchall()
    return max_id


@database_common.connection_handler
def get_tags(cursor):
    cursor.execute('''
                    SELECT * FROM tag

    ''')
    max_id = cursor.fetchall()
    return max_id


@database_common.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute('''
                    SELECT name FROM tag FULL JOIN question_tag
                    ON question_tag.tag_id = tag.id
                    WHERE question_id = %(question_id)s

    ''',    {"question_id":question_id})
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def delete_tags(cursor, question_id):
    cursor.execute('''
    DELETE from question_tag
    WHERE question_id = %(question_id)s
    ''',
                   {"question_id": question_id})

@database_common.connection_handler
def count_tags(cursor):
    cursor.execute('''
                    SELECT COUNT(tag_id), name FROM question_tag JOIN tag
                    ON question_tag.tag_id = tag.id
                    GROUP BY name
                    

    ''')
    count_tag = cursor.fetchall()
    return count_tag