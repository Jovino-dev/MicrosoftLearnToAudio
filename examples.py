#!/usr/bin/env python3
"""
Script de ejemplo para Microsoft Learn to Audio Converter
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.scraper import MicrosoftLearnScraper
from src.text_processor import TextProcessor
from src.audio_converter import AudioConverter
from src.utils import print_colored, estimate_audio_duration, clean_text_for_display
from colorama import Fore, init

# Inicializar colorama
init()


def example_basic_usage():
    """Ejemplo básico de uso del convertidor"""
    print_colored("🚀 Ejemplo: Uso básico del convertidor", Fore.CYAN)
    print_colored("=" * 50, Fore.CYAN)
    
    # URL de ejemplo
    url = "https://learn.microsoft.com/es-es/training/modules/introduction-power-platform"
    
    print_colored(f"📄 URL: {url}", Fore.BLUE)
    
    # 1. Extraer contenido
    print_colored("\n1️⃣  Extrayendo contenido...", Fore.YELLOW)
    scraper = MicrosoftLearnScraper(verbose=True)
    course_data = scraper.extract_course_content(url)
    
    if course_data:
        print_colored(f"✅ Título: {course_data['title']}", Fore.GREEN)
        print_colored(f"📝 Contenido: {len(course_data['content'])} caracteres", Fore.GREEN)
        
        # Mostrar preview del contenido
        preview = clean_text_for_display(course_data['content'], 200)
        print_colored(f"👀 Preview: {preview}", Fore.BLUE)
        
        # 2. Procesar texto
        print_colored("\n2️⃣  Procesando texto...", Fore.YELLOW)
        processor = TextProcessor()
        processed_text = processor.clean_and_structure(course_data['content'])
        
        print_colored(f"🔄 Texto procesado: {len(processed_text)} caracteres", Fore.GREEN)
        
        # Estimar duración
        estimated_duration = estimate_audio_duration(processed_text)
        print_colored(f"⏱️  Duración estimada: {estimated_duration // 60}m {estimated_duration % 60}s", Fore.BLUE)
        
        # 3. Convertir a audio (simulado)
        print_colored("\n3️⃣  Configurando conversión a audio...", Fore.YELLOW)
        converter = AudioConverter(language='es', voice_type='online', verbose=True)
        
        output_path = "output/ejemplo_power_platform.mp3"
        print_colored(f"💾 Archivo de salida: {output_path}", Fore.CYAN)
        
        print_colored("✅ Configuración completada", Fore.GREEN)
        print_colored("\n💡 Para ejecutar la conversión real, usa: python main.py \"URL\"", Fore.YELLOW)
        
    else:
        print_colored("❌ No se pudo extraer el contenido", Fore.RED)


def example_advanced_usage():
    """Ejemplo de uso avanzado con opciones personalizadas"""
    print_colored("\n\n🔧 Ejemplo: Uso avanzado", Fore.CYAN)
    print_colored("=" * 50, Fore.CYAN)
    
    # Configuración personalizada
    config = {
        'language': 'es',
        'speed': 0.9,
        'voice_type': 'online',
        'output_name': 'curso_personalizado'
    }
    
    print_colored("⚙️  Configuración personalizada:", Fore.BLUE)
    for key, value in config.items():
        print_colored(f"   {key}: {value}", Fore.WHITE)
    
    print_colored("\n💡 Comando equivalente:", Fore.YELLOW)
    cmd = f"python main.py \"URL\" --output \"{config['output_name']}\" --language {config['language']} --speed {config['speed']} --voice {config['voice_type']} --verbose"
    print_colored(f"   {cmd}", Fore.WHITE)


def example_text_processing():
    """Ejemplo de procesamiento de texto"""
    print_colored("\n\n📝 Ejemplo: Procesamiento de texto", Fore.CYAN)
    print_colored("=" * 50, Fore.CYAN)
    
    # Texto de ejemplo con problemas comunes
    sample_text = """
    Skip to main content    Introduction to Power Platform
    
    
    Microsoft Power Platform is a suite of business applications that helps organizations  
    analyze data, build solutions, automate processes, and create virtual agents.
    
    
    Table of contents:
    1. What is Power Platform
    2. Components overview
    
    Next unit: Power Apps overview
    
    Was this page helpful? Yes No
    """
    
    print_colored("📄 Texto original:", Fore.BLUE)
    print_colored(sample_text, Fore.WHITE)
    
    processor = TextProcessor()
    processed_text = processor.clean_and_structure(sample_text)
    
    print_colored("\n✨ Texto procesado:", Fore.GREEN)
    print_colored(processed_text, Fore.WHITE)
    
    # Mostrar chunks
    chunks = processor.split_into_chunks(processed_text, max_chunk_size=100)
    print_colored(f"\n📊 Dividido en {len(chunks)} chunks:", Fore.BLUE)
    for i, chunk in enumerate(chunks, 1):
        print_colored(f"   Chunk {i}: {clean_text_for_display(chunk, 80)}", Fore.WHITE)


def main():
    """Función principal de ejemplos"""
    print_colored("🎵 Microsoft Learn to Audio Converter - Ejemplos", Fore.MAGENTA)
    print_colored("=" * 60, Fore.MAGENTA)
    
    try:
        # Ejecutar ejemplos
        example_basic_usage()
        example_advanced_usage()
        example_text_processing()
        
        print_colored("\n\n🎉 ¡Ejemplos completados!", Fore.GREEN)
        print_colored("👉 Para usar el convertidor: python main.py \"URL_DEL_CURSO\"", Fore.CYAN)
        
    except KeyboardInterrupt:
        print_colored("\n⚠️  Ejemplos interrumpidos", Fore.YELLOW)
    except Exception as e:
        print_colored(f"\n❌ Error en ejemplos: {str(e)}", Fore.RED)


if __name__ == "__main__":
    main()
