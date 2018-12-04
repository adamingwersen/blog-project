import sys
import os


def read_cast_upper(file_in, file_out):
    file_in = open(file_in, 'r')
    file_out = open(file_out, 'w')
    for line in file_in:
        file_out.write(line.upper())
    return(0)

