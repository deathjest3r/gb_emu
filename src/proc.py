import logging

from vcpu import Vcpu
from helper import Helper

class Ram:
  def __init__(self):
    self.size = 0xffff
    self.ram = self.size * [0]
  
  def __setitem__(self, idx, val):
    if type(val) is int:
      self.ram[idx] = val
    elif type(val) is Vcpu.Registers.Register:
      self.ram[idx] = val.value

  def __getitem__(self, idx):
    #print("GETTING")
    return self.ram[idx]

class Proc:
  def __init__(self):
    self.vcpu = Vcpu()
    self.helper = Helper()
    super(Proc, self).__setattr__('ram', Ram())

  def __setattr__(self, attr, value):
    if(attr == 'ram'):
      self.ram.ram = value
    else:
      super(Proc, self).__setattr__(attr, value)

  def fetch_byte(self):
    insn = self.ram[self.vcpu.pc]
    self.vcpu.pc+=1
    return insn

  def emulate_cycle(self):
    self.decode_insn()

  def decode_insn(self):
    op1 = self.fetch_byte()
    method_name = "opcode_0x{:02x}".format(op1)
    print("0x{:04x}:\t0x{:02x}\t".format(self.vcpu.pc - 1, op1), end = '')
    method = getattr(self, method_name, self.unknown)
    return method(op1)

  def unknown(self, op1):
    print("Unknown instruction")

  def opcode_0x00(self, op1): #NOP
    print("NOP")

  def opcode_0x06(self, op1): # LD B, n
    self.vcpu.gp.B = self.fetch_byte()
    print("LD B,\t0x{:02x}".format(self.vcpu.gp.B))

  def opcode_0x0d(self, op1): # DEC C
    self.vcpu.gp.C -= 1
    print("DEC C\t; 0x{:02x}".format(self.vcpu.gp.C))

  def opcode_0x0e(self, op1): # LD C, n
    self.vcpu.gp.C = self.fetch_byte()
    print("LD C,\t0x{:02x}".format(self.vcpu.gp.C))

  def opcode_0x21(self, op1): # LD HL, nn
    self.vcpu.gp.H = self.fetch_byte()
    self.vcpu.gp.L = self.fetch_byte()
    print("LD HL,\t0x{:02x}{:02x}".format(self.vcpu.gp.H, self.vcpu.gp.L))

  def opcode_0x32(self, op1): # LD (nn), A
    op2 = self.fetch_byte()
    op3 = self.fetch_byte()
    tmp = ((op3 << 8) | op2)
    self.ram[tmp] = self.vcpu.gp.A
    print("LD (0x{:04x}), A\t; 0x{:02x}".format(tmp, self.vcpu.gp.A))

  def opcode_0xc3(self, op1): # JP nn
    op2 = self.fetch_byte()
    op3 = self.fetch_byte()
    self.vcpu.pc = (op3 << 8) | op2
    print("JP 0x{:04x}".format(self.vcpu.pc))

  def opcode_0xaf(self, op1): # XOR A
    self.vcpu.gp.A = self.vcpu.gp.A ^ self.vcpu.gp.s_reg(op1)
    print("XOR A,\tA\t; {:x}".format(self.vcpu.gp.s_reg(op1)))

  def opcode_0xfc(self, op1): # SET 7, H
    self.vcpu.gp.H = (self.vcpu.gp.H | (1 << 7))
    print("SET 7, H\t; {:x}".format(self.vcpu.gp.H))
