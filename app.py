import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuración de conexión a la base de datos
conn = psycopg2.connect(
    host="ep-bold-grass-a5n4ss38.us-east-2.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="puyIlEJ8Z1Wb",
    port = 5432
)

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

# Ruta para actualizar producto
@app.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    cantidad = data.get('cantidad')
    precio = data.get('precio')

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE Productos SET nombre=%s, descripcion=%s, cantidad=%s, precio=%s WHERE id=%s",
            (nombre, descripcion, cantidad, precio, product_id)
        )
        conn.commit()
    return jsonify({"message": "Producto actualizado"})

# Ruta para eliminar producto
@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Productos WHERE id=%s", (product_id,))
        conn.commit()
    return jsonify({"message": "Producto eliminado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
