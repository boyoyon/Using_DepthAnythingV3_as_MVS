
import torch
from depth_anything_3.api import DepthAnything3
import numpy as np
import urllib.request
import cv2, glob, os, sys

DEFAULT_OUTPUT_FOLDER = 'result'

argv = sys.argv
argc = len(argv)

print('%s executs DepthAnythingV3' % argv[0])
print('[usage] python %s <wildcard for images>' % argv[0])

if argc < 2:
    quit()

paths = glob.glob(argv[1])

if len(paths) < 1:
    print('images are not specified')
    quit()

OUTPUT_FOLDER = DEFAULT_OUTPUT_FOLDER
no = 2
while os.path.exists(OUTPUT_FOLDER):
    OUTPUT_FOLDER = DEFAULT_OUTPUT_FOLDER + '_%d' % no
    no += 1
os.mkdir(OUTPUT_FOLDER)
print('output folder %s is created' % OUTPUT_FOLDER)

# デバイス設定

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)


# モデルの読み込み

model_size = "DA3-LARGE"  # "DA3-SMALL", "DA3-BASE", "DA3-LARGE", "DA3-GIANT", 

model = DepthAnything3.from_pretrained(f"depth-anything/{model_size}")
model = model.to(device).eval()

# 推論実行

result = model.inference(paths)

for i, image in enumerate(result.processed_images):

    dst_path = os.path.join(OUTPUT_FOLDER, 'rgb_%04d.png' % (i+1))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(dst_path, image)
    print('save %s' % dst_path)

for i, depth in enumerate(result.depth):

    dst_npy = os.path.join(OUTPUT_FOLDER, 'depth_%04d.npy' % (i+1))
    np.save(dst_npy, depth)
    print('save %s' % dst_npy)

for i, conf in enumerate(result.conf):

    dst_npy = os.path.join(OUTPUT_FOLDER, 'conf_%04d.npy' % (i+1))
    np.save(dst_npy, conf)
    print('save %s' % dst_npy)

for i, intrinsic in enumerate(result.intrinsics):

    dst_npy = os.path.join(OUTPUT_FOLDER, 'intrinsic_%04d.npy' % (i+1))
    np.save(dst_npy, intrinsic)
    print('save %s' % dst_npy)

for i, extrinsic in enumerate(result.extrinsics):

    dst_npy = os.path.join(OUTPUT_FOLDER, 'extrinsic_%04d.npy' % (i+1))
    np.save(dst_npy, extrinsic)
    print('save %s' % dst_npy)








