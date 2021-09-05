#锁起来了！！！
import pynput
def lock(aims,mouse,x,y):
    mouse_pos_x,mouse_pos_y = mouse.position
    dist_list=[]

    for det in aims:
        _, x_c, y_c, _, _ =det
        dist = (x * float(x_c)-mouse_pos_x) ** 2 +  (y*float(y_c) - mouse_pos_y) ** 2
        dist_list.append(dist)


    det = aims[dist_list.index(min(dist_list))] #索引最小值（移动到最近处）
    tag,x_center,y_center,width,height=det #数值是string type
    tag=int(tag)
    x_center,width=x*float(x_center),x*float(width)
    y_center, height = y * float(y_center), y * float(height)
    if tag==0 or tag==2:
        mouse.position=(x_center,y_center)
    elif tag ==1 or tag == 3:
        mouse.position= (x_center,y_center - 1/6 * height)