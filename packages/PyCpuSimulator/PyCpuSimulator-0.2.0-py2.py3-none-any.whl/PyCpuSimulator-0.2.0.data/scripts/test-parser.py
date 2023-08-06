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

"""Test the HDL parser.
"""

####################################################################################################
#
# Logging
#

import PyCpuSimulator.Logging.Logging as Logging

logger = Logging.setup_logging('pysimavr')

####################################################################################################

from PyCpuSimulator.Core.CoreHdlParser import Parser

micro_code_parser = Parser()

source = '''
R0 = 10; R2 = 10;
R1 = 20;

if (R1)
  R0 = 10;
else {
  R0 = 10; R2 = 10;
  R1 = 20;
  Foo (R2, 1 + 1);
}

if (R1)
  R0 = 10;
else if (R2)
   R5 = 10;

'''

rule = '\n' + '-'*100 + '\n'

print(source)

print(rule)
micro_code_parser.test_lexer(source)

print(rule)
ast_program = micro_code_parser.parse(source)
print(ast_program)
