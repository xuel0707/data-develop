import json
import sys

def convert_json_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin:
        with open(output_file, 'w', encoding='utf-8') as fout:
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    # 将单个对象包装成数组
                    fout.write(json.dumps([item], ensure_ascii=False) + '\n')
                except json.JSONDecodeError as e:
                    print(f"JSON 解码错误: {e}，跳过该行。")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python convert_json.py <输入文件路径> <输出文件路径>")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        convert_json_format(input_path, output_path)