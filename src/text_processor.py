"""
Module to process and clean extracted text
"""

import re


class TextProcessor:
    def __init__(self):
        # Patterns to clean text
        self.cleanup_patterns = [
            # Remove multiple spaces
            (r'\s+', ' '),
            # Remove multiple newlines
            (r'\n\s*\n\s*\n+', '\n\n'),
            # Clean problematic special characters
            (r'[^\w\s\-.,;:!?¡¿áéíóúñüÁÉÍÓÚÑÜ()[\]"\'/]', ''),
            # Normalize punctuation
            (r'\.{2,}', '.'),
            (r'\?{2,}', '?'),
            (r'!{2,}', '!'),
        ]
        
        # Words/phrases to filter (navigation, UI, etc.)
        self.filter_phrases = [
            'skip to main content', 'breadcrumb navigation', 'table of contents',
            'in this article', 'next steps', 'feedback', 'was this page helpful',
            'submit and view feedback', 'microsoft learn', 'sign in', 'search',
            'browse', 'theme', 'light', 'dark', 'high contrast', 'previous unit',
            'next unit', 'completed', 'check your knowledge', 'knowledge check',
            # User-specific intro phrases
            'leer en ingles', 'agregar', 'agregar al plan', 'logros', 'preguntar a learn', 'completado',
            # User-specific outro phrases
            'comentarios', 'le ha resultado util esta pagina', 
            # Time pattern
            'minutos'
        ]

    def clean_and_structure(self, raw_text):
        """
        Cleans and structures the text for audio conversion
        
        Args:
            raw_text (str): Unprocessed text
            
        Returns:
            str: Clean and structured text
        """
        if not raw_text:
            return ""
        
        # Limpiar texto básico
        text = self._basic_cleanup(raw_text)
        
        # Filtrar contenido no deseado
        text = self._filter_unwanted_content(text)
        
        # Estructurar para audio
        text = self._structure_for_audio(text)
        
        # Normalizar espaciado
        text = self._normalize_spacing(text)
        
        return text.strip()

    def _basic_cleanup(self, text):
        """Basic text cleanup"""
        # Convertir a minúsculas para comparaciones
        text_lower = text.lower()
        
        # Aplicar patrones de limpieza
        for pattern, replacement in self.cleanup_patterns:
            text = re.sub(pattern, replacement, text)
        
        return text

    def _filter_unwanted_content(self, text):
        """Filters unwanted content such as navigation, UI, etc."""
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            line = line.strip()
            line_lower = line.lower()
            
            # Filtrar líneas muy cortas o vacías
            if len(line) < 3:
                continue
            
            # Filtrar frases específicas
            should_filter = False
            for phrase in self.filter_phrases:
                if phrase in line_lower:
                    should_filter = True
                    break
            
            # Filtrar líneas que parecen navegación o metadatos
            if (line_lower.startswith(('http', 'www.', 'mailto:')) or
                line_lower.endswith(('min', 'sec', 'hr')) or
                re.match(r'^\d+\s*(min|sec|hr|minute|second|hour)', line_lower) or
                re.match(r'^(step \d+|unit \d+|\d+\.)$', line_lower)):
                should_filter = True
            
            if not should_filter:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)

    def _structure_for_audio(self, text):
        """Structures the text to sound more natural when listening"""
        lines = text.split('\n')
        structured_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Agregar pausas después de títulos/encabezados
            if self._is_heading(line):
                structured_lines.append(f"{line}.")
                structured_lines.append("")  # Línea vacía para pausa
            else:
                # Asegurar que las oraciones terminen con puntuación
                if line and not line[-1] in '.!?':
                    line += '.'
                structured_lines.append(line)
        
        return '\n'.join(structured_lines)

    def _is_heading(self, line):
        """Determines if a line is a heading"""
        # Encabezados suelen ser más cortos y no terminar en puntuación
        return (len(line) < 100 and 
                not line.endswith(('.', '!', '?', ',', ';', ':')) and
                (line.isupper() or line.istitle() or 
                 any(word.isupper() for word in line.split())))

    def _normalize_spacing(self, text):
        """Normalizes text spacing"""
        # Eliminar espacios extra
        text = re.sub(r' +', ' ', text)
        
        # Normalizar saltos de línea
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Eliminar espacios al inicio y final de líneas
        lines = [line.strip() for line in text.split('\n')]
        
        return '\n'.join(lines)

    def split_into_chunks(self, text, max_chunk_size=4000):
        """
        Splits the text into chunks for TTS processing, preserving sentence boundaries and natural pauses.
        
        Args:
            text (str): Text to split
            max_chunk_size (int): Maximum size of each chunk
            
        Returns:
            list: List of text chunks
        """
        import re
        # Ensure all sentences end with proper punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        # Remove empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            # Add a space after each sentence for natural pause
            sentence_with_space = sentence if sentence.endswith(('.', '!', '?')) else sentence + '.'
            sentence_with_space += ' '
            if len(current_chunk) + len(sentence_with_space) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence_with_space
            else:
                current_chunk += sentence_with_space
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks
