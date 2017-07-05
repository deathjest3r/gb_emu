
class Vcpu:
  class Registers:
    CARRY_FLAG           = 0x10 # C
    HALFCARRY_FLAG       = 0x20 # H
    SUBTRACT_FLAG        = 0x40 # N
    ZERO_FLAG            = 0x80 # Z

    class Register:
      def __init__(self, name, value, regs):
        self.name = name
        self.value = value
        self.regs = regs

      def __or__(self, op):
        if type(op) is int:
          return (self.value | op)
        elif type(op) is Vcpu.Registers.Register:
          return (self.value | op.value)

      def __xor__(self, op):
        tmp = self.value ^ op.value
        if(tmp == 0):
          self.regs.flags |= Vcpu.Registers.ZERO_FLAG
        return tmp
      
      def __isub__(self, op):
        self.value -= op
        return self.value

      def __format__(self, spec):
        return "{:02x}".format(self.value)

    def __init__(self, regs):
      super(Vcpu.Registers, self).__setattr__('regs', [Vcpu.Registers.Register(name, value, self) for (name, value) in regs])
      #self.regs = [Vcpu.Registers.Register(name, value, self) for (name, value) in regs]
      super(Vcpu.Registers, self).__setattr__('flags', 0xB0)
    
    def __setattr__(self, attr, value):
      for reg in self.regs:
          if reg.name == attr:
            reg.value = value
            break
      #self.regs[attr] = value
   
    def __getattr__(self, attr):
      for reg in self.regs:
        if reg.name == attr:
          return reg

    def s_reg(self, op):
      reg = (op & 0x07)
      if(reg == 0x07): return self.A
      elif(reg == 0x00) : return self.B
      elif(reg == 0x01) : return self.C
      elif(reg == 0x02) : return self.D
      elif(reg == 0x03) : return self.E
      elif(reg == 0x04) : return self.H
      elif(reg == 0x05) : return self.L

    def non_zero(self):
      if(self.flags & ZERO) == 0:
        return
      else:
        pass 

  def __init__(self):
    self.gp = Vcpu.Registers([['B', 0x00], ['C', 0x13], ['D', 0x00], ['E', 0xDE], ['H', 0x01], ['L', 0x4D], ['A', 0x0], ['F', 0x01]])
    self.pc = 0x100
    self.sp = 0xFFFE
    self.ioregs = 42 * [0]

  

