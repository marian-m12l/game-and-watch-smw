#!/bin/bash

. ./scripts/common.sh

if [[ $# -lt 1 ]]; then
    echo "Usage: $(basename $0) <currently_running_binary.elf> [backup file]"
    echo "This will dump smw save from the device to the backup file"
    exit 1
fi

ELF="$1"
OUTFILE=smw_save.srm

if [[ $# -gt 1 ]]; then
    OUTFILE="$2"
fi

# Start processing

address=$(get_symbol __SAVEFLASH_START__)
size=2048
echo ""
echo ""
echo "Dumping save data:"
printf "    save_address=0x%08x\n" $address
echo "    save_size=$size"
echo ""
echo ""
# openocd does not handle [ and ] well in filenames.
image_quoted=${OUTFILE//\[/\\[}
image_quoted=${image_quoted//\]/\\]}

export USE_4K_ERASE_CMD=0   # Used in stm32h7x_spiflash.cfg
${OPENOCD} -f scripts/interface_${ADAPTER}.cfg -c "init; reset halt; dump_image \"${image_quoted}\" ${address} ${size}; resume; exit;"

# Reset the device and disable clocks from running when device is suspended
reset_and_disable_debug
