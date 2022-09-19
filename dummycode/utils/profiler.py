#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: winson

This is smart-profiling script to track the performance of any `class object` or functions.



HOW TO USE:
OPTIONS 1 :--
to only profile certain `function` or `class`,
inside the script:
    
from profiler import profiling

@profiling()
class Model:
    def function1():
        pass
    
    def function2():
        pass

model = Model()
model.function1()              # <-- it shows the breakdown of all time spend in this operation
model.function2()              # <-- it shows the breakdown of all time spend in this operation
show_profiling_in_timeseries() $ <-- it shows time spend of this ops in chronological order


OPTIONS 2 :--
to profile all classes and functions in a module-script,
we assume the folder is as such:
- folder
    |- __init__.py
    |- api.py
    |- utils.py
    |- models.py
    |- io.py
    
then, inside __init__.py, add in this:
    from dummycode.utils.profiler import init_profiling
    from . import api     # <-- or import any module-script which needs profiling.
    init_profiling(api)   # <-- it crawls all classes and functions in script, and add `time-profiler` to all of them.

"""



import os
import time
import numpy as np
from functools import wraps
from decimal import Decimal
from collections import defaultdict
from inspect import isclass, isfunction
from .visual import header, lgreen, pink, cyan, VISUAL_CONFIG

################################ CONFIGURATION #################################
PROFILING = os.environ.get('SHOW_PROFILING')
PROFILING = {
    "0"     : False,
    "-1"    : False,
    "False" : False,
    "1"     : True,
    "True"  : True,
    }.get(PROFILING, True)

class PROFILECONFIG:
    show_profiling           = PROFILING
    visual_config            = VISUAL_CONFIG
    max_profiler_disp        = 70
    expanded_tree_tab_deco   = '  '
    expanded_tree_bullets    = '|-> '
    
PROFILE_CONFIG = PROFILECONFIG()
################################################################################


def print_(*args, **kwargs):
    if PROFILE_CONFIG.show_profiling:
        return print(*args, **kwargs)

def head(x,n=80, pop=True):
    if PROFILE_CONFIG.show_profiling:
        return header(x,n=n,pop=True)

highlight         = "\x1b[1;30;43m{}\x1b[0m" ## highlight in yellow
overall_profile   = defaultdict(list)
overall_timestamp = []
reset_new_profile = True
longest_name      = 0

def reset_profiler():
    global overall_profile
    global overall_timestamp
    global reset_new_profile
    reset_new_profile = True
    overall_profile   = defaultdict(list)
    overall_timestamp = []
    

def show_profiling_stats():
    global overall_profile
    global overall_timestamp
    global longest_name
    cyan(head('PROFILING STATS (AVERAGE)'))
    longest_name = min(max([len(i) for i in overall_profile.keys()]), PROFILE_CONFIG.max_profiler_disp)
    for k,vs in overall_profile.items():
        k = str(k).ljust(longest_name)
        v = list(zip(*vs))[-1]
        t = str(round(Decimal(np.average(v)),6)).ljust(8)
        T = str(round(Decimal(np.sum(v)),6)).ljust(8)
        t = lgreen(  f"{t}s @ {str(len(v)).ljust(2)} executions. ", pop=True)
        D = pink( f"Total {T}s", pop=True)
        name = f"{k[:longest_name]} : "
        if float(T) > 1 and '.predict_preprocess' not in k:
            name = highlight.format(name[5:])
        print_(name+t+D) 


def profiling_stats_track(func):
    """
        to calc the function execution time.
        How to use:
        
        @profiling_stats_main
        def resize(x):
            return cv2.resize(x,(10,10))
        
        resize(np.ones((3000,3000))).shape
        >>> time for resize :  0.000149
    """
    @wraps(func)
    def time_function(*args, **kwargs):
        global reset_new_profile
        global overall_profile
        global overall_timestamp
        profiling_main_node = False
        if reset_new_profile:
            reset_profiler()
            profiling_main_node = True
            reset_new_profile   = False
        s = time.time()
        x = func(*args, **kwargs)
        name     = '{}.{}'.format(func.__module__,func.__qualname__)
        e = time.time()
        duration = round(e-s,6)
        overall_profile[name] += [(s,e,duration)]
        overall_timestamp.insert(0,(s,e,duration,name))
        if profiling_main_node:
            if PROFILING:
                print_("Overall time for {} \t : {}s".format(name,duration))
                show_profiling_stats()
                reset_new_profile = True
        return x
    return time_function 

def profiling(decorator=profiling_stats_track):
    def decorate_cls(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)) and not any([attr == n for n in ['__init__']]):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    def decorate_func(f):
        return decorator(f)
    def decorate(obj):
        if isclass(obj):
            return decorate_cls(obj)
        if isfunction(obj):
            return decorate_func(obj)
        return obj
    return decorate


def show_profiling_in_timeseries(maxlvl=None):
    global overall_timestamp
    global longest_name
    if maxlvl is None:
        maxlvl = int( longest_name ** 0.4 )
    start = []
    end   = []
    tab   = PROFILE_CONFIG.expanded_tree_tab_deco
    deco  = PROFILE_CONFIG.expanded_tree_bullets
    level = 0
    info = sorted(overall_timestamp, key=lambda x: x[0])
    for i in info:
        s,e,d,name = i
        if not start:
            start.append(s)
            end.append(e)
            head("Profiling in Sequence",pop=False)
        while end and s > end[-1]:
            level -= 1
            start.pop()
            end.pop()
        long = longest_name+len(tab)*maxlvl
        msg  = (tab*level+deco + " " + name).ljust(long)[:long]
        print( msg if d < 1 else highlight.format(msg) , cyan(d,pop=True))
        if e > end[-1]:
            start.pop()
            end.pop()
            start.append(s)
            end.append(e)
        else:
            start.append(s)
            end.append(e)
            level += 1 

def init_profiling(module):
    for name, func in module.__dict__.items():
        if name[:2] != '__':
            if isclass(func) or isfunction(func):
                module.__dict__[name] = profiling()(func)




################ TESTING ###############
if __name__ == '__main__':
    @profiling()
    def subdummyfunc1():
        """to check if __docstring__ is retained after decorative function"""
        return 'ok'
    
    @profiling()
    def subdummyfunc2():
        """to check if __docstring__ is retained after decorative function"""
        subdummyfunc1()
        subdummyfunc1()
        subdummyfunc1()
        subdummyfunc1()
        return 'ok'
    
    @profiling()
    def dummyfunc1(x=1,y=2, default=None):
        """to check if __docstring__ is retained after decorative function"""
        subdummyfunc2()
        subdummyfunc2()
        subdummyfunc2()
        subdummyfunc2()
        return 'ok'
    print(dummyfunc1.__doc__)
    
    @profiling()
    class Main:
        def __init__(self):
            pass
        
        def a(self):
            subdummyfunc1()
            subdummyfunc1()
            pass

        def b(self):
            self.a()
            self.a()
            pass

        def c(self):
            self.b()
            return 12345
    
    subdummyfunc1()
    print('\n\n\n')
    subdummyfunc2()
    print('\n\n\n')
    dummyfunc1()
    print('\n\n\n')
    m = Main()
    print('\n\n\n')
    m.c()
    show_profiling_in_timeseries()
    
    
    
    