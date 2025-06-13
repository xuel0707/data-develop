import pdfplumber
import json
import os
import argparse
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    """
    提取单个 PDF 文件的文本内容。
    返回值为包含 'text' 字段的字典。
    """
    all_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text()
                    if text:
                        all_text += text.strip() + "\n"
                except Exception as e:
                    print(f"Error extracting page {page_num} from {pdf_path}: {e}")
    except Exception as e:
        print(f"Error opening PDF file {pdf_path}: {e}")
    
    return {
        "text": all_text.strip()
    }

def save_to_json(data, json_path):
    """
    将数据保存为 JSON 格式文件。
    """
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_pdfs_in_directory(directory_path, output_json_path):
    """
    遍历目录中的所有 PDF 文件，提取文本并保存为 JSON。
    每个 PDF 对应一条数据。
    """
    all_data = []
    pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
    
    for filename in tqdm(pdf_files, desc="Processing PDFs"):
        pdf_path = os.path.join(directory_path, filename)
        extracted_data = extract_text_from_pdf(pdf_path)
        all_data.append(extracted_data)
    
    save_to_json(all_data, output_json_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDFs in a directory and convert them to JSON format.")
    parser.add_argument('directory_path', type=str, help='The directory containing the PDF files.')
    parser.add_argument('output_json_path', type=str, help='The path to the output JSON file.')

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        print(f"The provided directory path '{args.directory_path}' does not exist or is not a directory.")
    else:
        process_pdfs_in_directory(args.directory_path, args.output_json_path)