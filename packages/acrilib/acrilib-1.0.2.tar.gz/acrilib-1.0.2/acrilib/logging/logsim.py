'''
Created on Oct 11, 2017

@author: arnon
'''

class LogSim(object):
    def __init__(self, file=None):
        self.file = file
        if file:
            self.file = open(file, 'w')
    
    def debug(self, msg):
        self._print('debug', msg)
    
    def info(self, msg):
        self._print('info', msg)
    
    def warning(self, msg):
        self._print('warning', msg)
    
    def error(self, msg):
        self._print('error', msg)
    
    def critical(self, msg):
        self._print('critical', msg)
        
    def _print(self, key, msg):
        print("{}: {}".format(key, msg), file=self.file)
        
    def close(self):
        if self.file:
            self.file.close()
            
    def __del__(self):
        self.close()

