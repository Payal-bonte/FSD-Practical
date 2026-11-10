from flask import Flask
import psycopg2

app = Flask(__name__)

def connect():
    return psycopg2.connect(
        dbname="vehicle",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )

@app.route("/")
def home():
    con = connect()
    cur = con.cursor()

    cur.execute("UPDATE Vehicle SET price = 700000 WHERE vid = 1")
    cur.execute("DELETE FROM Vehicle WHERE vid = 5")

    con.commit()

    cur.execute("SELECT vid, name, company, price FROM Vehicle")
    data = cur.fetchall()

    cur.close()
    con.close()

    return "<h2>Final Vehicle Records</h2>" + "<br>".join(str(row) for row in data)

app.run(debug=True)