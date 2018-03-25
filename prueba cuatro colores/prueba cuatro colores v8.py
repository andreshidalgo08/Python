import cv2, sys, os, threading, time, pdb

pdb.set_trace()

def nothing(x):
    pass

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def esc():
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        cv2.destroyAllWindows()
        restart()

cv2.namedWindow('HSV')
cv2.createTrackbar('H min','HSV',0,180,nothing)
cv2.createTrackbar('H max','HSV',0,180,nothing)
cv2.createTrackbar('S min','HSV',0,255,nothing)
cv2.createTrackbar('S max','HSV',0,255,nothing)
cv2.createTrackbar('V min','HSV',0,255,nothing)
cv2.createTrackbar('V max','HSV',0,255,nothing)


task1 = threading.Thread(target=esc)
task1.start()

'''
while(1):
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

cv2.destroyAllWindows()
restart()
'''
