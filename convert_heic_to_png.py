"""
Script para convertir imágenes HEIC a PNG
Procesa todas las carpetas dentro de 'carpetas' y crea una subcarpeta 'png' en cada una
Requiere: pip install pillow-heif pillow
"""

import os
from pathlib import Path
from PIL import Image
import pillow_heif

def convertir_heic_a_png(carpeta_origen):
    """
    Convierte todas las imágenes HEIC de una carpeta a PNG
    Crea una carpeta 'png' para guardar los archivos convertidos
    
    Args:
        carpeta_origen (str): Ruta de la carpeta con imágenes HEIC
    
    Returns:
        tuple: (convertidos, errores)
    """
    
    carpeta_origen = Path(carpeta_origen)
    carpeta_png = carpeta_origen / "png"
    
    # Crear carpeta png si no existe
    carpeta_png.mkdir(parents=True, exist_ok=True)
    
    # Obtener todos los archivos HEIC
    archivos_heic = list(carpeta_origen.glob("*.HEIC")) + list(carpeta_origen.glob("*.heic"))
    
    if not archivos_heic:
        return 0, 0
    
    convertidos = 0
    errores = 0
    
    for archivo_heic in archivos_heic:
        try:
            # Leer la imagen HEIC
            heif_file = pillow_heif.open_heif(str(archivo_heic))
            imagen = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data
            )
            
            # Crear nombre del archivo PNG
            nombre_png = archivo_heic.stem + ".png"
            ruta_png = carpeta_png / nombre_png
            
            # Guardar como PNG
            imagen.save(str(ruta_png), "PNG", quality=95)
            
            print(f"  ✓ {archivo_heic.name} → {nombre_png}")
            convertidos += 1
            
        except Exception as e:
            print(f"  ✗ Error al convertir {archivo_heic.name}: {str(e)}")
            errores += 1
    
    return convertidos, errores

def procesar_todas_carpetas():
    """
    Procesa todas las carpetas dentro de 'carpetas'
    """
    
    carpeta_principal = Path(r"c:\Users\User\Documents\Convert-HEICH-To-PNG\carpetas")
    
    if not carpeta_principal.exists():
        print(f"Error: No se encontró la carpeta {carpeta_principal}")
        return
    
    # Obtener todas las subcarpetas
    subcarpetas = [d for d in carpeta_principal.iterdir() if d.is_dir()]
    
    if not subcarpetas:
        print("No se encontraron carpetas dentro de 'carpetas'")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Procesando {len(subcarpetas)} carpeta(s)")
    print(f"{'=' * 60}\n")
    
    total_convertidos = 0
    total_errores = 0
    carpetas_procesadas = 0
    
    for subcarpeta in sorted(subcarpetas):
        # Verificar si ya tiene carpeta 'png'
        carpeta_png_existe = (subcarpeta / "png").exists()
        
        print(f"📁 {subcarpeta.name}", end="")
        if carpeta_png_existe:
            print(" [YA CONVERTIDA]")
            continue
        
        print()
        
        # Obtener archivos HEIC
        archivos_heic = list(subcarpeta.glob("*.HEIC")) + list(subcarpeta.glob("*.heic"))
        
        if not archivos_heic:
            print(f"  ⚠ No se encontraron archivos HEIC")
            continue
        
        print(f"  Se encontraron {len(archivos_heic)} archivos HEIC")
        
        convertidos, errores = convertir_heic_a_png(subcarpeta)
        
        total_convertidos += convertidos
        total_errores += errores
        carpetas_procesadas += 1
        
        print(f"  Resultado: {convertidos} convertidos, {errores} errores\n")
    
    print(f"{'=' * 60}")
    print(f"RESUMEN FINAL:")
    print(f"  Carpetas procesadas: {carpetas_procesadas}")
    print(f"  Total convertidos: {total_convertidos}")
    print(f"  Total errores: {total_errores}")
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    procesar_todas_carpetas()
