# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Simple Calculator
--------------------------------------------------------------------------
License:   
Copyright 2025 - Sandeep Ramlochan

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple calculator that will 
  - Take in two numbers from the user
  - Take in an operator from the user
  - Perform the mathematical operation and provide the number to the user
  - Repeat

Operations:
  - "+" : addition
  - "-" : subtraction
  - "*" : multiplication
  - "/" : division

Error conditions:
  - Invalid operator --> Program should exit
  - Invalid number   --> Program should exit

--------------------------------------------------------------------------
"""

# NOTE - Add import statements to allow access to Python library functions
# NOTE - Hint:  Look at  https://docs.python.org/3/library/operator.html

import operator

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# NOTE - No constants are needed for this example 

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# NOTE - Global variable to map an operator string (e.g. "+") to 
# NOTE - the appropriate function.
operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    ">>": operator.rshift,
    "<<": operator.lshift,
    "%": operator.mod,
    "**": operator.pow
}



# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

# redefining input
get_input = None # temp
try:
    get_input = raw_input
except NameError:
    get_input = input

def get_user_input():
    """ Get input from the user.
        Returns tuple:  (number, number, function) or 
                        (None, None, None) if inputs invalid
    """
    try:
        number1 = float(get_input("Enter first number : "))
        number2 = float(get_input("Enter second number: "))
        op = input("Enter function (valid values are +, -, *, /, <<, >>, %, **): ")
        func = operators.get(op)
        
        # Integer only operators
        if (op == "<<"  or op == ">>"):
            number1 = int(number1)
            number2 = int(number2)
            
        
        return (number1, number2, func)
        
        
        # NOTE - User input is generally returned as a string and must be translated.
    except:
        print("Invalid Input")
        return (None, None, None)

# End def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == "__main__":

    while True:
        (num1, num2, func) = get_user_input()
        
        if (num1 == None) or (num2 == None) or (func == None):
            print("Invalid input")
            break
        
        print(func(num1, num2))
