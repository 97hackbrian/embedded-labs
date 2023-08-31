//****************************************************************************
// Libreries default.
#include <stdio.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
//****************************************************************************

//Define corresponding sets of macros.
#include <stdint.h>

//*****************************************************************************
// The error routine that is called if the driver library encounters an error.
//****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif

//****************************************************************************
//Exercise 3. GPIO Tiva Exercise (Binary Counter)
//Using the 4 user LEDs and 2 user Switch integrated on Tiva develop a binary
//counter with all the values showed in table 1 following the next featues:

//• When switch 1 is pressed, binary counter increases.
//• When switch 2 is pressed, binary counter reduces.
//• All 4 user LEDs represent the binary values.
//• When counter reaches value 15 it shouldn’t keep increasing.
//• When counter goes to value 0 it shouldn’t keep decreasing.
//• Store the decimal value in an integer variable called “counter”.
//*****************************************************************************

int main(void)
{
  volatile uint32_t ui32Loop;
    //
    // Enable the GPIO port that is used for the on-board LED.
    // 
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    //
    // Check if the peripheral access is enabled.
    //
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }
    
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {
    }
    
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    {
    }
    
    //
    // enable the GPIO pin for digital function.
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x11);
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, 0x03);
    
    //
    // Loop forever.
    //
    
    //habilita las resistencias internas a 2mA
    GPIOPadConfigSet(GPIO_PORTJ_BASE, 0x03, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
    
    
    int counter=0;
    
    while(1)
    {
        
        //
        // Turn on the LED.
        //
        
	   if((uint8_t)GPIOPinRead(GPIO_PORTJ_BASE, 0x01)==0)
	   {
	   counter++;
	   }
	   else if ((uint8_t)GPIOPinRead(GPIO_PORTJ_BASE, 0x02)==0)
	   {
	   counter--;
	   }
	   
	   switch(counter){
	   
	   case 1:
	     
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x03,0x00);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0x00);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0xff);
	   break;
	   	   
	   case 2:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x03,0x00);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0x00);
	   break;
	   
	   case 3:
             GPIOPinWrite(GPIO_PORTN_BASE, 0x03,0x00);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0xff);
	   break;
	   
	   case 4:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0x00);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0xff);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0x00);
	   break;
	   
	   case 5:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0x00);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0xff);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0x00);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0xff);
	   break;
	   
	   case 6:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0x00);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0xff);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0x00);
	   break;
	   
	   case 7:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0x00);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0xff);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0xff);
	   break;
	   
	   case 8:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0xff);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0x00);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0x00);
	   break;
	   
	   case 9:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0xff);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0x00);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0x00);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0xff);
	   break;
	   
	   case 10:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0xff);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0x00);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0x00);
	   break;
	   
	   case 11:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x02,0xff);
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x01,0x00);  
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0xff);
	   break;
	   
	   case 12:
             GPIOPinWrite(GPIO_PORTN_BASE, 0x03,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0x00);
	   break;
	   
	   case 13:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x03,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0x00);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0xff);
	   break;
	   
	   case 14:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x03,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x10,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x01,0x00);
	   break;
	   
	   case 15:
	     GPIOPinWrite(GPIO_PORTN_BASE, 0x03,0xff);
	     GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0xff);
	   break;
	   }
	   
	   
	     if (counter>15) 
	     {
	     
	       counter=15;
	     }
	   
	   
	   
	     if (counter<0)
	     { 
	   	
	       counter=0;
	     
	       GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
	       GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x00);
	     }
	     
	   // GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0xf);
        //
        // Delay for a bit.
        //
        for(ui32Loop = 0; ui32Loop < 400000; ui32Loop++)
        {
        }
    }
}
