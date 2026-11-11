# 把官中版 ast 提取的 json 合并到 nekosdk_tools 导出的 json 文件中
import json
import os


def clean_text(s: str) -> str:
    '''
    清除全角空格、半角空格、换行
    '''
    return s.replace('　', '').replace(' ', '').replace('\n', '')

def main():
    input_dir = 'gt_input'
    output_dir = 'gt_output'
    ast_dir = 'ast_json'

    input_files = [f for f in os.listdir('gt_input') if f.endswith('.json')]

    for file_name in input_files:
        base_name = file_name.split('.')[0]
        ast_path = os.path.join(ast_dir, base_name, 'text.json')
        in_path = os.path.join(input_dir, file_name)
        out_path = os.path.join(output_dir, file_name)

        if not os.path.exists(ast_path):
            print(f'{base_name} - not exist')
            continue

        with open(in_path, 'r') as f_in, open(ast_path, 'r') as ast_in:
            in_data = json.load(f_in)
            ast_data = json.load(ast_in)

            # 长度校验，防止索引越界
            if len(in_data) != len(ast_data):
                print(f'{base_name}：条目数量不一致！gt_input:{len(in_data)} ast_json:{len(ast_data)}')
                continue

            for idx, item in enumerate(in_data):
                item_id = item['id']
                msg = clean_text(item['message'])
                ast_item = ast_data[idx]
                ast_msg = clean_text(ast_item['ja']['text'])

                if msg == ast_msg:
                    if 'name' in item:
                        item['name'] = ast_item['cn']['name']
                    item['message'] = ast_item['cn']['text']
                else:
                    print(f'{base_name} - {item_id} - {msg} 不对应')

            print(f'{file_name} - pass')

            with open(out_path, 'w') as f_out:
                json.dump(in_data, f_out, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()