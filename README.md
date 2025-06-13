# 一、提取各种文档内容转换为json格式
## 1、将PDF文档转换为json文件，每个pdf转换为json中的一条数据
```shell
python convert2json/convertPDF2JSON.py /mnt/sft/pdf json_dir/pdf.json
```

## 2、将doc或docx文档转换为json文件，每个doc文档转换为json中的一条数据
```shell
python convert2json/convertDOC2JSON.py /mnt/sft/doc json_dir/doc.json
```

## 3、将xlsx文档转换为json文件，每个xlsx文档转换为json中的一条数据
```shell
python convert2json/convertXLSX2JSON.py /mnt/sft/xlsx json_dir/xlsx.json
```

## 二、将目录下多个json合并为一个json
```shell
python convert2json/mergeJSON.py json_dir merge_data/data.jsonl 
```

# 三、对merge后的数据进行清洗
```shell
dj-process --config merge_process.yaml
```

# 四、将数据转换为instructiong格式
```shell
python convert2json/convert2instruction.py --input_jsonl process_data/data.jsonl --output_jsonl output.jsonl 
```

# 五、将instructiong格式转换为list格式
```shell
python convert2json/convert2list.py output.jsonl list.json 
```

