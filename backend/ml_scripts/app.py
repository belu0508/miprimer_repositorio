from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Cargar y preprocesar datos
df = pd.read_csv("tramites.csv")
le = LabelEncoder()
df["tipo_tramite_cod"] = le.fit_transform(df["tipo_tramite"])

X = df[["tipo_tramite_cod", "duracion_dias", "errores_previos"]]
y = df["prioridad"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

estados = {0: "Baja prioridad", 1: "Prioridad media", 2: "Alta prioridad"}

@app.route("/")
def index():
    return render_template("index.html", tipos=le.classes_)

@app.route("/predecir", methods=["POST"])
def predecir():
    data = request.json
    tipo = data["tipo_tramite"]
    duracion = int(data["duracion_dias"])
    errores = int(data["errores_previos"])
    ciudadano = data.get("ciudadano", "Usuario")

    # Codificar tipo
    if tipo not in le.classes_:
        return jsonify({"error": "Tipo de trámite no válido"}), 400
    tipo_cod = le.transform([tipo])[0]

    X_nuevo = [[tipo_cod, duracion, errores]]
    prioridad_pred = model.predict(X_nuevo)[0]
    estado = estados[prioridad_pred]

    # Simular envío de alerta (aquí solo retornamos mensaje)
    alerta = f"Estimado/a {ciudadano}, su trámite '{tipo}' está ahora en estado: {estado}."

    return jsonify({"prioridad": estado, "alerta": alerta})


if __name__ == "__main__":
    app.run(debug=True)
