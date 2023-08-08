# Port of reverse engineered Super Mario World for the Game and Watch

All credits for reverse engineering goes to https://github.com/snesrev/smw

# Build instructions

- Clone repository with submodules
```sh
git clone --recurse-submodules https://github.com/marian-m12l/game-and-watch-smw.git
```

- Install python requirements using pip
```sh
pip3 install -r requirements.txt
```

- Place your US ROM file named `smw.sfc` in `smw/assets/`.

- Compile and flash (e.g. on internal flash bank 2, leaving 1MB (out of 16) for stock firmware at the beginning of extflash)
```sh
make INTFLASH_BANK=2 EXTFLASH_SIZE_MB=15 EXTFLASH_OFFSET=1048576 ADAPTER=jlink OPENOCD=/path/to/patched/openocd-git/bin/openocd GNW_TARGET=mario flash
```

## List of build flags

To control how the firmware is programmed:

| Build flag    | Description |
| ------------- | ------------- |
| `INTFLASH_BANK` | Which internal flash bank to program.<br>1 or 2. |
| `EXTFLASH_OFFSET` | Offset after which to program external flash. In bytes. |
| `EXTFLASH_SIZE_MB` | Allocated space in external flash. In MB. |
| `LARGE_FLASH` | Required for external flash chips > 16MB. Enables 32-bit addressing. |

To control game options:

| Build flag    | Description |
| ------------- | ------------- |
| `LIMIT_30FPS` | Limit to 30 fps for improved stability.<br>Enabled by default.<br>Disabling this flag will result in unsteady framerate and stuttering. |
| `OVERCLOCK` | Overclock level: 0 (no overclocking), 1 (intermediate overclocking), or 2 (max overclocking).<br>Default value: 2. |
| `RENDER_FPS` | Render performance metrics. Disabled by default. |
| `ENABLE_SAVESTATE` | Enable savestate support. This allocates 178kB of external flash.<br>Disabled by default. |

## (WIP) Building as a Retro-Go application (a.k.a. running in RAM)

**DISCLAIMER: This is work-in-progress**

SMW can be run without flashing to intflash. The "intflash" binary can be stored in the Retro-Go filesystem and loaded into RAM for execution.

The Retro-Go filesystem must be large enough to fit the "intflash" binary on top of emulator savestates.

```
make [...] flash_extflash
make [...] build/gw_smw_intflash.bin
tamp compress build/gw_smw_intflash.bin -o build/gw_smw_intflash.bin.tamp
python3 gnwmanager.py push /apps/smw.bin.tamp build/gw_smw_intflash.bin.tamp
```

# Backing up and restoring saves

```sh
ADAPTER=jlink OPENOCD=/path/to/patched/openocd-git/bin/openocd ./scripts/saves_backup.sh build/gw_smw.elf 
ADAPTER=jlink OPENOCD=/path/to/patched/openocd-git/bin/openocd ./scripts/saves_erase.sh build/gw_smw.elf 
ADAPTER=jlink OPENOCD=/path/to/patched/openocd-git/bin/openocd ./scripts/saves_restore.sh build/gw_smw.elf 
```

# Applying additional features

Edit the `FEATURE_*` values in `Makefile` to enable additional features and bug fixes to the original game.

## List of features

| Build flag    | Description |
| ------------- | ------------- |
| `FEATURE_SAVE_AFTER_EACH_BEATEN_LEVEL` | Save to SRAM after each beaten level (instead of saving after castle is beaten).<br>SRAM save remains valid/compatible with emulators. |
