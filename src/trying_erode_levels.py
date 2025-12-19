import os, sys, cv2
import numpy as np

# keycode for cv2.waitKeyEx()
LEFT  = 2424832
UP    = 2490368
RIGHT = 2555904
DOWN  = 2621440

TRACKBAR_MIN = 0
TRACKBAR_MAX = 10

def callback(x):
    pass # do nothing

argv = sys.argv
argc = len(argv)

if(argc < 2):
    print('%s adjusts erode parameter' % argv[0])
    print('[usgae] python %s <input image>' % argv[0])
    quit()

src = cv2.imread(argv[1])
H = src.shape[0]
W = src.shape[1]

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
mask = np.empty((H, W, 1), np.uint8)

mask[np.where(gray == 0)] = 0
mask[np.where(gray != 0)] = 255

# create a window
cv2.namedWindow('eroded_mask')

# create trackbar
cv2.createTrackbar('erode', 'eroded_mask', TRACKBAR_MIN, TRACKBAR_MAX, callback)

SCALE = 1.0

pos = TRACKBAR_MIN
prevPos = -1

prevScale = 1.0
fUpdate = True

print('Slide Trackbar or Press arrow-key to adjust erode parameter')
print('Press Arrow-keys to adjust erode parameter')
print('Press ESC-key to terminate this program')
print('Press S-key to save erode image and terminate this program')

kernel_size = pos * 2 + 1
kernel = np.ones((kernel_size, kernel_size), np.uint8)
erodedMask = cv2.erode(mask, kernel, iterations=1)

while(1):
    # retrieve the current position of trackbar
    pos = cv2.getTrackbarPos('erode', 'eroded_mask')

    if pos != prevPos or SCALE != prevScale:
        size = pos * 2 + 1
        print('execute dilation with the size %d' % size)

        kernel = np.ones((size, size), np.uint8)
        erodedMask = cv2.erode(mask, kernel, iterations=1)
        dst = src.copy()
        dst[erodedMask == 0]=(0,0,0)

        cloneSrc = cv2.resize(src, (int(W * SCALE), int(H * SCALE)))
        cloneDilatedMask = cv2.resize(erodedMask, (int(W * SCALE), int(H * SCALE)))
        cloneDst = cv2.resize(dst, (int(W * SCALE), int(H * SCALE)))

        cv2.imshow('src', cloneSrc)
        cv2.imshow('eroded_mask', cloneDilatedMask)
        cv2.imshow('dst', cloneDst)
        
        prevPos = pos
        prevScale = SCALE

    key = cv2.waitKeyEx(100)
    if key == 27 or key == ord('S') or key == ord('s'):
        break

    elif key == RIGHT:
        pos += 1
    elif key == UP:
        pos += 3
    elif key == LEFT:
        pos -= 1
    elif key == DOWN:
        pos -= 3
    elif key == ord('+'):
        SCALE *= 1.1
    elif key == ord('-'):
        SCALE *= 0.9

    if pos < TRACKBAR_MIN:
        pos = TRACKBAR_MIN

    if pos > TRACKBAR_MAX:
        pos = TRACKBAR_MAX

    if pos != prevPos:
        cv2.setTrackbarPos('erode', 'eroded_edge', pos) 

if key == ord('S') or key == ord('s'):

    cv2.imwrite('mask.png', mask)
    print('save mask.png')

    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    dst_path = '%s_erodedMask_%d.png' % (filename, size)
    cv2.imwrite(dst_path, erodedMask)
    print('save %s' % dst_path)

    dst_path = '%s_eroded_%d.png' % (filename, size)
    cv2.imwrite(dst_path, dst)
    print('save %s' % dst_path)

cv2.destroyAllWindows()
