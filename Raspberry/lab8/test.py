from pixie import img, showIMG
import cv2



'''
trafic= img("Raspberry/lab8/images/city.png","RGB")

trafic.resize_img(1000,700,0)

trafic.draw(1,0)
trafic.showIMG()

#showIMG([trafic.apply_otsu_threshold(255)])
'''
'''


trafic= img("Raspberry/lab8/images/city.png","RGB")
trafic.showIMG()
trafic.resize_img(900,600,0)
trafic.showIMG()


contours=trafic.Cannycontours(60,130,1,1,1)
showIMG([contours,trafic.retorno()])

imagenContours=img(contours,"RGB")
imagenContours.showIMG()

Dilate=imagenContours.apply_dilation(1,1,1)

ImgDilate=img(Dilate,"RGB")

Erosion=ImgDilate.apply_erosion(1,1,1)
showIMG([Erosion,Dilate])

'''

conejo=img("Raspberry/lab8/images/conejo2.jpg","RGB")
conejo.showIMG()
conejo.convIMGgray(0)
conejo.showIMG()
conejo.resize_img(500,500,0)
conejo.showIMG()
conejo.rotate_image(95,0)
conejo.showIMG()
conejo.save('x')
#conejo.save(0)
conejo.rotate_image(-45,0)
conejo.resize_img(600,600,0)
conejoIzq,conejoDer,_,_=conejo.cutHalves()
showIMG([conejoIzq,conejoDer])

conejo2=img(conejo.retorno(),"RGB")
m1,m2,m3,m4=conejo2.cutHalves()

showIMG([m1,m2,m3,m4])

q1,q2,q3,q4=conejo2.cutQ()
showIMG([q1,q2,q3,q4])

