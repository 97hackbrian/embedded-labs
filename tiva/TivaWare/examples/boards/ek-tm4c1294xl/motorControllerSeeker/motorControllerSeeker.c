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
#include "inc/hw_memmap.h"
uint32_t reloj;
volatile uint32_t width;

#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif




void timer1A_handler(void);
void timer2A_handler(void);
void timer3A_handler(void);
int state=0;
uint32_t FS = 120000000/100; //frecuencia del timer
uint32_t FS2 = 120000000/100; //frecuencia del timer
uint32_t FS3 = 120000000/100; //frecuencia del timer

char data[50];
char comand[50];
int vel[2];

int flagMotor1=0;
int flagMotor2=0;
int flagMotor3=0;
int flagmainMotor1=0;
int flagLeds=0;
int flagMosfet = 0;


int motvel1[2];
int motvel2[2];
int motvel3[2];
int mainvel1[2];

int leds[4];
int mosfet[6];

int interpolar(int valor, int entrada_min, int entrada_max, int salida_min, int salida_max) {
    // Asegurar que el valor de entrada esté dentro del rango
    valor = (valor <= entrada_min) ? entrada_min : valor;
    valor = (valor >= entrada_max) ? entrada_max : valor;

    // Calcular la interpolación lineal
    double porcentaje = (valor - entrada_min) / (double)(entrada_max - entrada_min);
    int resultado = salida_min + porcentaje * (salida_max - salida_min);

    return resultado;
}

int main(void)
{

    //volatile uint32_t ui32Loop;
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock
    //habilitacion de pines
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);//LED boardTiva,M4=PN2,M5=PN3
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);//LED boardTiva, PWM0, PWM1, PWM2, PWM3,
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOG);// PWM4, PWM5
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);//UART
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);//BOTONES
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);// PWM6, PWM7, INA2,INB2,
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);// INA1,INB1, 
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOM);// INA3,INB3,M1=PM3
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOH);// ENDER,ENIZQ,M2=H2,M3=H3
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOP);// M6=PP2
    //SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);
    


    //SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER2);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER3);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);


    


    //configuracion timer 1A
    TimerConfigure(TIMER1_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER1_BASE, TIMER_A, FS2);
    IntEnable(INT_TIMER1A);
    TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER1_BASE, TIMER_A);
    IntMasterEnable();

    //configuracion timer 2A
    TimerConfigure(TIMER2_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER2_BASE, TIMER_A, FS3);
    IntEnable(INT_TIMER2A);
    TimerIntEnable(TIMER2_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER2_BASE, TIMER_A);
    IntMasterEnable();

    //configuracion timer3A
    TimerConfigure(TIMER3_BASE, TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER3_BASE, TIMER_A, FS);
    IntEnable(INT_TIMER3A);
    TimerIntEnable(TIMER3_BASE, TIMER_TIMA_TIMEOUT);   
    TimerEnable(TIMER3_BASE, TIMER_A);
    IntMasterEnable();
   

    // Configuracion del pin uart
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE,0x03);
  
    
    //PINS ENABLES
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0xF);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x11);
    //GPIOPinTypeGPIOOutput(GPIO_PORTG_BASE, 0x01);

    
    GPIOPinTypeGPIOOutput(GPIO_PORTL_BASE, 0xC);// PL2,PL3
    GPIOPinTypeGPIOOutput(GPIO_PORTK_BASE, 0xC0);// PK6,PK7
    GPIOPinTypeGPIOOutput(GPIO_PORTM_BASE, 0xB);// PM0,PM1,PM3
    GPIOPinTypeGPIOOutput(GPIO_PORTH_BASE, 0xF);// PH0,PH1,PH2,PH3
    GPIOPinTypeGPIOOutput(GPIO_PORTP_BASE, 0x04);// PP2




    //Configuracion uart
    UARTStdioConfig(0,9600,120000000);
    
    //configuracion botones 2
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE,0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE,0x03,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPU);
    


    //pwm
    //GPIOPinConfigure(GPIO_PF0_M0PWM0);
    GPIOPinConfigure(GPIO_PF1_M0PWM1);
    GPIOPinConfigure(GPIO_PF2_M0PWM2);
    GPIOPinConfigure(GPIO_PF3_M0PWM3);
    GPIOPinConfigure(GPIO_PG0_M0PWM4);
    GPIOPinConfigure(GPIO_PG1_M0PWM5);
    GPIOPinConfigure(GPIO_PK4_M0PWM6);
    GPIOPinConfigure(GPIO_PK5_M0PWM7);

    
    //GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_0);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_1);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_2);
    GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_3);
    GPIOPinTypePWM(GPIO_PORTG_BASE,GPIO_PIN_0);
    GPIOPinTypePWM(GPIO_PORTG_BASE,GPIO_PIN_1);
    GPIOPinTypePWM(GPIO_PORTK_BASE,GPIO_PIN_4);
    GPIOPinTypePWM(GPIO_PORTK_BASE,GPIO_PIN_5);


    width=10000;
    PWMGenConfigure(PWM0_BASE,PWM_GEN_0,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM0_BASE,PWM_GEN_1,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    //PWMGenConfigure(PWM1_BASE,PWM_GEN_1,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM0_BASE,PWM_GEN_2,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM0_BASE,PWM_GEN_3,PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_0,width);
    //PWMGenPeriodSet(PWM1_BASE,PWM_GEN_1,width);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_1,width);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_2,width);
    PWMGenPeriodSet(PWM0_BASE,PWM_GEN_3,width);
    
    

    
    
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_3,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_5,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_6,width);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_7,width);
    
    
    PWMGenEnable(PWM0_BASE,PWM_GEN_0);
    PWMGenEnable(PWM0_BASE,PWM_GEN_1);
    //PWMGenEnable(PWM1_BASE,PWM_GEN_1);
    PWMGenEnable(PWM0_BASE,PWM_GEN_2);
    PWMGenEnable(PWM0_BASE,PWM_GEN_3);    
    

     
    PWMOutputState(PWM0_BASE,(PWM_OUT_1_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_2_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_3_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_4_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_5_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_6_BIT),true);
    PWMOutputState(PWM0_BASE,(PWM_OUT_7_BIT),true);

   




    while(1){
        //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
        UARTgets(data,50);
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
                flagmainMotor1 = 1;
                //GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
            }
            
            

        }
        else{
            flagmainMotor1=0;
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
        
        if(strcmp(comand, "mosfet") == 0) {
            char *token = strtok(NULL, ",");
            if (token != NULL) {
                mosfet[0] = atoi(token);
                token = strtok(NULL, ",");
                if (token != NULL) {
                    mosfet[1] = atoi(token);
                    token = strtok(NULL, ",");
                    if (token != NULL) {
                        mosfet[2] = atoi(token);
                        token = strtok(NULL, ",");
                        if (token != NULL) {
                            mosfet[3] = atoi(token);
                            token = strtok(NULL, ",");
                            if (token != NULL) {
                                mosfet[4] = atoi(token);
                                token = strtok(NULL, ",");
                                if (token != NULL) {
                                    mosfet[5] = atoi(token);
                                    flagMosfet = 1;
                                }
                            }
                        }
                    }
                }
            }
        } 
        else {
            flagMosfet = 0;
        }
    }
}







void timer1A_handler(void) {
    TimerIntClear(TIMER1_BASE, TIMER_A);

    GPIOPinWrite(GPIO_PORTN_BASE, 0x02, (leds[0] == 1) ? 0x02 : 0x00);
    GPIOPinWrite(GPIO_PORTN_BASE, 0x01, (leds[1] == 1) ? 0x01 : 0x00);
    GPIOPinWrite(GPIO_PORTF_BASE, 0x10, (leds[2] == 1) ? 0x10 : 0x00);
    GPIOPinWrite(GPIO_PORTF_BASE, 0x01, (leds[3] == 1) ? 0x01 : 0x00);
}


void timer2A_handler(void) {
   TimerIntClear(TIMER2_BASE, TIMER_A);
   //GPIOPinWrite(GPIO_PORTN_BASE, 0x02, 0x02);
   if (flagMosfet == 1) {
        //GPIOPinWrite(GPIO_PORTN_BASE, 0x02, 0x02);
        GPIOPinWrite(GPIO_PORTM_BASE, 0x08, mosfet[0] ? 0x08 : 0x00);
        GPIOPinWrite(GPIO_PORTH_BASE, 0x04, mosfet[1] ? 0x04 : 0x00);
        GPIOPinWrite(GPIO_PORTH_BASE, 0x08, mosfet[2] ? 0x08 : 0x00);
        GPIOPinWrite(GPIO_PORTN_BASE, 0x04, mosfet[3] ? 0x04 : 0x00);
        GPIOPinWrite(GPIO_PORTN_BASE, 0x08, mosfet[4] ? 0x08 : 0x00);
        GPIOPinWrite(GPIO_PORTP_BASE, 0x04, mosfet[5] ? 0x04 : 0x00);
   }
}

void timer3A_handler(void)
{
    TimerIntClear(TIMER3_BASE, TIMER_A);
    /*
    GPIOPinWrite(GPIO_PORTN_BASE, 0x02, 0x02);

    GPIOPinWrite(GPIO_PORTH_BASE, 0x02, 0x02);
    GPIOPinWrite(GPIO_PORTH_BASE, 0x01, 0x01);

    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,100);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,0);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_3,5000);
    PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,0);

    
    */   


    if (flagmainMotor1==1){
        if(vel[1]<0){
            GPIOPinWrite(GPIO_PORTH_BASE, 0x02, 0x02);

            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,interpolar(vel[1]*-1,0,100,10000,1));
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,0);
        }
        else{
            GPIOPinWrite(GPIO_PORTH_BASE, 0x02, 0x02);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,0);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,interpolar(vel[1],0,100,10000,1));
        }


        if(vel[0]<0){
            GPIOPinWrite(GPIO_PORTH_BASE, 0x01, 0x01);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_3,interpolar(vel[0]*-1,0,100,10000,1));
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,0);
        }
        else{
            GPIOPinWrite(GPIO_PORTH_BASE, 0x01, 0x01);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_3,0);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,interpolar(vel[0],0,100,10000,1));
        }


        if(vel[0]==0){
            GPIOPinWrite(GPIO_PORTH_BASE, 0x01, 0x00);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_3,0);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_4,0);
        }
        else if(vel[1]==0){
            GPIOPinWrite(GPIO_PORTH_BASE, 0x02, 0x00);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_1,0);
            PWMPulseWidthSet(PWM0_BASE,PWM_OUT_2,0);
        }
   }
   
   
   
}