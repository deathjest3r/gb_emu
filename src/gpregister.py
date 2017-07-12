from flag import Flag

class GPRegister:
  def __init__(self, name, value, regs):
    self.name = name
    self.value = value
    self.regs = regs

  def __and__(self, op):
    if type(op) is int:
      tmp = self.value & op
    elif type(op) is GPRegister:
      tmp = self.value & op.value
    if(tmp == 0):
      self.regs.flags |= Flag.ZERO
    return tmp

  def __or__(self, op):
    if type(op) is int:
      tmp = self.value | op
    elif type(op) is GPRegister:
      tmp = self.value | op.value
    if(tmp == 0):
      self.regs.flags |= Flag.ZERO
    return tmp

  def __xor__(self, op):
    tmp = self.value ^ op.value
    if(tmp == 0):
      self.regs.flags |= Flag.ZERO
    return tmp

  def __rshift__(self, op):
    if type(op) is int:
      tmp = self.value >> op
    elif type(op) is GPRegister:
      tmp = self.value >> op.value
    if(tmp == 0):
      self.regs.flags |= Flag.ZERO
    return tmp

  def __sub__(self, op):
    tmp = self.value - op
    self.regs.flags |= Flag.SUBTRACT
    if(tmp & 0x10):
      self.regs.flags |= Flag.HALFCARRY
    else:
      self.regs.flags &= ~Flag.HALFCARRY
    if(tmp == 0):
      self.regs.flags |= Flag.ZERO
    else:
      self.regs.flags &= ~Flag.ZERO
    if(self.value < op):
      self.regs.flags |= Flag.CARRY
    else:
      self.regs.flags &= ~Flag.CARRY
    return tmp

  def __format__(self, spec):
    return "{:02x}".format(self.value)
