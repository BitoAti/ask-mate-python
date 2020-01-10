import app as app
from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, redirect, request, url_for
import data_manager

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def index():
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


@app.route('/visitor')
def enter_as_visitor():
    user_name = "visitor"
    session["user_name"] = "visitor"
    session["type"] = "visitor"
    return list(user_name)


@app.route('/list')
def list(user_name):
    if session["type"] == "visitor":
        print("visitor")
    if session["type"] == "user":
        print("user")
    return render_template('list.html', user_name = session["user_name"])


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

if __name__ == '__main__':
    app.run(debug=True)
