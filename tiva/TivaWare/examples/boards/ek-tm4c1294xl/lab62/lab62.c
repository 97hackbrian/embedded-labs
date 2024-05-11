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
int state=0;
uint32_t FS = 120000000/1; //frecuencia del timer
int flag=0;
char data[10];

int main(void)
{

    //volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock
    //habilitacion de pines
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    //configuracion timer
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER0_BASE, TIMER_A);
    IntMasterEnable();
   

    // Configuracion del pin uart
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);

    GPIOPinTypeUART(GPIO_PORTA_BASE,0x03);

  
    

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x11);
    // configuracion uart
    UARTStdioConfig(0,9600,120000000);
    //char msg[]="osita\n";
    
    //configuracion botones 2
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);
    // configuracion buzzer
    
    
    while(1){

        UARTgets(data,10);
        if(strcmp(data,"1")==0){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
            GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x00);
        }
        else if (strcmp(data,"2")==0)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x02);
            GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x00);
        }
        else if(strcmp(data,"3")==0){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
            GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x00);
        }
        else if (strcmp(data,"4")==0)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
            GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x10);
        }
        else if (strcmp(data,"5")==0){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
            GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x11);
        }
        

        
        
}
}

void timer0A_handler(void)
{
    
   TimerIntClear(TIMER0_BASE, TIMER_A);
   
   
}





