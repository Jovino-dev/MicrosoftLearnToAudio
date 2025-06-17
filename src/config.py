"""
Configuración del proyecto Microsoft Learn to Audio
"""

# Configuración de scraping
SCRAPING_CONFIG = {
    'request_timeout': 30,
    'delay_between_requests': 1,
    'max_units_per_module': 10,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Configuración de procesamiento de texto
TEXT_PROCESSING_CONFIG = {
    'max_chunk_size': 4000,
    'min_sentence_length': 10,
    'filter_navigation': True,
    'normalize_punctuation': True
}

# Configuración de audio
AUDIO_CONFIG = {
    'default_language': 'es',
    'default_speed': 1.0,
    'default_voice_type': 'online',
    'output_format': 'mp3',
    'audio_quality': 'high'
}

# Configuración de archivos
FILE_CONFIG = {
    'output_directory': 'output',
    'temp_directory': 'temp',
    'max_filename_length': 50,
    'file_encoding': 'utf-8'
}

# Idiomas soportados para TTS
SUPPORTED_LANGUAGES = {
    'es': 'Español',
    'en': 'English',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português'
}

# URLs y patrones de Microsoft Learn
MICROSOFT_LEARN_CONFIG = {
    'base_domains': [
        'learn.microsoft.com',
        'docs.microsoft.com'
    ],
    'content_selectors': [
        '.content',
        'main',
        '[role="main"]',
        '.main-content',
        'article',
        '.module-content'
    ],
    'title_selectors': [
        'h1[data-bi-name="page-title"]',
        'h1.title',
        'h1',
        '.page-title h1',
        '[data-bi-name="page-title"]'
    ]
}
