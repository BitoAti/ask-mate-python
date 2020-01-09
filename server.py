from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, redirect, request, url_for
import data_manager


app = Flask(__name__)


@app.route('/')
def index():
    questions = data_manager.get_five_question()
    return render_template('index.html', question=questions)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get("password")

        hashed_pw = data_manager.hash_password(password)
        data_manager.save_user_data(username,hashed_pw)
        return redirect(url_for('/'))
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)
