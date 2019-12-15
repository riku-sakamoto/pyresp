
"""
csvファイル読み取り部
ファイルサイズが大きくなることを想定して、
はじめに適当な長さにファイルを分割。
その後、正規表現でマッチング。
"""
import csv, re
from typing import Sequence
import sys_enum as SysEnum
import pandas as pd

class Parser(object):
  """共通パーサー"""
  def __init__(self,file_path):
    self.file_path = file_path
  
  def extract_information(self,analysis_type:SysEnum.ReadableAnalysisType):
    for block_text in self.block_generator(): 
      if analysis_type == SysEnum.ReadableAnalysisType.General:
        pass
      elif analysis_type == SysEnum.ReadableAnalysisType.EigenAnalysis:
        pattern = "EigenVector(.*?)(?=EigenVector)"
        results = re.findall(pattern, block_text, re.S)
        for result in results:
          print(result)
      else:
        pass


  def block_generator(self):
    """空白行区切りの一定区間で値を取得するジェネレータ"""
    block = []

    with open(self.file_path) as fr:
      csv_reader = csv.reader(fr)
      for row in csv_reader:
        if row:
          block.append(row)
        else:
          yield block
          block = []
  
  def extract_general_information(self,item_name:str):
    """共通一般情報の出力（一つのみ）"""
    for block in self.block_generator():
      for rows in block:
        if rows[0] == item_name:
          return rows[1]
  
  def extract_story_information(self):
    """階の出力（一つのみ）"""
    for block in self.block_generator():
      for rows in block:
        if rows[0] == "Story":
          # 始めの空白セルを削除
          return [row[1:] for row in block]
  
  def extract_eigen_value(self):
    for block in self.block_generator():
      if block[0][0] == "*** Eigen Analysis ***":
        block_text = ",".join(block)
        pattern = "EigenValue,(.*?)(?=EigenVector)"



if __name__ == "__main__":
  parser = Parser("./MainAnalysis.story.csv")
  #parser.extract_information(SysEnum.ReadableAnalysisType.EigenAnalysis)
  # parser.extract_general_information("Control","Input")
  a = parser.extract_general_information("Version")
  b = parser.extract_story_information()
  a1 = parser.extract_general_information("Version")
  
  print(a)
  print(a1)
  print(pd.DataFrame(b))
  # print(pd.DataFrame(b,index_col = 0))
