import cv2
import numpy
from abc import ABC, abstractmethod

import numpy as np


class img_abs(ABC):

    '''
    @abstractmethod
    def readIMG(self):
        pass
    '''
    
    @abstractmethod
    def showIMG(self):
        pass
    
    @abstractmethod
    def resize_img(self):
        pass
    
    @abstractmethod
    def rotate_image(self):
        pass
    
    @abstractmethod
    def cutHalves(self):
        pass

    @abstractmethod
    def cutQ(self):
        pass

    @abstractmethod
    def convIMGgray(self):
        pass

    @abstractmethod
    def convIMGhsv(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def retorno(self):
        pass
    
    @abstractmethod
    def Cannycontours(self):
        pass
    
    @abstractmethod
    def apply_binary_threshold(self):
        pass

    @abstractmethod
    def apply_otsu_threshold(self):
        pass

    @abstractmethod
    def apply_inverse_binary_threshold(self):
        pass

    @abstractmethod
    def apply_truncated_threshold(self):
        pass

    @abstractmethod
    def apply_tozero_threshold(self):
        pass


    @abstractmethod
    def apply_inverse_tozero_threshold(self):
        pass

    @abstractmethod
    def apply_erosion(self):
        pass

    @abstractmethod
    def apply_dilation(self):
        pass

    @abstractmethod
    def draw(self):
        pass




class img(img_abs):
    def __init__(self,image,tipo) -> None:
        self.contador_imagenes=0
        if type(image)==str:
            #imagen="/imagenes/perrito1.png"
            self.imagen = cv2.imread(image)
            self.imagen=self.tipos(self.imagen,tipo)
            print("dir!")
        #print("OriginalSize",img.shape)
        elif type(image)==numpy.ndarray:
            print("np!")
            self.imagen=self.tipos(image,tipo)


    def tipos(self,img,tipo):
        
        if(tipo=="BGR"):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # type: ignore
        elif(tipo=="HSV"):
            img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB) # type: ignore
        elif(tipo=="RGB"):
            pass
        return img
    
    def showIMG(self):
        cv2.imshow('showed Instance',self.imagen) # type: ignore
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    


    def resize_img(self,width, height,retorno):
        up_points = (width, height)
        img_resize = cv2.resize(self.imagen, up_points) # type: ignore
        print("NewSize",img_resize.shape)
        if(retorno==1):
            return img_resize
        else:
            self.imagen=img_resize
        

    
    def rotate_image(self, degrees,retorno):
        height, width = self.imagen.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, degrees, 1.0)
        rotated_image = cv2.warpAffine(self.imagen, rotation_matrix, (width, height))
        if(retorno==1):
            return rotated_image
        else:
            self.imagen=rotated_image
        

    def cutHalves(self):
        resized_image=self.imagen.copy()
        height, width = resized_image.shape[:2]
        half_height = height // 2
        upper_half = resized_image[:half_height, :]
        lower_half = resized_image[half_height:, :]

        half_width = width // 2
        left_half = resized_image[:, :half_width]
        right_half = resized_image[:, half_width:]
        
        return left_half,right_half,upper_half,lower_half
    
    def cutQ(self):
        # Divide the image into quadrants
        image=self.imagen.copy()
        height, width = image.shape
        quadrant1 = image[:height // 2, :width // 2]
        quadrant2 = image[:height // 2, width // 2:]
        quadrant3 = image[height // 2:, :width // 2]
        quadrant4 = image[height // 2:, width // 2:]


        return quadrant1,quadrant2,quadrant3,quadrant4
        #return super().cutQ()


    def convIMGgray(self,retorno):
        img = cv2.cvtColor(self.imagen, cv2.COLOR_RGB2GRAY)
        
        if retorno==1:
            return img
        else:
            self.imagen=img
        

    def convIMGhsv(self,retorno):
        img = cv2.cvtColor(self.imagen, cv2.COLOR_RGB2HSV)
        if retorno==1:
            return img
        else:
            self.imagen=img
        
    
    def save(self,key,key2):
        if type(key)==str:
            while(1):
                cv2.imshow("save?",self.imagen)
                if cv2.waitKey(0) & 0xFF == ord(key):
                    ruta_imagen = f'Raspberry/lab8/Saves/image{self.contador_imagenes}.jpg'
                    cv2.imwrite(ruta_imagen, self.imagen)
                    print(f"Imagen guardada en {ruta_imagen}")
                    self.contador_imagenes += 1
                    cv2.destroyAllWindows()
                    break
                elif cv2.waitKey(0) & 0xFF == ord(key2):
                    print("Guardado cancelado")
                    cv2.destroyAllWindows()
                    break
                else:
                    print("No key")

        elif(key==0):
            ruta_imagen = f'Raspberry/lab8/Saves/image{self.contador_imagenes}.jpg'
            cv2.imwrite(ruta_imagen, self.imagen)
            print(f"Imagen guardada en {ruta_imagen}")
            self.contador_imagenes += 1

    def retorno(self):
        return self.imagen
    
    def Cannycontours(self,u1,u2,b1,b2,retorno):
        img=self.convIMGgray(1)
        img = cv2.GaussianBlur(self.imagen,(b1,b2),0)
        Canny = cv2.Canny(img, u1, u2)

        if retorno==1:
            return Canny
        else:
            self.imagen= Canny
    
    def apply_binary_threshold(self, threshold_value,retorno):
        _, binary_threshold = cv2.threshold(self.imagen, threshold_value, 255, cv2.THRESH_BINARY)
        if retorno==1:
            return binary_threshold
        else:
            
            self.imagen=binary_threshold


    
    def apply_otsu_threshold(self, threshold_value,retorno):
        _, otsu_threshold = cv2.threshold(self.imagen, threshold_value, 255, cv2.THRESH_OTSU)
        if retorno==1:
            return otsu_threshold
        else:
            self.imagen=otsu_threshold

    def apply_inverse_binary_threshold(self, threshold_value,retorno):
        _, inverse_binary_threshold = cv2.threshold(self.imagen, threshold_value, 255, cv2.THRESH_BINARY_INV)
        if retorno==1:
            return inverse_binary_threshold
        else:
            self.imagen=inverse_binary_threshold

    def apply_truncated_threshold(self, threshold_value,retorno):
        _, truncated_threshold = cv2.threshold(self.imagen, threshold_value, 255, cv2.THRESH_TRUNC)
        if retorno==1:
            return truncated_threshold
        else:
            self.imagen=truncated_threshold

    def apply_tozero_threshold(self, threshold_value,retorno):
        _, tozero_threshold = cv2.threshold(self.imagen, threshold_value, 255, cv2.THRESH_TOZERO)
        if retorno==1:
            return tozero_threshold
        else:
            self.imagen=tozero_threshold

    def apply_inverse_tozero_threshold(self, threshold_value,retorno):
        _, inverse_tozero_threshold = cv2.threshold(self.imagen, threshold_value, 255, cv2.THRESH_TOZERO_INV)
        if retorno==1:
            return inverse_tozero_threshold
        else:
            self.imagen=inverse_tozero_threshold

    def apply_erosion(self, threshold_value, erosion_iterations,retorno):
        binary_threshold = self.apply_binary_threshold(threshold_value,1) # type: ignore
        kernel = np.ones((2, 2), np.uint8)
        erosion = cv2.erode(binary_threshold, kernel, iterations=erosion_iterations) # type: ignore
        if retorno==1:
            return erosion
        else:
            self.imagen=erosion

    def apply_dilation(self, threshold_value, dilation_iterations,retorno):
        binary_threshold = self.apply_binary_threshold(threshold_value,1) # type: ignore
        kernel = np.ones((2, 2), np.uint8)
        dilation = cv2.dilate(binary_threshold, kernel, iterations=dilation_iterations)
        if retorno==1:
            return dilation
        else:
            self.imagen=dilation
    

    def draw(self,val,retorno):
        contour_image = self.imagen.copy()
        gray=self.convIMGgray(1)
        _, thresholding=cv2.threshold(gray, val, 255, cv2.THRESH_OTSU) # type: ignore
        contours, _ = cv2.findContours(thresholding, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(contour_image, contours, -1, (0, 0, 255), 1)
        if retorno==1:
            return contour_image,contours
        else:
            self.imagen=contour_image



def showIMG(imagenes):
    c=0
    for x in imagenes:
        cv2.imshow(str(c),x) # type: ignore
        c=c+1
    cv2.waitKey(0)
    cv2.destroyAllWindows()