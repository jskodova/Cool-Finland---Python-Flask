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
    if request.method == "POST":
        print("Hello")
    else:
        return render_template('schedule.html')

    if __name__ == '__main__':
        app.run(debug=True)