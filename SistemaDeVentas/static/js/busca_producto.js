const productoInput = document.getElementById('input1');
const cantidadInput = document.getElementById('input2');

document.addEventListener('keydown', async (event) => {
    if (event.target === productoInput && event.key === 'Tab') {
        const productoCodigo = productoInput.value.trim();

        if (!productoCodigo) {
            alert("INGRESE PRODUCTO.");
            event.preventDefault(); // Previene el enfoque en el siguiente campo
            return;
        }
        try {
            const response = await fetch('/asigna_ncod', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ NCOD: productoCodigo })
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.error || "Error al buscar el producto.");
                event.preventDefault(); // Previene el enfoque si hay un error
            }
        } catch (error) {
            console.error("Error al buscar producto:", error);
            event.preventDefault(); // Previene el enfoque si hay un error
        }
    }

    if (event.target === cantidadInput && event.key === 'Tab') {
        const productoCantidad = cantidadInput.value.trim();

        if (!productoCantidad) {
            alert("INGRESE CANTIDAD.");
            event.preventDefault(); // Previene el enfoque en el siguiente campo
            return;
        }
        try {
            const response = await fetch('/PREF9701', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ CANT: productoCantidad })
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.error || "Error al buscar la cantidad.");
                event.preventDefault(); // Previene el enfoque si hay un error
            }
            window.location.reload();
        } catch (error) {
            console.error("Error al buscar cantidad:", error);
            event.preventDefault(); // Previene el enfoque si hay un error
        }
    }
});
