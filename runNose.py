import unittest
import nose
import sys

env='sit'

if __name__ == '__main__':
    arguments=['nosetests','-v','-s','--with-doctest','--with-xunit']
    for i in sys.argv:
        arguments.append(str(i))
    nose.run(argv=arguments)

