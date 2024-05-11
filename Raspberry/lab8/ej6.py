from pixie import Camara, img, showIMG, video, videosPlays


if __name__ == "__main__":
    camara=Camara(0)
    camara.videoCanny(img,0,130,7,7)
