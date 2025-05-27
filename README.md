# Project Zip File Extractor

A simple and easy-to-use Flask web application that extracts and consolidates contents from ZIP project files. It supports filtering out system files and can optionally remove comments from code files during extraction.

---

## Features

- Upload ZIP files via a clean web UI.
- Extract and consolidate file contents into a single text file.
- Automatically filters out common system and metadata files (`.git`, `__MACOSX`, `.DS_Store`, `.gitignore`, etc.).
- Optionally remove comments from code files (supports Python, JavaScript, Java, C/C++).
- Supports many common code and text file extensions.
- Shows extraction summary including counts of text and binary files.
- Secure Flask app with environment-configurable secret key.

---

## Screenshots

![Upload Page](docs/upload_page.png)  
*Clean UI with two extraction modes.*

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repo:

```bash
git clone https://github.com/Aniketkumar121/zip-file-extractor.git
cd zip-file-extractor
```

2. Create and activate a virtual environment:

```bash
Copy
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
Copy
pip install -r requirements.txt
```

4. Hosted on Render

```bash
https://zip-file-extractor.onrender.com
```

---
