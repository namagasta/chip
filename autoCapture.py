from __future__ import print_function
import cv2
import numpy
import io
import time
import picamera
import os 

class autoCap:

        stream = io.BytesIO()
        cam = picamera.PiCamera()
        vidNum_full = str(time.time())
        vidNum = vidNum_full[:10]
        vidNum = vidNum[2:]
        w,h = 800,600
        center = (w/2, h/2)        
        
        folderNum = vidNum
        filePrep = '../hold/%s/' % folderNum

        num = 0
        seriesNum = 0
        seriesReset = 0

        #master frame
        master = None

        if not os.path.isdir(filePrep):
                os.makedirs(filePrep)

        if not os.path.isdir(filePrep + 'images%s' % seriesNum):
                os.makedirs(filePrep + 'images%s' % seriesNum)
        
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
                
                self.seriesReset = self.seriesReset + 1
                #print('Reset:',self.seriesReset)

                if self.seriesReset == 1000:
                        print('Series:', self.seriesNum)
                        self.seriesReset = 0
                        self.seriesNum = self.seriesNum + 1
                        if not os.path.isdir(self.filePrep + 'images%s' % self.seriesNum):
                                os.makedirs(self.filePrep + 'images%s' % self.seriesNum)

                # rotate the image by 180 degrees
                piv = cv2.getRotationMatrix2D(self.center, 180, 1.0)
                dst = cv2.warpAffine(dst, piv, (self.w, self.h))
                self.dst = dst
                imagePrep = '../hold/%s/' %self.folderNum + 'images%s/' %self.seriesNum
                imageSave = imagePrep + 'dst_%s.jpeg' %self.num
                print('Frame:', imageSave)
                cv2.imwrite(imageSave, dst)
                self.num = self.num + 1

        #def target(self, TARGET, x_tar, y_tar):
        def target(self):
        
                self.cam.capture(self.stream, use_video_port=True, format='jpeg')
                self.stream.seek(0)
                data = numpy.fromstring(self.stream.getvalue(), dtype=numpy.uint8)

                frame0 = cv2.imdecode(data, 1)
                piv = cv2.getRotationMatrix2D(self.center, 180, 1.0)
                frame0 = cv2.warpAffine(frame0, piv, (self.w, self.h))

                # gray frame
                frame1 = cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)

                # blur frame
                frame2 = cv2.GaussianBlur(frame1,(21,21),0)
                
                #master = frame2
                                
                # initialize master
                if self.master is None:
                        self.master = frame2
                        #continue

                # delta frame
                frame3 = cv2.absdiff(self.master,frame2)

                # threshold frame
                frame4 = cv2.threshold(frame3,15,255,cv2.THRESH_BINARY)[1]

                # dilate the thresholded image to fill in holes
                kernel = numpy.ones((5,5),numpy.uint8)
                frame5 = cv2.dilate(frame4,kernel,iterations=4)

                # find contours on thresholded image
                contours,_ = cv2.findContours(frame5.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                # make coutour frame
                frame6 = frame0.copy()

                # target contours
                targets = []

                count = 0

                # loop over the contours
                for c in contours:
                        count = count + 1
                        area = cv2.contourArea(c)
                        
                        #print('Option',count,':',area)
                        
                        # if the contour is too small, ignore it
                        if area < 500:
                                #print('Rejected:', area)
                                continue

                        # contour data
                        M = cv2.moments(c)#;print( M )
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        x,y,w2,h2 = cv2.boundingRect(c)
                        rx = x+int(w2/2)
                        ry = y+int(h2/2)
                        ca = cv2.contourArea(c)

                        # plot contours
                        cv2.drawContours(frame6,[c],0,(0,0,255),2)
                        cv2.rectangle(frame6,(x,y),(x+w2,y+h2),(0,255,0),2)
                        cv2.circle(frame6,(cx,cy),2,(0,0,255),2)
                        cv2.circle(frame6,(rx,ry),2,(0,255,0),2)

                        # save target contours
                        targets.append((rx,ry,ca))

                # make target
                area = sum([x[2] for x in targets])
                mx = 0
                my = 0
            
                if targets:
                        for x,y,a in targets:
                                mx += x
                                my += y
                        mx = int(round(mx/len(targets),0))
                        my = int(round(my/len(targets),0))

                # plot target
                tr = 50
                frame7 = frame0.copy()
            
                if targets:
                        cv2.circle(frame7,(mx,my),tr,(0,0,255,0),2)
                        cv2.line(frame7,(mx-tr,my),(mx+tr,my),(0,0,255,0),2)
                        cv2.line(frame7,(mx,my-tr),(mx,my+tr),(0,0,255,0),2)
            
                # update master
                self.master = frame2
                self.frame = frame7
                self.area_tar = area
                self.x_tar = mx
                self.y_tar = my
                
#SETUP
scanSize = autoCap(autoCap.w, autoCap.h)
#trigger = scanSize.snap('../hold/dst.jpeg')
#targetMay = scanSize.target()
#target = frame7
