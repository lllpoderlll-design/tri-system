# =======================================================
# TRI-SISTEMA AI FOREX API
# Sistema de integración entre MetaTrader 5 (MT5) y 3 IAs:
# - ChatGPT 5.1
# - Gemini 1.5 Pro
# - DeepSeek R1
#
# Este archivo contiene los endpoints que reciben datos
# enviados desde MT5 y los distribuyen a cada IA para
# análisis, procesamiento y generación de señales.
# =======================================================
# ============================================================
#  TRI-SISTEMA AI FOREX API 
#  ChatGPT (GPT-5.1) + Gemini 1.5 Pro + DeepSeek Reasoner
#  Endpoints listos para MT5 + Render
# ============================================================

import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ============================================================
# 1. CARGAR CLAVES DESDE VARIABLES DE ENTORNO
# ============================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Modelos por defecto:
OPENAI_MODEL = "gpt-5.1"
GEMINI_MODEL = "gemini-1.5-pro"
DEEPSEEK_MODEL = "deepseek-reasoner"


# ============================================================
# 2. ENDPOINT PARA RECIBIR DATA DE MT5
# ============================================================
@app.route("/mt5", methods=["POST"])
def mt5_webhook():
    data = request.json

    if not data:
        return jsonify({"error": "No MT5 data received"}), 400

    print("📥 DATA RECIBIDA DE MT5 →", data)

    return jsonify({"status": "MT5 data received successfully"}), 200


# ============================================================
# 3. CHATGPT (GPT-5.1)
# ============================================================
@app.route("/chatgpt", methods=["POST"])
def chatgpt_endpoint():
    payload = request.json
    prompt = payload.get("prompt", "")

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    response = r.json()
    return jsonify(response)


# ============================================================
# 4. GEMINI (GOOGLE)
# ============================================================
@app.route("/gemini", methods=["POST"])
def gemini_endpoint():
    payload = request.json
    prompt = payload.get("prompt", "")

    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}",
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )

    response = r.json()
    return jsonify(response)


# ============================================================
# 5. DEEPSEEK (RAZONAMIENTO / REASONER)
# ============================================================
@app.route("/deepseek", methods=["POST"])
def deepseek_endpoint():
    payload = request.json
    prompt = payload.get("prompt", "")

    r = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": DEEPSEEK_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    response = r.json()
    return jsonify(response)


# ============================================================
# 6. HOME (CHECK)
# ============================================================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "TRI-SISTEMA AI Forex API Running"})


# ============================================================
# 7. RUN LOCAL (Render ignora esto)
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
