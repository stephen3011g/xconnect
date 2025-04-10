import cv2
import numpy as np
import time

def board_capture():
    cam_port =0
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()
    image = cv2.resize(image, (960,560))
    crop = image[10:500, 240:720]
    cv2.imwrite('/home/pcblab/Downloads/tictactoe_old_doc/FYP/alpha_image.png', crop)
    return crop
def shape_detect(shape):
    shape_locations=[]
    board_capture()
    xo_table = cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/FYP/alpha_image.png')
    if shape=='CIRCLE':
        computer='TRIANGLE'
        image0=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/Designer3.png')
        image2=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/Designer5.png')
        image3=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/Designer6.png')
        image4=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/Designer7.png')
        image5=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/Designercic1.png')
        image6=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/Designercic2.png')
        images=[image0,image2,image3,image4,image5,image6]
        print("POGTHU")
    elif shape=='TRIANGLE':
        computer='CIRCLE'
        image0=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/alpha_traingle5.png')
        image2=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/alpha_triangle6.png')
        image3=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/alpha_triangle7.png')
        image4=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/alpha_triangle8.png')
        image5=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/alpha_triangle9.png')
        image7=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/alpha_triangle10.png')
        image8=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/alpha_triangle11.png')
        image6=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/Designercrosstriangle.png')
        imageA=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/FYP/triangle_temp.png')
        image9=cv2.imread(r'/home/pcblab/Downloads/tictactoe_old_doc/FYP/triangle2_temp.png')
        images=[image0,image2,image3,image4,image5,image6,image7,image8,imageA,image9]
    for image in images:
        result=cv2.matchTemplate(xo_table,image,cv2.TM_CCOEFF_NORMED)
        threshold=0.78
        locations=np.where(result>=threshold)
        locations=list(zip(*locations[::-1]))
        wtemp=image.shape[1]
        htemp=image.shape[0]
        for loc in locations:
            mid_pt = ((loc[0] + wtemp // 2), (loc[1] + htemp // 2))

            if (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                if 1 not in shape_locations:
                    shape_locations.append(1)
            elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                if 2 not in shape_locations:
                    shape_locations.append(2)
            elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                if 3 not in shape_locations:
                    shape_locations.append(3)
            elif (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                if 4 not in shape_locations:
                    shape_locations.append(4)
            elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                if 5 not in shape_locations:
                    shape_locations.append(5)
            elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                if 6 not in shape_locations:
                    shape_locations.append(6)
            elif (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                if 7 not in shape_locations:
                    shape_locations.append(7)
            elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                if 8 not in shape_locations:
                    shape_locations.append(8)
            elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                if 9 not in shape_locations:
                    shape_locations.append(9)
    return shape_locations
print("circles",shape_detect('CIRCLE'))

print("triangles",shape_detect('TRIANGLE'))
