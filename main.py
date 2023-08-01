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
    datos = format_data(list(prolog.query("sintomas(X)")))
    return render_template("test.html", data=datos)

@app.route("/diseases")
def diseases():
    datos = format_data(list(prolog.query("enfermedades(X)")))
    return render_template("diseases.html", data=datos)

@app.route("/symptoms")
def symptoms():
    datos = format_data(list(prolog.query("sintomas(X)")))
    return render_template("symptoms.html", data=datos)

@app.route("/diseasebysymptom")
def diseasebysymptom():

    diseases = format_data(list(prolog.query("enfermedades(X)")))
    symptoms = format_data(list(prolog.query("sintomas(X)")))
    diseasebysymptom = format_data(list(prolog.query("enfermedad_sintomas(X)")))
    
    return render_template("diseasebysymptom.html", data=[diseases, symptoms, diseasebysymptom ])

@app.route("/diseasebytreatment")
def diseasebytreatment():

    diseases = format_data(list(prolog.query("enfermedades(X)")))
    treatments = format_data(list(prolog.query("tratamientos(X)")))    
    
    return render_template("diseasebytreatment.html", data=[diseases,treatments])


#METODO POST
@app.route("/diseases", methods=["POST"])
def add_diseases():
    if request.method == "POST":
        name = request.form["name_diase"]

        print(name)

        list(prolog.query("es_enfermedad(" + replace_space_by_underscore(name) + ",X)"))
  
        flash("Added successfully")

        return redirect(url_for("diseases"))

@app.route("/symptoms", methods=["POST"])
def add_symptoms():
    if request.method == "POST":
        name = request.form["name_symtom"]

        print(name)

        list(prolog.query("es_sintoma(" + replace_space_by_underscore(name) + ",X)"))
  
        flash("Added successfully")

        return redirect(url_for("symptoms"))
    
@app.route("/diseasebysymptom", methods=["POST"])
def add_diseasebysymptom():
    if request.method == "POST":
        enfermedad = request.form["enfermedad"]
        sintoma = request.form["sintoma"]

        print(enfermedad, sintoma)

        list(prolog.query("tiene_sintoma("+enfermedad+"," + sintoma + ",X)"))
  
        flash("Added successfully")

        return redirect(url_for("diseasebysymptom"))

@app.route("/diseasebytreatment", methods=["POST"])
def add_diseasebytreatment():
    if request.method == "POST":
        enfermedad = request.form["enfermedad"]
        tratamiento = request.form["tratamiento"]

        print(enfermedad, tratamiento)

        list(prolog.query("tiene_tratamiento("+enfermedad+"," + replace_space_by_underscore(tratamiento) + ",X)"))
  
        flash("Added successfully")

        return redirect(url_for("diseasebytreatment"))

@app.route("/test", methods=["POST"])
def diagnostic():
    if request.method == "POST":
        #sintomas = request.form["sintomas"]
        frutas = request.form.getlist('frutas[]')
        print(len(frutas))
        if len(frutas) == 0:
           flash("Seleccione los sintomas para diagnosticar", "error")
           return redirect(url_for("test"))
        
        print(frutas)
        print(', '.join(frutas))
        print( 'Las Frutas seleccionadas son: ' + ', '.join(frutas))
        #print(sintomas)
        """ tratamiento = request.form["tratamiento"]


        list(prolog.query("tiene_tratamiento("+enfermedad+"," + replace_space_by_underscore(tratamiento) + ",X)")) """
  
        flash("Added successfully", 'info')


        return redirect(url_for("test"))

#Funtions
def format_data(datos):
    newdata = []
    for fila in datos:
        data =fila['X'].replace("row(","").replace(")","").split(',')
        newdata.append(data)
    return newdata

def replace_space_by_underscore(text):
    name = text.replace(" ","_")
    return name.lower()

# starting the app
if __name__ == "__main__":
    app.run(port=4000, debug=True)
