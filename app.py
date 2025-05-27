# import os
# import tempfile
# import zipfile
# import chardet
# from datetime import datetime
# from pathlib import Path
# from flask import Flask, request, render_template, send_file, redirect, url_for, flash

# # Optional: load environment variables from a .env file (for local dev)
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     pass  # dotenv not installed, ignore

# app = Flask(__name__)

# # ====== SECRET KEY SETUP =======
# # Best practices for Flask secret key:
# # 1) Hardcoded (not recommended for production):
# #    app.secret_key = 'your-hardcoded-secret-key'
# #
# # 2) Use environment variable (recommended):
# #    export FLASK_SECRET_KEY="your-secret-key"  # Linux/macOS shell
# #    set FLASK_SECRET_KEY=your-secret-key       # Windows CMD
# #
# # 3) Use a .env file + python-dotenv for local dev (easy and secure)
# #
# # 4) Generate a secure secret key in Python:
# #    >>> import secrets
# #    >>> secrets.token_hex(32)
# #
# # Here, we read from environment variable, with fallback for dev only:
# app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-for-local-only')

# # -------------------------------
# # Your full ProjectExtractor class goes here (unchanged)
# class ProjectExtractor:
#     def __init__(self):
#         self.supported_text_extensions = {
#             '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
#             '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r',
#             '.sql', '.html', '.htm', '.css', '.scss', '.sass', '.less', '.xml',
#             '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.config',
#             '.txt', '.md', '.rst', '.log', '.csv', '.tsv', '.dockerfile', '.env',
#             '.gitignore', '.gitattributes', '.editorconfig', '.prettierrc',
#             '.eslintrc', '.babelrc', '.npmrc', '.requirements', '.pipfile',
#             '.makefile', '.cmake', '.sh', '.bat', '.ps1', '.dockerfile'
#         }

#         self.binary_extensions = {
#             '.exe', '.dll', '.so', '.dylib', '.bin', '.dat', '.db', '.sqlite',
#             '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp',
#             '.mp3', '.mp4', '.avi', '.mov', '.wav', '.pdf', '.zip', '.tar',
#             '.gz', '.rar', '.7z', '.dmg', '.iso', '.img'
#         }

#     def detect_encoding(self, file_path):
#         try:
#             with open(file_path, 'rb') as f:
#                 raw_data = f.read(10000)
#                 result = chardet.detect(raw_data)
#                 return result['encoding'] if result['encoding'] else 'utf-8'
#         except:
#             return 'utf-8'

#     def is_text_file(self, file_path):
#         file_ext = Path(file_path).suffix.lower()
#         file_name = Path(file_path).name.lower()

#         if file_ext in self.supported_text_extensions:
#             return True

#         special_files = {
#             'dockerfile', 'makefile', 'rakefile', 'gemfile', 'procfile',
#             'vagrantfile', 'jenkinsfile', 'readme', 'license', 'changelog',
#             'authors', 'contributors', 'copying', 'install', 'news', 'todo'
#         }

#         if file_name in special_files:
#             return True

#         if file_ext in self.binary_extensions:
#             return False

#         try:
#             with open(file_path, 'rb') as f:
#                 chunk = f.read(1024)
#                 if b'\x00' in chunk:
#                     return False
#                 return True
#         except:
#             return False

#     def read_file_content(self, file_path):
#         if not self.is_text_file(file_path):
#             return f"[BINARY FILE - Content not displayed]\nFile size: {os.path.getsize(file_path)} bytes"

#         try:
#             encoding = self.detect_encoding(file_path)
#             with open(file_path, 'r', encoding=encoding, errors='replace') as f:
#                 content = f.read()
#                 if content.strip():
#                     return content
#                 else:
#                     return "[EMPTY FILE]"
#         except Exception as e:
#             return f"[ERROR READING FILE: {str(e)}]"

#     def get_file_info(self, file_path):
#         try:
#             stat = os.stat(file_path)
#             size = stat.st_size
#             modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
#             return f"Size: {size} bytes | Modified: {modified}"
#         except:
#             return "Size: Unknown | Modified: Unknown"

#     def should_skip_file(self, relative_path):
#         path_parts = relative_path.replace('\\', '/').split('/')
#         filename = os.path.basename(relative_path)
#         path_normalized = relative_path.replace('\\', '/')

#         # Skip macOS metadata files
#         if any(part.startswith('._') for part in path_parts):
#             return True

#         # Skip __MACOSX folder entirely
#         if '__MACOSX' in path_parts:
#             return True

#         # Skip .git folder entirely
#         if '.git' in path_parts:
#             return True

#         # Add .gitignore to system files to skip
#         system_files = ['.DS_Store', 'Thumbs.db', 'desktop.ini', '.gitignore']
#         if filename in system_files:
#             return True

#         if filename.startswith('~'):
#             return True
#         if filename.startswith('.tmp'):
#             return True
#         if filename.startswith('.temp'):
#             return True

#         if filename.endswith('.bak'):
#             return True
#         if filename.endswith('.backup'):
#             return True
#         if filename.endswith('.swp'):
#             return True
#         if filename.endswith('.swo'):
#             return True

#         skip_dirs = [
#             'node_modules', '__pycache__', '.pytest_cache', '.coverage',
#             'dist', 'build', '.venv', 'venv', '.env/lib', '.env/bin',
#             '.tox', '.idea', '.vscode', '.vs', 'target', 'bin', 'obj'
#         ]

#         for skip_dir in skip_dirs:
#             if ('/' + skip_dir + '/') in path_normalized or path_normalized.startswith(skip_dir + '/'):
#                 return True

#         return False

#     def extract_zip_contents(self, zip_path, output_file):
#         if not os.path.exists(zip_path):
#             raise FileNotFoundError(f"Zip file not found: {zip_path}")

#         with tempfile.TemporaryDirectory() as temp_dir:
#             with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#                 zip_ref.extractall(temp_dir)

#             all_files = []
#             for root, dirs, files in os.walk(temp_dir):
#                 dirs[:] = [d for d in dirs if not (d.startswith('._') or d == '__MACOSX' or d == '.git')]
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     relative_path = os.path.relpath(file_path, temp_dir)

#                     if not self.should_skip_file(relative_path):
#                         all_files.append((file_path, relative_path))

#             all_files.sort(key=lambda x: x[1])

#             with open(output_file, 'w', encoding='utf-8', errors='replace') as output:
#                 output.write("=" * 80 + "\n")
#                 output.write(f"PROJECT CONTENT EXTRACTION\n")
#                 output.write(f"Source: {os.path.basename(zip_path)}\n")
#                 output.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
#                 output.write(f"Total files: {len(all_files)}\n")
#                 output.write("=" * 80 + "\n\n")

#                 output.write("TABLE OF CONTENTS\n")
#                 output.write("-" * 40 + "\n")
#                 for i, (_, relative_path) in enumerate(all_files, 1):
#                     output.write(f"{i:3d}. {relative_path}\n")
#                 output.write("\n" + "=" * 80 + "\n\n")

#                 for i, (file_path, relative_path) in enumerate(all_files, 1):
#                     output.write(f"FILE {i}: {relative_path}\n")
#                     output.write("-" * (len(f"FILE {i}: {relative_path}")) + "\n")
#                     output.write(f"Path: {relative_path}\n")
#                     output.write(f"Info: {self.get_file_info(file_path)}\n")
#                     output.write("-" * 40 + "\n")

#                     content = self.read_file_content(file_path)
#                     output.write(content)

#                     output.write(f"\n\n{'=' * 80}\n\n")

#                 text_files = sum(1 for file_path, _ in all_files if self.is_text_file(file_path))
#                 binary_files = len(all_files) - text_files

#                 output.write("EXTRACTION SUMMARY\n")
#                 output.write("-" * 40 + "\n")
#                 output.write(f"Total files processed: {len(all_files)}\n")
#                 output.write(f"Text files: {text_files}\n")
#                 output.write(f"Binary files: {binary_files}\n")
#                 output.write(f"Output file: {output_file}\n")
#                 output.write("Note: System files (__MACOSX, ._files, .git folder) were filtered out\n")
#                 output.write("=" * 80 + "\n")

# # Instantiate extractor
# extractor = ProjectExtractor()

# # Flask routes
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         if 'zip_file' not in request.files:
#             flash("No file part")
#             return redirect(request.url)

#         file = request.files['zip_file']
#         if file.filename == '':
#             flash("No selected file")
#             return redirect(request.url)

#         if file and file.filename.lower().endswith('.zip'):
#             with tempfile.TemporaryDirectory() as tmpdirname:
#                 zip_path = os.path.join(tmpdirname, file.filename)
#                 file.save(zip_path)

#                 output_filename = file.filename.rsplit('.', 1)[0] + "_extracted_content.txt"
#                 output_path = os.path.join(tmpdirname, output_filename)

#                 try:
#                     extractor.extract_zip_contents(zip_path, output_path)
#                 except Exception as e:
#                     flash(f"Error processing zip file: {e}")
#                     return redirect(request.url)

#                 return send_file(output_path, as_attachment=True, download_name=output_filename)

#         else:
#             flash("Please upload a valid .zip file")
#             return redirect(request.url)

#     return render_template("index.html")


# if __name__ == "__main__":
#     app.run(debug=True)

import os
import tempfile
import zipfile
import chardet
import re
from datetime import datetime
from pathlib import Path
from flask import Flask, request, render_template, send_file, redirect, url_for, flash

# Optional: load environment variables from a .env file (for local dev)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, ignore

app = Flask(__name__)

# ====== SECRET KEY SETUP =======
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-for-local-only')


class ProjectExtractor:
    def __init__(self):
        self.supported_text_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r',
            '.sql', '.html', '.htm', '.css', '.scss', '.sass', '.less', '.xml',
            '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.config',
            '.txt', '.md', '.rst', '.log', '.csv', '.tsv', '.dockerfile', '.env',
            '.gitignore', '.gitattributes', '.editorconfig', '.prettierrc',
            '.eslintrc', '.babelrc', '.npmrc', '.requirements', '.pipfile',
            '.makefile', '.cmake', '.sh', '.bat', '.ps1', '.dockerfile'
        }

        self.binary_extensions = {
            '.exe', '.dll', '.so', '.dylib', '.bin', '.dat', '.db', '.sqlite',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp',
            '.mp3', '.mp4', '.avi', '.mov', '.wav', '.pdf', '.zip', '.tar',
            '.gz', '.rar', '.7z', '.dmg', '.iso', '.img'
        }

    def detect_encoding(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)
                result = chardet.detect(raw_data)
                return result['encoding'] if result['encoding'] else 'utf-8'
        except:
            return 'utf-8'

    def is_text_file(self, file_path):
        file_ext = Path(file_path).suffix.lower()
        file_name = Path(file_path).name.lower()

        if file_ext in self.supported_text_extensions:
            return True

        special_files = {
            'dockerfile', 'makefile', 'rakefile', 'gemfile', 'procfile',
            'vagrantfile', 'jenkinsfile', 'readme', 'license', 'changelog',
            'authors', 'contributors', 'copying', 'install', 'news', 'todo'
        }

        if file_name in special_files:
            return True

        if file_ext in self.binary_extensions:
            return False

        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:
                    return False
                return True
        except:
            return False

    def read_file_content(self, file_path):
        if not self.is_text_file(file_path):
            return f"[BINARY FILE - Content not displayed]\nFile size: {os.path.getsize(file_path)} bytes"

        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
                if content.strip():
                    return content
                else:
                    return "[EMPTY FILE]"
        except Exception as e:
            return f"[ERROR READING FILE: {str(e)}]"

    def get_file_info(self, file_path):
        try:
            stat = os.stat(file_path)
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            return f"Size: {size} bytes | Modified: {modified}"
        except:
            return "Size: Unknown | Modified: Unknown"

    def should_skip_file(self, relative_path):
        path_parts = relative_path.replace('\\', '/').split('/')
        filename = os.path.basename(relative_path)
        path_normalized = relative_path.replace('\\', '/')

        if any(part.startswith('._') for part in path_parts):
            return True

        if '__MACOSX' in path_parts:
            return True

        if '.git' in path_parts:
            return True

        # Add .gitignore to system files to skip
        system_files = ['.DS_Store', 'Thumbs.db', 'desktop.ini', '.gitignore']
        if filename in system_files:
            return True

        if filename.startswith('~'):
            return True
        if filename.startswith('.tmp'):
            return True
        if filename.startswith('.temp'):
            return True

        if filename.endswith('.bak'):
            return True
        if filename.endswith('.backup'):
            return True
        if filename.endswith('.swp'):
            return True
        if filename.endswith('.swo'):
            return True

        skip_dirs = [
            'node_modules', '__pycache__', '.pytest_cache', '.coverage',
            'dist', 'build', '.venv', 'venv', '.env/lib', '.env/bin',
            '.tox', '.idea', '.vscode', '.vs', 'target', 'bin', 'obj'
        ]

        for skip_dir in skip_dirs:
            if ('/' + skip_dir + '/') in path_normalized or path_normalized.startswith(skip_dir + '/'):
                return True

        return False

    def extract_zip_contents(self, zip_path, output_file):
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found: {zip_path}")

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            all_files = []
            for root, dirs, files in os.walk(temp_dir):
                dirs[:] = [d for d in dirs if not (d.startswith('._') or d == '__MACOSX' or d == '.git')]
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, temp_dir)

                    if not self.should_skip_file(relative_path):
                        all_files.append((file_path, relative_path))

            all_files.sort(key=lambda x: x[1])

            with open(output_file, 'w', encoding='utf-8', errors='replace') as output:
                output.write("=" * 80 + "\n")
                output.write(f"PROJECT CONTENT EXTRACTION\n")
                output.write(f"Source: {os.path.basename(zip_path)}\n")
                output.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                output.write(f"Total files: {len(all_files)}\n")
                output.write("=" * 80 + "\n\n")

                output.write("TABLE OF CONTENTS\n")
                output.write("-" * 40 + "\n")
                for i, (_, relative_path) in enumerate(all_files, 1):
                    output.write(f"{i:3d}. {relative_path}\n")
                output.write("\n" + "=" * 80 + "\n\n")

                for i, (file_path, relative_path) in enumerate(all_files, 1):
                    output.write(f"FILE {i}: {relative_path}\n")
                    output.write("-" * (len(f"FILE {i}: {relative_path}")) + "\n")
                    output.write(f"Path: {relative_path}\n")
                    output.write(f"Info: {self.get_file_info(file_path)}\n")
                    output.write("-" * 40 + "\n")

                    content = self.read_file_content(file_path)
                    output.write(content)

                    output.write(f"\n\n{'=' * 80}\n\n")

                text_files = sum(1 for file_path, _ in all_files if self.is_text_file(file_path))
                binary_files = len(all_files) - text_files

                output.write("EXTRACTION SUMMARY\n")
                output.write("-" * 40 + "\n")
                output.write(f"Total files processed: {len(all_files)}\n")
                output.write(f"Text files: {text_files}\n")
                output.write(f"Binary files: {binary_files}\n")
                output.write(f"Output file: {output_file}\n")
                output.write("Note: System files (__MACOSX, ._files, .git folder) were filtered out\n")
                output.write("=" * 80 + "\n")

    def remove_comments(self, text, file_ext):
        """Remove comments based on file extension"""
        # Simple example: remove Python, JS, Java style comments

        if file_ext in ['.py']:
            # Remove Python comments (# and multiline """ """)
            text = re.sub(r'#.*', '', text)  # remove single-line #
            text = re.sub(r'"""(.*?)"""', '', text, flags=re.DOTALL)  # remove multiline
            text = re.sub(r"'''(.*?)'''", '', text, flags=re.DOTALL)
        elif file_ext in ['.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp']:
            # Remove single line // comments and multiline /* */
            text = re.sub(r'//.*', '', text)
            text = re.sub(r'/\*(.*?)\*/', '', text, flags=re.DOTALL)
        # Add more languages or comment styles if needed
        return text

    def extract_zip_contents_without_comments(self, zip_path, output_file):
        """Extract zip but remove unwanted comments in code files"""

        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found: {zip_path}")

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            all_files = []
            for root, dirs, files in os.walk(temp_dir):
                dirs[:] = [d for d in dirs if not (d.startswith('._') or d == '__MACOSX' or d == '.git')]
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, temp_dir)

                    if not self.should_skip_file(relative_path):
                        all_files.append((file_path, relative_path))

            all_files.sort(key=lambda x: x[1])

            with open(output_file, 'w', encoding='utf-8', errors='replace') as output:
                output.write("=" * 80 + "\n")
                output.write(f"PROJECT CONTENT EXTRACTION (Comments Removed)\n")
                output.write(f"Source: {os.path.basename(zip_path)}\n")
                output.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                output.write(f"Total files: {len(all_files)}\n")
                output.write("=" * 80 + "\n\n")

                output.write("TABLE OF CONTENTS\n")
                output.write("-" * 40 + "\n")
                for i, (_, relative_path) in enumerate(all_files, 1):
                    output.write(f"{i:3d}. {relative_path}\n")
                output.write("\n" + "=" * 80 + "\n\n")

                for i, (file_path, relative_path) in enumerate(all_files, 1):
                    output.write(f"FILE {i}: {relative_path}\n")
                    output.write("-" * (len(f"FILE {i}: {relative_path}")) + "\n")
                    output.write(f"Path: {relative_path}\n")
                    output.write(f"Info: {self.get_file_info(file_path)}\n")
                    output.write("-" * 40 + "\n")

                    content = self.read_file_content(file_path)
                    file_ext = Path(file_path).suffix.lower()

                    # Remove comments if text file
                    if self.is_text_file(file_path):
                        content = self.remove_comments(content, file_ext)

                    output.write(content)
                    output.write(f"\n\n{'=' * 80}\n\n")

                text_files = sum(1 for file_path, _ in all_files if self.is_text_file(file_path))
                binary_files = len(all_files) - text_files

                output.write("EXTRACTION SUMMARY\n")
                output.write("-" * 40 + "\n")
                output.write(f"Total files processed: {len(all_files)}\n")
                output.write(f"Text files: {text_files}\n")
                output.write(f"Binary files: {binary_files}\n")
                output.write(f"Output file: {output_file}\n")
                output.write("Note: System files (__MACOSX, ._files, .git folder) were filtered out\n")
                output.write("=" * 80 + "\n")


# Instantiate extractor
extractor = ProjectExtractor()

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'zip_file' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['zip_file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        extract_type = request.form.get('extract_type', 'normal')

        if file and file.filename.lower().endswith('.zip'):
            with tempfile.TemporaryDirectory() as tmpdirname:
                zip_path = os.path.join(tmpdirname, file.filename)
                file.save(zip_path)

                output_filename = file.filename.rsplit('.', 1)[0]
                if extract_type == 'clean':
                    output_filename += "_clean_extracted_content.txt"
                else:
                    output_filename += "_extracted_content.txt"

                output_path = os.path.join(tmpdirname, output_filename)

                try:
                    if extract_type == 'clean':
                        extractor.extract_zip_contents_without_comments(zip_path, output_path)
                    else:
                        extractor.extract_zip_contents(zip_path, output_path)
                except Exception as e:
                    flash(f"Error processing zip file: {e}")
                    return redirect(request.url)

                return send_file(output_path, as_attachment=True, download_name=output_filename)

        else:
            flash("Please upload a valid .zip file")
            return redirect(request.url)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
