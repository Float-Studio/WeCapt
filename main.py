from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Valeurs à jour du capteur
last_values = {
    "temp": "N/A",
    "hum": "N/A"
}

# Route principale : HTML avec script JavaScript
@app.route("/")
def index():
    return """
    <html>
    <head>
        <meta charset="utf-8">
        <title>🌱 Données en direct</title>
        <style>
            body { font-family: sans-serif; text-align: center; margin-top: 50px; }
            h1 { font-size: 2rem; }
            p { font-size: 1.5rem; }
        </style>
        <script>
            async function fetchData() {
                try {
                    const res = await fetch('/data');
                    const data = await res.json();
                    document.getElementById('temp').textContent = data.temp || "N/A";
                    document.getElementById('hum').textContent = data.hum || "N/A";
                } catch (e) {
                    console.error("Erreur de récupération des données", e);
                }
            }

            setInterval(fetchData, 2000); // actualise toutes les 2s
            window.onload = fetchData;
        </script>
    </head>
    <body>
        <h1>🌿 Serre Connectée</h1>
        <p>🌡️ Température : <span id="temp">N/A</span> °C</p>
        <p>💧 Humidité : <span id="hum">N/A</span> %</p>
    </body>
    </html>
    """

# L'ESP32 appelle cette route pour envoyer ses données
@app.route("/update")
def update():
    temp = request.args.get("temp")
    hum = request.args.get("hum")
    if temp and hum:
        last_values["temp"] = temp
        last_values["hum"] = hum
        return "✅ Données reçues"
    return "❌ Paramètres manquants", 400

# Cette route est appelée par le JavaScript pour actualiser l'affichage
@app.route("/data")
def data():
    return jsonify(last_values)
# ... tout le code précédent

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
