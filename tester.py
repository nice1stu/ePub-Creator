# tester.py - Version 2.3.0
import os
import shutil
import time
from converter_logic import eBookConverterLogic

def run_metadata_test():
    print(f"{'='*60}")
    print("eBook Converter - Metadata & Parsing Test Suite v2.3.0")
    print(f"{'='*60}\n")
    
    logic = eBookConverterLogic()
    source_dir = "Test_Inputs"
    output_dir = "Test_Outputs"
    
    # Refresh test folders
    for d in [source_dir, output_dir]:
        if os.path.exists(d): shutil.rmtree(d)
        os.makedirs(d)

    # Test cases named "Author - Title" to test the parser and scraper
    test_cases = [
        "J.R.R. Tolkien - The Hobbit.rtf",
        "George Orwell - 1984.txt",
        "Mary Shelley - Frankenstein.rtf"
    ]

    print(f"{'Filename':<35} | {'Parse':<10} | {'Scrape':<10}")
    print("-" * 60)

    for filename in test_cases:
        input_path = os.path.join(source_dir, filename)
        
        # 1. Create the dummy file
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(f"This is a test file for {filename}")

        # 2. Test the Parser (Internal Logic)
        title, author = logic.parse_filename(input_path)
        parse_ok = "✅" if title and author else "❌"

        # 3. Test the Scraper (Google Books API)
        # We add a tiny sleep so we don't spam the API too fast
        time.sleep(1)
        meta = logic.fetch_metadata_online(title, author)
        scrape_ok = "✅" if meta and 'title' in meta else "❌"

        print(f"{filename:<35} | {parse_ok:<10} | {scrape_ok:<10}")

        # 4. Final Conversion Test
        final_title = meta['title'] if meta else title
        final_author = meta['author'] if meta else author
        
        success, result = logic.convert_to_epub(input_path, output_dir, final_title, final_author)
        
        if not success:
            print(f"   ⚠️ Conversion failed for {filename}: {result}")

    print(f"\n{'='*60}")
    print("Test Complete.")
    print("Check 'Test_Outputs' to see the generated EPUBs.")
    print(f"{'='*60}\n")

    input("Press Enter to cleanup test files and exit...")
    shutil.rmtree(source_dir)
    shutil.rmtree(output_dir)
    if os.path.exists("temp_cover.jpg"): os.remove("temp_cover.jpg")

if __name__ == "__main__":
    run_multi_format_test = run_metadata_test()