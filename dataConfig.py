import os
from zipfile import ZipFile
import shutil

#put dataconfig file in same directory as zip files

curdir = os.curdir
root = os.path.join(curdir, 'data')
os.mkdir(root)

print("Unzipping testing files...")
with ZipFile(os.path.join(root, 'indoor_test.zip'), 'r') as zip1:
    zip1.extractall(root)

print("Unzipping training files...")
with ZipFile(os.path.join(root, 'indoor_train.zip'), 'r') as zip2:
    zip2.extractall(root)

print("Unzipped.")

print('Configuring data...')

os.rename(os.path.join(root, 'test/LR'), os.path.join(root, 'test/LR_2'))
os.rename(os.path.join(root, 'test/HR'), os.path.join(root, 'test/HR_2'))

shutil.move(os.path.join(root, 'train/LR'), root)
shutil.move(os.path.join(root, 'train/HR'), root)
shutil.move(os.path.join(root, 'test/LR_2'), root)
shutil.move(os.path.join(root, 'test/HR_2'), root)

os.rmdir(os.path.join(root, 'test'))
os.rmdir(os.path.join(root, 'train'))

for d1 in os.listdir(root):
    d1_path = os.path.join(root, d1)
    for d2 in os.listdir(d1_path):
        d2_path = os.path.join(d1_path, d2)
        for d3 in os.listdir(d2_path):
             if (d3 == 'depth_filled') or (d3 == 'depth_raw'):
                d3_path = os.path.join(d2_path, d3)
                shutil.rmtree(d3_path)

for d1 in os.listdir(root):
    d1_path = os.path.join(root, d1)
    if (d1 == 'LR_2') or (d1 == 'HR_2'):
        for d2 in os.listdir(d1_path):
            d2_path = os.path.join(d1_path, d2)
            for d3 in os.listdir(d2_path):
                d3_path = os.path.join(d2_path, d3)
                files = os.listdir(d3_path)
                for f in files:
                    f_path = os.path.join(d3_path, f)
                    p_path = os.path.join(root, d1[:2])
                    p_path = os.path.join(p_path, d2)
                    p_path = os.path.join(p_path, d3)
                    p_path = os.path.join(p_path, f)
                    shutil.move(f_path, p_path)

for d1 in os.listdir(root):
    d1_path = os.path.join(root, d1)
    if (d1 == 'LR_2') or (d1 == 'HR_2'):
        shutil.rmtree(d1_path)

hr_rgb = os.path.join(root, 'HR/RGB')
hr_d = os.path.join(root, 'HR/D')

lr_rgb = os.path.join(root, 'LR/RGB')
lr_d = os.path.join(root, 'LR/D')

os.mkdir(hr_rgb)
os.mkdir(hr_d)
os.mkdir(lr_rgb)
os.mkdir(lr_d)

hr_rgb_sub = os.path.join(hr_rgb, 'sub')
hr_d_sub = os.path.join(hr_d, 'sub')

lr_rgb_sub = os.path.join(lr_rgb, 'sub')
lr_d_sub = os.path.join(lr_d, 'sub')

os.mkdir(hr_rgb_sub)
os.mkdir(hr_d_sub)
os.mkdir(lr_rgb_sub)
os.mkdir(lr_d_sub)

for d1 in os.listdir(root):
    d1_path = os.path.join(root, d1)
    for d2 in os.listdir(d1_path):
        if (d2 == 'RGB') or (d2 == 'D'):
            break
        d2_path = os.path.join(d1_path, d2)
        for d3 in os.listdir(d2_path):
            d3_path = os.path.join(d2_path, d3)
            files = os.listdir(d3_path)
            for f in files:
                f_path = os.path.join(d3_path, f)
                if d1 == 'HR':
                    if d3 == 'color': shutil.move(f_path, hr_rgb_sub)
                    elif d3 == 'depth_vi': shutil.move(f_path, hr_d_sub)
                elif d1 == 'LR':
                    if d3 == 'color': shutil.move(f_path, lr_rgb_sub)
                    elif d3 == 'depth_vi': shutil.move(f_path, lr_d_sub)

for d1 in os.listdir(root):
    d1_path = os.path.join(root, d1)
    for d2 in os.listdir(d1_path):
        if (d2 == 'RGB') or (d2 == 'D'):
            break
        d2_path = os.path.join(d1_path, d2)
        shutil.rmtree(d2_path)

for d1 in os.listdir(root):
    dest = os.path.join(root, d1)
    rgb_path = os.path.join(dest, 'RGB/sub')
    d_path = os.path.join(dest, 'D/sub')
    rgb_files = os.listdir(rgb_path)
    d_files = os.listdir(d_path)

    for f in rgb_files:
        tag = f[:-6]
        f_path = os.path.join(rgb_path, f)
        match = os.path.join(d_path, tag + '_depth_vi.png')
        if os.path.isfile(match) and os.path.isfile(f_path):
            new = os.path.join(dest, tag)
            os.mkdir(new)
            shutil.move(f_path, new)
            shutil.move(match, new)
        else:
            print('No match found.')

shutil.rmtree(os.path.join(root, 'HR/RGB'))
shutil.rmtree(os.path.join(root, 'HR/D'))
shutil.rmtree(os.path.join(root, 'LR/RGB'))
shutil.rmtree(os.path.join(root, 'LR/D'))

print('Data configuration complete.')

for d1 in os.listdir(root):
    print('\nSL1: ')
    print(d1)
    d1_path = os.path.join(root, d1)
    print('\nSL2: ')
    folders = os.listdir(d1_path)
    print('Folders: ' + str(len(folders)))
    for f in folders:
        print(f)
        f_path = os.path.join(d1_path, f)
        files = os.listdir(f_path)
        print('Images: ' + str(len(files)))
