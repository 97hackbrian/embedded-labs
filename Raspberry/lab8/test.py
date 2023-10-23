from pixie import img, showIMG
import cv2


trafic= img("Raspberry/lab8/images/city.png","RGB")
trafic.showIMG()
trafic.resize_img(900,600)
trafic.showIMG()
contours=trafic.contours(60,130,1,1)
showIMG([contours,trafic.retorno()])
'''

conejo=img("Raspberry/lab8/images/conejo2.jpg","RGB")
conejo.showIMG()
conejo.convIMGgray()
conejo.showIMG()
conejo.resize_img(500,500)
conejo.showIMG()
conejo.rotate_image(95)
conejo.showIMG()
conejo.save('x')
#conejo.save(0)
conejo.rotate_image(-45)
conejo.resize_img(600,600)
conejoIzq,conejoDer,_,_=conejo.cutHalves()
showIMG([conejoIzq,conejoDer])

conejo2=img(conejo.retorno(),"RGB")
m1,m2,m3,m4=conejo2.cutHalves()

showIMG([m1,m2,m3,m4])



q1,q2,q3,q4=conejo2.cutQ()
showIMG([q1,q2,q3,q4])

'''