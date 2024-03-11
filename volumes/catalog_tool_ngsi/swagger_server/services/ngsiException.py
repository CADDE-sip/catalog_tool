# -*- coding: utf-8 -*-

class ngsiException(Exception):
   def __init__(self, message, status):
       self.message = message
       self.status = status
   def __str__(self):
       return repr(self.message)