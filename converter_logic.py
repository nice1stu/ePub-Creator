# converter_logic.py - Version 2.1.0
import subprocess
import os

class eBookConverterLogic:
    def __init__(self):
        self.version = "2.1.0"

    def convert_to_epub(self, input_path, output_folder, title, author, cover_path=None):
        """Converts file and saves it specifically to the output_folder."""
        if not os.path.exists(input_path):
            return False, "Input file not found."
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Create output filename based on the input filename, but placed in output_folder
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}.epub")
        
        try:
            command = [
                'pandoc', 
                input_path, 
                '--metadata', f'title={title}', 
                '--metadata', f'author={author}',
                '-o', output_path
            ]
            
            if cover_path and os.path.exists(cover_path):
                command.extend(['--epub-cover-image', cover_path])
            
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True, output_path

        except subprocess.CalledProcessError as e:
            return False, f"Pandoc Error: {e.stderr}"
        except FileNotFoundError:
            return False, "System Error: Pandoc not found."