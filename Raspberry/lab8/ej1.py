from pixie import img, showIMG, video, videosPlays

if __name__ == "__main__":
    video1=video()
    video1.load("Raspberry/lab8/videos/Sunset.mp4")


    '''video1.videoPlay()
    #video1.rotate(45,0)
    video1.resize(400,600,0)
    video1.videoPlay()
    video1.canny(50,140,1,1,0)
    video1.videoPlay()

    #video1.videoPlay()'''
    
    h1,h2,h3,h4 = video1.halves(1) # type: ignore
    videosPlays(video1,[h1,h2])

   # c1,c2,c3,c4 = video1.quadrants(1) # type: ignore
   # videosPlays(video1,[c1,c2,c3,c4])