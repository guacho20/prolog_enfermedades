from flask import Flask, request, render_template, flash, redirect, url_for
from pyswip import Prolog

# Application initializations
app = Flask(__name__)

# settings como va ir protegida la session
app.secret_key = "mysecretkey"

# prolog
prolog = Prolog()
prolog.consult("program.pl", True)

@app.route("/")
def Index():
    return render_template("index.html", data=[])

@app.route("/test")
def test():
    return render_template("test.html", data=[])

@app.route("/diseases")
def diseases():
    datos = list(prolog.query("enfermedades(X)"))
    diseases = []
    for fila in datos:
        data =fila['X'].replace("row(","").replace(")","").split(',')
        diseases.append(data)
    return render_template("diseases.html", data=diseases)

@app.route("/symptoms")
def symptoms():
    return render_template("symptoms.html", data=[])

@app.route("/reset")
def reset():
    return redirect(url_for("Index"))

@app.route("/diseases", methods=["POST"])
def search():
    if request.method == "POST":
        name = request.form["name_diase"]

        print(name)

        list(prolog.query("es_enfermedad(" + name + ",X)"))
  
        flash("Added successfully")

        return redirect(url_for("diseases"))


# starting the app
if __name__ == "__main__":
    app.run(port=4000, debug=True)
