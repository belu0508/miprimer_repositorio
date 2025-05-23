from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Datos de ejemplo (simulando base de datos)
tramites = [
    {"id": 1, "descripcion": "Licencia de Funcionamiento", "estado": "En Proceso"},
    {"id": 2, "descripcion": "Permiso de Obra", "estado": "Aprobado"},
]

# Ruta principal para servir la interfaz
@app.route('/')
def home():
    return render_template('miprimer_repositorio/index.html')

# Ruta para consultar el estado de un trámite
@app.route('/trámite/<int:id_tramite>', methods=['GET'])
def consultar_tramite(id_tramite):
    # Buscar el trámite por ID
    tramite = next((t for t in tramites if t['id'] == id_tramite), None)
    
    if tramite:
        return jsonify({"estado": tramite["estado"]})
    else:
        return jsonify({"error": "Trámite no encontrado"}), 404

# Ruta para registrar un nuevo trámite
@app.route('/registrar-tramite', methods=['POST'])
def registrar_tramite():
    # Obtener los datos del trámite desde la solicitud JSON
    data = request.get_json()
    descripcion = data.get('descripcion')
    tipo = data.get('tipo')
    
    if descripcion and tipo:
        # Generar un nuevo ID y añadir el trámite
        nuevo_id = len(tramites) + 1
        nuevo_tramite = {"id": nuevo_id, "descripcion": descripcion, "estado": "En Proceso"}
        tramites.append(nuevo_tramite)
        
        return jsonify({"success": True, "id": nuevo_id}), 201
    else:
        return jsonify({"error": "Faltan datos"}), 400

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
