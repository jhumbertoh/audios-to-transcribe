# Utilitario de Transcripción de Audio por Lotes con OpenAI Whisper

Este proyecto te permite leer de manera automática todos los archivos de audio de una carpeta (`.mp3`, `.wav`, `.m4a`) y exportar una transcripción en texto limpio (`.txt`) para cada uno de ellos.

Esta guía está totalmente optimizada y adaptada para **Mac con procesador Intel (Core i9) y macOS Sequoia**, resolviendo de forma definitiva los conflictos de compilación de librerías (`CMake/LLVM`), incompatibilidades de `PyTorch` y el secuestro de comandos globales (`Python 2.7` / `pip`).

---

## 📋 Guía Completa de Configuración Paso a Paso

### 🛠️ Paso 1: Requisitos Previos del Sistema
Antes de configurar el entorno de desarrollo, necesitamos preparar tu Mac con las herramientas base del sistema operativo. Abre tu **Terminal** y ejecuta estos comandos uno por uno:

```bash
# 1. Instalar Homebrew (el gestor de paquetes de macOS si aún no lo tienes)
/bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"

# 2. Instalar FFmpeg (el procesador de audio esencial para que Whisper pueda leer tus archivos)
brew install ffmpeg

# 3. Instalar Miniconda (gestor de entornos para IA que nos permite usar paquetes pre-compilados)
brew install --cask miniconda

# 4. Inicializar Conda en tu terminal
conda init zsh
```

> ⚠️ **SÚPER IMPORTANTE:** Después de ejecutar `conda init zsh`, debes **cerrar por completo tu aplicación de Terminal y volver a abrir una ventana nueva**. Al hacerlo, verás la palabra `(base)` al inicio de la línea de comandos, lo cual confirma que el **Paso 1** se completó con éxito.

---

### 📦 Paso 2: Creación del Entorno Virtual (Solución Definitiva)
Para evitar que tu sistema operativo sufra conflictos de seguridad con macOS Sequoia, crearemos una "burbuja" limpia y aislada con una versión de Python ultraestable para Inteligencia Artificial (Python 3.10).

Navega en la terminal hasta la carpeta donde vas a guardar tu proyecto y ejecuta estos comandos en orden estricto:

```bash
# 1. Crear el entorno virtual llamado 'transcriptor' con Python 3.10
conda create -n transcriptor python=3.10 -y

# 2. Activar tu nuevo entorno (notarás que el inicio de tu terminal cambia de '(base)' a '(transcriptor)')
conda activate transcriptor

# 3. Instalar las librerías matemáticas pesadas en su versión pre-construida (evita errores de CMake/LLVM)
conda install -c conda-forge numba llvmlite -y

# 4. Instalar PyTorch oficial para Mac Intel (evita errores de 'Symbol not found' y choques de C++)
conda install pytorch -c pytorch -y
```

---

### 🔑 Paso 3: Instalación de Whisper mediante la Llave Maestra
Debido a que algunas Mac retienen configuraciones antiguas que secuestran la palabra `pip` y te redirigen a un Python 2.7 obsoleto, utilizaremos la variable `$CONDA_PREFIX`. Esta ruta absoluta le da la dirección física exacta a tu terminal para que no se confunda.

Con tu entorno `(transcriptor)` activo, ejecuta:

```bash
# 1. Forzar una versión compatible de NumPy (para evitar advertencias con PyTorch)
$CONDA_PREFIX/bin/pip install "numpy<2"

# 2. Instalar OpenAI Whisper de forma completamente blindada
$CONDA_PREFIX/bin/pip install openai-whisper
```

---

### 📝 Paso 4: Creación del Código (`transcriptor_lotes.py`)
Crea un archivo de texto en tu carpeta de proyecto, cámbiale el nombre a `transcriptor_lotes.py` y pega el siguiente código automatizado:

```python
import whisper
import os
import glob

def transcribir_carpeta(ruta_carpeta, modelo_whisper="base"):
    """
    Lee todos los archivos de audio en una carpeta y exporta 
    la transcripción a archivos de texto individuales.
    """
    if not os.path.exists(ruta_carpeta):
        print(f"Error: No se encontró la carpeta '{ruta_carpeta}'")
        return

    print(f"Cargando el modelo '{modelo_whisper}'...")
    modelo = whisper.load_model(modelo_whisper)

    extensiones = ['*.mp3', '*.wav', '*.m4a']
    archivos_audio = []
    
    for ext in extensiones:
        archivos_audio.extend(glob.glob(os.path.join(ruta_carpeta, ext)))

    if not archivos_audio:
        print(f"No se encontraron archivos de audio en: {ruta_carpeta}")
        return

    print(f"Se encontraron {len(archivos_audio)} archivos. Iniciando proceso por lotes...\n")
    print("-" * 50)

    for ruta_audio in archivos_audio:
        nombre_base = os.path.splitext(ruta_audio)[0]
        ruta_texto = f"{nombre_base}.txt"

        if os.path.exists(ruta_texto):
            print(f"Saltando '{os.path.basename(ruta_audio)}' (Ya fue transcrito)")
            continue

        print(f"Procesando: {os.path.basename(ruta_audio)}...")
        try:
            resultado = modelo.transcribe(ruta_audio)
            
            with open(ruta_texto, "w", encoding="utf-8") as archivo:
                archivo.write(resultado["text"].strip())
                
            print(f"  ✓ Guardado exitosamente como: {os.path.basename(ruta_texto)}")
            
        except Exception as e:
            print(f"  x Error al procesar {os.path.basename(ruta_audio)}: {e}")

    print("-" * 50)
    print("¡Proceso por lotes finalizado con éxito!")

if __name__ == "__main__":
    # Define aquí la carpeta donde colocarás tus audios.
    # Puedes crear una carpeta llamada 'mis_audios' junto al script.
    carpeta_audios = "./mis_audios" 
    
    transcribir_carpeta(carpeta_audios)
```

---

### 🏃‍♂️ Paso 5: Ejecución del Utilitario
Para evitar que tu sistema operativo intercepte la ejecución y te devuelva un error de módulo no encontrado por culpa de Python antiguo, ejecutaremos el script utilizando de nuevo la llave maestra.

1. Crea una carpeta llamada `mis_audios` dentro de tu proyecto.
2. Coloca allí todos los audios que desees procesar.
3. Ejecuta tu utilitario con este comando exacto en la terminal:

```bash
$CONDA_PREFIX/bin/python transcriptor_lotes.py
```

---

## 🔁 Uso Diario (Resumen Rápido)

Cada vez que vuelvas a abrir la terminal en el futuro para usar tu transcriptor, solo debes seguir este flujo rápido de 3 pasos:

```bash
# 1. Navegar a tu carpeta de proyecto
cd ~/Tu/Ruta/De/Proyecto

# 2. Activar la burbuja de Conda
conda activate transcriptor

# 3. Lanzar la transcripción de tus audios
$CONDA_PREFIX/bin/python transcriptor_lotes.py
```

*Nota: Si el script se detiene a la mitad, no te preocupes. Al volverlo a ejecutar, omitirá de forma inteligente todos los audios que ya tengan su archivo `.txt` creado, procesando únicamente los nuevos.*