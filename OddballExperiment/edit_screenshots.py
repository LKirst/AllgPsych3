
from PIL import Image
import os


def openImg(fps = ['stimuli1.png', 'stimuli2.png', 'stimuli3.png'], dir = 'testdata'):
    
    imgList = []
    for i, fp in enumerate(fps):
        imgList.append(Image.open(dir + os.sep + fp))
    
    return(imgList)


def cropImg(imgs, cropW = 500, cropH = 300):
    
    # crop the images (remove empty room around the stimulus)
    
    
    for i, img in enumerate(imgs):
        
        w, h = img.size
        
        imgs[i] = img.crop(box = (cropW, cropH, w-cropW, h-cropH)) # The box is (x, y, width, height)
    
    return(imgs)


def frameImg(imgs):
    
    for i, img in enumerate(imgs):
        # create a black image 10% bigger than the old one
        biggerSize = (round(img.size[0]*1.1), round(img.size[1]*1.1))
        blackImg = Image.new('RGB', biggerSize)
        
        # paste the img in the bigger, black img
        blackImg.paste(img, ((biggerSize[0]-img.size[0])//2,
                             (biggerSize[1]-img.size[1])//2))
        
        imgs[i] = blackImg
    
    return(imgs)
    


def saveImg(imgs):
    
    for i, img in enumerate(imgs):
        img.save(fp = 'testdata/stimuli_cropped{}.png'.format(i))
        


imgs_raw = openImg()

imgs_crop = cropImg(imgs_raw, cropW = 600)

imgs_frame = frameImg(imgs_crop)

saveImg(imgs_frame)



