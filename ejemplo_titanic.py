import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carga el archivo CSV "database_titanic.csv" en un DataFrame de pandas.
df = pd.read_csv("database_titanic.csv")

# Muestra un título y una descripción en la aplicación Streamlit.
st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

# Usando la notación "with" para crear una barra lateral en la aplicación Streamlit.
with st.sidebar:
    # Título para la sección de opciones en la barra lateral.
    st.write("# Opciones")
    
    # Crea un control deslizante (slider) que permite al usuario seleccionar un número de bins
    # en el rango de 0 a 10, con un valor predeterminado de 2.
    div = st.slider('Número de bins:', 0, 10, 2)
    
    # Muestra el valor actual del slider en la barra lateral.
    st.write("Bins=", div)

# Desplegamos un histograma con los datos del eje X
fig, ax = plt.subplots(1, 2, figsize=(10, 3))
ax[0].hist(df["Age"], bins=div)
ax[0].set_xlabel("Edad")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title("Histograma de edades")

# Tomando datos para hombres y contando la cantidad
df_male = df[df["Sex"] == "male"]
cant_male = len(df_male)

# Tomando datos para mujeres y contando la cantidad
df_female = df[df["Sex"] == "female"]
cant_female = len(df_female)

ax[1].bar(["Masculino", "Femenino"], [cant_male, cant_female], color = "red")
ax[1].set_xlabel("Sexo")
ax[1].set_ylabel("Cantidad")
ax[1].set_title('Distribución de hombres y mujeres')

# Desplegamos el gráfico
st.pyplot(fig)

st.write("""
## Muestra de datos cargados
""")
# Graficamos una tabla
st.table(df.head())




try:
    df = pd.read_csv("database_titanic.csv")
except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'database_titanic.csv'. Asegúrese de que esté en el directorio correcto.")
    st.stop() # Detiene la ejecución si el archivo no se encuentra

# Muestra un título y una descripción en la aplicación Streamlit.
st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

# Usando la notación "with" para crear una barra lateral en la aplicación Streamlit.
with st.sidebar:
    # Título para la sección de opciones en la barra lateral.
    st.write("# Opciones")
    
    # Crea un control deslizante (slider)
    # Ajustado el rango para que sea más útil (1 a 30) y un valor por defecto de 10
    div = st.slider('Número de bins para Edad:', 1, 30, 10)
    
    # Muestra el valor actual del slider en la barra lateral.
    st.write("Bins=", div)

# --- Definición de los Gráficos ---

# Desplegamos los gráficos en 1 fila y 2 columnas
fig, ax = plt.subplots(1, 2, figsize=(12, 5)) # Tamaño ajustado para claridad

# --- Gráfico 1: Histograma de Edades (Original) ---
# Usamos .dropna() para evitar errores con valores nulos (NaN) en 'Age'
ax[0].hist(df["Age"].dropna(), bins=div)
ax[0].set_xlabel("Edad")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title("Histograma de edades")

# --- Gráfico 2: Sobrevivientes por Sexo (Nuevo Gráfico Solicitado) ---

# Calcular sobrevivientes (Survived == 1) agrupados por 'Sex'
try:
    # Filtra por sobrevivientes y agrupa por sexo, contando el tamaño de cada grupo
    survivors_by_sex = df[df['Survived'] == 1].groupby('Sex').size()
    
    # Obtener los conteos (usando .get() con un default de 0 si un sexo no tiene sobrevivientes)
    female_survivors = survivors_by_sex.get('female', 0)
    male_survivors = survivors_by_sex.get('male', 0)
    
    # Etiquetas y datos para el gráfico
    sex_labels = ["Femenino", "Masculino"]
    survivor_counts = [female_survivors, male_survivors]
    
    # Crear el gráfico de barras en el segundo subplot (ax[1])
    colors = ['lightpink', 'lightblue']
    ax[1].bar(sex_labels, survivor_counts, color=colors)
    ax[1].set_xlabel("Sexo")
    ax[1].set_ylabel("Cantidad de Sobrevivientes")
    ax[1].set_title("Total de Sobrevivientes por Sexo")
    
    # Añadir los números (cantidad) encima de las barras para mayor claridad
    for i, count in enumerate(survivor_counts):
        ax[1].text(i, count + 2, str(count), ha='center', va='bottom') # +2 para dar espacio
        
except KeyError as e:
    # Manejo de error si las columnas 'Survived' o 'Sex' no existen
    ax[1].text(0.5, 0.5, f"Error: Columna '{e.args[0]}' no encontrada", 
             ha='center', va='center', color='red', wrap=True)

# Ajustar el layout para que los títulos y etiquetas no se superpongan
plt.tight_layout()

# --- Mostrar el gráfico en Streamlit ---
# Esta línea es crucial y faltaba en el script original para mostrar el plot
st.pyplot(fig)
