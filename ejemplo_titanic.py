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
with st.expander("Haz clic para ver una muestra de los datos"):

    st.dataframe(df.head())

st.write("""
# Análisis de Sobrevivientes del Titanic
## Gráfico por Sexo
""")

try:
    df = pd.read_csv("database_titanic.csv")
    survivors_by_sex = df[df['Survived'] == 1].groupby('Sex').size()
    
    female_survivors = survivors_by_sex.get('female', 0)
    male_survivors = survivors_by_sex.get('male', 0)
    
    sex_labels = ["Femenino", "Masculino"]
    survivor_counts = [female_survivors, male_survivors]
    
    fig, ax = plt.subplots(figsize=(7, 5))  
    colors = ['lightpink', 'lightblue']
    bars = ax.bar(sex_labels, survivor_counts, color=colors)
    
    ax.set_xlabel("Sexo")
    ax.set_ylabel("Cantidad de Sobrevivientes")
    ax.set_title("Total de Sobrevivientes por Sexo")
    
    # Añadir los números (cantidad) encima de las barras

    plt.tight_layout()
    
    st.pyplot(fig)

except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'database_titanic.csv'. Asegúrese de que esté en el mismo directorio.")
except KeyError as e:
    st.error(f"Error: La columna '{e.args[0]}' no se encontró en el archivo CSV. Verifique los datos.")




st.write("# Gráfico Interactivo: Tasa de Supervivencia por Clase")


try:
    clases_opciones = sorted(df['Pclass'].unique())
except KeyError:
    st.error("Error: La columna 'Pclass' no se encuentra en el archivo.")
    st.stop()

# El widget multiselect
clases_seleccionadas = st.sidebar.multiselect(
    'Seleccione Clases de Pasajero:',
    options=clases_opciones,
    default=clases_opciones  # Por defecto, todas están seleccionadas
)

# --- Lógica del Gráfico y Visualización ---

# Solo proceder si el usuario ha seleccionado al menos una clase
if not clases_seleccionadas:
    st.warning("Por favor, seleccione al menos una clase de pasajero desde la barra lateral.")
else:
    try:
        # 1. Filtrar el DataFrame según la selección
        df_filtrado = df[df['Pclass'].isin(clases_seleccionadas)]
        
        # 2. Calcular la tasa de supervivencia
        # .mean() en una columna 0/1 da la tasa (porcentaje)
        survival_rate = df_filtrado.groupby('Pclass')['Survived'].mean().reset_index()
        
        # 3. Convertir a porcentaje (ej. 0.62 a 62.0)
        survival_rate['Survived'] = survival_rate['Survived'] * 100
        
        # --- Creación del Gráfico ---
        fig, ax = plt.subplots()
        
        # Mapeo de colores robusto (para que el color no cambie si se quita una clase)
        color_map = {1: 'gold', 2: 'silver', 3: 'brown'}
        bar_colors = survival_rate['Pclass'].map(color_map)

        # Crear las barras
        bars = ax.bar(survival_rate['Pclass'], 
                      survival_rate['Survived'], 
                      color=bar_colors,
                      edgecolor='black')
        
        # --- Estética y Etiquetas ---
        ax.set_xlabel("Clase de Pasajero (Pclass)")
        ax.set_ylabel("Tasa de Supervivencia (%)")
        ax.set_title("Tasa de Supervivencia Promedio por Clase")
        
        # Asegurar que los ticks del eje X sean 1, 2, 3 (no 1.5, 2.5, etc.)
        ax.set_xticks(clases_opciones)
        
        # Fijar el límite del eje Y entre 0 y 100
        ax.set_ylim(0, 100)
        
        # Añadir etiquetas de porcentaje encima de cada barra
        for index, row in survival_rate.iterrows():
            ax.text(row['Pclass'],       # Posición X (la clase)
                    row['Survived'] + 2, # Posición Y (altura + 2)
                    f"{row['Survived']:.1f}%", # Texto (ej. "62.5%")
                    ha='center', va='bottom')
        
        plt.tight_layout()
        
        # --- Mostrar en Streamlit ---
        st.pyplot(fig)

    except KeyError as e:
        st.error(f"Error: Falta la columna '{e.args[0]}' en el archivo CSV.")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")

