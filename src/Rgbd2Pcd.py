import cv2, glob, os, sys
import numpy as np
import open3d as o3d

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s creates Point Cloud (.ply) from the results of Depth Anything V2 inference' % argv[0])
    print('[usage] python %s <result folder>' % argv[0])

    if argc < 2:
        quit()

    folder = argv[1]

    paths_rgb = glob.glob(os.path.join(folder, 'rgb_*.png'))
    paths_depth = glob.glob(os.path.join(folder, 'depth_*.npy'))
    paths_intrinsic = glob.glob(os.path.join(folder, 'intrinsic_*.npy'))
    paths_extrinsic = glob.glob(os.path.join(folder, 'extrinsic_*.npy'))

    last_row = np.array([0, 0, 0, 1])
    
    pcd = None

    for i, path_rgb in enumerate(paths_rgb):

        rgb = cv2.imread(path_rgb)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    
        RGB = o3d.geometry.Image(rgb)
    
        depth_numpy = np.load(paths_depth[i])
        depth_image = o3d.geometry.Image(np.ascontiguousarray(depth_numpy))
    
        DEPTH = o3d.geometry.Image(depth_image)
        
        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
                RGB, DEPTH, depth_scale=1.0, convert_rgb_to_intensity=False)
    
    
        cam = o3d.camera.PinholeCameraIntrinsic()
        cam.intrinsic_matrix = np.load(paths_intrinsic[i])
    
        extrinsic3x4 = np.load(paths_extrinsic[i])
        extrinsic = np.vstack([extrinsic3x4, last_row])
    
        if i == 0:
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
                rgbd,
                cam,
                extrinsic=extrinsic
            )

        else:
            pcd += o3d.geometry.PointCloud.create_from_rgbd_image(
                rgbd,
                cam,
                extrinsic=extrinsic
            )

    dst_path = os.path.join(folder, 'Rgbd2Pcd.ply')
    o3d.io.write_point_cloud(dst_path, pcd)
    print('save %s' % dst_path)

    o3d.visualization.draw_geometries([pcd])

if __name__ == '__main__':
    main()
