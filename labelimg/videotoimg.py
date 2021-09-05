import cv2
def save_image(addr,image,num):
    address=addr+'img_'+str(num)+'.jpg'
    print(address)
    cv2.imwrite(address,image)
    #命名函数
video_path=r'D:\yolov5\labelimg\video\sbww.mp4'
out_path='D:/yolov5/labelimg/images/'
is_all_frame= True #是否需要取所有帧
sta_frame=1 #起始帧
end_frame=1000 #结束帧
time_interval = 8 #时间间隔
videocapture = cv2.VideoCapture(video_path)
success, frame=videocapture.read()
#print(success)
i=0
j=0
while success:
    i +=1
    if i % time_interval==0:
        if not is_all_frame:
            if sta_frame <= i<= end_frame:
                j +=1
                print('save frame',j)
                save_image(out_path,frame,j)
            elif i>end_frame:
                break
        else:
                j +=1
                print('save frame',j)
                save_image(out_path,frame,j)

    success,frame=videocapture.read()