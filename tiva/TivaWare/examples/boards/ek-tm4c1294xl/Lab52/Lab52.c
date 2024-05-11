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
char data[2];
int entero=1;
int main(void)
{

    //volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER0_BASE, TIMER_A);
    IntMasterEnable();
   

    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);



    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);

    GPIOPinTypeUART(GPIO_PORTA_BASE,0x03);


    

    

    UARTStdioConfig(0,9600,120000000);
    //char msg[]="osita\n";
    

    

    //GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);
    //GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x11);
    
    while(1)
   {
    
    //if(UARTCharsAvail(0)>0){
    //UARTgetc();
    //data=UARTCharGet(0);
    UARTgets(data,2);
    //strcat(data,"\n");
    //UARTprintf(data);
    //}
    entero = (int) strtol(data, NULL, 2);
        
    }
}


void timer0A_handler(void)
{
    
    TimerIntClear(TIMER0_BASE, TIMER_A);
    volatile uint32_t ui32Loop;
    //volatile uint32_t ui32Loop;
    //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
    //GPIOPinWrite(GPIO_PORTF_BASE, 0x017, 0x11);
    GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
    GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x01);
    

    for(ui32Loop = 0; ui32Loop < 1000000+(1000000*entero); ui32Loop++)
    {
    }

    GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x02);
    GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x010);

    
    for(ui32Loop = 0; ui32Loop < 1000000+(1000000*entero); ui32Loop++)
    {
    }
    GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x0);
    GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x0);

    
    for(ui32Loop = 0; ui32Loop < 1000000+(1000000*entero); ui32Loop++)
    {
    }
    GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x0);
    GPIOPinWrite(GPIO_PORTF_BASE, 0x11,0x0);
    for(ui32Loop = 0; ui32Loop < 1000000+(1000000*entero); ui32Loop++)
    {
    }
    state++;
}





