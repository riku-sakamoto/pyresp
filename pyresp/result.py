# -*- coding = utf-8 -*-

from ResperKit.parser import Parser

class StoryCSV(object):
  def __init__(self,file_path):
    self._file_path = file_path
    self._parser = Parser(self._file_path)
  
  def get_title(self):
    pass


