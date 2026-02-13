ePub Creator

ePub Creator is a streamlined desktop utility designed to convert text-based documents into professionally formatted ePub files. It automates the heavy lifting of metadata retrieval and cover art fetching while keeping the user in total control of the final output.

🚀 Key Features
Batch Processing: Convert entire directories of documents in one session.

Smart Metadata: Automatically queries the Google Books API to find official titles, authors, and high-quality cover thumbnails.

Human-in-the-Loop: Every file undergoes a mandatory review, allowing you to correct AI guesses, swap Author/Title fields, or strip out unwanted noise (like product codes).

Path Persistence: Remembers your Source and Output folders between sessions so you don't have to re-navigate your file system.

Multi-Threaded UI: A responsive interface with a real-time activity log and a "Stop" button to cancel batches safely.

🛠 Installation
1. Prerequisites
Python 3.10+: Ensure Python is installed and added to your System PATH.

Pandoc: This is the core engine used for conversion. This app will not work without it.

Download and install it from pandoc.org.

2. Python Dependencies
Open your terminal or command prompt and install the required requests library:

Bash
pip install requests
📖 How to Use
Launch: Run main_gui.py.

Configure Folders:

Click Source Folder to select where your raw documents (.txt, .rtf, .docx, .html) are located.

Click Output Folder to select where the finished ePubs should be saved.

Note: These paths are saved automatically for your next visit.

Start Batch: Click ▶ Start Batch.

The Review Process: For every file, a Confirm Metadata window will appear:

Verify: Check if the AI found the correct book.

Edit: Manually fix typos or rename the title/author as you see fit.

Swap: If the Author and Title are in the wrong fields, click 🔄 Swap Title/Author.

Commit: Click OK to process the file, or Cancel to skip it.

Monitor: View the Activity Log for real-time success/failure status. If you need to stop early, click ⏹ Stop Process.

📝 Best Practices for Filenames
The app parses metadata based on the filename. For the highest initial accuracy, name your source files using this format:
Author Name - Book Title.extension

(Example: Michael A. Stackpole - Warrior; Coupé.rtf)

Technical Note: An active internet connection is required for the "Fetch Metadata" feature. If offline, the app will default to the information parsed directly from your filenames.