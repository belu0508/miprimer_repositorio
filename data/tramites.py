import pandas as pd
import random

# Simular tipos de trámite
tipos_tramite = [
    "Licencia de construcción",
    "Permiso de eventos",
    "Licencia de funcionamiento",
    "Constancia de posesión",
    "Solicitud de servicios",
    "Certificado de numeración",
    "Cambio de razón social",
    "Renovación de licencia",
    "Permiso de publicidad",
    "Autorización de cierre de vía"
]

# Generar 200 registros simulados
data = []
for _ in range(200):
    tipo = random.choice(tipos_tramite)
    duracion = random.randint(1, 30)  # duración del trámite en días
    errores = random.randint(0, 5)    # cantidad de errores previos
    prioridad = 2 if duracion > 15 or errores > 3 else (1 if duracion > 5 else 0)
    data.append([tipo, duracion, errores, prioridad])

# Crear DataFrame y guardar como CSV
df = pd.DataFrame(data, columns=["tipo_tramite", "duracion_dias", "errores_previos", "prioridad"])
df.to_csv("tramites.csv", index=False)
