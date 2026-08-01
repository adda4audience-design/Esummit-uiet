import os
import re

# --- CONFIGURATION ---
FOLDER_PATH = '.'  # '.' means the folder where this script is located
# ---------------------

def clean_html_files(folder_path):
    # 1. HTML comments: <!-- comment -->
    html_pattern = re.compile(r'<!--.*?-->', re.DOTALL)
    
    # 2. CSS/JS block comments: /* comment */
    block_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
    
    # 3. Safe JS single-line comments: // comment
    # ^\s* ensures the // is at the start of the line (ignoring tabs/spaces).
    # This safely deletes full-line comments like "// ==================" 
    # but ignores inline ones like "https://" or "<span>// Text //</span>".
    single_line_pattern = re.compile(r'^\s*//.*$', re.MULTILINE)

    files_processed = 0
    total_removed = 0

    print(f"Scanning folder: {os.path.abspath(folder_path)}\n" + "-"*40)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Count matches to show in the terminal report
                    c1 = len(html_pattern.findall(content))
                    c2 = len(block_pattern.findall(content))
                    c3 = len(single_line_pattern.findall(content))
                    num_comments = c1 + c2 + c3
                    
                    if num_comments > 0:
                        # Strip all 3 types of comments
                        content = html_pattern.sub('', content)
                        content = block_pattern.sub('', content)
                        content = single_line_pattern.sub('', content)
                        
                        # Clean up excess blank lines left behind by deleted comments
                        content = re.sub(r'\n\s*\n', '\n\n', content)
                        
                        # Overwrite the file with the pristine code
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                            
                        print(f"Cleaned: {file} | Removed: {c1} HTML, {c2} Block, {c3} Line comments")
                        files_processed += 1
                        total_removed += num_comments
                        
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    print("-" * 40)
    print(f"Task Complete! Modified {files_processed} file(s) and removed {total_removed} comments in total.")

if __name__ == "__main__":
    clean_html_files(FOLDER_PATH)