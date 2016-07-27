import nose
import sys
reload(sys)

sys.setdefaultencoding('UTF8')
# from core.osutils import Logger

# sys.stdout = Logger.Logger("Logs/log.txt")

if __name__ == '__main__':
    arguments = ['nosetests', '-v', '-s', '--with-doctest', '--with-xunit']
    for i in sys.argv:
        arguments.append(str(i))
    nose.run(argv=arguments)

