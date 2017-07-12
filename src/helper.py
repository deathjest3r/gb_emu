
class Helper:
  def __init__(self):
    pass

  def dump_stack(self, ram, sp):
    print(sp)
    print("TOP of STACK:\n-----------------------------------")
    for i in range(sp + 64, sp - 64, -1):
      if (i % 16) == 1:
        print("\n{:04x}: ".format(i), end = '')
      if sp == i:
        print("[{:02x}] ".format(ram[i]), end = '')
      else:
        print(" {:02x}  ".format(ram[i]), end = '')
    print("\n-----------------------------------\n\n")
