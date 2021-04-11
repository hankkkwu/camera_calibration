import cv2
import os

"""
For cut the image in half, so it will seperate the left and right image from left and right camera
""" 
 
# Global variables preset
total_photos = 20
img_height = 360
img_width = int(640 / 2)
photo_counter = 0 


# Main pair cut cycle
if (os.path.isdir("./pairs")==False):
    os.makedirs("./pairs")
while photo_counter != total_photos:
    
    filename = './captured_images/img'+str(photo_counter) + '.jpg'
    if os.path.isfile(filename) == False:
        print ("No file named "+filename)
        continue
    pair_img = cv2.imread(filename,-1)
  
    photo_counter +=1
    #cv2.imshow("ImagePair", pair_img)
    #cv2.waitKey(0)
    imgLeft = pair_img [0:img_height,0:img_width] #Y+H and X+W
    imgRight = pair_img [0:img_height,img_width:]
    leftName = './pairs/left_'+str(photo_counter).zfill(2)+'.jpg'
    rightName = './pairs/right_'+str(photo_counter).zfill(2)+'.jpg'
    cv2.imwrite(leftName, imgLeft)
    cv2.imwrite(rightName, imgRight)
    print ('Pair No '+str(photo_counter)+' saved.')
    
print ('End cycle')
