#!/usr/bin/env python3
"""
Script de instalación para Microsoft Learn to Audio Converter
"""

import subprocess
import sys
import os
from pathlib import Path


def print_step(message, step_num=None):
    """Imprime un paso de instalación"""
    if step_num:
        print(f"\n{'='*50}")
        print(f"PASO {step_num}: {message}")
        print('='*50)
    else:
        print(f"🔧 {message}")


def check_python_version():
    """Verifica la versión de Python"""
    print_step("Verificando versión de Python", 1)
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 o superior es requerido")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True


def install_requirements():
    """Instala las dependencias del requirements.txt"""
    print_step("Instalando dependencias", 2)
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ Archivo requirements.txt no encontrado")
        return False
    
    try:
        print("📦 Instalando paquetes de Python...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False


def create_directories():
    """Crea los directorios necesarios"""
    print_step("Creando directorios", 3)
    
    directories = ["output", "temp", "logs"]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"📁 Directorio creado: {directory}/")
    
    print("✅ Directorios creados correctamente")
    return True


def test_installation():
    """Prueba la instalación"""
    print_step("Probando instalación", 4)
    
    try:
        # Importar módulos principales
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        print("🧪 Probando importaciones...")
        
        from scraper import MicrosoftLearnScraper
        print("   ✅ scraper.py")
        
        from text_processor import TextProcessor
        print("   ✅ text_processor.py")
        
        from audio_converter import AudioConverter
        print("   ✅ audio_converter.py")
        
        from utils import validate_url
        print("   ✅ utils.py")
        
        # Probar funciones básicas
        print("\n🔍 Probando funciones básicas...")
        
        # Test URL validation
        test_url = "https://learn.microsoft.com/es-es/training/modules/introduction-power-platform"
        if validate_url(test_url):
            print("   ✅ Validación de URL")
        else:
            print("   ❌ Validación de URL")
            return False
        
        print("✅ Instalación verificada correctamente")
        return True
        
    except ImportError as e:
        print(f"❌ Error importando módulo: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")
        return False


def show_usage_examples():
    """Muestra ejemplos de uso"""
    print_step("Ejemplos de uso")
    
    examples = [
        {
            "descripcion": "Uso básico",
            "comando": 'python main.py "https://learn.microsoft.com/es-es/training/modules/introduction-power-platform"'
        },
        {
            "descripcion": "Con nombre personalizado",
            "comando": 'python main.py "URL_DEL_CURSO" --output "mi_curso" --verbose'
        },
        {
            "descripcion": "Velocidad personalizada",
            "comando": 'python main.py "URL_DEL_CURSO" --speed 0.8 --language es'
        },
        {
            "descripcion": "Ejecutar ejemplos",
            "comando": 'python examples.py'
        }
    ]
    
    print("📚 Ejemplos de uso:")
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['descripcion']}:")
        print(f"   {example['comando']}")


def main():
    """Función principal de instalación"""
    print("🎵 Microsoft Learn to Audio Converter - Instalación")
    print("=" * 60)
    
    success = True
    
    # Verificar Python
    if not check_python_version():
        success = False
    
    # Instalar dependencias
    if success and not install_requirements():
        success = False
    
    # Crear directorios
    if success and not create_directories():
        success = False
    
    # Probar instalación
    if success and not test_installation():
        success = False
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("\n✅ El proyecto está listo para usar")
        show_usage_examples()
        
        print(f"\n💡 Consejos:")
        print("   - Usa --verbose para ver información detallada")
        print("   - Los archivos se guardan en el directorio 'output/'")
        print("   - Ejecuta 'python examples.py' para ver demostraciones")
        
    else:
        print("❌ INSTALACIÓN FALLÓ")
        print("\n🔧 Posibles soluciones:")
        print("   1. Verificar que Python 3.7+ esté instalado")
        print("   2. Ejecutar: pip install --upgrade pip")
        print("   3. Instalar manualmente: pip install -r requirements.txt")
        print("   4. Verificar permisos de escritura en el directorio")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
