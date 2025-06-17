#!/usr/bin/env python3
"""
Microsoft Learn to Audio Converter
Convert Microsoft Learn courses to MP3 audio files
"""

import argparse
import sys
import os
from pathlib import Path
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
import requests

# Initialize colorama for terminal colors
init()

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper import MicrosoftLearnScraper
from text_processor import TextProcessor
from audio_converter import AudioConverter
from utils import validate_url, create_safe_filename, print_colored


def main():
    parser = argparse.ArgumentParser(
        description="Convert Microsoft Learn courses to audio",
        epilog="Example: python main.py 'https://learn.microsoft.com/es-es/training/modules/introduction-power-platform'"
    )
    
    parser.add_argument(
        'url',
        help='Microsoft Learn course URL'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file name (without extension)',
        default=None
    )
    
    parser.add_argument(
        '--language', '-l',
        help='Language for text-to-speech (es, en, etc.)',
        default='es'
    )
    
    parser.add_argument(
        '--speed', '-s',
        type=float,
        help='Playback speed (0.5 - 2.0)',
        default=1.0
    )
    
    parser.add_argument(
        '--voice',
        choices=['online', 'offline'],
        help='Voice type to use',
        default='offline'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed information'
    )

    args = parser.parse_args()

    try:
        # Validate URL
        if not validate_url(args.url):
            print_colored("❌ Invalid URL", Fore.RED)
            return 1

        print_colored("🚀 Starting Microsoft Learn to Audio Converter", Fore.CYAN)
        print_colored(f"📄 URL: {args.url}", Fore.BLUE)

        # 1. Get unit links
        print_colored("\n🔗 Searching for unit links...", Fore.YELLOW)
        scraper = MicrosoftLearnScraper(verbose=args.verbose)
        unit_links = scraper.get_units_links(args.url)
        if not unit_links:
            print_colored("❌ No units found in the module", Fore.RED)
            return 1
        print_colored(f"✅ {len(unit_links)} units found", Fore.GREEN)

        processor = TextProcessor()
        converter = AudioConverter(
            language=args.language,
            speed=args.speed,
            voice_type=args.voice,
            verbose=args.verbose
        )

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # Get the module name for the output folder
        try:
            # Use the main page title as folder name
            response = scraper.session.get(args.url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            module_title = scraper._extract_title(soup)
        except Exception:
            module_title = "module"
        safe_module_title = create_safe_filename(module_title)
        module_output_dir = output_dir / safe_module_title
        module_output_dir.mkdir(exist_ok=True)

        for idx, unit_url in enumerate(unit_links, 1):
            print_colored(f"\n📥 Processing unit {idx}: {unit_url}", Fore.YELLOW)
            unit_content = scraper._extract_unit_content(unit_url)
            if not unit_content.strip():
                print_colored(f"⚠️  Empty or not extracted unit: {unit_url}", Fore.YELLOW)
                continue
            processed_text = processor.clean_and_structure(unit_content)
            # Get unit title for file name
            try:
                unit_title = scraper._extract_title(BeautifulSoup(requests.get(unit_url).content, 'html.parser'))
            except:
                unit_title = f"unit_{idx}"
            safe_title = create_safe_filename(unit_title)
            output_path = module_output_dir / f"unit_{idx}-{safe_title}.mp3"
            print_colored(f"🔊 Converting to audio: {output_path.name}", Fore.YELLOW)
            success = converter.text_to_audio(processed_text, str(output_path))
            if success:
                print_colored(f"🎉 Unit converted: {output_path.absolute()}", Fore.GREEN)
            else:
                print_colored(f"❌ Error converting unit: {unit_url}", Fore.RED)
        print_colored("\n✅ Process finished.", Fore.CYAN)
        return 0

    except KeyboardInterrupt:
        print_colored("\n⚠️  Process interrupted by user", Fore.YELLOW)
        return 1
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {str(e)}", Fore.RED)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
