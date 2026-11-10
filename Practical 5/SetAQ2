from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def add():
        if request.method == "POST":
           a = int(request.form["a"])
           b = int(request.form["b"])
           return "Addition = " + str(a + b)
        return '<form method="post"><input name="a"><input name="b"><button>Add</button></form>'

app.run()