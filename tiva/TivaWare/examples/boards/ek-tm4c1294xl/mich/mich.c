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



void timer1A_handler(void);
void GPIOJ_handler(void);
int state=0;
uint32_t FS = 120000000*1; //frecuencia del timer
int flag=0;
char data[2];
uint8_t switch_state = 0;
uint32_t button=0;
int count1=0;
int count2=0;


int main(void)
{

    //volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock
    //habilitacion de pines
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    //configuracion timer
    TimerConfigure(TIMER1_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER1_BASE, TIMER_A, FS);
    IntEnable(INT_TIMER1A);
    TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER1_BASE, TIMER_A);
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
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, 0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, 0x03, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    GPIOIntTypeSet(GPIO_PORTJ_BASE, 0x03, GPIO_FALLING_EDGE);
    //GPIOIntTypeSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_FALLING_EDGE);
    GPIOIntEnable(GPIO_PORTJ_BASE, 0x03);
    IntEnable(INT_GPIOJ);
    // configuracion buzzer
    
    while(1)
   {
    
    
    
    //if(UARTCharsAvail(0)>0){
    //UARTgetc();
    //data=UARTCharGet(0);
    
    //strcat(data,"\n");
    //UARTprintf(data);
    //}
    
    UARTgets(data,2);
    FS=120000000*((int) strtol(data, NULL, 10));
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    TimerConfigure(TIMER1_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER1_BASE, TIMER_A, FS);
    IntEnable(INT_TIMER1A);
    TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER1_BASE, TIMER_A);
    IntMasterEnable();
    
    
    
    
    /*
    UARTprintf(msg);
    UARTgets(data,10);
    strcat(data,"\n");
    UARTprintf(data);
    */
    }
}


void timer1A_handler(void){
    TimerIntClear(TIMER1_BASE, TIMER_A);
    if(flag==0)
    {
    
        if (count1==1){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
            count1 =0;
        }
        else{
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
            count1++;
        }    }

        
    else if (flag==1){
        if (count1==1){
            GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x11);
            count1 =0;
        }
        else{
            GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x00);
            count1++;
        }    }
    }



void GPIOJ_handler(void) {
    uint32_t status = GPIOIntStatus(GPIO_PORTJ_BASE, true);
    GPIOIntClear(GPIO_PORTJ_BASE, status);
/*
    if (status & GPIO_PIN_0) {


        
       
    }
  */  
    if(status & GPIO_PIN_1){
        
        if(flag==0){
            flag=1;
        }
        else{
            flag=0;
            
        }
        GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x00);
        GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
    }
    else{
        if(GPIOPinRead(GPIO_PORTJ_BASE,0x01)==0){
        UARTprintf("Turnon\n");    
    }
    
    }
}




