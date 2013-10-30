# @name    Utility.py
# @author  Samuel A.
# @date    Oct 11 13
# @purpose Various classes for various stuff, read the code docs below


from collections import namedtuple

##
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)


##
# @staticmethod
# def obj(dic):
# 	return Struct(**dic)

		