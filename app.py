from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Cargar el conjunto de datos de universidades colombianas
universities_data = pd.read_csv("universidades_colombia.csv")
desercion_data = pd.read_csv("desercion_escolar.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    # Convertir todos los valores a cadenas de texto antes de ordenarlos
    locations = sorted(map(str, universities_data["Ubicacion"].unique()))
    academic_offers = sorted(map(str, universities_data["Oferta Academica"].unique()))
    if request.method == "POST":
        # Obtener los criterios de búsqueda del formulario
        location = request.form.get("location")
        academic_offer = request.form.get("academic_offer")
        # Realizar la búsqueda en el conjunto de datos
        results = search_universities(location, academic_offer)
        return render_template("results.html", results=results)
    return render_template("index.html", locations=locations, academic_offers=academic_offers)

@app.route("/opiniones", methods=["GET"])
def opiniones():
    return render_template("opiniones.html")

@app.route("/graficas", methods=["GET"])
def graficas():
    desercion_data_json = desercion_data.to_dict(orient='list')
    return render_template("graficas.html", desercion_data=desercion_data_json)
def search_universities(location, academic_offer):
    # Filtrar el conjunto de datos según los criterios de búsqueda
    results = universities_data
    if location:
        results = results[results["Ubicacion"] == location]
    if academic_offer:
        results = results[results["Oferta Academica"] == academic_offer]
    return results.to_dict("records")

if __name__ == "__main__":
    app.run(debug=True)
