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

//pwm
#include "driverlib/pwm.h"
uint32_t reloj;
volatile uint32_t width;

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
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);//LED
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);//LED
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOG);//PG0 PWM
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);//UART
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);//BOTONES
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);//
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);//
    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);//PROBAR



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


    //GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE,0x0C);

  
    

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x15);

    GPIOPinTypeGPIOOutput(GPIO_PORTG_BASE, 0x01);//PG0 PWMB
    GPIOPinTypeGPIOOutput(GPIO_PORTK_BASE, 0xFF);//PK4,PK5,PK6,PK7

    // configuracion uart
    UARTStdioConfig(0,9600,120000000);
    //char msg[]="osita\n";
    
    //configuracion botones 2
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);
    // configuracion buzzer


    //pwm
    GPIOPinConfigure(GPIO_PF2_M0PWM2);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_2);

    PWMGenConfigure(PWM0_BASE,PWM_GEN_0,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_0,400);

    width=300;
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,width);

    PWMGenEnable(PWM0_BASE,PWM_GEN_0);    
    
    PWMOutputState(PWM0_BASE,(PWM_OUT_2_BIT),true);




    while(1){

        //UARTgets(data,10);
        width=200;
        GPIOPinWrite(GPIO_PORTK_BASE, 0xFF, 0x10);
        PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,width);

        /*
        SysCtlDelay(15000000);
        
        GPIOPinWrite(GPIO_PORTB_BASE, 0x0C, 0x04);
        SysCtlDelay(15000000);*/
        
    }
}

void timer0A_handler(void)
{
    
   TimerIntClear(TIMER0_BASE, TIMER_A);
   
   
}





