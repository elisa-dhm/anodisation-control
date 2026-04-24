from flask import Flask, render_template, jsonify

app = Flask(__name__)

# ----------------------------
# PAGE PRINCIPALE
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------
# API DE COMMANDE MACHINE
# ----------------------------
@app.route("/mode/<cmd>")
def mode(cmd):

    print("Commande reçue :", cmd)

    response = {
        "status": "ok",
        "command": cmd
    }

    # ----------------------------
    # LOGIQUE MACHINE (BASIC)
    # ----------------------------

    if cmd == "avance":
        print("➡️ MOTEUR : AVANCE")
    elif cmd == "recul":
        print("⬅️ MOTEUR : RECUL")

    elif cmd == "stop":
        print("⛔ MOTEUR : STOP")

    else:
        print("❌ COMMANDE INCONNUE")
        response["status"] = "error"

    return jsonify(response)


# ----------------------------
# LANCEMENT SERVEUR
# ----------------------------
if __name__ == "__main__":
    print("🚀 Serveur Eloxage 26 démarré")
    app.run(host="0.0.0.0", port=5000, debug=True)
