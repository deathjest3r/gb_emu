import logging
from array import array

class Loader:
  def __init__(self):
    self.rom_type = ["ROM ONLY", "ROM+MBC", "ROM+MBC1+RAM", "ROM+MBC1+RAM+BATT", "4", "ROM+MBC2",
              "ROM+MBC2+BATTERY", "7", "ROM+RAM", "ROM+RAM+BATTERY", "A", "ROM+MMM01",
              "ROM+MMM01+SRAM", "ROM+MMM01+SRAM+BATT", "E", "F", "10", "11", "ROM+MBC3+RAM",
              "ROM+MBC3+RAM+BATT", "14", "15", "16", "17", "18", "ROM+MBC5", "ROM+MBC5+RAM",
              "ROM+MBC5+RAM+BATT", "ROM+MBC5+RUMBLE", "ROM+MBC5+RUMBLE+SRAM",
              "ROM+MBC5+RUMBLE+SRAM+BATT", "Pocket Camera", "FD-Bandai TAMA5", "FE - Hudson HuC-3" ]
  
  def load_rom(self, path):
    rom_buffer = None
    blocks = 0
    try:
      with open(path, "rb") as rom_fd:
        rom_buffer = rom_fd.read()
        rom_buffer = array('B', rom_buffer)
        logging.info("Loaded rom from {}".format(path))
        logging.info("Rom title: {}".format(''.join(([chr(c) for c in rom_buffer[0x134:0x142]]))))
        if rom_buffer[0x146] == 0x00:
          logging.info("GAME BOY rom")
        elif rom_buffer[0x146] == 0x03:
          logging.info("SUPER Game BOY rom")
        else:
          logging.error("Unknown rom type")

        logging.info("Cartridge type: {}".format(self.rom_type[rom_buffer[0x147]]))

        if rom_buffer[0x148] == 0x0:
          rs = "32 KBytes - 2 Banks"
        #case 0x1: strncpy(rs, "64 KBytes - 4 Banks", 24); break;
        # case 0x2: strncpy(rs, "128 KBytes - 8 Banks", 24); break;
        #case 0x3: strncpy(rs, "256 KBytes - 16 Banks", 24); break;
        # case 0x4: strncpy(rs, "512 KBytes - 32 Banks", 24); break;
        #case 0x5: strncpy(rs, "1 MByte - 64 Banks", 24); break;
        # case 0x6: strncpy(rs, "2 MBytes - 128 Banks", 24); break;
        #case 0x52: strncpy(rs, "1.1 MBytes - 72 Banks", 24); break;
        # case 0x53: strncpy(rs, "1.2 MBytes - 80 Banks", 24); break;
        #case 0x54: strncpy(rs, "1.5 MBytes - 96 Banks", 24); break;
        # default: strncpy(rs, "[ERROR] Unknown", 24); breaku;
        logging.info("ROM Size: {}".format(rs))
        logging.info("RAM Size: TODO")

        if rom_buffer[0x14A] == 0x00:
          logging.info("Destination code: Japanese")
        elif rom_buffer[0x14A] == 0x01:
          logging.info("Destination code: Non-Japanese")
        else:
          logging.error("Unknown destination code")
        
        return rom_buffer
    except IOError:
      logging.error("Can't open {}".format(path))












