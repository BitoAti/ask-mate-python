from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, redirect, request, \
    url_for
import data_manager
from time import gmtime, strftime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def index():
    return login_as_test()
    if request.method == 'POST':
        username = request.form.get('user_name')

        password = request.form.get("password")
        result_list = data_manager.get_line(username)

        if len(result_list) != 1:
            return redirect('/')
        user_row = result_list[0]
        if not data_manager.verify_password(password, user_row['password']):
            return redirect('/')

        session["user_name"] = username
        if username == "Admin":
            session["type"] = "Admin"
        else:
            session["type"] = "user"
        return redirect(url_for("list"))

    session.pop('type', None)
    session.pop('user_name', None)
    questions = data_manager.get_five_question()
    return render_template('index.html', question=questions)


def login_as_test():
    session["user_name"] = "Admin"
    session["type"] = "Admin"
    return list()


@app.route('/visitor')
def enter_as_visitor():
    session["user_name"] = "visitor"
    session["type"] = "visitor"
    return redirect("/list")


@app.route('/list', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        word_for_search = request.form.get("search_phrase")
        return redirect(url_for("result", search_phrase=word_for_search))
    column = request.args.get("order_by")
    direction = request.args.get("direction")
    if column == None:
        column = "message"
        direction = "ASC"
    question = data_manager.get_all_question(column, direction)
    my_id = data_manager.get_user_id(session["user_name"])
    return render_template("list.html", question=question, my_id=my_id)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get("password")
        hashed_pw = data_manager.hash_password(password)
        try:
            data_manager.save_user_data(username, hashed_pw)
            session["user_name"] = username
            session["type"] = "user"
            return redirect(url_for("list", user_name=username))
        except:
            return redirect(url_for('registration'))
    return render_template('registration.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('type', None)

    return redirect(url_for('index'))


@app.route('/user/<user_id>')
def my_profile(user_id):
    name = session["user_name"]
    profile = data_manager.my_profile(name)
    my_questions = data_manager.get_my_questions(name)
    my_answers = data_manager.get_my_answers(name)
    print(my_answers)
    my_comments = data_manager.get_my_comments(name)
    return render_template("my_profile.html", profile=profile[0], my_questions=my_questions, my_answers=my_answers, my_comments=my_comments)


@app.route("/add-question", methods=['POST', 'GET'])
def add_question():
    new_question = ()
    if request.method == 'POST':
        new_question += (0,)
        new_question += (0,)
        new_question += (request.form.get('title'),)
        new_question += (request.form.get('message'),)
        new_question += (strftime("%Y-%m-%d %H:%M:%S", gmtime()),)
        new_question += (session["user_name"],)
        data_manager.add_new_question(new_question)
        return redirect("/list")
    return render_template("add_question.html")


@app.route("/display_question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question(question_id)
    answer = data_manager.get_answers(question_id)
    question_comments = data_manager.get_question_comments(question_id)
    answer_comments = data_manager.get_answer_comments(question_id)
    print(answer_comments)
    return render_template("display_question.html", question=question, answer=answer,
                           question_comments=question_comments, answer_comments=answer_comments)


@app.route('/display_question/<question_id>/add_answer', methods=['POST', 'GET'])
def add_answer(question_id):
    new_answer = ()
    if request.method == 'POST':
        new_answer += (0,)
        new_answer += (question_id,)
        new_answer += (request.form.get('ans'),)
        new_answer += (strftime("%Y-%m-%d %H:%M:%S", gmtime()),)
        new_answer += (session["user_name"],)
        data_manager.add_new_answer(new_answer)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_answer.html', question_id=question_id)


@app.route('/display_question/<question_id>/delete_question')
def delete_question(question_id):
    data_manager.delete_all_comment(int(question_id))
    data_manager.delete_all_answer(int(question_id))
    data_manager.delete_question(int(question_id))
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    question_to_edit = data_manager.get_question(question_id)
    if request.method == 'POST':
        new_title = ()
        new_message = ()
        new_title += (request.form.get('title'),)
        new_message += (request.form.get('message'),)
        data_manager.write_edited_question(new_title, new_message, question_id)
        return redirect(url_for("display_question", question_id=question_id))
    return render_template('edit_question.html', question_to_edit=question_to_edit)


@app.route('/answer/<answer_id>/edit', methods=['POST', 'GET'])
def edit_answer(answer_id):
    answer_to_edit = data_manager.get_one_answer(answer_id)
    if request.method == 'POST':
        new_answer = (request.form.get('ans'),)
        data_manager.edit_answer(new_answer, answer_id)
        result = data_manager.get_question_id(answer_id)
        res = result[0]
        question_id = res["question_id"]
        return redirect(url_for('display_question', question_id=question_id, ))
    return render_template('edit_answer.html', answer_to_edit=answer_to_edit)


@app.route('/display_question/<question_id>/question_vote_up')
def question_vote_up(question_id):
    data_manager.question_vote_up(question_id)
    return redirect(url_for('display_question', question_id=question_id, ))


@app.route('/display_question/<question_id>/question_vote_down')
def question_vote_down(question_id):
    data_manager.question_vote_down(question_id)
    return redirect(url_for('display_question', question_id=question_id, ))


@app.route('/display_question/<question_id>/delete_answer/<answer_id>')
def delete_answer(question_id, answer_id):
    data_manager.delete_one_answer(int(answer_id))
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    data_manager.answer_vote_up(answer_id)
    result = data_manager.get_question_id(answer_id)
    res = result[0]
    question_id = res["question_id"]
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    data_manager.answer_vote_down(answer_id)
    result = data_manager.get_question_id(answer_id)
    res = result[0]
    question_id = res["question_id"]
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/search?q=<search_phrase>')
def result(search_phrase):
    word = "%" + search_phrase + "%"
    questions = data_manager.get_result_q(word)
    answer = data_manager.get_result_a(word)
    return render_template('result.html', questions=questions, answer=answer)


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def add_comment_to_question(question_id):
    if request.method == "POST":
        comment = ()
        comment += (question_id,)
        comment += (request.form.get("question_comment"),)
        comment += (strftime("%Y-%m-%d %H:%M:%S", gmtime()),)

        comment += (session["user_name"],)
        data_manager.add_question_comment(comment)
        return redirect(url_for("display_question", question_id=question_id))
    return render_template("comment_question.html", question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_comment_to_answer(answer_id):
    ques_id = data_manager.get_question_id(answer_id)
    q_id=ques_id[0]
    question_id = q_id['question_id']
    if request.method == "POST":
        comment = ()
        comment += (question_id, )
        comment += (answer_id, )
        comment += (request.form.get('answer_comment'), )
        comment += (strftime("%Y-%m-%d %H:%M:%S", gmtime()),)
        comment += (session['user_name'], )
        print(comment)
        data_manager.add_answer_comment(comment)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("comment_answer.html", answer_id=answer_id, question_id=question_id)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_question_comment(comment_id):
    comment = data_manager.get_one_comment(comment_id)
    comm = comment[0]
    question_id = comm["question_id"]
    print(question_id)

    if request.method == "POST":
        new_comment = request.form.get("new_question_comment")
        print(new_comment)
        data_manager.edit_comment(new_comment, comment_id)
        return redirect(url_for("display_question", question_id=question_id))
    return render_template("edit_question_comment.html", comment=comment)


@app.route('/comment/<comment_id>/delete/<question_id>')
def delete_question_comment(comment_id,question_id):
    data_manager.delete_question_comments(comment_id)
    return redirect(url_for("display_question", question_id=question_id))



@app.route('/userlist')
def list_of_users():
    user_list = data_manager.get_all_user()
    return render_template("list_of_users.html", user_list=user_list)




if __name__ == '__main__':
    app.run(debug=True)
