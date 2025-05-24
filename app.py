import streamlit as st
import pandas as pd
import time

# Cargar los datos desde el archivo CSV (simula una base de datos)
@st.cache_data
def cargar_tramites():
    return pd.read_csv("tramites.csv")

df_tramites = cargar_tramites()

# Título de la aplicación
st.title("Sistema de Gestión de Trámites Municipales")

# Descripción
st.write("""
Bienvenido al sistema automatizado de gestión de trámites de la **Municipalidad Provincial de Yau**.
Puedes consultar el estado de tus trámites y recibir notificaciones sobre el avance de tus solicitudes.
""")

# Agregar un menú lateral para seleccionar la sección
# Asegurémonos de que esta opción no se cree más de una vez
if 'opcion' not in st.session_state:
    st.session_state['opcion'] = "Consulta de Trámites"  # Opción por defecto

menu = ["Consulta de Trámites", "Notificaciones", "Información General"]
opcion = st.sidebar.selectbox("Selecciona una opción", menu, index=menu.index(st.session_state['opcion']))

# Actualizar el estado de la opción seleccionada
st.session_state['opcion'] = opcion

if opcion == "Consulta de Trámites":
    # Consulta de trámites
    st.header("Consulta de Estado de Trámites")
    
    # Campo para que el usuario ingrese el ID del trámite
    id_tramite = st.text_input("Ingresa tu ID de trámite", "")
    
    if id_tramite:
        # Verificar si el ID está en la base de datos
        if id_tramite in df_tramites["id_tramite"].values:
            tramite = df_tramites[df_tramites["id_tramite"] == id_tramite].iloc[0]
            st.write(f"**ID del Trámite**: {tramite['id_tramite']}")
            st.write(f"**Nombre del Trámite**: {tramite['nombre_tramite']}")
            st.write(f"**Estado**: {tramite['estado']}")
            st.write(f"**Fecha de Solicitud**: {tramite['fecha_solicitud']}")
            st.write(f"**Prioridad**: {tramite['prioridad']}")
            
            # Alertas basadas en el estado del trámite
            if tramite['estado'] == 'Pendiente':
                st.warning("🚨 **Alerta**: Tu trámite está pendiente de revisión. ¡Pronto se procesará!")
            elif tramite['estado'] == 'En Proceso':
                st.info("🔄 **Estado en Progreso**: El trámite está siendo procesado.")
            elif tramite['estado'] == 'Completado':
                st.success("✅ **Trámite Completado**: El trámite ha sido aprobado y está finalizado.")
            elif tramite['estado'] == 'Rechazado':
                st.error("❌ **Trámite Rechazado**: Lamentablemente tu solicitud ha sido rechazada.")
        else:
            st.error("No se ha encontrado un trámite con ese ID.")
    
elif opcion == "Notificaciones":
    # Sección de notificaciones
    st.header("Notificaciones sobre el Estado de los Trámites")
    
    # Simulación de una lista de notificaciones
    notificaciones = [
        "Tu trámite de Licencia de Funcionamiento está en proceso.",
        "Tu Permiso de Construcción ha sido completado.",
        "Se requiere revisión en tu solicitud de Aguas.",
        "Papeleo General pendiente de revisión.",
    ]
    
    # Mostrar las notificaciones
    if notificaciones:
        st.write("**Notificaciones Recientes**")
        for notificacion in notificaciones:
            st.write(f"- {notificacion}")
    else:
        st.write("No tienes notificaciones en este momento.")
    
elif opcion == "Información General":
    # Información general sobre el sistema
    st.header("Información General sobre los Trámites")
    st.write("""
    El sistema automatizado de gestión de trámites tiene como objetivo mejorar la eficiencia en la atención
    al ciudadano y reducir los tiempos de espera. A través de esta plataforma podrás realizar consultas sobre
    el estado de tus trámites, recibir notificaciones y acceder a información relevante sobre tus solicitudes.
    """)
    
    st.write("**¿Cómo funciona?**")
    st.write("""
    1. Ingresa tu ID de trámite para consultar su estado.
    2. Recibe notificaciones automáticas sobre el avance de tu solicitud.
    3. Si tienes dudas o necesitas más información, visita la sección de Información General.
    """)

# Simulando una pequeña carga de procesamiento para mejorar la experiencia de usuario
with st.spinner('Cargando datos...'):
    time.sleep(2)
