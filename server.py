import app as app
from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, redirect, request, url_for
import data_manager

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        username = request.form.get('user_name')
        password = request.form.get("password")
        check_line = data_manager.get_line(username)
        print(check_line)

        return redirect('/list')
    session.pop('user_name', None)
    print(session)
    questions = data_manager.get_five_question()
    print(questions)
    return render_template('index.html', question=questions)


@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get("password")
        hashed_pw = data_manager.hash_password(password)

        try:
            data_manager.save_user_data(username,hashed_pw)
            session["user_name"] = username
            return redirect('/list')
        except:
            return redirect(url_for('registration'))
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)
