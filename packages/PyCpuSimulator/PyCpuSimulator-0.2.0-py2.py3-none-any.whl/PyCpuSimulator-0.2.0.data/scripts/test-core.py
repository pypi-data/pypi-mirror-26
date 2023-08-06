#!python

####################################################################################################
#
# PyCpuSimulator - AVR Simulator
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################
#
# Logging
#

import PyCpuSimulator.Logging.Logging as Logging

logger = Logging.setup_logging('pysimavr')

####################################################################################################

from PyCpuSimulator.Core.CoreHdlParser import Parser
from PyCpuSimulator.Core.Core import (StandardCore,
                                RegisterFile, RamMemory,
                                MappedRegister, Register8, Register16)

####################################################################################################

micro_code_parser = Parser()

ram = RamMemory('RAM', cell_size=8, size=8*1024)

# Define some general purpose registers
general_purpose_registers = [Register8('R' + str(i)) for i in range(4)]

registers = [
    Register16('PC'), # Pointer Counter
    Register16('STACK'), # Stack Pointer
    Register8('SREG'), # AVR Status Register
    Register16('X'),
    MappedRegister('Y', ram.cell(0)), # Y is mapped to ram[0]
]
registers.extend(general_purpose_registers)

# Fixme: X = R27:R26

register_file = RegisterFile('REGISTER', registers)

core = StandardCore(memories=(register_file, ram))

####################################################################################################

print()

source = '''
R0 = 10 + 10;
R1 = 20;
R2 = R0 + R1;
R2 = R2 ^ R2;
R2 = R0 + 30;
X = 0x3;
[X] = R2;
R1 = 1;
if (R1 == 1) {
  R2 = 3;
  [0x4] = 0x1F;
}
else
  R2 = 4;
Y = 23;
'''

rule = '\n' + '-'*100 + '\n'

print(source)

# micro_code_parser.test_lexer(source)
ast_program = micro_code_parser.parse(source)

print(rule)
print(ast_program)

print(rule)
core.run_ast_program(ast_program)

print(rule)
print('RAM:', ram[:10])
