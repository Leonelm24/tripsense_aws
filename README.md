# TripSense – Sistema de recomendación de actividades para viajeros

TripSense es un proyecto de análisis y recomendación de actividades personalizadas para huéspedes de hotel, basado en datos de reservas y lugares extraídos con la API de Google Places. El objetivo es transformar datos crudos en dashboards dinámicos y visuales en Power BI, simulando un sistema real de recomendaciones.

---

## 📁 Estructura del proyecto

```
TripSense/
│
├── data/
│   ├── raw/               # Datos sin procesar (extracción)
│   ├── processed/         # Datos limpios y listos para análisis
│
├── src/                   # Módulos Python organizados
│   ├── extract.py         # Extracción desde API o CSVs
│   ├── transformation.py  # Limpieza y transformación de datos
│   ├── load.py            # Guardado de datos procesados
│   ├── eda.py             # Análisis exploratorio (EDA)
│   └── stats.py           # Modelado y estadísticas
│
├── pipeline/              # Pipelines para cada tabla
│   ├── pipeline_places.py
│   ├── pipeline_reservations.py
│   └── pipeline_itineraries.py
│
├── main.py                # Script que ejecuta todo el proceso ETL
├── config.py   
├── requirements.txt       # Librerías necesarias
└── README.md              # Este archivo
```

---

## 🔄 Flujo del proyecto

1. **Extracción (Extract)**  
   - Se extraen datos de lugares (places) usando la API de Google Places.
   - Se carga un CSV real de reservas de hotel (`Hotel_Reservations.csv` de Kaggle).

2. **Transformación (Transform)**  
   - Limpieza de columnas, cambio de tipos de datos, creación de índices y fechas de check-in/check-out.
   - Simulación de ratings, generación de comentarios con OpenAI (opcional), cálculo de distancias.

3. **Carga (Load)**  
   - Se guardan los datos limpios en `/data/processed/`.

4. **Análisis y Visualización**  
   - Se diseñan dashboards en Power BI a partir de las tablas generadas, conectando los datos con relaciones bien definidas.

---

## 📊 Dashboards de Power BI

- **Resumen general**: reservas, ingresos, actividades, cupones, tipo de viajero/habitación.
- **Top Actividades**: ranking por estrellas, tipos de actividad, embudo de aceptación.
- **Ficha por lugar**: detalles, aceptación, distribución por tipo de viajero.
- **Time Slot & Temporadas**: horarios preferidos, ranking por franja horaria.
- **Análisis financiero** (opcional): cruces entre precio habitación, tipo viajero y uso de cupones.

> Puedes ver capturas de los dashboards en https://drive.google.com/drive/folders/1O-JhVkMK-Ym3KJc8SRd5wvZFaduPojsj?usp=sharing

---

## 🧠 Técnicas utilizadas

- Python (ETL, generación de datos, simulaciones)
- Google Places API
- Power BI (modelado, medidas DAX, visualizaciones)
- Pandas, NumPy, Seaborn, Matplotlib
- Organización modular y orientada a pipelines

---

## ▶ Cómo ejecutar

```bash
# Instala las dependencias
pip install -r requirements.txt

# Añade en config.py tu API KEY y las coordenadas del hotel al que quieres analizar

# Ejecuta el proyecto completo
python main.py
```

---

## 📌 Notas adicionales

- Se han añadido datos realistas como fotos, distancias, categorías de lugares, y simulación de comportamientos de usuarios.
- Ideal para entender cómo trabajar un proyecto ETL realista como Data Analyst o Data Engineer.

---

## 👤 Autor

Leonel Martinez
Contacto: lic.leonelmartinez@gmail.com

---

