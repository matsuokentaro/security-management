from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("database/guards.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        qualification TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database/guards.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM guards")
    total_guards = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM guards WHERE status='出勤中'"
    )
    working_guards = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM guards WHERE status='休暇'"
    )
    vacation_guards = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_guards=total_guards,
        working_guards=working_guards,
        vacation_guards=vacation_guards
    )
@app.route("/guards")
def guards():

    conn = sqlite3.connect("database/guards.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM guards")

    guards = cursor.fetchall()

    conn.close()

    return render_template(
        "guards.html",
        guards=guards
    )

@app.route("/delete/<int:id>")
def delete_guard(id):

    conn = sqlite3.connect("database/guards.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM guards WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/guards")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_guard(id):

    conn = sqlite3.connect("database/guards.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        qualification = request.form["qualification"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE guards
            SET name = ?,
                phone = ?,
                qualification = ?,
                status = ?
            WHERE id = ?
        """, (name, phone, qualification, status, id))

        conn.commit()
        conn.close()

        return redirect("/guards")

    cursor.execute(
        "SELECT * FROM guards WHERE id = ?",
        (id,)
    )

    guard = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_guard.html",
        guard=guard
    )


@app.route("/guard-form", methods=["GET", "POST"])
def guard_form():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        qualification = request.form["qualification"]
        status = request.form["status"]

        conn = sqlite3.connect("database/guards.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO guards
        (name, phone, qualification, status)
        VALUES (?, ?, ?, ?)
        """, (name, phone, qualification, status))

        conn.commit()
        conn.close()

        return redirect("/guards")

    return render_template("guard_form.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

@app.route("/sites")
def sites():
    return "<h1>現場管理（作成中）</h1>"


@app.route("/shifts")
def shifts():
    return "<h1>シフト管理（作成中）</h1>"