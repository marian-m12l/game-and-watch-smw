import struct

assets_location = [
        (0,     'ram'),          # Graphics                     (144582 B)
        (1,     'ram'),          # Graphics 32                   (23808 B)
        (2,     'ram'),          # Graphics 33                   (9216 B)
        (3,     'ram'),          # Strip Image                   (9205 B)
        (4,     'ram'),          # Layer3 Image                  (5400 B)
        (5,     'ram'),          # Overworld Layer2 Tiles        (3328 B)
        #(6,     'ram'),          # Credits Music                 (6624 B)
        (7,     'ram'),          # Level Music                   (16899 B)
        (8,     'ram'),          # SPC engine                    (6323 B)
        (9,     'ram'),          # SPC samples                   (28538 B)
        (10,    'ram'),          # Overworld music               (5667 B)
        (11,    'ram'),          # Map16 Overworld Layer1        (1544 B)
        (12,    'ram'),          # Overworld Layer2 Tile Props   (1664 B)
        (13,    'ram'),          # Map16 Data                    (8448 B)
        (14,    'ram'),          # Map16 Castle                  (1424 B)
        (15,    'ram'),          # Map16 Rope                    (1424 B)
        (16,    'ram'),          # Map16 Underground             (1424 B)
        (17,    'ram'),          # Map16 GhostHouse              (1424 B)
        #(18,    'ram')          # Ending Cinema Tilemaps        (1873 B)
        #(19,    'ram')          # Ending Cinema Rows            (404 B)
        (20,    'ram'),          # Level Info                    (512 B)
        (21,    'ram'),          # Level Info                    (512 B)
        (22,    'ram'),          # Level Info                    (512 B)
        (23,    'ram'),          # Level Info                    (512 B)
        (24,    'ram'),          # Level Info                    (512 B)
        (25,    'ram'),          # Level Info                    (512 B)
        (26,    'ram'),          # Level Info                    (512 B)
        (27,    'ram'),          # Level Info                    (512 B)
        (28,    'ram'),          # Load Level Data               (256 B)
        #(29,    'ram')          # Display Message               (2854 B)
        (30,    'ram'),          # Overworld Lightning Clouds    (128 B)
        (31,    'ram'),          # Level Names                   (512 B)
        (32,    'ram'),          # Overworld Layer2 Tilemap      (6904 B)
        (33,    'ram'),          # Overworld Layer2 Tilemap Props(5709 B)
        (34,    'ram'),          # Overworld Layer1 Data         (2048 B)
        (35,    'ram'),          # Line Guide Speed Table Data   (536 B)
        (36,    'ram'),          # Level Data Layer1             (40654 B)
        (37,    'ram'),          # Entrance Data Layer1          (120 B)
        (38,    'ram'),          # Chocolate Island Layer1       (863 B)
        (39,    'ram'),          # Roll Call Layer1              (329 B)
        (40,    'ram'),          # Level Data Layer2             (10666 B)
        (41,    'ram'),          # Level Data Layer2 IsBg        (512 B)
        (42,    'ram'),          # Entrance Data Layer2          (1223 B)
        (43,    'ram'),          # Entrance Data Layer2 IsBg     (6 B)
        (44,    'ram'),          # Chocolate Island Layer2       (439 B)
        (45,    'ram'),          # Chocolate Island Layer2 IsBg  (9 B)
        (46,    'ram'),          # Roll Call Layer2              (5830 B)
        (47,    'ram'),          # Roll Call Layer2 IsBG         (13 B)
        #(48,    'ram'),          # Credits Background Layer2     (3383 B)
        #(49,    'ram'),          # Credits Background Layer2 IsBg(7 B)
        (50,    'ram'),          # Load Level Sprite List        (9901 B)
        (51,    'ram'),          # Load Level Sprite Data        (1024 B)
        (52,    'ram'),          # File Select Text              (407 B)
        (53,    'ram'),          # Mode7 Tilemap Data            (912 B)
        (54,    'ram'),          # Layer2 Tile Entries           (1484 B)
        #(55,    'ram'),          # Level Name Strings            (460 B)
        (56,    'ram'),          # Show Enemy Roll Call Tile     (1681 B)
        #(57,    'ram')          # Whole ROM file                (524288 B)
        
        # FIXME asset 57 is the whole rom file (512KB) --> no need to package it!
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
