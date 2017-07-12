import array

from gpregister import GPRegister

class Ram:
  def __init__(self):
    self.size = 0x10000
    self.ram = self.size * [0]
    self.ram[0xFF10] = 0x80 # NR10
    self.ram[0xFF11] = 0xBF # NR11
    self.ram[0xFF12] = 0xF3 # NR12
    self.ram[0xFF14] = 0xBF # NR14
    self.ram[0xFF16] = 0x3F # NR21
    self.ram[0xFF19] = 0xBF # NR24
    self.ram[0xFF1A] = 0x7F # NR30
    self.ram[0xFF1B] = 0xFF # NR31
    self.ram[0xFF1C] = 0x9F # NR32
    self.ram[0xFF1E] = 0xBF # NR33
    self.ram[0xFF20] = 0xFF # NR41
    self.ram[0xFF23] = 0xBF 
    self.ram[0xFF24] = 0x77 # NR50
    self.ram[0xFF25] = 0xF3 # NR51
    self.ram[0xFF26] = 0xF1 # NR52
    self.ram[0xFF40] = 0x91 # LCDC 
    self.ram[0xFF47] = 0xFC # BGP 
    self.ram[0xFF48] = 0xFF # OBP0
    self.ram[0xFF49] = 0xFF # OBP1

  def __check_length(self, val):
    if(val > 0xff):
      raise TypeError("Trying to assign > 8Bit value to ram address")

  def __setitem__(self, idx, val):
    if type(val) is int:
      self.__check_length(val)
      self.ram[idx] = val
    elif type(val) is GPRegister:
      self.__check_length(val.value)
      self.ram[idx] = val.value
    elif type(val) is array.array:
      for i in val:
        self.__check_length(i)
      self.ram[idx:len(val)] = val[:]

  def __getitem__(self, idx):
    #print("GETTING")
    return self.ram[idx]
