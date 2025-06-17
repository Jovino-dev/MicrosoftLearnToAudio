"""
Module to extract content from Microsoft Learn
"""

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import re
from utils import print_colored
from colorama import Fore


class MicrosoftLearnScraper:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def extract_course_content(self, url):
        """
        Extracts the content of a Microsoft Learn course
        
        Args:
            url (str): URL of the Microsoft Learn course
            
        Returns:
            dict: Dictionary with title and content of the course
        """
        try:
            if self.verbose:
                print_colored(f"🌐 Connecting to: {url}", Fore.BLUE)
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract main content
            content = self._extract_main_content(soup)
            
            # Check if it's a module with multiple units
            units = self._extract_units_links(soup, url)
            
            if units and self.verbose:
                print_colored(f"📚 Found {len(units)} additional units", Fore.BLUE)
            
            # Add content from the units
            for unit_url in units:
                if self.verbose:
                    print_colored(f"📖 Processing unit: {unit_url}", Fore.BLUE)
                
                unit_content = self._extract_unit_content(unit_url)
                if unit_content:
                    content += "\n\n" + unit_content
                
                # Short pause to be respectful to the server
                time.sleep(1)
            
            if not content.strip():
                raise ValueError("No content could be extracted from the course")
            
            return {
                'title': title,
                'content': content,
                'url': url
            }
            
        except requests.RequestException as e:
            if self.verbose:
                print_colored(f"❌ Connection error: {str(e)}", Fore.RED)
            return None
        except Exception as e:
            if self.verbose:
                print_colored(f"❌ Error extracting content: {str(e)}", Fore.RED)
            return None

    def get_units_links(self, url):
        """Returns a list of unit links from the module (class='unit-title')"""
        try:
            if self.verbose:
                print_colored(f"🌐 Searching for units in: {url}", Fore.BLUE)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            units = []
            for a in soup.find_all('a', class_='unit-title', href=True):
                full_url = urljoin(url, a['href'])
                if full_url not in units:
                    units.append(full_url)
            if self.verbose:
                print_colored(f"🔗 {len(units)} units found", Fore.GREEN)
            return units
        except Exception as e:
            if self.verbose:
                print_colored(f"❌ Error searching for units: {str(e)}", Fore.RED)
            return []

    def _extract_title(self, soup):
        """Extracts the course title"""
        # Try several selectors for the title
        title_selectors = [
            'h1[data-bi-name="page-title"]',
            'h1.title',
            'h1',
            '.page-title h1',
            '[data-bi-name="page-title"]'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text().strip()
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        return "Microsoft Learn Course"

    def _extract_main_content(self, soup):
        """Extracts the main content of the page"""
        content_parts = []
        
        # Selectors for the main content
        content_selectors = [
            '.content',
            'main',
            '[role="main"]',
            '.main-content',
            'article',
            '.module-content'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup
        
        # Extract paragraphs, headers, and lists
        for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div']):
            text = element.get_text().strip()
            if text and len(text) > 10:  # Filter very short texts
                # Clean text
                text = re.sub(r'\s+', ' ', text)
                text = re.sub(r'\n+', '\n', text)
                
                # Add spacing for headers
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    content_parts.append(f"\n\n{text}\n")
                else:
                    content_parts.append(text)
        
        return ' '.join(content_parts)

    def _extract_units_links(self, soup, base_url):
        """Extracts links to module units"""
        units = []
        
        # Search for links to units
        unit_links = soup.find_all('a', href=True)
        base_path = urlparse(base_url).path
        
        for link in unit_links:
            href = link.get('href')
            if href and ('unit-' in href or '/units/' in href):
                # Build full URL
                full_url = urljoin(base_url, href)
                
                # Avoid duplicates and self-reference
                if full_url != base_url and full_url not in units:
                    units.append(full_url)
        
        return units[:10]  # Limit to 10 units to avoid overload

    def _extract_unit_content(self, unit_url):
        """Extracts content from a specific unit"""
        try:
            response = self.session.get(unit_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._extract_main_content(soup)
            
        except Exception as e:
            if self.verbose:
                print_colored(f"⚠️  Error extracting unit {unit_url}: {str(e)}", Fore.YELLOW)
            return ""
