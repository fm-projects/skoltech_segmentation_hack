import os
import numpy as np
from tqdm import tqdm
import cv2
from glob import glob
import click


PATCH_SIZE = 256
BASE_PATH = '.'
SEED = 123


def data_processing(base_path: str = BASE_PATH, 
                    train_data_dir_name: str = 'train',
                    new_save_dir_name_with_train_word: str = 'patches_train',
                    val_part: float = 0.2):
    np.random.seed(SEED)
    source_img_dir = os.path.join(base_path, 
                                  os.path.join(train_data_dir_name, 
                                               'images')
    )
    source_mask_dir = os.path.join(base_path, 
                                   os.path.join(train_data_dir_name, 
                                                'masks')
    )

    new_save_dir = os.path.join(base_path, new_save_dir_name_with_train_word)
    os.makedirs(new_save_dir, exist_ok=True)

    save_img_dir = os.path.join(new_save_dir, 'images')
    save_mask_dir = os.path.join(new_save_dir, 'masks')
    os.makedirs(save_img_dir, exist_ok=True)
    os.makedirs(save_mask_dir, exist_ok=True)
    os.makedirs(os.path.join(
        base_path,
        os.path.relpath(save_img_dir, base_path).replace('train', 'val')
    ), exist_ok=True)
    os.makedirs(os.path.join(
        base_path,
        os.path.relpath(save_mask_dir, base_path).replace('train', 'val')
    ), exist_ok=True)

    img_train_id = 0
    img_val_id = 0
    cnt_zero_pics = 0
    for id in range(len(glob(source_img_dir + '/*'))):
        print(f'---- id: {id} ----')
        img_path = f'{source_img_dir}/train_image_{id:03}.png'
        mask_path = f'{source_mask_dir}/train_mask_{id:03}.png'
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
        mask = cv2.imread(mask_path)
        print(mask_path.split('/')[-1][:-4])
        if img.shape != mask.shape:
            continue
        img_name = os.path.join(save_img_dir, img_path.split('/')[-1][:-4])
        img_name = img_name[:img_name.rfind('_')]
        mask_name = os.path.join(save_mask_dir, mask_path.split('/')[-1][:-4])
        mask_name = mask_name[:mask_name.rfind('_')]
        for i in tqdm(range(0, img.shape[0] // PATCH_SIZE * 256, 128)):
            for j in range(0, img.shape[1] // PATCH_SIZE * 256, 128):
                patch_img = img[i:i + PATCH_SIZE, j:j + PATCH_SIZE]
                patch_mask = mask[i:i + PATCH_SIZE, j:j + PATCH_SIZE]
                if patch_mask.sum() <= 4:
                    cnt_zero_pics += 1
                    if cnt_zero_pics % 2 == 0:
                        continue

                # generate validation and train
                if np.random.uniform(0, 1) < val_part:
                    img_name_cur = os.path.join(
                            base_path,
                            os.path.relpath(img_name, base_path).replace('train', 'val')
                        )
                    mask_name_cur = os.path.join(
                            base_path,
                            os.path.relpath(mask_name, base_path).replace('train', 'val')
                        )
                    cur_id = img_val_id
                    img_val_id += 1
                else:
                    img_name_cur = img_name
                    mask_name_cur = mask_name
                    cur_id = img_train_id
                    img_train_id += 1

                cv2.imwrite(f"{img_name_cur}_{cur_id:03}.png", patch_img)
                cv2.imwrite(f"{mask_name_cur}_{cur_id:03}.png", patch_mask)


@click.command()
@click.option('--base_path', 
              default=BASE_PATH, 
              type=str, 
              help='Path to parent dir where train dir')
@click.option('--train_data_dir_name', 
              default='train', 
              type=str, 
              help='The person to greet.')
@click.option('--new_save_dir_name_with_train_word', 
              default='pathces_train', 
              type=str,
              help='new dir name with "train" word. It will be saved in base_path')
@click.option('--val_part',
              default=0.2,
              type=float,
              help='part of validation')
def click_run_data_gen(base_path, train_data_dir_name, new_save_dir_name_with_train_word, val_part):
    data_processing(base_path=base_path, 
                    train_data_dir_name=train_data_dir_name,
                    new_save_dir_name_with_train_word=new_save_dir_name_with_train_word,
                    val_part=val_part)


if __name__ == '__main__':
    click_run_data_gen()
