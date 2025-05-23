import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Cargar los datos
df = pd.read_csv("data/tramites.csv")

# Vista previa
print("Primeras filas:\n", df.head())

# Estadísticas generales
print("\nResumen estadístico:\n", df.describe())

# Codificar tipo de trámite
le = LabelEncoder()
df['tipo_tramite_cod'] = le.fit_transform(df['tipo_tramite'])

# Distribución de prioridades
df['prioridad'].value_counts().plot(kind='bar', title="Distribución de prioridades")
plt.xlabel("Prioridad")
plt.ylabel("Cantidad de trámites")
plt.tight_layout()
plt.show()

# Guardar los datos preprocesados
df.to_csv("data/tramites_preprocesado.csv", index=False)
