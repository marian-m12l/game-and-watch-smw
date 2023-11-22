#!/bin/bash

. ./scripts/common.sh

if [[ $# -lt 1 ]]; then
    echo "Usage: $(basename $0) <currently_running_binary.elf> [backup file]"
    echo "This will program smw savestate from the backup file"
    exit 1
fi

ELF="$1"
INFILE=smw_savestate.sav

if [[ $# -gt 1 ]]; then
    INFILE="$2"
fi

# Start processing

# Note that 0x90000000 is subtracted from the address.
address=$(get_symbol __SAVEFLASH_START__)
address=$(($address + 4096))
size=$((4096*66))
image="${INFILE}"

if [[ -e "$image" ]]; then
    echo ""
    echo ""
    echo "Programming savestate:"
    printf "    save_address=0x%08x\n" $address
    echo "    save_size=$size"
    echo ""
    echo ""
    export USE_4K_ERASE_CMD=1   # Used in stm32h7x_spiflash.cfg
	${OPENOCD} -f scripts/interface_${ADAPTER}.cfg -c "program ${image} ${address} verify reset exit"
else
    echo ""
    echo ""
    echo "FAILED: missing savestate file"
    echo ""
    echo ""
fi

# Reset the device and disable clocks from running when device is suspended
reset_and_disable_debug
