import struct

assets_location = [
        # FIXME Assets list and allocation --> total 58 assets
]
assets_in_intflash = [index for (index, location) in assets_location if location == 'intflash']
assets_in_ram = [index for (index, location) in assets_location if location == 'ram']
assets_in_extflash = [index for index in range(58) if index not in assets_in_intflash and index not in assets_in_ram]


def bundle_assets(assets_to_keep, path):
        assets_data_addr = []
        assets_data_length = []
        with open("smw/assets/smw_assets.dat", mode="rb") as f:
                with open(path, "wb") as output:
                        output.write(struct.pack('<I', len(assets_to_keep)))
                        f.seek(80)
                        nbAssets, *_ = struct.unpack('<I', f.read(4))
                        print(nbAssets)
                        offset, *_ = struct.unpack('<I', f.read(4))
                        print(offset)
                        addr = 88 + nbAssets*4 + offset
                        addr_out = 4 + len(assets_to_keep)*8
                        f.seek(88)
                        for asset in range(nbAssets):
                                length, *_ = struct.unpack('<I', f.read(4))
                                addr = (addr + 3) & ~3  # Alignment
                                if asset in assets_to_keep:
                                        addr_out = (addr_out + 3) & ~3
                                        assets_data_addr.append(addr)
                                        assets_data_length.append(length)
                                        print(f'Asset #{asset}: {length} bytes @ 0x{addr:05x} --> @ Ox{addr_out:05x}')
                                        output.write(struct.pack('<II', asset, length))
                                        addr_out += length
                                else:
                                        print(f'Asset #{asset}: {length} bytes @ 0x{addr:05x} --> DROPPED')
                                addr += length
                        addr_out = 4 + len(assets_to_keep)*8
                        for asset in range(len(assets_to_keep)):
                                f.seek(assets_data_addr[asset])
                                addr_out = (addr_out + 3) & ~3
                                print(f'COPYING asset #{assets_to_keep[asset]}: {assets_data_length[asset]} bytes @ 0x{assets_data_addr[asset]:05x} --> @ Ox{addr_out:05x}')
                                output.seek(addr_out)
                                output.write(f.read(assets_data_length[asset]))
                                addr_out += assets_data_length[asset]


print('Bundling intflash assets')
bundle_assets(assets_in_intflash, "scripts/smw_assets_in_intflash.dat")
print('Bundling ram assets')
bundle_assets(assets_in_ram, "scripts/smw_assets_in_ram.dat")
print('Bundling extflash assets')
bundle_assets(assets_in_extflash, "scripts/smw_assets_in_extflash.dat")
