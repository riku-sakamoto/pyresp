# -*- coding: utf-8 -*-
from . import helpers
from .separater import StorySeparater

def sepearate_story_csv(story_file_path,out_dir=None):
  story_sep = StorySeparater(story_file_path,out_dir)
  story_sep.separate()

