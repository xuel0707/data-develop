import os
import glob
import json
import argparse


def is_json_file(filename):
    """判断是否是 .json 文件"""
    return filename.lower().endswith('.json')


def is_jsonl_file(filename):
    """判断是否是 .jsonl 文件"""
    return filename.lower().endswith('.jsonl')


def merge_json_files(input_dir, output_file):
    """
    将指定目录下的所有 .json 和 .jsonl 文件合并为一个 JSON 数组文件。
    
    :param input_dir: 包含 json/jsonl 文件的目录路径
    :param output_file: 合并后的输出文件路径
    """
    # 获取所有支持的文件（.json 和 .jsonl）
    json_files = sorted(glob.glob(os.path.join(input_dir, "*.json")))
    jsonl_files = sorted(glob.glob(os.path.join(input_dir, "*.jsonl")))
    all_files = json_files + jsonl_files

    if not all_files:
        print("❌ No .json or .jsonl files found in the directory.")
        return

    # 创建输出目录（如果不存在）
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"🔍 Found {len(all_files)} files to merge (.json and .jsonl).")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('[\n')
        first_item = True

        for file_index, file_path in enumerate(all_files):
            print(f"📄 Processing file {file_index + 1}/{len(all_files)}: {file_path}")

            try:
                if is_json_file(file_path):
                    # 处理 .json 文件（整个文件是一个 JSON 数组）
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        data = json.load(infile)
                        if isinstance(data, list):
                            for item in data:
                                line = json.dumps(item, ensure_ascii=False)
                                if not first_item:
                                    outfile.write(',\n')
                                outfile.write(line)
                                first_item = False
                        else:
                            print(f"⚠️ File {file_path} does not contain a JSON array.")

                elif is_jsonl_file(file_path):
                    # 处理 .jsonl 文件（每行一个 JSON 对象）
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        for line_number, line in enumerate(infile):
                            line = line.strip()
                            if not line:
                                continue
                            if not first_item:
                                outfile.write(',\n')
                            outfile.write(line)
                            first_item = False

            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")
                continue

        outfile.write('\n]')
        print(f"✅ Merged JSON saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge all .json and .jsonl files in a directory into one JSON array file.")
    parser.add_argument('input_dir', type=str, help='Directory containing .json and/or .jsonl files')
    parser.add_argument('output_file', type=str, help='Path to save the merged output JSON file')

    args = parser.parse_args()

    merge_json_files(args.input_dir, args.output_file)