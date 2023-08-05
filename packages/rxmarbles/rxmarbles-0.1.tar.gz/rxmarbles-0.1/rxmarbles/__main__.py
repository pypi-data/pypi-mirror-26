#!/usr/bin/env python

from __future__ import print_function
from pyparsing import *
import sys
import argparse
import math
import importlib
from .svgshapes import *
from .generator import *


def generate_single(diagram, fileName, args, theme):
        if args.verbose > 0:
            print ("Generating diagram for '%s' => %s" % (diagram[0], fileName))
    
        marbles = diagram[1:]
        r = getObjects(marbles, theme)
        svg = SvgDocument(r, theme, args.scale)
        f = file(fileName, "w")
        f.write(svg.getDocument())
        f.close()

def generate_batch(diagrams, args, theme):
    for diagram in diagrams:
        diagramName = diagram.diagram_name
        filename = diagramName + ".svg"
        generate_single(diagram, filename, args, theme)
        
def main():
    parser = argparse.ArgumentParser(description='Generate marbles from textual representation.')
    parser.add_argument('inputfile', metavar='MARBLES-FILE', type=str, help='path to a text file with marble diagrams')
    parser.add_argument('--scale', type=float, default=100.0, help='scale used to control zoom level of the generated images')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='enables verbose mode')
    parser.add_argument('--output', '-o', default=None, type=str, help='Sets the file name for the output. Note: only first diagram from the input file will be generated.')
    parser.add_argument('--theme', '-t', default='default', type=str, help='Sets the theme used to render SVG output.')
    args = parser.parse_args()
    
    # this is where we import global theme object
    theme = importlib.import_module('rxmarbles.theme.' + args.theme)
    
    diagramsFileName = args.inputfile
    f = open(diagramsFileName, "r")
    a = f.read()
    f.close()
    
    marbleDiagrams = marble_diagrams.parseString(a)
    
    if not args.output is None:
        fileName = args.output
        generate_single(marbleDiagrams[0], fileName, args, theme)
    else:
        generate_batch(marbleDiagrams, args, theme)
            

if __name__ == "__main__":
    main()    
