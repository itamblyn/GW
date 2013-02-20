#! /usr/bin/python

import os, sys

def example_function(a,b,c=17.5):
    sum = a+b+c
    
return sum


def main():

    try:
        # Attempt to retrieve required input from user
        prog = sys.argv[0]
        a = float(sys.argv[1])
        b = float(sys.argv[2])
    except IndexError:
        # Tell the user what they need to give
        print '\nusage: '+prog+' a b    (where a & b are numbers)\n'
        # Exit the program cleanly
        sys.exit(0)

    # Execute the function defined above
    sum = example_function(a,b)

    print 'sum =',sum


# This executes main() only if executed from shell
if __name__ == '__main__':
    main()
