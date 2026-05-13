import json
import os
from PIL import Image

def via_to_labelme(via_json_path, image_dir, output_dir):
    try:
        # 读取 VIA 格式的 JSON 文件
        with open(via_json_path, 'r', encoding='utf-8') as f:
            via_data = json.load(f)
    except FileNotFoundError:
        print(f"未找到 VIA 格式的 JSON 文件: {via_json_path}")
        return

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    labelme_data_list = []
    for image_id, image_info in via_data['file'].items():
        image_name = image_info['fname']
        image_path = os.path.join(image_dir, image_name)

        try:
            # 打开图像文件，获取图像的高度和宽度
            with Image.open(image_path) as img:
                image_width, image_height = img.size
        except FileNotFoundError:
            print(f"未找到图像文件: {image_path}")
            continue

        labelme_data = {
            "version": "4.5.6",
            "flags": {},
            "shapes": [],
            "imagePath": image_name,
            "imageData": None,
            "imageHeight": image_height,
            "imageWidth": image_width
        }

        for metadata_id, metadata_info in via_data['metadata'].items():
            if metadata_info['vid'] == image_id:
                behavior_option_id = metadata_info['av']['1']
                behavior = via_data['attribute']['1']['options'][behavior_option_id]

                xy = metadata_info['xy']
                x1, y1, width, height = xy[1], xy[2], xy[3], xy[4]
                x2, y2 = x1 + width, y1 + height

                shape = {
                    "label": behavior,
                    "points": [
                        [x1, y1],
                        [x2, y2]
                    ],
                    "group_id": None,
                    "shape_type": "rectangle",
                    "flags": {}
                }
                labelme_data["shapes"].append(shape)

        labelme_data_list.append(labelme_data)

    # 保存为 Labelme 格式的 JSON 文件
    for i, labelme_data in enumerate(labelme_data_list):
        labelme_json_path = os.path.join(output_dir, f'labelme_{i}.json')
        try:
            with open(labelme_json_path, 'w', encoding='utf-8') as f:
                json.dump(labelme_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存 Labelme 格式的 JSON 文件时出错: {labelme_json_path}, 错误信息: {e}")

# 使用示例
via_json_path = 'D:/labeled data/3000/3000.json'
image_dir = 'D:/labeled data/3000'  # 图像文件所在的目录
output_dir = 'D:/labeled data/3000/labelme_output'  # 输出目录
via_to_labelme(via_json_path, image_dir, output_dir)


