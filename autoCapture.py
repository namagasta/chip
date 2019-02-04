import cv2
import numpy
import io
import time
import picamera
import os 

class autoCap:

        stream = io.BytesIO()
        cam = picamera.PiCamera()
        vidNum = str(time.time())
        vidNum = vidNum[:10]
        vidNum = vidNum[2:]
        w,h = 640,480
        center = (w/2, h/2)        
        
        folderNum = vidNum
        filePrep = '../hold/%s/' % folderNum

        num = 0
        seriesNum = 0

        if not os.path.isdir(filePrep):
                os.makedirs(filePrep)

        if not os.path.isdir(filePrep + 'images'):
                os.makedirs(filePrep + 'images')

##        if not os.path.isdir(filePrep + 'images%s'% seriesNum):
##                os.makedirs(filePrep + 'images%s' % seriesNum)                
        
        def __init__(self, w, h):
                
                #h,w = self.WIDTH, self.HEIGHT
                self.WIDTH = w
                self.HEIGHT = h
                size = (w, h)
                self.cam.resolution = size
                
        def snap(self,DST):
                
                self.cam.capture(self.stream, use_video_port=True, format='jpeg')
                self.stream.seek(0)
                data = numpy.fromstring(self.stream.getvalue(), dtype=numpy.uint8)
                dst = cv2.imdecode(data, 1)
                self.TEMPIMAGE = DST
                cv2.imwrite(self.TEMPIMAGE, dst)
                dst = cv2.imread(self.TEMPIMAGE)

                # rotate the image by 180 degrees
                piv = cv2.getRotationMatrix2D(self.center, 180, 1.0)
                dst = cv2.warpAffine(dst, piv, (self.w, self.h))

                imagePrep = '../hold/%s/images/' %self.folderNum
                imageSave = imagePrep + 'dst.%s.jpeg' %self.num
                cv2.imwrite(imageSave, dst)
                self.num = self.num + 1
                print('Frame Number:', self.num)

#SETUP
scanSize = autoCap(640,480)
trigger = scanSize.snap('../hold/dst.jpeg')

#CHECK
print(type(trigger))
