
B = 0x0
C = 0x1
D = 0x2
E = 0x3
H = 0x4
L = 0x5
A = 0x7

class Helper:
  def __init__(self):
    pass

  def decode_gp_reg(self, enc):
    if enc == A: return 'A'
    elif enc == B: return 'B'
    elif enc == C: return 'C'
    elif enc == D: return 'D'
    elif enc == E: return 'E'
    elif enc == H: return 'H'
    elif enc == L: return 'L'
    return '?'

  def dump_stack(self):
    print("TOP of STACK:\n-----------------------------------")
    for i in range(255, 191):
      if (i % 16) == 15:
        print("\n{:04x}: ".format(i))
      if proc_state.vcpu.sp == i:
        print("[{:02x}] ".format(proc_state.ram[i]))
      else:
        print(" {:02x}".format(proc_state.ram[i]))
    print("\n-----------------------------------\n\n")
