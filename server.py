
from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, redirect, request, url_for
import data_manager

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
from time import gmtime, strftime


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
        session["type"] = "user"
        return list(username)
    session.pop('user_name', None)
    questions = data_manager.get_five_question()
    return render_template('index.html', question=questions)


def login_as_test():
    username = "test"
    password = "test"
    session["user_name"] = "test"
    session["type"] = "user"
    return list(username)



@app.route('/visitor')
def enter_as_visitor():
    user_name = "visitor"
    session["user_name"] = "visitor"
    session["type"] = "visitor"
    return list(user_name)


@app.route('/list')
def list(user_name):
    question = data_manager.get_all_question()

    """
    column = request.args.get("order_by")
    direction = request.args.get("direction")
    if column == None:
        column = "message"
        direction = "ASC"
    question = data_manager.get_all_question(column, direction)
    """
    return render_template('list.html', user_name = session["user_name"],question=question)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get("password")
        hashed_pw = data_manager.hash_password(password)
        try:
            data_manager.save_user_data(username,hashed_pw)
            session["user_name"] = username
            session["type"] = "user"
            return list(username)
        except:
            return redirect(url_for('registration'))
    return render_template('registration.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/my_profile')
def my_profile():
    return render_template("my_profile.html")


@app.route("/add-question", methods=['POST', 'GET'])
def add_question():
    new_question = ()

    if request.method == 'POST':
        new_question += (0,)
        new_question += (0,)
        new_question += (request.form.get('title'),)
        new_question += (request.form.get('message'),)
        new_question += (strftime("%Y-%m-%d %H:%M:%S", gmtime()),)
        list_of_id = data_manager.get_user_id(session["user_name"])
        user_row = list_of_id[0]
        new_question += (user_row["user_id"],)
        data_manager.add_new_question(new_question)
        return list(session["user_name"])
    return render_template("add_question.html")


if __name__ == '__main__':
    app.run(debug=True)
