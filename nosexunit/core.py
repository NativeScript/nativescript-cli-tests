# -*- coding: utf-8 -*-
import StringIO
import codecs
import logging
import os
import sys
import time
import traceback

import nosexunit.const as nconst
import nosexunit.tools as ntools


# Get a logger
logger = logging.getLogger('%s.%s' % (nconst.LOGGER, __name__))

class StdRecorder:
    '''Class to capture the standard outputs'''

    def __init__(self, fd):
        '''Initialize with an empty record'''
        # Initialize record
        self.record = None
        # Do not record directly
        self.rec = False
        # Try to get the encoding with the stream
        try: self.encoding = fd.encoding
        # No encoding attribute
        except AttributeError: self.encoding = None
        # If not specified, set to UTF-8
        if self.encoding is None: self.encoding = 'utf-8'
        # Save the stream for
        self.save = fd
        # Prepare the record
        self.reset()

    def __getattr__(self, attr):
        '''Call the functions on the output'''
        return getattr(self.save, attr)

    def write(self, value):
        '''Write on the record and on the standard output'''
        # Check if UTF-8 value
        if isinstance(value, unicode):
            # Write on record
            if self.rec: self.record.write(value)
            # Encode to write output
            self.save.write(value.encode(self.encoding, 'replace'))
        # Basic string
        else:
            # Write on record but decode before
            if self.rec: self.record.write(value.decode(self.encoding, 'replace'))
            # Write on default
            return self.save.write(value)

    def start(self):
        '''Start to record the stream given by constructor'''
        self.rec = True

    def stop(self):
        '''Stop recording the steam given by constructor'''
        self.rec = False

    def content(self):
        '''Return the content of the record'''
        return self.record.getvalue()

    def reset(self):
        '''Reset the recorder'''
        self.record = StringIO.StringIO()

    def end(self):
        '''End the recorder'''
        self.stop()

class StdOutRecoder(StdRecorder):
    '''Class to record the standard output'''

    def __init__(self):
        '''Replace the sys.stdout output by this one'''
        StdRecorder.__init__(self, sys.stdout)
        sys.stdout = self

    def end(self):
        '''Replace the sys.stdout output by his old value'''
        StdRecorder.end(self)
        sys.stdout = self.save

class StdErrRecorder(StdRecorder):
    '''Class to record the error output'''

    def __init__(self):
        '''Replace the sys.stderr output by this one'''
        StdRecorder.__init__(self, sys.stderr)
        sys.stderr = self

    def end(self):
        '''Replace the sys.stderr output by his old value'''
        StdRecorder.end(self)
        sys.stderr = self.save

class XTestElmt:
    '''Root class for suites and tests'''

    def __init__(self):
        '''Initialize the test element'''
        self.begin = None
        self.end = None

    def start(self):
        '''Set the start time'''
        self.begin = time.time()

    def stop(self):
        '''Set the end time'''
        self.end = time.time()

    def setStart(self, begin):
        '''Set the start time'''
        self.begin = begin

    def setStop(self, end):
        '''Set the end time'''
        self.end = end

    def getTime(self):
        '''Get the running time'''
        if self.begin != None and self.end != None:
            return self.end - self.begin
        else: return nconst.UNK_TIME

class XSuite(XTestElmt):
    '''Class for the suite notion'''

    def __init__(self, module):
        '''Init the suite'''
        XTestElmt.__init__(self)
        self.module = module
        self.tests = []
        self.count = {}
        self.stdout = ''
        self.stderr = ''

    def setStderr(self, string):
        '''Set the standard outputs for the suite'''
        self.stderr = string

    def setStdout(self, string):
        '''Set the error outputs for the suite'''
        self.stdout = string

    def getName(self):
        '''Get the name of the suite'''
        return self.module

    def addTest(self, test):
        '''Add a test in the right section'''
        self.tests.append(test)
        kind = test.getKind()
        if self.count.has_key(kind): self.count[kind] += 1
        else: self.count[kind] = 1

    def getNbrTests(self):
        '''Return the total number of test'''
        nbrTests = 0
        for kind in self.count.keys():
            nbrTests += self.count[kind]
        return nbrTests

    def getNbrTestsFromKind(self, kind):
        '''Get the number of tests given the kind'''
        if self.count.has_key(kind):
            return self.count[kind]
        else: return 0

    def getNbrTestsFromKinds(self, kinds):
        '''Get the number of tests given the kind'''
        nbrTests = 0
        for kind in kinds:
            nbrTests += self.getNbrTestsFromKind(kind)
        return nbrTests

    def getXmlName(self, folder):
        '''
        Return the name of the suite for the XML
        Avoid data erasing
        '''
        name = self.getName()
        path = self.getXmlPath(folder, name)
        if not os.path.exists(path): return name
        else:
            cpt = 1
            while True:
                name = "%s.%d" % (self.getName(), cpt)
                path = self.getXmlPath(folder, name)
                if not os.path.exists(path): return name
                cpt += 1

    def getXmlPath(self, folder, xml_name):
        '''Return the output xml path'''
        return os.path.join(folder, '%s%s.xml' % (nconst.PREFIX_CORE, xml_name))

    def writeXml(self, folder):
        '''Write the xml file on disk'''
        if self.getNbrTestsFromKinds([nconst.TEST_SUCCESS, nconst.TEST_FAIL, nconst.TEST_ERROR, ]) > 0:
            xname = self.getXmlName(folder)
            xpath = self.getXmlPath(folder, "Report")
            xfile = codecs.open(xpath, 'w', encoding='utf-8')
            self.writeXmlOnStream(xfile, xname)
            xfile.close()

    def writeXmlOnStream(self, stream, xname):
        '''Write the test suite on the stream'''
        nbrTests = self.getNbrTestsFromKinds([nconst.TEST_SUCCESS, nconst.TEST_FAIL, nconst.TEST_ERROR, ])
        nbrFails = self.getNbrTestsFromKind(nconst.TEST_FAIL)
        nbrErrors = self.getNbrTestsFromKind(nconst.TEST_ERROR)
        stream.write('<?xml version="1.0" encoding="UTF-8"?>')
        stream.write('<testsuite name="%s" tests="%d" errors="%d" failures="%d" time="%.3f">' % (xname, nbrTests, nbrErrors, nbrFails, self.getTime()))
        for test in self.tests:
            test.writeXmlOnStream(stream)
        stream.write('<system-out><![CDATA[%s]]></system-out>' % self.stdout)
        stream.write('<system-err><![CDATA[%s]]></system-err>' % self.stderr)
        stream.write('</testsuite>')

class XTest(XTestElmt):
    '''Class for the test notion'''

    def __init__(self, kind, elmt, err=None):
        '''Init the test result'''
        XTestElmt.__init__(self)
        self.elmt = elmt
        self.kind = kind
        self.err = err

    def getKind(self):
        '''Return the kind of text'''
        return self.kind

    def getName(self):
        '''Return the name of the method'''
        return '.'.join(ntools.get_test_id(self.elmt).split('.')[2:])

    def getClass(self):
        '''Return the class name'''
        return '.'.join(ntools.get_test_id(self.elmt).split('.')[:2])

    def _get_err_type(self):
        '''Return the human readable error type for err'''
        if self.err != None:
            if isinstance(self.err, tuple): return '%s.%s' % (self.err[1].__class__.__module__, self.err[1].__class__.__name__)
            else:
                lines = self.err.replace('\r', '').split('\n')
                while len(lines) != 0 and lines[-1].strip() == '': lines.pop()
                if len(lines) != 0:
                    err_type = lines[-1].strip().split()[0]
                    if err_type[-1] == ':': err_type = err_type[:-1]
                    return err_type
                else: return nconst.UNK_ERR_TYPE
        else: return None

    def _get_err_formated(self):
        '''Return the the formated error for output'''
        if self.err != None:
            if isinstance(self.err, tuple): return '<![CDATA[%s]]>' % '\n'.join((''.join(traceback.format_exception(*self.err))).split('\n')[:-1])
            else: return '<![CDATA[%s]]>' % self.err
        else: return None

    def writeXmlOnStream(self, stream):
        '''Write the xml result on the stream'''
        if self.kind in [nconst.TEST_SUCCESS, nconst.TEST_FAIL, nconst.TEST_ERROR, ]:
            stream.write('<testcase classname="%s' % self.getClass().replace("__main__.", "") + '" name="%s' % self.getName() + '"' + ' time="%.3f"' % self.getTime())
#            if self.kind == nconst.TEST_SUCCESS: stream.write('/>')
#            else:
            stream.write('>')
            tag = "success"
            if self.kind == nconst.TEST_ERROR: tag = 'error'
            if self.kind == nconst.TEST_FAIL: tag = 'failure'
            stream.write('<%s type="%s">' % (tag, self._get_err_type()))
            stream.write(self._get_err_formated())
            stream.write('</%s>' % tag)
            stream.write('</testcase>')
