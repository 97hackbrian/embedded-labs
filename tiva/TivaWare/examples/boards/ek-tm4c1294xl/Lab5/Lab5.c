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
uint32_t FS = 120000000/400; //frecuencia del timer
int flag=0;
char data[7];

int main(void)
{

    volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER0_BASE, TIMER_A);
    IntMasterEnable();
   

    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOQ);

    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);

    GPIOPinTypeUART(GPIO_PORTA_BASE,0x03);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }
    

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);

    UARTStdioConfig(0,9600,120000000);
    //char msg[]="osita\n";
    

    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);

    GPIOPinTypeGPIOOutput(GPIO_PORTQ_BASE,0X01);
    
    while(1)
   {
    if(GPIOPinRead(GPIO_PORTJ_BASE,0x01)==0){
        UARTprintf("motor1\n");    
    }
    else if(GPIOPinRead(GPIO_PORTJ_BASE,0x02)==0){
        UARTprintf("motor2\n");    
    }
    else{
        UARTprintf("notpressed\n");
    }
    
    //if(UARTCharsAvail(0)>0){
    //UARTgetc();
    //data=UARTCharGet(0);
    UARTgets(data,7);
    //strcat(data,"\n");
    //UARTprintf(data);
    //}
    
    if(strcmp(data, "buzzer")==0){//ard.write('1'.encode())
        flag=1;
        for(ui32Loop = 0; ui32Loop < 10000000; ui32Loop++)
        {
        }
        //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
        UARTprintf("Ok!\n");
    }
    else{
        //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
        flag=0;
    }
    
    
    /*
    UARTprintf(msg);
    UARTgets(data,10);
    strcat(data,"\n");
    UARTprintf(data);
    */
    }
}


void timer0A_handler(void)
{
    
   TimerIntClear(TIMER0_BASE, TIMER_A);
    if(flag==1)
    {
        
        //for (int i = 0; i < 200; i++)
        //{
        if(state <=1){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
            GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x01);
            
        }
        
        else if(state>2){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
            GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x00);
            state=0;
            
        }
        /*
        if(state==4){
            state=0;
        }*/
        state++;

    //} 
    
    /*
    while (1){
	TimerIntClear(TIMER0_BASE, TIMER_A);
    
    UARTgets(data,20);
    if(data=="buzzer"){//ard.write('1'.encode())
        flag=1;
        UARTprintf("Ok!\n");
    }
    else{
        flag=0;
    }

	if(flag==1)
    {
        for (size_t i = 0; i < 3; i++)
        {
        if(state <=2){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
            GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x01);
            
        }
        
        else if(state>2){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
            GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x00);
            
        }
        if(state==4){
            state=0;
        }
        
        state++;
        }

        UARTprintf("Ok!\n");
    }
    else{
        GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
        GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x00);
    }

}
*/
}
else{
        GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
        GPIOPinWrite(GPIO_PORTQ_BASE, 0x01, 0x00);
    }
}





