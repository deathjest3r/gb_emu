from gpregisters import GPRegisters
from ioregisters import IORegisters

class Vcpu:
  def __init__(self):
    self.gpregs = GPRegisters([['B', 0x00], ['C', 0x13], ['D', 0x00], ['E', 0xDE], ['H', 0x01], ['L', 0x4D], ['A', 0x0], ['F', 0x01]])
    self.pc = 0x100
    self.sp = 0xFFFE
#    self.ioregs = IORegisters([['P1', 0x00, 0xFF00], ['SB', 0x00, 0x00F1],
#                              ['SC', 0x00, 0xFF02], ['DIV', 0x00, 0xFF04]],
#                              ['TIMA', 0x00, 0xFF05], ['TMA', 0x00, 0xFF06],
#                             ['TAC', 0x00, 0xFF07], ['NR10', 0x80, 0xFF10],
#                             ['NR11', 0xBF, 0xFF11], ['NR12', 0xF3, 0xFF12],
#                             ['NR14', 0xBF, 0xFF14], ['NR21', 0x3F, 0xFF16],
#                             ['NR22', 0x00, 0xFF17], ['NR24', 0xBF, 0xFF19],
#                             ['NR30', 0x7F, 0xFF1A], ['NR31', 0xFF, 0xFF1B],
#                             ['NR32', 0x9F, 0xFF1C], ['NR33', 0xBF, 0xFF1E],
#                             ['NR41', 0xFF, 0xFF20], ['NR42', 0x00, 0xFF21],
#                             ['NR42', 0x00, 0xFF22], ['NRXX', 0xBF, 0xFF23],
#                             ['NR50', 0x77, 0xFF24], ['NR51', 0xF3, 0xFF25],
#                             ['NR52', 0xF1, 0xFF26], ['LCDC', 0x91, 0xFF40],
#                             ['SCY', 0x00, 0xFF42], ['SCX', 0x00, 0xFF43],
#                             ['LYC', 0x00,x 0xFF45], ['BGP', 0xFC, 0xFF47],
#                             ['OBP0', 0xFF, 0xFF48], ['OBP1', 0xFF, 0xFF49],
#                             ['WY', 0x00, 0xFF4A], ['WX', 0x00, 0xFF4B],
#                             ['IE', 0x00, 0xFFFF]])
