"""
Utilidades comunes para el proyecto
"""

import re
import validators
from urllib.parse import urlparse
from colorama import Fore, Style


def validate_url(url):
    """
    Valida si una URL es válida y pertenece a Microsoft Learn
    
    Args:
        url (str): URL a validar
        
    Returns:
        bool: True si la URL es válida
    """
    if not url or not isinstance(url, str):
        return False
    
    # Validar formato de URL
    if not validators.url(url):
        return False
    
    # Verificar que sea de Microsoft Learn
    parsed = urlparse(url)
    allowed_domains = [
        'learn.microsoft.com',
        'docs.microsoft.com'
    ]
    
    return any(domain in parsed.netloc for domain in allowed_domains)


def create_safe_filename(title):
    """
    Crea un nombre de archivo seguro a partir de un título
    
    Args:
        title (str): Título original
        
    Returns:
        str: Nombre de archivo seguro
    """
    if not title:
        return "microsoft_learn_course"
    
    # Limpiar caracteres especiales
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '_', filename)
    filename = filename.strip('_').lower()
    
    # Limitar longitud
    if len(filename) > 50:
        filename = filename[:50]
    
    # Asegurar que no esté vacío
    if not filename:
        filename = "microsoft_learn_course"
    
    return filename


def print_colored(message, color=Fore.WHITE):
    """
    Imprime un mensaje con color
    
    Args:
        message (str): Mensaje a imprimir
        color: Color de colorama
    """
    print(f"{color}{message}{Style.RESET_ALL}")


def format_duration(seconds):
    """
    Formatea duración en segundos a formato legible
    
    Args:
        seconds (int): Duración en segundos
        
    Returns:
        str: Duración formateada
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def estimate_audio_duration(text, words_per_minute=150):
    """
    Estima la duración del audio basada en el texto
    
    Args:
        text (str): Texto a procesar
        words_per_minute (int): Velocidad de lectura promedio
        
    Returns:
        int: Duración estimada en segundos
    """
    if not text:
        return 0
    
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    return int(minutes * 60)


def truncate_text(text, max_length=100):
    """
    Trunca texto a una longitud máxima
    
    Args:
        text (str): Texto a truncar
        max_length (int): Longitud máxima
        
    Returns:
        str: Texto truncado
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def get_file_size_mb(file_path):
    """
    Obtiene el tamaño de un archivo en MB
    
    Args:
        file_path (str): Ruta del archivo
        
    Returns:
        float: Tamaño en MB
    """
    try:
        import os
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0


def clean_text_for_display(text, max_length=200):
    """
    Limpia texto para mostrar en consola
    
    Args:
        text (str): Texto a limpiar
        max_length (int): Longitud máxima
        
    Returns:
        str: Texto limpio para mostrar
    """
    if not text:
        return ""
    
    # Eliminar saltos de línea múltiples
    text = re.sub(r'\n+', ' ', text)
    
    # Eliminar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    # Truncar si es necesario
    text = truncate_text(text.strip(), max_length)
    
    return text
