import whisper
import os
import glob

def transcribir_carpeta(ruta_carpeta, modelo_whisper="base"):
    """
    Lee todos los archivos de audio en una carpeta y exporta 
    la transcripción a archivos de texto individuales.
    """
    # 1. Validar que la carpeta exista
    if not os.path.exists(ruta_carpeta):
        print(f"Error: No se encontró la carpeta '{ruta_carpeta}'")
        return

    print(f"Cargando el modelo '{modelo_whisper}'...")
    modelo = whisper.load_model(modelo_whisper)

    # 2. Definir los formatos soportados
    extensiones = ['*.mp3', '*.wav', '*.m4a', '*.opus']
    archivos_audio = []
    
    for ext in extensiones:
        # Busca los archivos dentro de la carpeta indicada
        archivos_audio.extend(glob.glob(os.path.join(ruta_carpeta, ext)))

    if not archivos_audio:
        print(f"No se encontraron archivos de audio en: {ruta_carpeta}")
        return

    print(f"Se encontraron {len(archivos_audio)} archivos. Iniciando proceso por lotes...\n")
    print("-" * 50)

    # 3. Procesar cada archivo encontrado
    for ruta_audio in archivos_audio:
        # Extraer el nombre del archivo sin la extensión y crear la ruta del .txt
        nombre_base = os.path.splitext(ruta_audio)[0]
        ruta_texto = f"{nombre_base}.txt"

        # Validar si el archivo de texto ya existe para no repetir trabajo
        if os.path.exists(ruta_texto):
            print(f"Saltando '{os.path.basename(ruta_audio)}' (Ya fue transcrito)")
            continue

        print(f"Procesando: {os.path.basename(ruta_audio)}...")
        try:
            # Realizar la transcripción
            resultado = modelo.transcribe(ruta_audio)
            
            # Guardar el texto exportado
            with open(ruta_texto, "w", encoding="utf-8") as archivo:
                archivo.write(resultado["text"].strip())
                
            print(f"  ✓ Guardado exitosamente como: {os.path.basename(ruta_texto)}")
            
        except Exception as e:
            print(f"  x Error al procesar {os.path.basename(ruta_audio)}: {e}")

    print("-" * 50)
    print("¡Proceso por lotes finalizado con éxito!")

# Ejecución del utilitario
if __name__ == "__main__":
    # Cambia esto por la ruta de tu carpeta con audios.
    # Ejemplo en macOS: "/Users/TuNombre/Desktop/AudiosParaTranscribir"
    carpeta_audios = "/Users/jhumbertoh/Proyectos/Publicos/scripts/audios-to-transcribe" 
    
    transcribir_carpeta(carpeta_audios)