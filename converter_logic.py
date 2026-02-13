# converter_logic.py - Version 2.3.4
import subprocess
import os
import requests
import re

class eBookConverterLogic:
    def __init__(self):
        self.version = "2.3.4"

    def sanitize_filename(self, filename):
        # Removes illegal characters and replaces ; with ,
        clean = filename.replace(";", ",")
        clean = re.sub(r'[<>:"/\\|?*]', '', clean)
        return " ".join(clean.split()).strip()

    def parse_filename(self, filepath):
        """Extracts core keywords from complex filenames for better searching."""
        filename = os.path.splitext(os.path.basename(filepath))[0]
        # Remove known noise like "BattleTech" or product codes like "08610"
        noise = [r'BattleTech', r'\d{5}'] 
        clean_name = filename
        for pattern in noise:
            clean_name = re.sub(pattern, '', clean_name, flags=re.I)
        
        # Standard split
        if " - " in clean_name:
            parts = clean_name.split(" - ")
            author = parts[-1].strip()
            title = " ".join(parts[:-1]).strip()
            return title.strip(" -"), author
        return clean_name.strip(), ""

    def fetch_metadata_online(self, title, author=""):
        """Cleanly fetches only the core Title and Author from Google."""
        search_query = f"{title} {author}".replace(";", " ")
        url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults=1"
        try:
            response = requests.get(url, timeout=5).json()
            if "items" in response:
                info = response["items"][0]["volumeInfo"]
                raw_title = info.get("title", title)
                # Remove subtitles like ": The Warrior Trilogy" to keep it clean
                clean_title = raw_title.split(":")[0].split("(")[0].strip()
                return {
                    "title": clean_title,
                    "author": info.get("authors", [author])[0],
                    "cover_url": info.get("imageLinks", {}).get("thumbnail")
                }
        except: pass
        return None

    def convert_to_epub(self, input_path, output_folder, title, author, cover_path=None):
        if not os.path.exists(output_folder): os.makedirs(output_folder)
        
        # Enforce "Author - Title.epub"
        safe_title = self.sanitize_filename(title)
        safe_author = self.sanitize_filename(author)
        file_name = f"{safe_author} - {safe_title}.epub"
        output_path = os.path.join(output_folder, file_name)
        
        try:
            command = [
                'pandoc', input_path, 
                '--metadata', f'title={title}', 
                '--metadata', f'author={author}',
                '-o', output_path
            ]
            if cover_path and os.path.exists(cover_path):
                command.extend(['--epub-cover-image', cover_path])
            
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True, output_path
        except Exception as e:
            return False, str(e)