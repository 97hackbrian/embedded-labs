#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h" // Agrega esta cabecera para las funciones y constantes del temporizador
#include "driverlib/interrupt.h"
#include "inc/hw_ints.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.c"
#include "string.h"
#include "driverlib/pin_map.h"


uint8_t switch_case=0;
uint32_t FS=120000000*2;
void timer0A_handler(void);
#ifdef DEBUG
void error(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif
void timer0A_handler(void)
{
	switch_case++;
	
	TimerIntClear(TIMER0_BASE, TIMER_A);
	//2 Sequence
	
	if(switch_case == 1)
	{
		GPIOPinWrite(GPIO_PORTN_BASE, 0x04, 0x04);
		GPIOPinWrite(GPIO_PORTN_BASE, 0x08, 0x00);
		GPIOPinWrite(GPIO_PORTF_BASE, 0x04, 0x00);
	
	}
	
	if(switch_case == 2)
	{
		GPIOPinWrite(GPIO_PORTN_BASE, 0x04, 0x00);
		GPIOPinWrite(GPIO_PORTN_BASE, 0x08, 0x08);
		GPIOPinWrite(GPIO_PORTF_BASE, 0x04, 0x00);
	
	}
	
	if(switch_case == 3)
	{
		GPIOPinWrite(GPIO_PORTN_BASE, 0x04, 0x00);
		GPIOPinWrite(GPIO_PORTN_BASE, 0x08, 0x00);
		GPIOPinWrite(GPIO_PORTF_BASE, 0x04, 0x04);
	
	}
	
	if(switch_case == 3) switch_case=0;
}


int main(void)
{

	//Configurar Clock///
	SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);
	//Habilitar puertos///
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
	GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x0C);
	
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
	GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x04);
	
	while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
	{
	}

	//Enable Timer
	SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
	//Set time
	TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
	//Set the count time for Timer
	//FS=120000000*2;
	TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
	//Enable processor interrupts
	IntMasterEnable();
	//Enable interrupt
	IntEnable(INT_TIMER0A);
	//Enable timer A interrupt
	TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
	//Enable the timer
	TimerEnable(TIMER0_BASE, TIMER_A);
	
	
	while(!SysCtlPeripheralReady(SYSCTL_PERIPH_UART0) || !SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOA))
	{
	}
	
	while(1)
	{	
		
	}
}