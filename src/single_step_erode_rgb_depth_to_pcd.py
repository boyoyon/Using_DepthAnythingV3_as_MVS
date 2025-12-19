import cv2, os, sys
import numpy as np
import open3d as o3d

def save_ply(ply_path, lines):


    with open(ply_path, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % len(lines)
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'property uchar red\n'
        f.write(line)

        line = 'property uchar green\n'
        f.write(line)

        line = 'property uchar blue\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for line in lines:
            f.write(line)

def main():
    
    KERNEL_SIZE = 5

    argv = sys.argv
    argc = len(argv)

    print('%s creates ply from rgb_image and depth_image' % argv[0])
    print('[usage] python %s <rgb image> <depth(.npy)> <intrinsic(.npy)> <extrinsic(.npy)>' % argv[0])
    
    if argc < 5:
        quit()

    rgb = cv2.imread(argv[1])
    H, W = rgb.shape[:2]
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    mask = np.zeros((H,W,1), np.uint8)
    mask[np.where(gray != 0)] = 255

    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)

    depth = np.load(argv[2])

    intrinsic = np.load(argv[3])
    fx = intrinsic[0][0]
    fy = intrinsic[1][1]
    cx = intrinsic[0][2]
    cy = intrinsic[1][2]

    extrinsic = np.load(argv[4])
    R = extrinsic[:,0:3]
    T = extrinsic[:,3]

    lines = []
    for y in range(H):
        for x in range(W):
            m = mask[y][x]
            if m == 0:
                continue

            r = rgb[y][x][2]
            g = rgb[y][x][1]
            b = rgb[y][x][0]
            zc = depth[y][x]
            xc = (x - cx) * zc / fx
            yc = (y - cy) * zc / fy

            C = np.array([xc,yc,zc]).T
            w = R@C+T

            xw = w[0]
            yw = w[1]
            zw = w[2]

            line = '%f %f %f %d %d %d\n' % (xw, yw, zw, r, g, b)
            lines.append(line)

    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    ply_path = '%s_erode_%d.ply' % (filename, KERNEL_SIZE)
    save_ply(ply_path, lines)
    print('save %s' % ply_path)


if __name__ == '__main__':
    main()
