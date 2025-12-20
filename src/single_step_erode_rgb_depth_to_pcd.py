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
    print('[usage] python %s <folder> <number>' % argv[0])
    
    if argc < 3:
        quit()

    folder = argv[1]
    no = int(argv[2])

    rgb = cv2.imread(os.path.join(folder, 'rgb_%04d.png' % no))
    H, W = rgb.shape[:2]
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    mask = np.zeros((H,W,1), np.uint8)
    mask[np.where(gray != 0)] = 255

    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)

    depth = np.load(os.path.join(folder, 'depth_%04d.npy' % no))

    K = np.load(os.path.join(folder, 'intrinsic_%04d.npy' % no))
    K_inv = np.linalg.inv(K)

    E = np.load(os.path.join(folder, 'extrinsic_%04d.npy' % no))
    R = E[:,0:3]
    R_inv = R.T
    t = E[:,3]

    lines = []
    for y in range(H):
        for x in range(W):
            m = mask[y][x]
            if m == 0:
                continue

            r = rgb[y][x][2]
            g = rgb[y][x][1]
            b = rgb[y][x][0]
            d = depth[y][x]

            Coord_pixel = np.array([x/d, y/d, 1.0])
            Coord_camera = d * (K_inv @ Coord_pixel)
            Coord_world = R_inv @ (Coord_camera - t)

            xw = Coord_world[0]
            yw = Coord_world[1]
            zw = Coord_world[2]

            line = '%f %f %f %d %d %d\n' % (xw, yw, zw, r, g, b)
            lines.append(line)

    ply_path = 'rgb_%04d_erode_%d.ply' % (no, KERNEL_SIZE)
    save_ply(ply_path, lines)
    print('save %s' % ply_path)


if __name__ == '__main__':
    main()
