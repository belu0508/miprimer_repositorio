document.addEventListener('DOMContentLoaded', function () {
    // Consultar estado de trámite
    const consultaForm = document.getElementById('consulta-form');
    const estadoTramiteDiv = document.getElementById('estado-tramite');

    consultaForm.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const idTramite = document.getElementById('id_tramite').value;

        fetch(`/trámite/${idTramite}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    estadoTramiteDiv.textContent = `Error: ${data.error}`;
                    estadoTramiteDiv.classList.add('error');
                } else {
                    estadoTramiteDiv.textContent = `Estado del trámite: ${data.estado}`;
                    estadoTramiteDiv.classList.remove('error');
                    estadoTramiteDiv.classList.add('success');
                }
            })
            .catch(error => {
                estadoTramiteDiv.textContent = 'Hubo un error al consultar el estado.';
                estadoTramiteDiv.classList.add('error');
            });
    });

    // Registrar nuevo trámite
    const nuevoTramiteForm = document.getElementById('nuevo-tramite-form');
    const confirmacionTramiteDiv = document.getElementById('confirmacion-tramite');

    nuevoTramiteForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const descripcionTramite = document.getElementById('descripcion_tramite').value;
        const tipoTramite = document.getElementById('tipo_tramite').value;

        fetch('/registrar-tramite', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ descripcion: descripcionTramite, tipo: tipoTramite }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                confirmacionTramiteDiv.textContent = `Trámite registrado con éxito: ID ${data.id}`;
                confirmacionTramiteDiv.classList.add('success');
                mostrarAlerta('success', `Nuevo trámite registrado: ${data.id}`);
            } else {
                confirmacionTramiteDiv.textContent = `Error al registrar el trámite: ${data.error}`;
                confirmacionTramiteDiv.classList.add('error');
            }
        });
    });

    // Sistema de alertas
    function mostrarAlerta(tipo, mensaje) {
        const alertaContainer = document.getElementById('alertas-container');
        const alertaDiv = document.createElement('div');
        alertaDiv.classList.add('alerta', tipo);
        alertaDiv.textContent = mensaje;
        alertaContainer.appendChild(alertaDiv);
    }
});
