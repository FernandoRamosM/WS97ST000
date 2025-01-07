const productoInput = document.getElementById('input1');
const productosTabla = document.getElementById('productosTabla');

productoInput.addEventListener('keydown', async (event) => {
    if (event.key === 'Enter' || event.key === 'Tab') {
        const productoNombre = productoInput.value.trim();

        if (!productoNombre) {
            alert("Por favor ingrese un nombre de producto.");
            return;
        }

        try {
            const response = await fetch('/buscar_producto', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombre: productoNombre })
            });

            if (response.ok) {
                const data = await response.json();

                // Limpiar la tabla
                productosTabla.innerHTML = '';

                // Agregar el producto encontrado a la tabla
                const fila = `
                    <tr>
                        <td>${data.id}</td>
                        <td>${data.nombre}</td>
                        <td>${data.precio}</td>
                    </tr>
                `;
                productosTabla.insertAdjacentHTML('beforeend', fila);

                // Limpiar el input después de buscar
                productoInput.value = '';
            } else {
                const error = await response.json();
                alert(error.error || "Error al buscar el producto.");
            }
        } catch (error) {
            console.error("Error al buscar producto:", error);
        }
    }
});