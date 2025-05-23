import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Cargar los datos simulados
df = pd.read_csv("tramites.csv")

print("Vista previa de los datos:")
print(df.head())

# Codificar el tipo de trámite con números
le = LabelEncoder()
df["tipo_tramite_cod"] = le.fit_transform(df["tipo_tramite"])

# Mostrar cómo se codificaron los tipos
print("\nCodificación de tipos de trámite:")
for original, codificado in zip(le.classes_, le.transform(le.classes_)):
    print(f"{original} --> {codificado}")

# Visualizar distribución de prioridades
plt.figure(figsize=(6, 4))
df["prioridad"].value_counts().sort_index().plot(kind="bar", color="skyblue")
plt.title("Distribución de Prioridades")
plt.xlabel("Nivel de prioridad (0 = baja, 1 = media, 2 = alta)")
plt.ylabel("Cantidad de trámites")
plt.tight_layout()
plt.savefig("distribucion_prioridades.png")
plt.show()

# Guardar los datos ya codificados
df.to_csv("tramites_preprocesado.csv", index=False)
print("\nArchivo 'tramites_preprocesado.csv' guardado con éxito.")
