#-*- coding: utf-8 -*-
import os
import time
import shutil
import logging
import datetime
import compiler
import StringIO
import traceback

import nosexunit
import nosexunit.const as nconst
import nosexunit.tools as ntools
import nosexunit.cyclo as ncyclo

# Get a logger
logger =  logging.getLogger('%s.%s' % (nconst.LOGGER, __name__))

try:
    import coverage
except: pass

class Source(object):
    '''Representation a source file'''

    def __init__(self, full, all=0, exe=0, err=None):
        '''Initialize the source'''
        # Store the description
        self.i_full = full
        # Store the number of statements
        self.i_all = all
        # Store the number of executed statements
        self.i_exe = exe
        # Store the error
        self.i_err = err
        # Get the complexity
        self.i_cyclo = None
        # Store the total lines number
        self.i_lines = 0
        
    def full(self):
        '''Get the description'''
        return self.i_full

    def all(self):
        '''Get the number of statements'''
        return self.i_all
    
    def exe(self):
        '''Get the number of executed statements'''
        return self.i_exe
    
    def err(self):
        '''Get the error'''
        return self.i_err
    
    def has_err(self):
        '''Return True if has error'''
        return self.i_err is not None

    def percent(self):
        '''Return coverage percentage: 0 - 100'''
        try: return 100 * float(self.exe()) / self.all()
        except ZeroDivisionError: return 100

    def cyclonize(self, content):
        '''Get the complexity'''
        # Try to get
        try:
            # Get the AST
            ast = compiler.parse('%s\n\n' % content)
            # Get the visitor
            visitor = ncyclo.PathGraphingAstVisitor()
            # Go threw
            visitor.preorder(ast, visitor)
            # Store the complexity
            self.i_cyclo = max([ graph.complexity() for graph in visitor.graphs.values() ])
        # Failed to do it
        except: logger.error('failed to cyclonize %s' % self.full())

    def linize(self, lines):
        '''Store the code lines'''
        self.i_lines = lines

    def cyclo(self):
        '''Get the complexity'''
        if self.i_cyclo is None: return 0
        else: return self.i_cyclo

    def lines(self):
        '''Get the line of code'''
        return self.i_lines

    def __str__(self):
        '''String representation'''
        return self.full()

class Sources(list):
    '''Store the sources'''
    
    def percent(self):
        '''Get the global coverage: 0 - 100'''
        try: return 100 * float(sum([ source.exe() for source in self if not source.has_err() ])) / sum([ source.all() for source in self if not source.has_err() ])
        except ZeroDivisionError: return 100
        
    def all(self):
        '''Get the global number of statements'''
        return sum([ source.all() for source in self ])

    def exe(self):
        '''Get the global number of executed statements'''
        return sum([ source.exe() for source in self ])
    
    def cyclo(self):
        '''Get the complexity'''
        return max([ source.cyclo() for source in self ])
    
    def lines(self):
        '''Get the line number'''
        return sum([ source.lines() for source in self ])

def report(target, sources):
    '''Create report'''
    # Extract the Java Script and the CSS
    ntools.extract_pic_js_css(target)
    # Get the date
    date = datetime.datetime.now()
    # Process the index
    ntools.kiding(__name__, 'index.html', target)
    # Process the listing
    ntools.kiding(__name__, 'listing.html', target, sources=sources, date=date)
    # Process the abstract
    ntools.kiding(__name__, 'abstract.html', target, sources=sources, date=date)
    # Get CSS class
    cls = {'>': 'covered',
           '!': 'uncovered',
           '-': 'skipped',
           ' ': 'no', }
    # Go threw the sources
    for entity in sources:
        # Try to process the package
        try:
            # Get the path of the coverage file
            path = os.path.join(target, '%s.py,cover' % entity.full())
            # Check if has error
            if entity.has_err(): ntools.kiding(__name__, 'error.html', target, bn='%s-code.html' % entity.full(), entity=entity, error=entity.err(), date=date)
            # Coverage file doesn't exists
            elif not os.path.isfile(path): ntools.kiding(__name__, 'error.html', target, bn='%s-code.html' % entity.full(), entity=entity, error="Coverage file doesn't exists", date=date)
            # Got file to process
            else:
                # Store the source content
                content = []
                # Store annotation
                data = []
                # Go threw the lines to fill content and data
                for line in ntools.load(path).splitlines():
                    # Set data
                    data.append(cls[line[0]])
                    # Get the content. If void, add a space
                    if line[2:] == '': content.append(' ')
                    # Else add the content
                    else: content.append(line[2:])
                # Get the text
                text = '%s' % ('\n'.join(content), )
                # Get the highlighted lines
                lines = ntools.highlight(text)
                # Get complexity
                entity.cyclonize(text)
                # Set lines
                entity.linize(len(content))
                # Fill data in case of file without content
                while len(data) < len(lines): data.append(' ')
                # Process the code
                try: ntools.kiding(__name__, 'code.html', target, bn='%s-code.html' % entity.full(), entity=entity, lines=lines, data=data, date=date)
                # Unable to create source
                except:
                    # Log the error
                    logger.error(traceback.format_exc())
                    # Create the error page
                    ntools.kiding(__name__, 'error.html', target, bn='%s-code.html' % entity.full(), entity=entity, error='Failed to highlight source code', date=date)
        # Unable to process the package
        except: logger.error(traceback.format_exc())
    # Create the COBERTURA and CLOVER reports
    for fn in ['cobertura.xml', 'clover.xml', ]: ntools.kiding(__name__, fn, target, output='xml', sources=sources, version=nosexunit.__version__, date='%d' % time.mktime(date.timetuple()))

def parse(content):
    '''Parse the report'''
    # Get the object containing the sources
    sources = Sources()
    # Get the lines of the report
    lines = content.replace('\r', '').split('\n')
    # Search statements entry
    e_all = lines[0].index('Stmts') - 1
    # Search execution entry
    e_exe = lines[0].index('Exec') - 2
    # True if has to record data
    record = False
    # Go threw the lines of the report
    for line in lines:
        # Check if not void
        if line.strip() != '':
            # Check the beginning and the end of the report
            if line.startswith('----'):
                # Start or stop recording
                record = not record
            # Check if in record section
            elif record:
                # Try to get the source
                try:
                    # Get the source with no error
                    source = Source(line[:e_all].strip(),
                                    all=int(line[e_all:e_all+6]),
                                    exe=int(line[e_exe:e_exe+6]))
                except:
                    # Get the source with error
                    source = Source(line[:e_all].strip(),
                                    err=line[e_all:].strip())
                # Add source to the sources
                sources.append(source)
    # Return the sources
    return sources

def available():
    '''Check if coverage is available'''
    # Try to get coverage
    try:
        # All needed modules
        import kid
        import coverage
        import pygments
        import pygments.lexers
        import pygments.formatters
    # Unable to get it
    except BaseException, e: return False, str(e)    # pylint: disable-msg=E0601
    # OK, it's available
    return True, None

def start(clean, packages, target):
    '''Start the coverage'''
    # Set the coverage data storing path
    os.environ['COVERAGE_FILE'] = os.path.join(target, nconst.COVER_OUTPUT_BASE)
    # Check if clean
    if clean: ntools.clean(target, nconst.COVER_OUTPUT_BASE)
    # Start
    coverage.start()
    # Load packages
    for package in packages:
        # Try to get it
        try: __import__(package)
        # Unable to get it, don't care
        except: pass

def stop(stream, packages, target, collect=False):
    '''Stop coverage'''
    # Call stop
    coverage.stop()
    # Collect if asked
    if collect: coverage.the_coverage.collect()
    # Get the file descriptor for the report
    fd = StringIO.StringIO()
    # Get the report
    coverage.report(packages, file=fd)
    # Flush
    fd.flush()
    # Write on stream
    stream.write(fd.getvalue())
    # Write in target
    ntools.save(fd.getvalue(), os.path.join(target, 'coverage.dat'), binary=False)
    # Get the sources
    sources = parse(fd.getvalue())
    # Close the file descriptor
    fd.close()
    # Annotate source files
    annotate(packages, target, ignore_errors=True)
    # Create report
    report(target, sources)

def annotate(morfs, directory, ignore_errors=0, omit_prefixes=[]):
    '''Copied from coverage to be able to specify file'''
    # Filter files
    morfs = coverage.the_coverage.filter_by_prefix(morfs, omit_prefixes)
    # Go threw the modules
    for morf in morfs:
        # Try to perform annotation
        try:
            # Get the data on the module 
            filename, statements, excluded, missing, _ = coverage.the_coverage.analysis2(morf)
            # In order to generate the ?cover at the right place, we're obliges to copy the source file in the destination folder
            path = os.path.join(directory, '%s.py' % morf.__name__)
            # Actually copy the source
            shutil.copyfile(filename, path)
            # Process the file
            coverage.the_coverage.annotate_file(path, statements, excluded, missing, directory)
            # Delete file
            os.remove(path)
        # Get user interruption
        except KeyboardInterrupt: raise
        # Get other exceptions
        except:
            # Log the error
            logger.error(traceback.format_exc())
            # Check if ignore errors
            if not ignore_errors: raise

