import logging

from gpregisters import GPRegisters
from flag import Flag
from helper import Helper
from ram import Ram

class Proc:
  def __init__(self):
    self.helper = Helper()
    super(Proc, self).__setattr__('ram', Ram())
    self.gpregs = GPRegisters([['B', 0x00], ['C', 0x13], ['D', 0x00],
                               ['E', 0xDE], ['H', 0x01], ['L', 0x4D],
                               ['A', 0x00], ['F', 0x01]])
    self.pc = 0x100
    self.sp = 0xFFFE

    # Fancy formatting modifier
    self.__spacing = ""

  def __setattr__(self, attr, value):
    if(attr == 'ram'):
      raise ValueError("Can\'t assign ram variable")
    else:
      super(Proc, self).__setattr__(attr, value)

  def fetch_byte(self):
    insn = self.ram[self.pc]
    self.pc+=1
    return insn

  def fetch_d8(self):
    return self.fetch_byte()

  def fetch_d16(self):
    d16_l = self.fetch_byte()
    d16_h = self.fetch_byte()
    return ((d16_h << 8) | d16_l)

  def invert_d8(self, d8):
    tmp = 0
    for i in range(8):
      if(not (d8 & 0x1)):
        tmp |= (0x1 << i)
      d8 = d8 >> 1
    return d8

  def push_d8(self, d8):
    self.sp -= 1
    self.ram[self.sp] = d8

  def push_d16(self, d16):
    self.sp -= 1
    self.ram[self.sp] = ((d16 >> 8) & 0xFF)
    self.sp -= 1
    self.ram[self.sp] = (d16 & 0xFF)

  def pop_d16(self):
    d16_l = self.ram[self.sp]
    self.sp += 1
    d16_h = self.ram[self.sp]
    self.sp += 1
    return ((d16_h << 8) | d16_l)

  def emulate_cycle(self):
    self.decode_insn()

  def decode_insn(self):
    op1 = self.fetch_byte()
    method_name = "opcode_0x{:02x}".format(op1)
    print("{}0x{:04x}: 0x{:02x}\t".format(self.__spacing, self.pc - 1, op1), end = '')
    method = getattr(self, method_name, self.unknown)
    return method(op1)

  def unknown(self, op1):
    print("Unknown instruction")

  def opcode_0x00(self, op1): #NOP
    print("NOP")

  def opcode_0x01(self, op1): # LD BC, nn
    self.gpregs.B = self.fetch_d8()
    self.gpregs.C = self.fetch_d8()
    print("LD BC,\t0x{:02x}{:02x}".format(self.gpregs.B, self.gpregs.C))

  def opcode_0x05(self, op1): # DEC B
    self.gpregs.B -= 1
    print("DEC B\t; 0x{:02x}".format(self.gpregs.B))

  def opcode_0x06(self, op1): # LD B, n
    self.gpregs.B = self.fetch_d8()
    print("LD B,\t0x{:02x}".format(self.gpregs.B))

  def opcode_0x0d(self, op1): # DEC C
    self.gpregs.C -= 1
    print("DEC C\t\t; 0x{:02x}".format(self.gpregs.C))

  def opcode_0x0e(self, op1): # LD C, n
    self.gpregs.C = self.fetch_byte()
    print("LD C,\t0x{:02x}".format(self.gpregs.C))

  def opcode_0x20(self, op1): # JR NZ, e
    e = self.fetch_byte()
    if(not (self.gpregs.flags & Flag.ZERO)):
      self.pc += (e - 2)
      print("JR NZ, 0x{:02x}\t; true".format(e))
    else:
      print("JR NZ, 0x{:02x}\t; false".format(e))

  def opcode_0x21(self, op1): # LD HL, nn
    self.gpregs.H = self.fetch_d8()
    self.gpregs.L = self.fetch_d8()
    print("LD HL,\t0x{:02x}{:02x}".format(self.gpregs.H, self.gpregs.L))

  def opcode_0x2a(self, op1): # LD HL, (nn)
    d16 = self.fetch_d16()
    self.gpregs.L = self.ram[d16]
    self.gpregs.H = self.ram[d16+1]
    print("LD HL, (0x{:04x})\t; 0x{:02x}{:02x}".format(d16, self.gpregs.H, self.gpregs.L))

  def opcode_0x2f(self, op1): # CPL
    self.gpregs.flags |= Flag.SUBTRACT
    self.gpregs.flags |= Flag.HALFCARRY
    self.gpregs.A = self.invert_d8(self.gpregs.A)
    print("CPL\t; 0x{:02x}".format(self.gpregs.A))

  def opcode_0x31(self, op1): # LD SP, nn
    d16 = self.fetch_d16()
    self.sp = d16
    print("LD SP, 0x{:04x}".format(self.sp))

  def opcode_0x32(self, op1): # LD (nn), A
    d16 = self.fetch_d16()
    self.ram[d16] = self.gpregs.A
    print("LD (0x{:04x}), A\t; 0x{:02x}".format(d16, self.gpregs.A))

  def opcode_0x3e(self, op1): # LD A, n
    self.gpregs.A = self.fetch_d8()
    print("LD A, 0x{:02x}".format(self.gpregs.A))

  def opcode_0x3f(self, op1): # CCF
    self.gpregs.flags ^= Flag.CARRY
    print("CCF\t\t; {:d}".format(self.gpregs.flags & Flag.CARRY))

  def opcode_0xaf(self, op1): # XOR A
    self.gpregs.A = self.gpregs.A ^ self.gpregs.A
    print("XOR A,\tA\t; 0x{:02x}".format(self.gpregs.A))

  def opcode_0xb1(self, op1): # OR C
    self.gpregs.A = self.gpregs.A | self.gpregs.C
    print("OR A,\tC\t; 0x{:02x}".format(self.gpregs.A))

  def opcode_0xc3(self, op1): # JP nn
    d16 = self.fetch_d16()
    self.pc = d16
    print("JP 0x{:04x}".format(self.pc))

  def opcode_0xc9(self, op1): # RET
    d16 = self.pop_d16()
    self.pc = d16
    self.__spacing = ""
    print("RET\t; 0x{:04x}".format(self.pc))

  def opcode_0xcd(self, op1): # CALL nn
    d16 = self.fetch_d16()
    self.push_d16(self.pc)
    self.pc = d16
    self.__spacing = "  "
    print("CALL 0x{:04x}".format(d16))

  def opcode_0xe0(self, op1): # LDH (n), A
    op2 = self.fetch_d8()
    self.ram[(0xFF00 | op2)] = self.gpregs.A
    print("LDH (0x{:02x}), A\t; 0x{:02x}".format((0xFF00 | op2), self.gpregs.A))

  def opcode_0xe6(self, op1): # AND n
    op2 = self.fetch_d8()
    self.gpregs.A &= op2
    print("AND 0x{:02x}\t; 0x{:02x}".format(op2, self.gpregs.A))

  def opcode_0xea(self, op1): # LD (nn), A
    tmp = self.fetch_d16()
    self.ram[tmp] = self.gpregs.A
    print("LD (0x{:04x}), A\t; 0x{:02x}".format(tmp, self.gpregs.A))

  def opcode_0xf0(self, op1): #LDH A, (n)
    op2 = self.fetch_d8()
    self.gpregs.A = self.ram[(0xFF00 | op2)]
    print("LDH A, (0x{:02x})\t; 0x{:02x}".format((0xFF00 | op2), self.gpregs.A))

  def opcode_0xf3(self, op1): # DI
    self.ram[0xFFFF] = 0
    print("DI")

  def opcode_0xfb(self, op1): # EI
    self.ram[0xFFFF] = 1
    print("EI")

  def opcode_0xfc(self, op1): # SET 7, H
    self.gpregs.H = (self.gpregs.H | (1 << 7))
    print("SET 7, H\t; 0x{:02x}".format(self.gpregs.H))

  def opcode_0xfe(self, op1): # CP n
    op2 = self.fetch_byte()
    tmp = self.gpregs.A - op2
    print("CP A, n\t; 0x{:02x}".format(op2))
