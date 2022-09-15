import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from passlib.hash import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '7c7b7cd8dacf674501f743dfa8c57d90'


def login_val(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    users = conn.execute('select * from "users"').fetchall()
    conn.close()

    hasher = bcrypt.using(rounds=13)

    for user in users:
        if user["email"] == username:
            print(user['email'] + " " + username)
            print(password + " " + user["password"])
            print(hasher.verify(password, user["password"]))
            if hasher.verify(password, user["password"]):
                return True

    return False


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/admin")
def admin():
    conn = get_db_connection()
    cur = conn.cursor()
    users = conn.execute('select * from "users"').fetchall()
    conn.close()
    return render_template("admin.html", users=users)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        valid = form.validate_on_submit()
        if valid:
            email = form.email.data
            passw = form.passw.data
            comp = form.comp.data
            rep_name = form.rep_name.data
            rep_lname = form.rep_lname.data
            rep_pnum = form.rep_pnum.data

            hasher = bcrypt.using(rounds=13)
            h_passw = hasher.hash(passw)

            conn = get_db_connection()
            cur = conn.cursor()

            print(f"{email} {passw} {h_passw} {comp} {rep_name} {rep_lname} {rep_pnum}")

            conn.execute('insert into "users" (email, password, comp_name, rep_name, rep_lname, rep_pnumber, priority) values (?, ?, ?, ?, ?, ?, ?)'
                        ,(email, h_passw, comp, rep_name, rep_lname, rep_pnum, False))

            conn.commit()
            conn.close()
            return render_template('register.html', form=form, valid=valid)

        else:
           return render_template('register.html', form=form, valid=not valid)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        form_valid = form.validate_on_submit()

        if form_valid:

            email = form.email.data
            passw = form.passw.data
            rm = form.rem.data

            print(f"{email} {passw} {rm}")
            logged = login_val(email, passw)

            print(logged)

            if logged:
                return render_template("login.html", form=form, error=None)
            else:
                return render_template("login.html", form=form, error=1)
        else:
            return render_template("login.html", form=form, error=2)





@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    enable = "enable"
    disabled = "disabled"

    if request.method == "POST":
        weight = request.form.get('weight')
        return render_template('schedule.html', enable_switch=disabled, disabled_switch=enable)
    else:
        return render_template('schedule.html', disabled_switch=disabled)

    if __name__ == '__main__':
        app.run(debug=True)