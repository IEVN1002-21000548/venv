from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'menu_tech'

mysql = MySQL(app)

'''========================================'''


#Funcion para ver registros de usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre, contrasena, es_admin FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    return jsonify([{'nombre': row[0], 'contrasena': row[1], 'es_admin': row[2]} for row in usuarios])

#Funcion para ver registros de clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, restaurante, direccion, puesto, contrato, fecha FROM clientes ")
    usuarios = cur.fetchall()
    cur.close()
    return jsonify([{'id': row[0], 'nombre': row[1], 'restaurante': row[2], 'direccion':row[3], 'puesto':row[4], 'contrato':row[5], 'fecha':row[6]} for row in usuarios])

#Funcion para ver registros de platillos
@app.route('/platillos', methods=['GET'])
def get_platillos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  nombre, descripcion, restaurante, precio, ingredientes, inf_nutricional, id FROM platillos")
    usuarios = cur.fetchall()
    cur.close()
    return jsonify([{'nombre': row[0], 'descripcion': row[1], 'restaurante': row[2], 'precio': row[3], 'ingredientes': row[4], 'inf_nutricional': row[5], 'id': row[6]} for row in usuarios])

#Funcion para agregar usuarios.
@app.route('/usuarios', methods=['POST'])
def add_usuario():
    if not request.is_json:
        return jsonify({"error": "El formato no es JSON"}), 415

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "El JSON debe ser un objeto, no una lista"}), 400

    try:
        # Conexión a la base de datos
        cur = mysql.connection.cursor()

        # Verificar si el usuario ya existe
        cur.execute("SELECT COUNT(*) FROM usuarios WHERE nombre = %s", (data['nombre'],))
        user_exists = cur.fetchone()[0]

        if user_exists:
            return jsonify({"error": "El nombre de usuario ya esta tomado"}), 409

        # Insertar nuevo usuario
        cur.execute(
            "INSERT INTO usuarios (nombre, contrasena, es_admin) VALUES (%s, %s, %s)",
            (data['nombre'], data['contrasena'], data['es_admin'])
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Usuario añadido exitosamente"}), 201
    
    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": f"Error al añadir al cliente: {str(e)}"}), 500

#Funcion para agregar clientes.
@app.route('/clientes', methods=['POST'])
def add_clientes():
    if not request.is_json:
        return jsonify({"error": "El formato no es JSON"}), 415

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "El JSON debe ser un objeto, no una lista"}), 400

    try:
        # Conexión a la base de datos
        cur = mysql.connection.cursor()

        # Verificar si el restaurante ya existe
        cur.execute("SELECT COUNT(*) FROM clientes WHERE restaurante = %s", (data['restaurante'],))
        user_exists = cur.fetchone()[0]

        if user_exists:
            return jsonify({"error": "El cliente ya esta agregado"}), 409

        # Insertar nuevo usuario
        cur.execute(
            "INSERT INTO clientes (nombre, restaurante, direccion, puesto) VALUES (%s, %s, %s, %s)",
            (data['nombre'], data['restaurante'], data['direccion'], data['puesto'])
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Cliente añadido exitosamente"}), 201

    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": f"Error al añadir al cliente: {str(e)}"}), 500

#Funcion para agregar platillos.
@app.route('/platillos', methods=['POST'])
def add_platillos():
    if not request.is_json:
        return jsonify({"error": "El formato no es JSON"}), 415

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "El JSON debe ser un objeto, no una lista"}), 400

    try:
        # Conexión a la base de datos
        cur = mysql.connection.cursor()

        # Verificar si el restaurante ya existe y tiene el platillo
        cur.execute("SELECT COUNT(*) FROM platillos WHERE restaurante = %s AND nombre = %s", (data['restaurante'], data['nombre'],))
        user_exists = cur.fetchone()[0]

        if user_exists:
            return jsonify({"error": "El platillo ya esta agregado en el restaurante"}), 409

        # Insertar nuevo platillo
        cur.execute(
            "INSERT INTO platillos (nombre, descripcion, precio, ingredientes, inf_nutricional, restaurante) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['nombre'], data['descripcion'], data['precio'], data['ingredientes'], data['inf_nutricional'], data['restaurante'],)
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Platillo añadido exitosamente"}), 201

    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": f"Error al añadir el platillo: {str(e)}"}), 500

#Funcion para borrar clientes
@app.route('/clientesborrar', methods=['POST'])
def borrar_clientes():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
   
    data = request.get_json()
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM clientes WHERE id = %s", (data['id'],))

        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Cliente borrado exitosamente"}), 201
    
    except Exception as e:
        
        print("Error en el servidor:", str(e))
        return jsonify({"error": f"Error borrar el cliente: {str(e)}"}), 500
    
#Funcion para borrar usuarios
@app.route('/usuariosborrar', methods=['POST'])
def borrar_usuarios():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
   
    data = request.get_json()
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM usuarios WHERE nombre = %s", (data['nombre'],))

        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Usuario borrado exitosamente"}), 201
    
    except Exception as e:
        
        print("Error en el servidor:", str(e))
        return jsonify({"error": f"Error borrar el usuario: {str(e)}"}), 500
    
#Funcion para borrar platillos
@app.route('/platillosborrar', methods=['POST'])
def borrar_platillos():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
   
    data = request.get_json()
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM platillos WHERE restaurante = %s", (data['restaurante'],))

        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Platillo borrado exitosamente"}), 201
    
    except Exception as e:
        
        print("Error en el servidor:", str(e))
        return jsonify({"error": f"Error borrar el platillo: {str(e)}"}), 500

#Funcion para borrar platillos
@app.route('/borrarplatillo', methods=['POST'])
def borrar_platillos_unico():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
   
    data = request.get_json()
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM platillos WHERE id = %s", (data['id'],))

        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Platillo borrado exitosamente"}), 201
    
    except Exception as e:
        
        print("Error en el servidor:", str(e))
        return jsonify({"error": f"Error borrar el platillo: {str(e)}"}), 500
    
''' Funciones para filtrar, buscar y manejar usuarios registrados '''

# Ruta para verificar al usuario
@app.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    nombre = data.get('nombre')
    contrasena = data.get('contrasena')

    # Verificar que se enviaron los datos necesarios
    if not nombre or not contrasena:
        return jsonify({'mensaje': 'Faltan datos para la verificación'}), 400
    
    # Realizar la consulta a la base de datos
    cur = mysql.connection.cursor()
    query = "SELECT contrasena, es_admin FROM usuarios WHERE nombre = %s"
    cur.execute(query, (nombre,))
    usuario = cur.fetchone()
    cur.close()

    # Verificar si se encontró el usuario
    if not usuario:
        return jsonify({'mensaje': 'Usuario no registrado', 'es_admin': 0}), 404

    # Validar la contraseña (comparar directamente con la base de datos)
    contrasena_db = usuario[0]  # Contraseña almacenada en la base de datos
    if contrasena != contrasena_db:
        return jsonify({'mensaje': 'Contraseña incorrecta', 'es_admin': 0}), 401

    # Responder con éxito si las credenciales son correctas
    es_admin = usuario[1]
    return jsonify({'mensaje': 'Inicio de sesión exitoso', 'es_admin': es_admin, 'nombre': nombre}), 200

#Funcion para filtrar los datos de clientes
@app.route('/datoscliente', methods=['POST'])
def obtenerDatos_Cliente():
    try:
        
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se recibió un cuerpo JSON válido"}), 400

        
        id = datos.get('id')

        if not id:
            return jsonify({"error": "No se encuentra el id especificado"}), 400

       
        cur = mysql.connection.cursor()

        query = "SELECT id, nombre, restaurante, direccion, puesto, contrato FROM clientes WHERE id = %s"
       
        cur.execute(query, (id,))
        ordenes = cur.fetchall()
        cur.close()

       
        return jsonify([{'id':row[0], 'nombre': row[1], 'restaurante': row[2], 'direccion': row[3], 'puesto':row[4],'contrato':row[5]} for row in ordenes])

    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": "Error al encontrar el cliente"}), 500

#Funcion para filtrar los platillos de clientes
@app.route('/platoscliente', methods=['POST'])
def obtenerPlatos_Cliente():
    try:
        
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se recibió un cuerpo JSON válido"}), 400

        
        restaurante = datos.get('restaurante')

        if not restaurante:
            return jsonify({"error": "No se encuentra el parametro restaurante"}), 400

       
        cur = mysql.connection.cursor()

        query = "SELECT nombre, descripcion, restaurante, precio, ingredientes, inf_nutricional, id FROM platillos WHERE restaurante = %s"
       
        cur.execute(query, (restaurante,))
        ordenes = cur.fetchall()
        cur.close()

       
        return jsonify([{'nombre': row[0], 'descripcion': row[1], 'restaurante': row[2], 'precio': row[3], 'ingredientes': row[4], 'inf_nutricional': row[5], 'id':row[6]} for row in ordenes])

    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": "Error al encontrar el restaurante"}), 500

@app.route('/actualizarcliente', methods=['POST'])
def actualizar_cliente():
    try:
        # Recibir los datos enviados en formato JSON
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se recibió un cuerpo JSON válido"}), 400

        # Extraer los campos necesarios
        id = datos.get('id')
        nombre = datos.get('nombre')
        restaurante = datos.get('restaurante')
        direccion = datos.get('direccion')
        puesto = datos.get('puesto')
        contrato = datos.get('contrato')

        # Verificar que todos los campos requeridos estén presentes
        if not id or not nombre or not restaurante or not direccion or not puesto:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # Conexión a la base de datos y ejecución del query
        cur = mysql.connection.cursor()

        query = """
            UPDATE clientes
            SET nombre = %s, restaurante = %s, direccion = %s, puesto = %s, contrato = %s
            WHERE id = %s
        """
        cur.execute(query, (nombre, restaurante, direccion, puesto, contrato, id))
        mysql.connection.commit()  # Confirmar los cambios en la base de datos
        cur.close()

        return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200

    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": "Error al actualizar el cliente"}), 500
    
@app.route('/actualizarplatillo', methods=['POST'])
def actualizar_platillo():
    try:
        # Recibir los datos enviados en formato JSON
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se recibió un cuerpo JSON válido"}), 400

        # Extraer los campos necesarios
        id = datos.get('id')
        nombre = datos.get('nombre')
        restaurante = datos.get('restaurante')
        descripcion = datos.get('descripcion')
        precio = datos.get('precio')
        ingredientes = datos.get('ingredientes')
        inf_nutricional = datos.get('inf_nutricional')

        # Verificar que todos los campos requeridos estén presentes
        if not id or not nombre or not restaurante:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # Conexión a la base de datos y ejecución del query
        cur = mysql.connection.cursor()

        query = """
            UPDATE platillos
            SET nombre = %s, restaurante = %s, descripcion = %s, precio = %s, ingredientes = %s, inf_nutricional = %s
            WHERE id = %s
        """
        cur.execute(query, (nombre, restaurante, descripcion, precio, ingredientes, inf_nutricional, id))
        mysql.connection.commit()  # Confirmar los cambios en la base de datos
        cur.close()

        return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200

    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": "Error al actualizar el cliente"}), 500
    
#Funcion para filtrar los datos de clientes
@app.route('/datosplatillo', methods=['POST'])
def obtenerDatos_Platillo():
    try:
        
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se recibió un cuerpo JSON válido"}), 400

        
        id = datos.get('id')

        if not id:
            return jsonify({"error": "No se encuentra el id especificado"}), 400

       
        cur = mysql.connection.cursor()

        query = "SELECT id, nombre, restaurante, descripcion, precio, ingredientes, inf_nutricional FROM platillos WHERE id = %s"
       
        cur.execute(query, (id,))
        ordenes = cur.fetchall()
        cur.close()

       
        return jsonify([{'id':row[0], 'nombre': row[1], 'restaurante': row[2], 'descripcion': row[3], 'precio':row[4],'ingredientes':row[5],'inf_nutricional':row[6]} for row in ordenes])

    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({"error": "Error al encontrar el cliente"}), 500


@app.route('/')
def hello_world():
    return '¡Servidor Flask de MenuTech!'

if __name__ == '__main__':
    app.run(debug=True)
