#!/usr/bin/env python3
"""
OFF KING - Educational Web Security Tool
For educational purposes only - Use responsibly
"""

import os
import sys
import time
import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import random
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class OffKing:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def display_banner(self):
        """Display the colorful OFF KING banner"""
        banner = f"""
{Colors.RED}{Colors.BOLD}
   ██████╗ ███████╗███████╗    ██╗  ██╗██╗███╗   ██╗ ██████╗ 
  ██╔═══██╗██╔════╝██╔════╝    ██║ ██╔╝██║████╗  ██║██╔════╝ 
  ██║   ██║█████╗  █████╗      █████╔╝ ██║██╔██╗ ██║██║  ███╗
  ██║   ██║██╔══╝  ██╔══╝      ██╔═██╗ ██║██║╚██╗██║██║   ██║
  ╚██████╔╝██║     ██║         ██║  ██╗██║██║ ╚████║╚██████╔╝
   ╚═════╝ ╚═╝     ╚═╝         ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
{Colors.END}
{Colors.CYAN}{Colors.BOLD}         Educational Web Security Toolkit{Colors.END}
{Colors.YELLOW}       For legal and educational purposes only!{Colors.END}
{Colors.GREEN}          Created for cybersecurity education{Colors.END}
{Colors.RED}⚠️  Use responsibly and only on websites you own!{Colors.END}
"""
        print(banner)
    
    def create_directory(self, url):
        """Create directory for cloned website"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('www.', '')
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        dir_name = f"cloned_{domain}_{timestamp}"
        
        os.makedirs(dir_name, exist_ok=True)
        return dir_name
    
    def download_resource(self, url, base_url, save_dir):
        """Download individual resource"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                parsed_url = urlparse(url)
                path = parsed_url.path
                
                if not path or path == '/':
                    path = '/index.html'
                
                file_path = os.path.join(save_dir, path.lstrip('/'))
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                return True
        except Exception as e:
            return False
        return False
    
    def clone_website(self, url, depth=1):
        """Clone website with specified depth"""
        print(f"{Colors.GREEN}[+] Cloning website: {url}{Colors.END}")
        print(f"{Colors.YELLOW}[!] This may take a while...{Colors.END}")
        
        save_dir = self.create_directory(url)
        downloaded_urls = set()
        
        def crawl(current_url, current_depth):
            if current_depth > depth or current_url in downloaded_urls:
                return
            
            downloaded_urls.add(current_url)
            print(f"{Colors.CYAN}[*] Downloading: {current_url}{Colors.END}")
            
            try:
                response = self.session.get(current_url, timeout=10)
                if response.status_code == 200:
                    parsed_url = urlparse(current_url)
                    path = parsed_url.path
                    
                    if not path or path == '/':
                        path = '/index.html'
                    
                    file_path = os.path.join(save_dir, path.lstrip('/'))
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    if current_depth < depth:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        for link in soup.find_all(['a', 'link', 'script', 'img'], href=True):
                            href = link.get('href')
                            if href:
                                absolute_url = urljoin(current_url, href)
                                if urlparse(absolute_url).netloc == urlparse(url).netloc:
                                    crawl(absolute_url, current_depth + 1)
                        
                        for link in soup.find_all(['img', 'script'], src=True):
                            src = link.get('src')
                            if src:
                                absolute_url = urljoin(current_url, src)
                                if urlparse(absolute_url).netloc == urlparse(url).netloc:
                                    self.download_resource(absolute_url, url, save_dir)
            
            except Exception as e:
                print(f"{Colors.RED}[!] Error downloading {current_url}: {e}{Colors.END}")
        
        crawl(url, 1)
        print(f"{Colors.GREEN}[+] Website cloned to: {save_dir}{Colors.END}")
        return save_dir

def main():
    """Main function"""
    tool = OffKing()
    tool.display_banner()
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        tool.clone_website(url)
    else:
        print(f"{Colors.RED}Usage: python offking.py <url>{Colors.END}")

if __name__ == "__main__":
    main()
