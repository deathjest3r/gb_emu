from gpregister import GPRegister
from flag import Flag

class GPRegisters:
  def __init__(self, regs):
    super(GPRegisters, self).__setattr__('regs', [GPRegister(name, value, self) for (name, value) in regs])
    #self.regs = [Vcpu.Registers.Register(name, value, self) for (name, value) in regs]
    super(GPRegisters, self).__setattr__('flags', 0xB0)
  
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

  def non_zero(self):
    if(self.flags & Flag.ZERO) == 0:
      return
    else:
      pass 
