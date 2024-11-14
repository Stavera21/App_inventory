
async function fetchProductById() {
    const productId = document.getElementById("productId").value;

    if (!productId) {
        alert("Por favor ingresa un ID de producto.");
        return;
    }

    const response = await fetch(`/product/${productId}`);
    if (response.ok) {
        const product = await response.json();
        const productDetails = document.getElementById("productDetails");
        productDetails.innerHTML = `
            <p><strong>Nombre:</strong> ${product.nombre}</p>
            <p><strong>Descripción:</strong> ${product.descripcion}</p>
            <p><strong>Cantidad:</strong> ${product.cantidad}</p>
            <p><strong>Precio:</strong> $${product.precio}</p>
        `;
    } else {
        alert("Producto no encontrado.");
    }
}

async function addProduct() {
    const nombre = document.getElementById("nombre").value;
    const descripcion = document.getElementById("descripcion").value;
    const cantidad = document.getElementById("cantidad").value;
    const precio = document.getElementById("precio").value;

    const response = await fetch('http://127.0.0.1:5000/add_product', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ nombre, descripcion, cantidad, precio })
    });

    const result = await response.json();
    alert(result.message);
    fetchProducts(); // Actualiza la lista después de agregar
}

// Función para obtener la lista de productos
async function fetchProducts() {
    const response = await fetch('/products');
    const products = await response.json();

    const productList = document.getElementById("productList");
    productList.innerHTML = '';

    products.forEach(product => {
        const item = document.createElement("li");
        item.innerHTML = `${product.nombre} - ${product.descripcion} - Cantidad: ${product.cantidad} - Precio: $${product.precio}`;
        productList.appendChild(item);
    });
}

async function updateProduct() {
    const productId = document.getElementById("updateProductId").value;
    const nombre = document.getElementById("updateNombre").value;
    const descripcion = document.getElementById("updateDescripcion").value;
    const cantidad = document.getElementById("updateCantidad").value;
    const precio = document.getElementById("updatePrecio").value;

    if (!productId || !nombre || !cantidad || !precio) {
        alert("Por favor, completa todos los campos requeridos (ID, Nombre, Cantidad y Precio).");
        return;
    }

    const response = await fetch(`/product/${productId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, descripcion, cantidad, precio })
    });

    const result = await response.json();
    alert(result.message);
    fetchProducts(); // Actualiza la lista después de la actualización
}

async function deleteProduct() {
    const productId = document.getElementById("deleteProductId").value;

    if (!productId) {
        alert("Por favor ingresa un ID de producto.");
        return;
    }

    const response = await fetch(`/product/${productId}`, {
        method: 'DELETE',
    });

    const result = await response.json();
    alert(result.message);
    fetchProducts(); // Actualiza la lista después de eliminar
}