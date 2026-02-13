# tester.py - Version 2.2.1
import os
import shutil
from converter_logic import eBookConverterLogic

def run_multi_format_test():
    print(f"{'='*50}")
    print("Universal eBook Converter - Multi-Format Test Suite")
    print(f"{'='*50}\n")
    
    logic = eBookConverterLogic()
    source_dir = "Test_Inputs"
    output_dir = "Test_Outputs"
    
    # Setup folders
    for d in [source_dir, output_dir]:
        if os.path.exists(d): shutil.rmtree(d)
        os.makedirs(d)

    # Only testing formats we can "fake" with simple text writing
    test_cases = {
        "text_sample.txt": "This is a plain text test.",
        "rich_sample.rtf": r"{\rtf1\ansi This is a Rich Text test.}"
    }

    results = []

    for filename, content in test_cases.items():
        input_path = os.path.join(source_dir, filename)
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Testing format: {filename.split('.')[-1].upper()}...")
        success, result = logic.convert_to_epub(input_path, output_dir, f"Test {filename}", "Tester Bot")
        
        if success and os.path.exists(result):
            print(f"  ✅ Success! Saved to: {os.path.basename(result)}")
            results.append(True)
        else:
            print(f"  ❌ Failed! Error: {result}")
            results.append(False)

    print(f"\n{'='*50}")
    passed = results.count(True)
    total = len(results)
    print(f"TEST SUMMARY: {passed}/{total} Passed")
    
    if passed == total:
        print("Final Verdict: CORE SYSTEMS OK 🚀")
        print("(Note: To test DOCX/PDF, please use 'real' files in the GUI)")
    else:
        print("Final Verdict: ISSUES DETECTED ⚠️")
    print(f"{'='*50}\n")

    input("Press Enter to delete test folders and exit...")
    shutil.rmtree(source_dir)
    shutil.rmtree(output_dir)

if __name__ == "__main__":
    run_multi_format_test()