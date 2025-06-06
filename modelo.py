import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import random

# Simula un conjunto de datos basado en tu estructura real
data = {
    "FECHA_REGISTRO": ["20220104", "20220104"],
    "OFICINA_DESPACHO": [
        "GERENCIA DE DESARROLLO ECONOMICO LOCAL",
        "SUB GERENCIA DE ATENCIÓN AL CIUDADANO, GESTIÓN DOCUMENTAL Y ARCHIVO"
    ],
    "DISTRITO": ["JESUS MARIA", "JESUS MARIA"],
}

df = pd.DataFrame(data)

# Repetir para generar más datos
df = pd.concat([df] * 100, ignore_index=True)

# Agregar prioridad aleatoria simulada
df['prioridad'] = [random.choice(['Alta', 'Media', 'Baja']) for _ in range(len(df))]

# Convertir FECHA_REGISTRO a datetime
df['FECHA_REGISTRO'] = pd.to_datetime(df['FECHA_REGISTRO'], format="%Y%m%d", errors="coerce")
df['año'] = df['FECHA_REGISTRO'].dt.year
df['mes'] = df['FECHA_REGISTRO'].dt.month
df['día'] = df['FECHA_REGISTRO'].dt.day

# Codificar texto a números
le_oficina = LabelEncoder()
le_distrito = LabelEncoder()

df['OFICINA_DESPACHO'] = le_oficina.fit_transform(df['OFICINA_DESPACHO'])
df['DISTRITO'] = le_distrito.fit_transform(df['DISTRITO'])

# Datos para el modelo
X = df[['año', 'mes', 'día', 'OFICINA_DESPACHO', 'DISTRITO']]
y = df['prioridad']

# Entrenamiento
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Guardar modelo y codificadores
with open("modelo_tramites_real.pkl", "wb") as f:
    pickle.dump(modelo, f)

with open("label_encoder_oficina.pkl", "wb") as f:
    pickle.dump(le_oficina, f)

with open("label_encoder_distrito.pkl", "wb") as f:
    pickle.dump(le_distrito, f)

print("✅ Modelo y codificadores guardados con éxito.")
