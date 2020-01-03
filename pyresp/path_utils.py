# -*- coding = utf-8 -*-

import shutil, os

def remake_folder(folder_path):
  if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
  os.makedirs(folder_path)

def extract_file_name(file_path):
  path_without_ext, _ = os.path.splitext(file_path)
  return os.path.basename(path_without_ext)

