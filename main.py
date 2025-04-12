from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Stockage simple des dernières valeurs
last_values = {
    "temp": "N/A",
    "hum": "N/A"
}

@app.route("/")
def index():
    return render_template_string("""
        <h1>🌿 Suivi de la serre</h1>
        <p>🌡️ Température : {{ temp }} °C</p>
        <p>💧 Humidité : {{ hum }} %</p>
    """, temp=last_values["temp"], hum=last_values["hum"])

@app.route("/update")
def update():
    temp = request.args.get("temp")
    hum = request.args.get("hum")
    if temp and hum:
        last_values["temp"] = temp
        last_values["hum"] = hum
        return "✅ Données mises à jour"
    return "❌ Paramètres manquants", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render donne le port via une variable d'env
    app.run(host='0.0.0.0', port=port)
