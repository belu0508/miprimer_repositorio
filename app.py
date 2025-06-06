from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import pandas as pd
from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para usar flash()

# Cargar modelo y codificadores
modelo = pickle.load(open('modelo_tramites_real.pkl', 'rb'))
le_oficina = pickle.load(open('label_encoder_oficina.pkl', 'rb'))
le_distrito = pickle.load(open('label_encoder_distrito.pkl', 'rb'))

# Inicializar base de datos SQLite para trámites
def init_db():
    conn = sqlite3.connect('tramites.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tramites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            oficina TEXT,
            distrito TEXT,
            correo TEXT,
            prioridad TEXT,
            estado TEXT DEFAULT 'Recibido'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Función para enviar correo (simulación con print o usando SMTP real)
def enviar_alerta(correo, asunto, mensaje):
    print(f"Enviando correo a {correo}:\nAsunto: {asunto}\nMensaje: {mensaje}\n")
    # Aquí puedes configurar SMTP real, ejemplo con Gmail:
    # try:
    #     smtp = smtplib.SMTP('smtp.gmail.com', 587)
    #     smtp.starttls()
    #     smtp.login('tu_email@gmail.com', 'tu_contraseña')
    #     msg = MIMEText(mensaje)
    #     msg['Subject'] = asunto
    #     msg['From'] = 'tu_email@gmail.com'
    #     msg['To'] = correo
    #     smtp.send_message(msg)
    #     smtp.quit()
    # except Exception as e:
    #     print("Error enviando correo:", e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fecha_str = request.form['fecha']
        oficina = request.form['oficina']
        distrito = request.form['distrito']
        correo = request.form['correo']

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        año = fecha.year
        mes = fecha.month
        dia = fecha.day

        # Codificar
        try:
            oficina_cod = le_oficina.transform([oficina])[0]
        except:
            oficina_cod = 0
        try:
            distrito_cod = le_distrito.transform([distrito])[0]
        except:
            distrito_cod = 0

        datos = pd.DataFrame([{
            'año': año,
            'mes': mes,
            'día': dia,
            'OFICINA_DESPACHO': oficina_cod,
            'DISTRITO': distrito_cod
        }])

        prioridad = modelo.predict(datos)[0]

        # Guardar trámite en BD
        conn = sqlite3.connect('tramites.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tramites (fecha, oficina, distrito, correo, prioridad)
            VALUES (?, ?, ?, ?, ?)
        ''', (fecha_str, oficina, distrito, correo, prioridad))
        conn.commit()
        conn.close()

        # Enviar alerta de registro
        enviar_alerta(
            correo,
            "Registro de trámite recibido",
            f"Su trámite en {oficina} ha sido registrado con prioridad: {prioridad}. Estado: Recibido."
        )

        flash(f'Trámite registrado con prioridad: {prioridad}. Se ha enviado una notificación a {correo}.', 'success')
        return redirect(url_for('index'))

    # Mostrar formulario
    return render_template('index.html')

@app.route('/estado', methods=['GET', 'POST'])
def estado():
    if request.method == 'POST':
        correo = request.form['correo']
        conn = sqlite3.connect('tramites.db')
        cursor = conn.cursor()
        cursor.execute('SELECT fecha, oficina, distrito, prioridad, estado FROM tramites WHERE correo=? ORDER BY id DESC', (correo,))
        tramites = cursor.fetchall()
        conn.close()
        if not tramites:
            flash('No se encontraron trámites para ese correo.', 'warning')
        return render_template('estado.html', tramites=tramites, correo=correo)
    return render_template('estado.html', tramites=None)

if __name__ == '__main__':
    app.run(debug=True)
