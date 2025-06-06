from flask import Flask, render_template, request
import pickle
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Cargar modelo y codificadores
modelo = pickle.load(open('modelo_tramites_real.pkl', 'rb'))
le_oficina = pickle.load(open('label_encoder_oficina.pkl', 'rb'))
le_distrito = pickle.load(open('label_encoder_distrito.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predecir', methods=['POST'])
def predecir():
    # Recibir datos del formulario
    fecha_str = request.form['fecha']
    oficina = request.form['oficina']
    distrito = request.form['distrito']

    # Procesar la fecha
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
    año = fecha.year
    mes = fecha.month
    dia = fecha.day

    # Codificar valores categóricos usando LabelEncoder entrenado
    try:
        oficina_cod = le_oficina.transform([oficina])[0]
    except:
        oficina_cod = 0  # Valor por defecto si no está en el encoder

    try:
        distrito_cod = le_distrito.transform([distrito])[0]
    except:
        distrito_cod = 0  # Valor por defecto si no está en el encoder

    # Crear DataFrame de entrada para el modelo
    datos = pd.DataFrame([{
        'año': año,
        'mes': mes,
        'día': dia,
        'OFICINA_DESPACHO': oficina_cod,
        'DISTRITO': distrito_cod
    }])

    # Realizar la predicción
    prediccion = modelo.predict(datos)[0]

    return render_template('index.html', resultado=prediccion)

if __name__ == '__main__':
    app.run(debug=True)
