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

char data[20];
char comand[7];

int flagMotor1=0;
int flagMotor2=0;
int flagMotor3=0;
int flagmainMotor1=0;
int flagLeds=0;

int motvel1[2];
int motvel2[2];
int motvel3[2];
int mainvel1[2];

int leds[4];

int main(void)
{

    //volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock
    //habilitacion de pines
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);//LED boardTiva
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);//LED boardTiva, PWM0, PWM1, PWM2, PWM3,
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOG);// PWM4, PWM5
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);//UART
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);//BOTONES
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);// PWM6, PWM7, INA2,INB2,
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);// INA1,INB1, 
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOM);// INA3,INB3,
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOH);// ENDER,ENIZQ,

    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM2);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM3);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM4);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM5);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM6);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM7);



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
  
    
    //LEDS ON BOARD
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x11);

    //PINS ENABLES
    GPIOPinTypeGPIOOutput(GPIO_PORTL_BASE, 0xC);// PL2,PL3
    GPIOPinTypeGPIOOutput(GPIO_PORTK_BASE, 0xC0);// PK6,PK7
    GPIOPinTypeGPIOOutput(GPIO_PORTM_BASE, 0x03);// PM0,PM1
    GPIOPinTypeGPIOOutput(GPIO_PORTH_BASE, 0x03);// PM0,PM1


    //Configuracion uart
    UARTStdioConfig(0,9600,120000000);
    
    //configuracion botones 2
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);
    


    //pwm
    GPIOPinConfigure(GPIO_PF0_M0PWM0);
    GPIOPinConfigure(GPIO_PF1_M0PWM1);
    GPIOPinConfigure(GPIO_PF2_M0PWM2);
    GPIOPinConfigure(GPIO_PF3_M0PWM3);
    GPIOPinConfigure(GPIO_PG0_M0PWM4);
    GPIOPinConfigure(GPIO_PG1_M0PWM5);
    GPIOPinConfigure(GPIO_PK4_M0PWM6);
    GPIOPinConfigure(GPIO_PK5_M0PWM7);

    
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_0);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_1);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_2);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_3);
    GPIOPinTypePWM(GPIO_PORTG_BASE,GPIO_PIN_0);
    GPIOPinTypePWM(GPIO_PORTG_BASE,GPIO_PIN_1);
    GPIOPinTypePWM(GPIO_PORTK_BASE,GPIO_PIN_4);
    GPIOPinTypePWM(GPIO_PORTK_BASE,GPIO_PIN_5);

    PWMGenConfigure(PWM0_BASE,PWM_GEN_0,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM1_BASE,PWM_GEN_0,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM2_BASE,PWM_GEN_1,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM3_BASE,PWM_GEN_1,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM4_BASE,PWM_GEN_2,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM5_BASE,PWM_GEN_2,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM6_BASE,PWM_GEN_3,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM7_BASE,PWM_GEN_3,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_0,100);
    PWMGenPeriodSet(PWM1_BASE,PWM_GEN_0,100);
    PWMGenPeriodSet(PWM2_BASE,PWM_GEN_1,100);
    PWMGenPeriodSet(PWM3_BASE,PWM_GEN_1,100);
    PWMGenPeriodSet(PWM4_BASE,PWM_GEN_2,100);
    PWMGenPeriodSet(PWM5_BASE,PWM_GEN_2,100);
    PWMGenPeriodSet(PWM6_BASE,PWM_GEN_3,100);
    PWMGenPeriodSet(PWM7_BASE,PWM_GEN_3,100);


    width=100;
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,width);

    PWMGenEnable(PWM0_BASE,PWM_GEN_1);
    PWMGenEnable(PWM0_BASE,PWM_GEN_2);    
    
    PWMOutputState(PWM0_BASE,(PWM_OUT_2_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_4_BIT),true);




    while(1){
        //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
        UARTgets(data,15);
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
        
    }
}

void timer0A_handler(void)
{
   TimerIntClear(TIMER0_BASE, TIMER_A);
   if (flagMotor==1){
        if(vel[1]<0){
            GPIOPinWrite(GPIO_PORTK_BASE, 0xC0, 0x40);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,vel[1]*-1);
        }
        else{
            GPIOPinWrite(GPIO_PORTK_BASE, 0xC0, 0x80);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,vel[1]);
        }


        if(vel[0]<0){
            GPIOPinWrite(GPIO_PORTK_BASE, 0x30, 0x10);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,vel[0]*-1);
        }
        else{
            GPIOPinWrite(GPIO_PORTK_BASE, 0x30, 0x20);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,vel[0]);
        }


        if(vel[0]==0 || vel[1]==0){
            GPIOPinWrite(GPIO_PORTK_BASE, 0xF0, 0x00);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,0);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,0);
        }
    


        
        //GPIOPinWrite(GPIO_PORTK_BASE, 0xF0, 0xA0);
        //PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,vel[0]);
        //PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,vel[1]);
   }
   else if(flagMotor==0){
        width=0;
        GPIOPinWrite(GPIO_PORTK_BASE, 0xF0, 0x00);//PF7 y PF5(adelante)0xA0 //0x50 PF4 y PF6(atras)0x50
        PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,width);
        PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,width);
   }
   
}






void timer1A_handler(void){ 
   TimerIntClear(TIMER1_BASE, TIMER_A);
   if (leds[0]==1){
    GPIOPinWrite(GPIO_PORTN_BASE, 0x02, 0x02);
   }
   else{
    GPIOPinWrite(GPIO_PORTN_BASE, 0x02, 0x00);
   }
   if (leds[1]==1){
    GPIOPinWrite(GPIO_PORTN_BASE, 0x01, 0x01);
   }
   else{
    GPIOPinWrite(GPIO_PORTN_BASE, 0x01, 0x00);
   }
   if (leds[2]==1){
    GPIOPinWrite(GPIO_PORTF_BASE, 0x10, 0x10);
   }
   else{
    GPIOPinWrite(GPIO_PORTF_BASE, 0x10, 0x00);
   }
   if (leds[3]==1){
    GPIOPinWrite(GPIO_PORTF_BASE, 0x01, 0x01);
   }
   else{
    GPIOPinWrite(GPIO_PORTF_BASE, 0x01, 0x00);
   }
   
}