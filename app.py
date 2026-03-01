from flask import Flask, render_template, request, jsonify
import anthropic
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

historique = []

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    question = request.json["message"]
    historique.append({"role": "user", "content": question})

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="Tu es un expert en finance et règles métier. Réponds toujours en français de façon claire et simple.",
        messages=historique
    )

    reponse = message.content[0].text
    historique.append({"role": "assistant", "content": reponse})

    dossier = os.path.expanduser("~/Documents/Coding/historique")
    os.makedirs(dossier, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    fichier_path = os.path.join(dossier, f"conversation_{date}.txt")

    with open(fichier_path, "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] Toi : {question}\n")
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] Claude : {reponse}\n")
        f.write("-" * 50 + "\n")

    return jsonify({"reponse": reponse})

if __name__ == "__main__":
    app.run(debug=True)
