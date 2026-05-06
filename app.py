import os
import time
import sys
import pymysql
from flask import Flask, render_template, request, redirect


app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "root"),
        database=os.environ.get("DB_NAME", "notesdb"),
        cursorclass=pymysql.cursors.DictCursor
    )


def init_db():
    for _ in range(20):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        text VARCHAR(255) NOT NULL
                    )
                """)

            connection.commit()
            connection.close()

            print("Database connected and notes table is ready.")
            return True

        except Exception as error:
            print("Waiting for database to be ready...")
            print(error)
            time.sleep(5)

    print("Database connection failed. Please check MySQL container.")
    return False


@app.route("/")
def index():
    connection = get_db_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM notes ORDER BY id DESC")
        notes = cursor.fetchall()

    connection.close()

    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    note_text = request.form.get("note")

    if note_text:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO notes (text) VALUES (%s)",
                (note_text,)
            )

        connection.commit()
        connection.close()

    return redirect("/")


@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    connection = get_db_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM notes WHERE id = %s",
            (note_id,)
        )

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    if init_db():
        app.run(host="0.0.0.0", port=5000)
    else:
        sys.exit(1)
