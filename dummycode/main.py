import os
import sys
import numpy

class Sub(object):
    """
    this is Sub Class
    """
    
    def __init__(self, mode, lang):
        """
        initialize the class
        """
        pass
    
    def run(self, x, y):
        r"""
        Run feature.
        

        Args:
            x (int)   : ``description`` for __x__
                
                .. versionadded:: 1.0.1
            
            y (float) : ``description`` for **y**
                
                .. versionadded:: 1.0.1
            
        Returns:
            out (ndarray) :
                this is the ``description`` for **out**
                
                .. versionadded:: 1.0.1
                .. versionchanged:: 1.2.0
            
        """

class Main(Sub):
    """
    this is Main Class
    """
    
    def __init__(self, mode, lang):
        """
        initialize the class
        """
        pass
    
    def forward(self, x):
        r"""
        forward processes.

        Parameters:
            x : (int)
                this is the ``description`` for `x`
                
                .. versionadded:: 1.0.0

        Returns:
            out : (ndarray)
                  this is the ``description`` for `out`
            
        See Also:
            Sub : Sub class
        
        References:
            https://docs.readthedocs.io/en/latest/index.html
            
        
        Examples:
            >>> import numpy as np
            >>> main = Main()
            >>> if __name__ == '__main__':
            >>>     main.forward()
            >>> ##### testing the extremal of the text box, to verify if the horizontal scrollbar would appear below #####
        

        
        """
        
        out = x
        return out
    
    def backward(self, x):
        """
        backward process
        """
        pass
    

