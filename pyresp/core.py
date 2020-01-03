# -*- coding: utf-8 -*-
from . import helpers
from pyresp.separater import StorySeparater
from pyresp.path_utils import remake_folder

def sepearate_story_csv(story_file_path,out_directory):
  """
  storyファイルを各テーブルに対応するcsvに分割する。
  story_file_path : storyファイルのパス
  out_directory : csvを出力するフォルダ
  """
  remake_folder(out_directory)
  story_seperater = StorySeparater(story_file_path,out_directory)
  story_seperater.separate()

