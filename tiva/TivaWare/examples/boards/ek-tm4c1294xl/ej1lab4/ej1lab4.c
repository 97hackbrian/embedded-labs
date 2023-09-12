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

//Funcion exterior para el uso de la interrupcion del timer 
void timer0A_handler(void);
int state=0;
uint32_t FS = 120000000/1; //frecuencia del timer

//
//*****************************************************************************

int main(void)
{
    //volatile uint32_t ui32Loop; //Tipo de variable
    
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000); //enable system /clock
    //
    // Enable the GPIO  N port that is used for the on-board LED.
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    //
    // Enable timer peripheral
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    
    //Programation of timer
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    //Adjust time output of timer 
    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    //Enable the interrupt
    IntEnable(INT_TIMER0A);
    //Enable interrupt of timer A
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);   
    //Enable of timer 
    TimerEnable(TIMER0_BASE, TIMER_A);
    IntMasterEnable();
   
    
    
    // Check if the peripheral N access is enabled.
    //
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }
    
 


    //
    // Enable the GPIO pin for the LED (PN0).  Set the direction as output, and
    // enable the GPIO pin for digital function.
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03); //enable 0 y 1 pins N

    

    while(1)
   {
    }
}


void timer0A_handler(void)
{
	TimerIntClear(TIMER0_BASE, TIMER_A);
	
	if(state <=2){
		GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
		
	}
	
	else if(state>2){
		GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
        
	}
    if(state==4){
        state=0;
    }
	
	state++;
}







