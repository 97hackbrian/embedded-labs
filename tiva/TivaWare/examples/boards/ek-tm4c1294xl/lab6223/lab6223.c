#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

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

//adc
#include "driverlib/adc.h"

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
void timer1A_handler(void);
int state=0;
int state2=0;
uint32_t FS = 120000000*1; //frecuencia del timer
uint32_t FS2 = 120000000*1; 
int flag=0;
int flag2=0;
char data[10];
uint32_t ui32Value=0;

int last=0;

char *itoa (int value, char *result, int base)
{
    // check that the base if valid
    if (base < 2 || base > 36) { *result = '\0'; return result; }

    char* ptr = result, *ptr1 = result, tmp_char;
    int tmp_value;

    do {
        tmp_value = value;
        value /= base;
        *ptr++ = "zyxwvutsrqponmlkjihgfedcba9876543210123456789abcdefghijklmnopqrstuvwxyz" [35 + (tmp_value - value * base)];
    } while ( value );

    // Apply negative sign
    if (tmp_value < 0) *ptr++ = '-';
    *ptr-- = '\0';
    while (ptr1 < ptr) {
        tmp_char = *ptr;
        *ptr--= *ptr1;
        *ptr1++ = tmp_char;
    }
    return result;
}

int main(void)
{

    //volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock
    //habilitacion de pines
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOQ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    //adc
    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);
    GPIOPinTypeADC(GPIO_PORTK_BASE,0x08);


    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    //
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



 
    

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    // configuracion uart
    UARTStdioConfig(0,9600,120000000);
    //char msg[]="osita\n";
    
    //configuracion botones 2
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);
    // configuracion buzzer
    GPIOPinTypeGPIOOutput(GPIO_PORTQ_BASE,0X01);
    GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE,0x0C);

    ///ADC configuration:
    //Enable the first sample sequencer to capture the value of chanel 19 when the procesor trigger occurs. Sequencer 3 captures 1 sample.
    ADCSequenceConfigure(ADC0_BASE,3,ADC_TRIGGER_PROCESSOR,0);
    //Configure the ADC step (interruption,end and chanel 19)
    ADCSequenceStepConfigure(ADC0_BASE,3,0,ADC_CTL_IE | ADC_CTL_END | ADC_CTL_CH19);
    //Enables ADC sequence
    ADCSequenceEnable(ADC0_BASE,3);
    //Clear the ADC interruptions
    ADCIntClear(ADC0_BASE,3); 
        
    //
    

    GPIOPinConfigure(GPIO_PF1_M0PWM1);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_1);

    PWMGenConfigure(PWM0_BASE,PWM_GEN_0,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_0,400);

    width=300;
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,width);

    PWMGenEnable(PWM0_BASE,PWM_GEN_0);    
    
    PWMOutputState(PWM0_BASE,(PWM_OUT_1_BIT),true);


    while(1){
    //Trigger the sample sequence.
    ADCProcessorTrigger(ADC0_BASE,3);
    //Wait until the sample sequence has completed.
    while(!ADCIntStatus(ADC0_BASE,3,false)){
    }
    //Clear the ADC interruptions
    ADCIntClear(ADC0_BASE,3); 
    //Read the value from ADC
    ADCSequenceDataGet(ADC0_BASE,3,&ui32Value);


    ui32Value=ui32Value/10;

    UARTprintf(itoa(ui32Value,data,10));
    GPIOPinWrite(GPIO_PORTB_BASE, 0x0C, 0x04);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,ui32Value);
    
    }
}


void timer0A_handler(void){
    
   TimerIntClear(TIMER0_BASE, TIMER_A);


}


void timer1A_handler(void){ 
   TimerIntClear(TIMER1_BASE, TIMER_A);


}




