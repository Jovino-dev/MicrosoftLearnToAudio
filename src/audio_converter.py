"""
Module to convert text to audio
"""

import os
import io
import tempfile
from pathlib import Path
import pygame
from gtts import gTTS
import pyttsx3
from tqdm import tqdm
from utils import print_colored
from colorama import Fore
from text_processor import TextProcessor


class AudioConverter:
    def __init__(self, language='es', speed=1.0, voice_type='online', verbose=False):
        self.language = language
        self.speed = speed
        self.voice_type = voice_type
        self.verbose = verbose
        self.text_processor = TextProcessor()
        # Initialize pygame mixer for playback
        pygame.mixer.init()
        # Configure offline TTS engine if needed
        if voice_type == 'offline':
            self.tts_engine = pyttsx3.init()
            self._configure_offline_tts()

    def text_to_audio(self, text, output_path):
        """
        Converts text to audio file

        Args:
            text (str): Text to convert
            output_path (str): Output file path

        Returns:
            bool: True if conversion was successful
        """
        try:
            # Create output directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            if self.voice_type == 'online':
                return self._convert_with_gtts(text, output_path)
            else:
                return self._convert_with_pyttsx3(text, output_path)

        except Exception as e:
            if self.verbose:
                print_colored(f"❌ Error in conversion: {str(e)}", Fore.RED)
            return False

    def _convert_with_gtts(self, text, output_path):
        """Conversion using Google TTS (online)"""
        try:
            # Split text into chunks if too long
            chunks = self.text_processor.split_into_chunks(text)

            if len(chunks) == 1:
                # Short text, direct conversion
                if self.verbose:
                    print_colored("🌐 Converting with Google TTS...", Fore.BLUE)

                tts = gTTS(text=text, lang=self.language, slow=False)
                tts.save(output_path)

            else:
                # Long text, process by chunks and combine
                if self.verbose:
                    print_colored(f"📝 Processing {len(chunks)} segments...", Fore.BLUE)

                temp_files = []

                # Process each chunk
                for i, chunk in enumerate(tqdm(chunks, desc="Converting chunks")):
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                    temp_files.append(temp_file.name)

                    tts = gTTS(text=chunk, lang=self.language, slow=False)
                    tts.save(temp_file.name)
                    temp_file.close()

                # Combine audio files
                self._combine_audio_files(temp_files, output_path)

                # Clean up temp files
                for temp_file in temp_files:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

            return True

        except Exception as e:
            if self.verbose:
                print_colored(f"❌ Error with Google TTS: {str(e)}", Fore.RED)
            return False

    def _convert_with_pyttsx3(self, text, output_path):
        """Conversion using pyttsx3 (offline)"""
        try:
            if self.verbose:
                print_colored("🔊 Converting with local TTS...", Fore.BLUE)

            # Set speed
            self.tts_engine.setProperty('rate', int(200 * self.speed))

            # Save to file
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()

            return True

        except Exception as e:
            if self.verbose:
                print_colored(f"❌ Error with local TTS: {str(e)}", Fore.RED)
            return False

    def _configure_offline_tts(self):
        """Configures the offline TTS engine"""
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')

            # Search for Spanish voice
            spanish_voice = None
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                    spanish_voice = voice
                    break

            if spanish_voice:
                self.tts_engine.setProperty('voice', spanish_voice.id)
                if self.verbose:
                    print_colored(f"🗣️  Selected voice: {spanish_voice.name}", Fore.GREEN)
            elif self.verbose:
                print_colored("⚠️  No Spanish voice found, using default voice", Fore.YELLOW)

            # Set properties
            self.tts_engine.setProperty('rate', int(200 * self.speed))
            self.tts_engine.setProperty('volume', 0.9)

        except Exception as e:
            if self.verbose:
                print_colored(f"⚠️  Error configuring offline TTS: {str(e)}", Fore.YELLOW)

    def _combine_audio_files(self, audio_files, output_path):
        """Combines multiple audio files into one"""
        try:
            # For this simple implementation, concatenate using pygame
            # For a more robust implementation, use pydub

            combined_data = b''

            for audio_file in audio_files:
                with open(audio_file, 'rb') as f:
                    combined_data += f.read()

            with open(output_path, 'wb') as f:
                f.write(combined_data)

            if self.verbose:
                print_colored("🔗 Audio files combined", Fore.GREEN)

        except Exception as e:
            if self.verbose:
                print_colored(f"⚠️  Error combining files: {str(e)}", Fore.YELLOW)
            # As fallback, copy the first file
            if audio_files:
                import shutil
                shutil.copy2(audio_files[0], output_path)

    def play_audio(self, audio_path):
        """Plays an audio file"""
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            print_colored("▶️  Playing audio (press Ctrl+C to stop)...", Fore.CYAN)

            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

        except KeyboardInterrupt:
            pygame.mixer.music.stop()
            print_colored("\n⏹️  Playback stopped", Fore.YELLOW)
        except Exception as e:
            print_colored(f"❌ Error playing audio: {str(e)}", Fore.RED)

    def get_audio_info(self, audio_path):
        """Gets information about the audio file"""
        try:
            file_size = Path(audio_path).stat().st_size
            return {
                'size_mb': file_size / (1024 * 1024),
                'size_bytes': file_size,
                'exists': True
            }
        except:
            return {'exists': False}
