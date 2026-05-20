import requests
import zipfile
import pandas as pd
import io
import os

def procesar_datos():
    url = "https://ssl.renfe.com/gtransit/Fichero_AV_LD/google_transit.zip"
    temp_dir = "temp_txt"
    output_dir = "data_csv"
    
    # 1. Descargar y extraer
    print("Accediendo a los datos de Renfe...")
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(temp_dir)
    else:
        print(f"Error al descargar: {response.status_code}")
        return

    # 2. Crear carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 3. Conversión de TXT a CSV
    for archivo in os.listdir(temp_dir):
        if archivo.endswith(".txt"):
            path_txt = os.path.join(temp_dir, archivo)
            nombre_csv = archivo.replace(".txt", ".csv")
            
            try:
                # Usamos sep=',' porque ya sabemos que es el delimitador
                # latin1 suele ser el estándar en estos ficheros de administración
                df = pd.read_csv(path_txt, sep=',', encoding='latin1', low_memory=False)
                
                # Limpieza rápida: quitar espacios en nombres de columnas
                df.columns = [c.strip() for c in df.columns]
                
                # Guardar como CSV estándar (separado por comas, UTF-8)
                df.to_csv(os.path.join(output_dir, nombre_csv), index=False, encoding='utf-8')
                print(f"Éxito: {archivo} -> {nombre_csv}")
            except Exception as e:
                print(f"Error procesando {archivo}: {e}")

if __name__ == "__main__":
    procesar_datos()