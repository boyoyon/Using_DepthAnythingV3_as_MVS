import cv2, glob, os, sys
import numpy as np
import open3d as o3d

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s loads plys and visualizes 3d model' % argv[0])
    print('[usage] python %s <wildcard for plys>' % argv[0])

    if argc < 2:
        quit()

    paths = glob.glob(argv[1])

    for i, path in enumerate(paths):

        if i == 0:
            pcd = o3d.io.read_point_cloud(path)
        else:
            pcd += o3d.io.read_point_cloud(path)

    o3d.visualization.draw_geometries([pcd])

if __name__ == '__main__':
    main()
