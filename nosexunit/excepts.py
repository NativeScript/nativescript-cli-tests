#-*- coding: utf-8 -*-

class NoseXUnitError(StandardError):
    '''Super class of error for NoseXunit'''
    pass

class PluginError(NoseXUnitError):
    '''Class of exception for plug in'''
    pass

class CoreError(NoseXUnitError):
    '''Class of exception for XUnit'''
    pass

class AuditError(NoseXUnitError):
    '''Class of exception for PyLint'''
    pass

class CoverError(NoseXUnitError):
    '''Class of exception for Coverage'''
    pass

class ToolError(NoseXUnitError):
    '''Class of exception for tools'''
    pass
    
    