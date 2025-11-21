from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API Funcionando Correctamente"

@app.route("/tri", methods=["POST"])
def tri():
    data = request.json
    return jsonify({
        "mensaje": "Tri recibido correctamente",
        "data": data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)