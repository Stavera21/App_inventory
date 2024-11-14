from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Configuración de conexión a la base de datos
try:
    conn = psycopg2.connect(
        host="ep-bold-grass-a5n4ss38.us-east-2.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="puyIlEJ8Z1Wb",
        port=5432
    )
    print("Conexión exitosa")
except psycopg2.Error as e:
    print(f"Error en la conexión: {e}")

# Ruta para servir la página principal
@app.route('/')
def index():
    return send_from_directory('.', 'main.html')

# Ruta para agregar producto
@app.route('/add_product', methods=['POST'])
def add_product():
    product = request.json
    nombre = product['nombre']
    descripcion = product.get('descripcion', '')
    cantidad = product['cantidad']
    precio = product['precio']

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Productos (nombre, descripcion, cantidad, precio) VALUES (%s, %s, %s, %s)",
            (nombre, descripcion, cantidad, precio)
        )
        conn.commit()
    return jsonify({"message": "Producto agregado"}), 201

# Ruta para listar productos
@app.route('/products', methods=['GET'])
def get_products():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Productos")
        products = cursor.fetchall()
        product_list = [
            {"id": row[0], "nombre": row[1], "descripcion": row[2], "cantidad": row[3], "precio": row[4]}
            for row in products
        ]
    return jsonify(product_list)

# Ruta para obtener un producto por ID
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Productos WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if product:
            product_data = {
                "id": product[0],
                "nombre": product[1],
                "descripcion": product[2],
                "cantidad": product[3],
                "precio": product[4]
            }
            return jsonify(product_data)
        else:
            return jsonify({"message": "Producto no encontrado"}), 404
        
@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = request.json
    nombre = product.get('nombre')
    descripcion = product.get('descripcion', '')
    cantidad = product.get('cantidad')
    precio = product.get('precio')

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Productos
                SET nombre = %s, descripcion = %s, cantidad = %s, precio = %s
                WHERE id = %s
                """,
                (nombre, descripcion, cantidad, precio, product_id)
            )
            if cursor.rowcount > 0:
                conn.commit()
                return jsonify({"message": "Producto actualizado"}), 200
            else:
                conn.rollback()
                return jsonify({"message": f"Producto con ID {product_id} no encontrado"}), 404
    except psycopg2.Error as e:
        conn.rollback()
        error_message = str(e)
        print(f"Error al actualizar el producto: {error_message}")
        return jsonify({"message": "Error al actualizar el producto", "error": error_message}), 500

# Ruta para eliminar un producto por ID
@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Productos WHERE id = %s", (product_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Producto eliminado"}), 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)