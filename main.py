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
    datos = list(prolog.query("sintomas(X)"))
    symptoms = []
    for fila in datos:
        data =fila['X'].replace("row(","").replace(")","").split(',')
        symptoms.append(data)
    return render_template("symptoms.html", data=symptoms)

@app.route("/diseases", methods=["POST"])
def add_diseases():
    if request.method == "POST":
        name = request.form["name_diase"]

        print(name)

        list(prolog.query("es_enfermedad(" + name + ",X)"))
  
        flash("Added successfully")

        return redirect(url_for("diseases"))

@app.route("/symptoms", methods=["POST"])
def add_symptoms():
    if request.method == "POST":
        name = request.form["name_symtom"]

        print(name)

        list(prolog.query("es_sintoma(" + name + ",X)"))
  
        flash("Added successfully")

        return redirect(url_for("symptoms"))

# starting the app
if __name__ == "__main__":
    app.run(port=4000, debug=True)
