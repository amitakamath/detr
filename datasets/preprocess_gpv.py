# Convert GPV splits to COCO-format

import os
import pdb
import json
import shutil
import argparse
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('split', choices=['train', 'val', 'test'], help='data split')
    args = parser.parse_args()

    if args.split == 'test':
        coco_path = '/home/amitak/detr/data/coco/annotations/instances_val2014.json'
        category_path = '/home/amitak/data/learning_phase_data/coco_detection/gpv_split/test_category_counts.json'
        images_path = '/home/amitak/detr/data/coco/val2014'
    else:
        coco_path = '/home/amitak/detr/data/coco/annotations/instances_train2014.json'
        category_path = '/home/amitak/data/learning_phase_data/coco_detection/gpv_split/train_category_counts.json'
        images_path = '/home/amitak/detr/data/coco/train2014'
        

    coco_data = json.load(open(coco_path, 'r'))
    category_data = json.load(open(category_path, 'r'))
    categories = category_data['seen'].keys()
    coco_categories = [d for d in coco_data['categories'] \
            if d['name'] in categories]

    gpv_path = '/home/amitak/data/learning_phase_data/coco_detection/gpv_split/{}.json'.format(args.split)
    gpv_data = json.load(open(gpv_path, 'r'))
    image_id_list = list(set([d['image']['image_id'] for d in gpv_data]))
    coco_images = [d for d in coco_data['images'] \
            if d['id'] in image_id_list]

    # read this info from OG COCO
    write_data = {'info': coco_data['info'], 
            'licenses': coco_data['licenses'],
            'categories': coco_categories, 
            'images': coco_images,
            'annotations': []
                }
    count = 0
    for instance in gpv_data:
        for box in instance['boxes']:
            coco_instance = {\
                    'image_id': instance['image']['image_id'], \
                    'category_id': instance['category_id'], \
                    'area': 0, 'bbox': box, 'id': count, \
                    'iscrowd': 0}
            count += 1
            write_data['annotations'].append(coco_instance)

    # Write write_data into annotations file
    json.dump(write_data, open('/home/amitak/detr/data/coco/annotations/instances_gpv_{}2014.json'.format(args.split), 'w'))
    # image_id_list images need to be shortcutted in the expected filepath.
    # for now, copy
    copy_files = [f for f in os.listdir(images_path) if int(f[-16:-4]) in image_id_list]
    target_path = '/home/amitak/detr/data/coco/gpv_{}2014'.format(args.split)
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    for c in tqdm(copy_files):
        shutil.copy(os.path.join(images_path,c), target_path)

if __name__ == '__main__':
    main()

