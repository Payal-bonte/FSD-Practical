from flask import Flask, request

app = Flask(__name__)

@app.route("/employee", methods=["GET"])
def employee():
 return {
 "name": "Amit",
 "department": "IT"
}

@app.route("/addemployee", methods=["POST"])
def addemployee():
 data = request.get_json()

 return {
    "name": data["name"],
    "department": data["department"]
}

app.run()