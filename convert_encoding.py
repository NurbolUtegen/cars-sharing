import os

def convert_to_utf8(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='cp1251') as f:
                        content = f.read()
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Converted: {file_path}")
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

convert_to_utf8(os.getcwd())
