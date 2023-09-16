//*****************************************************************************
//
// blinky.c - Simple example to blink the on-board LED.
//
// Copyright (c) 2013-2020 Texas Instruments Incorporated.  All rights reserved.
// Software License Agreement
// 
// Texas Instruments (TI) is supplying this software for use solely and
// exclusively on TI's microcontroller products. The software is owned by
// TI and/or its suppliers, and is protected under applicable copyright
// laws. You may not combine this software with "viral" open-source
// software in order to form a larger program.
// 
// THIS SOFTWARE IS PROVIDED "AS IS" AND WITH ALL FAULTS.
// NO WARRANTIES, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
// NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. TI SHALL NOT, UNDER ANY
// CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
// DAMAGES, FOR ANY REASON WHATSOEVER.
// 
// This is part of revision 2.2.0.295 of the EK-TM4C1294XL Firmware Package.
//
//*****************************************************************************

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

//uart
#include "driverlib/uart.h"
#include "utils/uartstdio.c"
#include "string.h"

//Interrupciones

#include "driverlib/interrupt.h"
#include "driverlib/timer.h"
#include "inc/tm4c1294ncpdt.h"
//*****************************************************************************
//
//! \addtogroup example_list
//! <h1>Blinky (blinky)</h1>
//!
//! A very simple example that blinks the on-board LED using direct register
//! access.
//
//*****************************************************************************

//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif

//*****************************************************************************
//
// Blink the on-board LED.













//
//*****************************************************************************

uint32_t FS=120000000*1;//1seg
uint32_t FS2=120000000*2;//2seg

uint32_t FS3=120000000/50;//0.005seg
void timer0A_handler(void);
void timer1A_handler(void);
//void timer2A_handler(void);
//void timer3A_handler(void);
void GPIOJ_handler(void);
uint8_t switch_state = 0;
uint32_t button=0;
int count1=0;
int count2=0;
int count3=0;
int flag =0;
int flag2 =0;
char data[2];


bool boton1Presionado = false;
bool boton2Presionado = false;
int main(void)
{
    // volatile uint32_t ui32Loop;



    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ|SYSCTL_OSC_MAIN|SYSCTL_USE_PLL|SYSCTL_CFG_VCO_480),120000000); //enables system clock
    //
    // Enable the GPIO port that is used for the on-board LED.
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER2);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER3);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x11);
    



    TimerConfigure(TIMER0_BASE,TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE,TIMER_A,FS);
    IntMasterEnable();
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE,TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER0_BASE,TIMER_A);

    

    TimerConfigure(TIMER1_BASE,TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER1_BASE,TIMER_A,FS2);
    IntMasterEnable();
    IntEnable(INT_TIMER1A);
    TimerIntEnable(TIMER1_BASE,TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER1_BASE,TIMER_A);

    // Configuracion del pin uart
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);

    GPIOPinTypeUART(GPIO_PORTA_BASE,0x03);
    UARTStdioConfig(0,9600,120000000);
    
    
    // Configura el puerto J para generar interrupciones por flanco de bajada (cuando se presiona el botón).
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, 0x03);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, 0x03, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    GPIOIntTypeSet(GPIO_PORTJ_BASE, 0x03, GPIO_FALLING_EDGE);
    //GPIOIntTypeSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_FALLING_EDGE);
    GPIOIntEnable(GPIO_PORTJ_BASE, 0x03);
    IntEnable(INT_GPIOJ);

    
    //TIGGER
/*
    TimerConfigure(TIMER2_BASE,TIMER_CFG_ONE_SHOT);
    TimerLoadSet(TIMER2_BASE,TIMER_A,FS3);
    IntMasterEnable();
    IntEnable(INT_TIMER2A);
    TimerIntEnable(TIMER2_BASE,TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER2_BASE,TIMER_A);

    TimerConfigure(TIMER3_BASE,TIMER_CFG_ONE_SHOT);
    TimerLoadSet(TIMER3_BASE,TIMER_A,FS3);
    IntMasterEnable();
    IntEnable(INT_TIMER3A);
    TimerIntEnable(TIMER3_BASE,TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER3_BASE,TIMER_A);
    //
    //
    */

    while(1)
    {
        UARTgets(data,2);
    //strcat(data,"\n");
    //UARTprintf(data);
    //}
    
    if(strcmp(data, "0")==0){

        flag=1;
    }
    else{
        flag=0;
        FS=120000000*((int) strtol(data, NULL, 10));
    }

    }
}

void timer0A_handler(void){
    TimerIntClear(TIMER0_BASE, TIMER_A);
    if(GPIOPinRead(GPIO_PORTJ_BASE,0x02)==0 &&flag==0){
    
        if (count1==1){
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x03);
            count1 =0;
        }
        else{
            GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
            count1++;
        }    
    }
    else{
        GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
    }
  
    
}


void timer1A_handler(void){
    TimerIntClear(TIMER1_BASE, TIMER_A);
}


void GPIOJ_handler(void) {
    uint32_t status = GPIOIntStatus(GPIO_PORTJ_BASE, true);
    GPIOIntClear(GPIO_PORTJ_BASE, status);

    if (status & GPIO_PIN_0) {
        FS=FS/2;
        SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
        TimerConfigure(TIMER0_BASE,TIMER_CFG_PERIODIC);
        TimerLoadSet(TIMER0_BASE,TIMER_A,FS);
        IntMasterEnable();
        IntEnable(INT_TIMER0A);
        TimerIntEnable(TIMER0_BASE,TIMER_TIMA_TIMEOUT);
        TimerEnable(TIMER0_BASE,TIMER_A);

        
       
    }
    
    else if(status & GPIO_PIN_1){
          SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
        TimerConfigure(TIMER0_BASE,TIMER_CFG_PERIODIC);
        TimerLoadSet(TIMER0_BASE,TIMER_A,FS);
        IntMasterEnable();
        IntEnable(INT_TIMER0A);
        TimerIntEnable(TIMER0_BASE,TIMER_TIMA_TIMEOUT);
        TimerEnable(TIMER0_BASE,TIMER_A);
    }
    else{
        GPIOPinWrite(GPIO_PORTF_BASE, 0x11, 0x00);
        GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
    }
}