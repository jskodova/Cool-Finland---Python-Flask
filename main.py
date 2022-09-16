import sqlite3
from datetime import date, timedelta
from flask import Flask, render_template, request, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from functools import wraps
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

            conn.execute(
                'insert into "users" (email, password, comp_name, rep_name, rep_lname, rep_pnumber, priority) values (?, ?, ?, ?, ?, ?, ?)'
                , (email, h_passw, comp, rep_name, rep_lname, rep_pnum, False))

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
def weightschedule():
    global enable
    enable = "enable"

    global disabled
    disabled = "disabled"

    global con
    con = sqlite3.connect("database.db")

    global cur
    cur = con.cursor()

    global today
    today = date.today()

    global dates
    dates = cur.execute("SELECT weight_amount,delivery_date FROM deliveries").fetchall()

    global all_Dates
    all_Dates = list
    all_Dates = []
    for i in range(21):
        free = today + timedelta(days=i)
        day_Free = free.strftime('%Y-%m-%d')
        all_Dates.append(day_Free)

    global occupied
    occupied = []
    for occ in dates:
        occupied.append(occ[1])

    if request.method == "POST":
        global weight
        weight = request.form.get('weight')
        # cur.execute("INSERT INTO deliveries VALUES(?, ?, ?, ?)", (3,3,20,"2022-06-24"))
        # con.commit()
        return redirect('/schedule/date')
    else:
        return render_template('schedule.html', disabled_switch=disabled, today=today, all_Dates=all_Dates,
                               occupied=occupied)


def weightrequire(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            weight
        except NameError:
            return redirect('/schedule')
        return f(*args, **kwargs)

    return decorated_function


@app.route("/schedule/date", methods=['GET', 'POST'])
@weightrequire
def dayschedule():
    weight_Amount = []
    for i in dates:
        if int(i[0]) + int(weight) > 40:
            weight_Amount.append(i[1])
    weight_amount_set = set(weight_Amount)
    occupied_set = set(occupied)

    occupied_w_weight = list(weight_amount_set - occupied_set)
    combined = weight_Amount + occupied_w_weight

    free_dates = set(all_Dates).difference(set(combined))
    print(free_dates)

    if request.method == "POST":
        return redirect('/schedule')
    else:
        return render_template('schedule_day.html', enable_switch=disabled, disabled_switch=enable, dates=dates,
                               today=today, occupied=occupied, all_Dates=all_Dates, free_Dates=free_dates)


if __name__ == '__main__':
    app.run(debug=True)
