import os
import json
import subprocess
from docx import Document as DocxDocument
import argparse
from tqdm import tqdm
import tempfile
import shutil


def extract_text_from_docx(docx_path):
    """提取 .docx 文件中的文本"""
    try:
        doc = DocxDocument(docx_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return text.strip()
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
        return ""


def convert_doc_to_txt(doc_path, temp_dir):
    """使用 LibreOffice 将 .doc 文件转换为文本"""
    try:
        # 使用 LibreOffice 转换 .doc 到 .txt
        result = subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'txt', '--outdir', temp_dir, doc_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"Error converting {doc_path} with LibreOffice: {result.stderr.decode()}")
            return ""

        # 找到生成的 .txt 文件
        base_name = os.path.splitext(os.path.basename(doc_path))[0]
        txt_path = os.path.join(temp_dir, f"{base_name}.txt")

        if not os.path.exists(txt_path):
            print(f"Converted file not found: {txt_path}")
            return ""

        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()

    except Exception as e:
        print(f"Error converting {doc_path}: {e}")
        return ""


def process_docs_in_directory(directory_path, output_json_path):
    """遍历目录中所有 .doc 和 .docx 文件，提取文本并保存为 JSON"""
    all_data = []

    supported_files = [f for f in os.listdir(directory_path) if f.lower().endswith(('.doc', '.docx'))]

    # 创建临时目录用于转换 .doc 文件
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename in tqdm(supported_files, desc="Processing DOC/DOCX files"):
            file_path = os.path.join(directory_path, filename)
            _, ext = os.path.splitext(filename)

            if ext.lower() == ".docx":
                text = extract_text_from_docx(file_path)
            elif ext.lower() == ".doc":
                text = convert_doc_to_txt(file_path, temp_dir)
            else:
                continue  # 不应走到这里

            if text:
                all_data.append({"text": text})

    # 保存到 JSON 文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process .doc and .docx files on Linux (Ubuntu).")
    parser.add_argument('directory_path', type=str, help='Directory containing .doc and .docx files.')
    parser.add_argument('output_json_path', type=str, help='Path to the output JSON file.')

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        print(f"The provided directory path '{args.directory_path}' does not exist or is not a directory.")
    else:
        process_docs_in_directory(args.directory_path, args.output_json_path)