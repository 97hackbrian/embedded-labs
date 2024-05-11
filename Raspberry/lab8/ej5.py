from pixie import Camara, img, showIMG, video, videosPlays


if __name__ == "__main__":
    trafic= img("Raspberry/lab8/images/city.png","RGB")

    trafic.resize_img(1000,700,0)
    trafic.draw(1,0)
    trafic.showIMG()
