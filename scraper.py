import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class DocumentationScraper:
    def __init__(self, base_url, output_dir="scraped_content"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()
        
        # Create output directories
        self.text_dir = os.path.join(output_dir, "text")
        self.images_dir = os.path.join(output_dir, "images")
        os.makedirs(self.text_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        print(f"Initializing scraper with base URL: {base_url}")

    def download_image(self, img_url, page_title):
        try:
            # Create a valid filename from the page title
            safe_title = "".join(c for c in page_title if c.isalnum() or c in (' ', '-', '_')).strip()
            
            # Get image filename from URL
            img_filename = os.path.basename(urlparse(img_url).path)
            if not img_filename:
                img_filename = f"image_{int(time.time())}.jpg"
            
            # Combine page title with image filename
            final_filename = f"{safe_title}_{img_filename}"
            img_path = os.path.join(self.images_dir, final_filename)
            
            print(f"Downloading image: {img_url}")
            # Download image
            response = requests.get(img_url, stream=True)
            response.raise_for_status()
            
            with open(img_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Successfully downloaded image to: {img_path}")
            return img_path
        except Exception as e:
            print(f"Error downloading image {img_url}: {str(e)}")
            return None

    def is_valid_ebus_url(self, url):
        """Vérifie si l'URL est une route ebus valide"""
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        # Vérifie si le chemin contient 'e-bus' ou 'ebus'
        return 'e-bus' in path or 'ebus' in path

    def scrape_page(self, url):
        if url in self.visited_urls:
            print(f"Already visited: {url}")
            return
        
        # Vérifier si l'URL est une route ebus valide
        if not self.is_valid_ebus_url(url):
            print(f"Skipping non-ebus URL: {url}")
            return
        
        self.visited_urls.add(url)
        print(f"\nScraping: {url}")
        
        try:
            print(f"Making request to: {url}")
            response = requests.get(url)
            response.raise_for_status()
            print(f"Response status: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Get page title
            title = soup.title.string if soup.title else "untitled"
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            print(f"Page title: {title}")
            
            # Extract and save text content
            text_content = []
            for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = p.get_text().strip()
                if text:  # Only add non-empty text
                    text_content.append(text)
            
            if text_content:
                # Save text content
                text_file = os.path.join(self.text_dir, f"{safe_title}.txt")
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write('\n\n'.join(text_content))
                print(f"Saved text content to: {text_file}")
            else:
                print("No text content found on page")
            
            # Download images
            images = soup.find_all('img')
            print(f"Found {len(images)} images on page")
            for img in images:
                img_url = img.get('src')
                if img_url:
                    img_url = urljoin(url, img_url)
                    self.download_image(img_url, safe_title)
            
            # Find and follow links to other documentation pages
            links = soup.find_all('a')
            print(f"Found {len(links)} links on page")
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    # Only follow links from the same domain and containing 'ebus'
                    if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                        print(f"Found valid link: {full_url}")
                        self.scrape_page(full_url)
                        
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")

    def start_scraping(self):
        print("\nStarting scraping process...")
        self.scrape_page(self.base_url)
        print("\nScraping completed!")
        print(f"Total pages scraped: {len(self.visited_urls)}")

if __name__ == "__main__":
    # Example usage
    base_url = "https://documentation.factory.orange-business.com/e-bus/"  # Replace with your documentation URL
    scraper = DocumentationScraper(base_url)
    scraper.start_scraping() 