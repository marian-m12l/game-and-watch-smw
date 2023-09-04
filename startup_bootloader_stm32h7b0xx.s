/* TODO ISR vector + reset handler + load to ram + hand over */
    
  .syntax unified
  .cpu cortex-m7
  .fpu softvfp
  .thumb

  /* FIXME Rename to avoid duplicates ??? */
.global  g_pfnVectors_bootloader
.global  Default_Handler_bootloader_bootloader

/* FIXME Set symbols of areas to copy in LD script ! */
/* start address for the initialization values of the .data section. 
defined in linker script */
.word  _sidata
/* start address for the .data section. defined in linker script */
.word  _sdata
/* end address for the .data section. defined in linker script */
.word  _edata
/* start address for the .bss section. defined in linker script */
.word  _sbss
/* end address for the .bss section. defined in linker script */
.word  _ebss
/* stack used for SystemInit_ExtMemCtl; always internal RAM used */

/* FIXME Rename to avoid duplicates ??? */
/* FIXME No need for a separate section ??? */
    .section  .text.Reset_Handler_bootloader
  .weak  Reset_Handler_bootloader
  .type  Reset_Handler_bootloader, %function
Reset_Handler_bootloader:  
  ldr   sp, =_estack      /* set stack pointer */

/* FIXME Don't call SystemInit (which is not in flash anyway...) but rewrite its function in assembly ??? */
/* Call the clock system intitialization function.*/
  bl  SystemInit

/* FIXME Load from intflash to RAM_UC */
/* Copy the data segment initializers from flash to SRAM */
  movs  r1, #0
  b  LoopCopyDataInit

CopyDataInit:
  ldr  r3, =_sidata
  ldr  r3, [r3, r1]
  str  r3, [r0, r1]
  adds  r1, r1, #4
    
LoopCopyDataInit:
  ldr  r0, =_sdata
  ldr  r3, =_edata
  adds  r2, r0, r1
  cmp  r2, r3
  bcc  CopyDataInit
  ldr  r2, =_sbss
  b  LoopFillZerobss
/* Zero fill the bss segment. */
FillZerobss:
  movs  r3, #0
  str  r3, [r2], #4
    
LoopFillZerobss:
  ldr  r3, = _ebss
  cmp  r2, r3
  bcc  FillZerobss
   
/* FIXME Just hand over to RAM_UC code ??? */
/* Call static constructors */
    bl __libc_init_array
/* Call the application's entry point.*/
  bl  main
  bx  lr
.size  Reset_Handler_bootloader, .-Reset_Handler_bootloader

/**
 * @brief  This is the code that gets called when the processor receives an 
 *         unexpected interrupt.  This simply enters an infinite loop, preserving
 *         the system state for examination by a debugger.
 * @param  None     
 * @retval None       
*/
    .section  .text.Default_Handler_bootloader_bootloader,"ax",%progbits
Default_Handler_bootloader_bootloader:
Infinite_Loop:
  b  Infinite_Loop
  .size  Default_Handler_bootloader_bootloader, .-Default_Handler_bootloader_bootloader
/******************************************************************************
*
* The minimal vector table for a Cortex M. Note that the proper constructs
* must be placed on this to ensure that it ends up at physical address
* 0x0000.0000.
* 
*******************************************************************************/
   .section  .isr_vector_bootloader,"a",%progbits
  .type  g_pfnVectors_bootloader, %object
  .size  g_pfnVectors_bootloader, .-g_pfnVectors_bootloader
   

/* FIXME All handlers whould be 0 ??? */
g_pfnVectors_bootloader:
  .word  _estack
  .word  Reset_Handler_bootloader

  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  .word  0
  
