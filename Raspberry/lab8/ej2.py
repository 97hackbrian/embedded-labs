from pixie import Camara, img, showIMG, video, videosPlays


if __name__ == "__main__":
    camara1=Camara(0)
    #camara1.change_to_color_channel(channel='Red')
    #camara1.videoPlay()
    #camara1.videoColor(img,"HSV",3)
    camara1.saveCameracapture(img,0,0)
    #camara1.videoRotate(img,45,"GRAY")