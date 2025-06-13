import json
import argparse
import re
from tqdm import tqdm

def extract_application_contents(text):
    """
    从高新技术企业认定申请书目录中提取所有材料名称。
    
    :param text: 包含目录信息的字符串
    :return: 材料名称列表
    """
    # 正则匹配类似“X.X、材料名称”或“一、材料名称”的条目
    pattern = r'[一二三四五六七八九十\d]\.?[\d\.]*、\s*([^0-9\n\r]+)'
    matches = re.findall(pattern, text)

    # 去除末尾可能存在的页码数字、多余空格等
    cleaned = [re.sub(r'\s*\d+[\.\d]*\s*$', '', item.strip()) for item in matches]

    return cleaned


def convert_jsonl_format(input_path, output_path):
    """
    将 JSONL 文件中的每个条目转换为 SFT 训练格式：
    {
      "instruction": "...",
      "input": "...",
      "output": "..."
    }
    每个样本一行（JSONL 格式）
    """
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line_number, line in enumerate(tqdm(lines, desc="Processing JSONL")):
            try:
                item = json.loads(line.strip())
            except json.JSONDecodeError:
                print(f"⚠️ Skipping invalid JSON line {line_number + 1}")
                continue

            raw_text = item.get('text', '').strip()
            if not raw_text:
                continue

            instruction = "根据以下内容，找出高新技术企业认定申请书需要包含哪些内容？"
            input_text = raw_text[:4096]  # 防止过长，限制输入长度

            contents = extract_application_contents(raw_text)
            if contents:
                output_summary = "高新技术企业认定申请书需要包含：" + "、".join(contents)
            else:
                output_summary = "无法提取申请书所需材料。"

            sample = {
                "instruction": instruction,
                "input": input_text,
                "output": output_summary
            }

            outfile.write(json.dumps(sample, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert policy JSONL to fine-tuning format.")
    parser.add_argument('--input_jsonl', type=str, required=True, help='Path to the input JSONL file.')
    parser.add_argument('--output_jsonl', type=str, required=True, help='Path to the output JSONL file.')

    args = parser.parse_args()

    convert_jsonl_format(args.input_jsonl, args.output_jsonl)