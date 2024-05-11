#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"

#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "inc/hw_ints.h"

//Interrupciones

#include "driverlib/interrupt.h"
#include "driverlib/timer.h"
#include "inc/tm4c1294ncpdt.h"

//uart
#include "driverlib/uart.h"
#include "utils/uartstdio.c"
#include "string.h"

#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif


void timer0A_handler(void);
void timer1A_handler(void);
int state=0;
int state2=0;
uint32_t FS = 120000000/900; //frecuencia del timer
uint32_t FS2 = 120000000/1500;
int flag=0;
int flag2=0;
char data[7];

int main(void)
{

    //volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock
    //habilitacion de pines
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOQ);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    //configuracion timer 0
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER0_BASE, TIMER_A);
    IntMasterEnable();


    //configuracion timer 1
    TimerConfigure(TIMER1_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER1_BASE, TIMER_A, FS2);
    IntEnable(INT_TIMER1A);
    TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER1_BASE, TIMER_A);
    IntMasterEnable();
   

    // Configuracion del pin uart
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);

    GPIOPinTypeUART(GPIO_PORTA_BASE,0x03);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }
    

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    // configuracion uart
    UARTStdioConfig(0,9600,120000000);
    //char msg[]="osita\n";
    
    //configuracion botones 2
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);
    // configuracion buzzer
    GPIOPinTypeGPIOOutput(GPIO_PORTQ_BASE,0X01);
    
    while(1)
   {
        UARTgets(data,7);
    
        
        if(strcmp(data, "buzzer")==0){//ard.write('1'.encode())
            flag2=1;
            UARTprintf("Ok!\n");
        }
        else{
            
            flag2=0;
        }
        }
    }


void timer0A_handler(void)
{
    
   TimerIntClear(TIMER0_BASE, TIMER_A);
    if(flag==1)
    {


         if(state <=1){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
            GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x01);
            
        }
        
        else if(state>2){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
            GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x00);
            state=0;
            
        }




    }
else{
        GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
        GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x00);
    }
}


void timer1A_handler(void){ 
   TimerIntClear(TIMER1_BASE, TIMER_A);
   if(flag2==1)
   {
    if(state2 ==1){
            flag=1;
            state2=0;
            
        }
        
        else{
            flag=0;
            state2++;
            
        }
   }
   else{
    flag=0;
   }

}




