from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

last_values = {
    "temp": None,
    "hum": None
}

@app.route("/")
def index():
    html = """
    <html>
    <head>
        <title>🌱 Capteur Serre</title>
        <meta charset="utf-8">
        <script>
            async function refreshData() {
                const response = await fetch('/data');
                const data = await response.json();
                document.getElementById('temp').innerText = data.temp || 'N/A';
                document.getElementById('hum').innerText = data.hum || 'N/A';
            }

            setInterval(refreshData, 2000); // refresh every 2 seconds
            window.onload = refreshData;
        </script>
    </head>
    <body>
        <h1>🌿 Données de la serre</h1>
        <p>🌡️ Température : <span id="temp">N/A</span> °C</p>
        <p>💧 Humidité : <span id="hum">N/A</span> %</p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/update")
def update():
    temp = request.args.get("temp")
    hum = request.args.get("hum")

    if temp and hum:
        last_values["temp"] = temp
        last_values["hum"] = hum
        return "✅ Données mises à jour"
    return "❌ Paramètres manquants", 400

@app.route("/data")
def data():
    return jsonify(last_values)
