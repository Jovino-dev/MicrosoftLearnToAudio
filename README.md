# Microsoft Learn to Audio Converter

This project allows you to download Microsoft Learn training courses and convert them to audio for easier auditory learning.

## Features

- 🌐 Extracts content from Microsoft Learn courses
- 📄 Processes and cleans the course text
- 🔊 Converts text to audio using TTS (Text-to-Speech)
- 💾 Saves audio files in MP3 format
- 📋 Easy-to-use command-line interface
- 📓 Includes a Google Colab notebook for interactive processing and audio conversion

## Installation

1. Clone this repository
2. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic usage
```bash
python main.py "https://learn.microsoft.com/es-es/training/modules/introduction-power-platform"
```

### Advanced options
```bash
python main.py "COURSE_URL" --output "my_course.mp3" --language "en" --speed 1.0 --voice offline
```

## Available parameters

- `--output`: Output file name (default: based on course title)
- `--language`: Language for TTS (default: es)
- `--speed`: Playback speed (default: 1.0)
- `--voice`: Voice type (`offline` for local pyttsx3, `online` for gTTS)

## Examples

```bash
# Basic example
python main.py "https://learn.microsoft.com/es-es/training/modules/introduction-power-platform"

# With custom options
python main.py "https://learn.microsoft.com/es-es/training/modules/introduction-power-platform" --output "power_platform_intro.mp3" --speed 0.9
```

## Project structure

```
├── main.py              # Main entry point
├── src/
│   ├── scraper.py       # Web content extractor
│   ├── text_processor.py # Text processor
│   ├── audio_converter.py # Text-to-audio converter
│   └── utils.py         # Common utilities
├── output/              # Generated audio files
├── requirements.txt     # Project dependencies
├── TextProcessor_colab.ipynb # Google Colab notebook
└── README.md           # This file
```

## Using the Google Colab Notebook

The file `TextProcessor_colab.ipynb` allows you to process and convert Microsoft Learn modules to audio interactively in Google Colab, with no local installation required.

### What can you do with the notebook?
- Enter the URL of a Microsoft Learn module.
- Download and process all module units.
- Generate MP3 audio files for each unit.
- Download all audios in a ready-to-use ZIP file.

#### How to use it
1. Open [a the notebook](TextProcessor_colab.ipynb)
2. Click "Open in collab".
4. Enter the URL and parameters
5. Execute the notebook


## Notes

- Audio files are saved in the `output/` folder (or a subfolder per module).
- Microsoft Learn terms of use are respected.
- The project is optimized for Spanish content by default, but you can use other languages.

## License

MIT License
