import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '7c7b7cd8dacf674501f743dfa8c57d90'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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