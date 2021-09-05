from grabscreen import grab_screen
from cs_model import load_model
from utils.general import non_max_suppression,scale_coords,xyxy2xywh
from utils.augmentations import letterbox
from mouse_control import lock
import cv2
import win32gui
import win32con
import torch
import  numpy as np
import  pynput
device = 'cuda' if torch.cuda.is_available() else 'cpu'
half = device!='cpu'
imgsz= 640
conf_thres= 0.5
iou_thres= 0.05

x,y=(1920,1080)
re_x,re_y=(1920,1080)


model=load_model()
stride = int(model.stride.max())
names = model.module.names if hasattr(model, 'module') else model.names

lock_mode = False
mouse=pynput.mouse.Controller()

with pynput.mouse.Events() as events:
    while True:
        it = next(events)
        while it is not None and not isinstance(it, pynput.mouse.Events.Click):
            it = next(events)
        if it is not None and it.button==it.button.x2 and it.pressed:
            lock_mode=not lock_mode
            print('锁人模式，','开启！' if lock_mode else '关闭！')


        img0 = grab_screen(region=(0,0,x,y))
        img0= cv2.resize(img0,(re_x,re_y))

        img = letterbox(img0, imgsz, stride=stride)[0]
        img = img.transpose((2, 0, 1))[::-1]# HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)


        img= torch.from_numpy(img).to(device)
        img=img.half() if half else img.float()
        img/= 255.
        if len(img.shape)==3:
            img=img[None]
        pred = model(img, augment=False, visualize=False)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres,agnostic=False)


        aims=[]
        for i, det in enumerate(pred):  # detections per image
            s=''
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                for *xyxy, conf, cls in reversed(det):
                    """""
                    0 ct_head
                    1 ct_body
                    2 t_head
                    3 t_body
                    """""

                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    line = (cls, *xywh)  # label format
                    aim = ('%g ' * len(line)).rstrip() %line
                    aim=aim.split(' ')
                    #print(aim)
                    aims.append(aim)


            if len(aims):
                if lock_mode:
                    lock(aims,mouse,x,y)#开锁！！！！
                for i, det in enumerate(aims):
                    _, x_center, y_center, width, height = det
                    x_center,width=re_x * float(x_center),re_x * float(width)
                    y_center,height=re_y * float(y_center),re_y * float(height)
                    top_left= (int(x_center - width/2.),int(y_center- height/2.))
                    bottom_right=(int(x_center + width/2.),int(y_center+ height/2.))#cv2不支持浮点数
                    color=(0,255,0)
                    cv2.rectangle(img0, top_left, bottom_right, color,thickness=4)#显示框


        #实时监控画面实现
        cv2.namedWindow('csgo-detect',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('csgo-detect',re_x // 3,re_y // 3 )#缩小屏幕
        cv2.imshow('csgo-detect', img0)#显示窗口

        hwnd = win32gui.FindWindow(None,'csgo-detect')
        CVRECT = cv2.getWindowImageRect('csgo-detect')
        win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)#传不定常参数方法，将两者都传递

       #显示窗口1/3，按1退出
        if cv2.waitKey(1) & 0xFF ==ord('1'):
            cv2.destroyAllWindows()
            break