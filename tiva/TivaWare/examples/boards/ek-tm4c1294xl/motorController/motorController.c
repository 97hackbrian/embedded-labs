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
void timer1A_handler(void);
int state=0;
uint32_t FS = 120000000/100; //frecuencia del timer
uint32_t FS2 = 120000000/100; //frecuencia del timer
int flagMotor=0;
int flagLeds=0;
char data[25];
char comand[7];
int vel[2];
int ser[2];
int vel2[2];
int leds[4];

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
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);//
    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);//PROBAR



    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    //configuracion timer
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


    //GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE,0x0C);

  
    

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    GPIOPinTypeGPIOOutput(GPIO_PORTL_BASE, 0xC);// PL2,PL3

    //GPIOPinTypeGPIOOutput(GPIO_PORTG_BASE, 0x01);//PG0 PWMB
    GPIOPinTypeGPIOOutput(GPIO_PORTK_BASE, 0xF0);//PK4,PK5,PK6,PK7

    // configuracion uart
    UARTStdioConfig(0,9600,120000000);
    //char msg[]="osita\n";
    
    //configuracion botones 2
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);
    // configuracion buzzer


    //pwm
    GPIOPinConfigure(GPIO_PF1_M0PWM1);//
    GPIOPinConfigure(GPIO_PF2_M0PWM2);
    GPIOPinConfigure(GPIO_PG0_M0PWM4);
    GPIOPinConfigure(GPIO_PG1_M0PWM5);
    width=255;
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_1);//
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_2);
    GPIOPinTypePWM(GPIO_PORTG_BASE,GPIO_PIN_0);
    GPIOPinTypePWM(GPIO_PORTG_BASE,GPIO_PIN_1);

    PWMGenConfigure(PWM0_BASE,PWM_GEN_0,PWM_GEN_MODE_DOWN);
    PWMGenConfigure(PWM0_BASE,PWM_GEN_1,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    //PWMGenConfigure(PWM1_BASE,PWM_GEN_1,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM0_BASE,PWM_GEN_2,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM0_BASE,PWM_GEN_3,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_0,100);
    //PWMGenPeriodSet(PWM1_BASE,PWM_GEN_1,width);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_1,width);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_2,width);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_3,width);

    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,1);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_5,width);

    PWMGenEnable(PWM0_BASE,PWM_GEN_0);
    PWMGenEnable(PWM0_BASE,PWM_GEN_1);
    //PWMGenEnable(PWM1_BASE,PWM_GEN_1);
    PWMGenEnable(PWM0_BASE,PWM_GEN_2);
    PWMGenEnable(PWM0_BASE,PWM_GEN_3);       
    
    PWMOutputState(PWM0_BASE,(PWM_OUT_1_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_2_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_4_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_5_BIT),true);




    while(1){
        //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
        UARTgets(data,25);
        strcpy(comand, strtok(data, ","));
        //UARTprintf(comand);
        

        if(strcmp(comand, "motor")==0){
            char *token = strtok(NULL, ",");
            if (token != NULL)
            {
                //UARTprintf(token);
                vel[0] = atoi(token);
                token = strtok(NULL, ",");
                if (token != NULL)
                {
                    //UARTprintf(token);
                    vel[1] = atoi(token);
                }
                flagMotor = 1;
                //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
            }
            
            

        }
        else{
            flagMotor=0;
            //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
        }

        if(strcmp(comand, "leds")==0){
            char *token = strtok(NULL, ",");
            if (token != NULL)
            {
                UARTprintf(token);
                leds[0] = atoi(token);
                token = strtok(NULL, ",");
                if (token != NULL)
                {
                    UARTprintf(token);
                    leds[1] = atoi(token);
                    token = strtok(NULL, ",");
                    if (token != NULL)
                    {
                        UARTprintf(token);
                        leds[2] = atoi(token);
                        token = strtok(NULL, ",");
                        if (token != NULL)
                        {
                            UARTprintf(token);
                            leds[3] = atoi(token);
                        }
                    }
                }
                //flagMotor = 1;
                //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
            }
            
            

        }
        else{
            flagLeds=0;
            //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
        }

        //width=65;
        //GPIOPinWrite(GPIO_PORTK_BASE, 0xF0, 0xA0);//PF7 y PF5(adelante)0xA0 //0x50 PF4 y PF6(atras)0x50
        //PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,width);
        //PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,width);

        /*
        SysCtlDelay(15000000);
        
        GPIOPinWrite(GPIO_PORTB_BASE, 0x0C, 0x04);
        SysCtlDelay(15000000);*/
        if(strcmp(comand, "gripper")==0){
            char *token = strtok(NULL, ",");
            if (token != NULL)
            {
                //UARTprintf(token);
                vel2[0] = atoi(token);
                token = strtok(NULL, ",");
                if (token != NULL)
                {
                 
                }
     
            }
            
            

        }
      
    }
}

void timer0A_handler(void)
{
   TimerIntClear(TIMER0_BASE, TIMER_A);

        if(vel[0]<0){
            GPIOPinWrite(GPIO_PORTK_BASE, 0xC0, 0x80);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,vel[0]*-1);
        }
        else{
            GPIOPinWrite(GPIO_PORTK_BASE, 0xC0, 0x40);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,vel[0]);
        }


        if(vel[1]<0){
            GPIOPinWrite(GPIO_PORTK_BASE, 0x30, 0x10);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,vel[1]*-1);
        }
        else{
            GPIOPinWrite(GPIO_PORTK_BASE, 0x30, 0x20);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,vel[1]);
        }


        if(vel[0]==0){
            GPIOPinWrite(GPIO_PORTK_BASE, 0xC0, 0x0);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,0);
        }
        if(vel[1]==0){
            GPIOPinWrite(GPIO_PORTK_BASE, 0x30, 0x0);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,0);
        }

        if(vel2[0]<0){
            GPIOPinWrite(GPIO_PORTL_BASE, 0xC, 0x04);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_5,vel2[0]*-1);
        }
        else{
        GPIOPinWrite(GPIO_PORTL_BASE, 0xC, 0x08);
        PWMPulseWidthSet(PWM0_BASE,PWM_OUT_5,vel2[0]);
    }
    if(vel2[0]==0){
        GPIOPinWrite(GPIO_PORTL_BASE, 0xC, 0x0);
        PWMPulseWidthSet(PWM0_BASE,PWM_OUT_5,0);
    }

    
    //PWMGenPeriodSet(PWM0_BASE,PWM_GEN_0,ser[0]);
    //PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,ser[0]);

        
        //GPIOPinWrite(GPIO_PORTK_BASE, 0xF0, 0xA0);
        //PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,vel[0]);
        //PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,vel[1]);
}






void timer1A_handler(void){ 
   TimerIntClear(TIMER1_BASE, TIMER_A);

   
}