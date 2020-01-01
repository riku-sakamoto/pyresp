
"""
csvファイル読み取り部

解析ケースごとに分割


"""
import csv, re, functools, os
from typing import List
import sys_enum as SysEnum

class StorySeparater(object):
  """共通パーサー"""
  def __init__(self,story_file_path):
    self.file_path = story_file_path
    self.folde_path = "./out"
  
  def separate(self):
    for title,block in self.generate_each_value_table():
      if self.is_active_block(block):
        file_path = os.path.join(self.folde_path,"sample_%s.csv"%(title))
        with open( file_path,"w",newline="") as fw:
            writer = csv.writer(fw, delimiter=',')
            writer.writerows(block)

  def generate_each_analysis_block(self) -> List[str]:
    """解析ケースごとのブロックに分割する"""
    block = []
    with open(self.file_path,"r") as fr:
      csv_reader = csv.reader(fr)
      for row in csv_reader:
        if self.is_active_row(row):
          block.append(row)
        else:
          yield block
          block = []
  
  def generate_each_value_table(self):
    """各表形式のブロックに分割する"""
    for block in self.generate_each_analysis_block():
      if block:
        analysis_type = self.get_analysis_type(block[0])
        case_number = self.get_case_number(block[0],analysis_type)

        if analysis_type == SysEnum.ReadableAnalysisType.EigenAnalysis:
          # 固有値解析結果のみ他と書式が異なる
          table_blocks = self.separate_eigen_block(block)
        else:
          table_blocks = self.separate_to_each_value_block(block)      

        for table_block in table_blocks:
          table = self.trim_to_each_table(table_block,analysis_type)
          title = self.get_table_title(table_block[0],case_number)
          yield title, table

  def separate_to_each_value_block(self,block:List[str]):
    """一列目に値が存在する区間に分割する（固有値解析以外で使用）"""
    # 一列目に値が入っているインデックスを取得
    separate_index = [block.index(row) for row in block if row[0]] 
    
    # 最初に0を加える
    separate_index.insert(0,0)
    separate_index.append(len(block)-1)

    # 一列目に値が入っている箇所でスライス
    table_blocks = [block[separate_index[i]:separate_index[i+1]] for i in range(len(separate_index)-1)]

    return [block for block in table_blocks if block]

  def separate_eigen_block(self,block):
    """固有値解析結果のブロックを分割する"""

    #HACK コードが最悪。書き換える。
    eigen_blocks = self.separate_eigen_value_and_vector_block(block)

    eigen_value_blocks = []
    tmp_eigen_value_block = []
    header = ""
    for block in eigen_blocks:
      for row in block:
        if row[0] == "*** Eigen Analysis ***":
          continue
        
        if "<" in row[0]:
          row[0] = row[0].replace("<","")
          header = row
          continue
  
        tmp_eigen_value_block.append(row)

      tmp_eigen_value_block.insert(1,header)
      eigen_value_blocks.append(tmp_eigen_value_block)
      tmp_eigen_value_block = []
      
    return [block for block in eigen_value_blocks if block]
  
  def separate_eigen_value_and_vector_block(self,block:List):
    """固有値解析結果のブロックを周期とベクトルに分割する"""
    separate_index = [block.index(row) for row in block if row[0]=="<" or row[0]=="EigenVector"]
    # 最初に0を加える
    separate_index.insert(0,0)
    separate_index.append(len(block)-1)
    # 一列目に<が入っている箇所でスライス
    table_blocks = [block[separate_index[i]:separate_index[i+1]] for i in range(len(separate_index)-1)]
    return table_blocks

  def trim_to_each_table(self,block:List[str],analysis_type:SysEnum.ReadableAnalysisType):
    """表形式になるように成型する（固有値解析以外）"""
    if block:
      if analysis_type == SysEnum.ReadableAnalysisType.EigenAnalysis:
        table = [row if row[0] else row[1:] for row in block[1:]]
      else:
        table = [row[1:] for row in block]
      return table
  
  def get_table_title(self,table_first_row:List[str],case_number:str):
    cell = table_first_row[0]
    value_title = ""
    """各表のタイトルを取得する"""
    if cell == "Version":
      value_title =  "version"
    elif cell == "Date":
      value_title =  "date"
    elif cell == "Title":
      value_title =  "title"
    elif cell == "Control":
      value_title =  "control"
    elif cell == "Story":
      value_title =  "story"
    elif cell == "*** Dynamic Non-Linear Analysis ***":
      value_title =  "DNLA_title"
    elif cell == "Abs.Max." and table_first_row[2] == "DriftU":
      value_title =  "drift_abs_max"
    elif cell == "Abs.MaxShearForceComponent.":
      value_title =  "shear_force_abs_max"
    elif cell == "Abs.Max." and table_first_row[2] == "ShearCoefficientU":
      value_title =  "shear_coefficient_abs_max"
    elif cell == "MaxD.F.":
      value_title =  "DF_max"
    elif cell == "Abs.Max." and table_first_row[2] == "DriftVelocityU":
      value_title =  "drift_velocity_abs_max"
    elif cell == "Abs.MaxOfUpperNode":
      value_title =  "max_of_upper_node"
    elif cell == "Abs.MaxOfLowerNode":
      value_title =  "max_of_lower_node"
    elif cell == "Abs.Max." and table_first_row[2] == "OtmU":
      value_title =  "otm_abs_max"
    elif cell == "EigenValue":
      value_title =  "eigen_value"
    elif cell == "EigenVector":
      mode = table_first_row[1]
      value_title =  "eigen_vector_mode_%s"%mode
    else:
      value_title =  "Error"
    
    return "%s_%s"%(case_number,value_title)

  def get_analysis_type(self,first_row:List[str]):
    first_cell = first_row[0]
    if "*** Eigen Analysis ***" in first_cell:
      return SysEnum.ReadableAnalysisType.EigenAnalysis
    elif "*** Dynamic Non-Linear Analysis ***" in first_cell:
      return SysEnum.ReadableAnalysisType.DynamicNonLinearAnalysis
    else:
      return SysEnum.ReadableAnalysisType.General
  
  def get_case_number(self,first_row:List[str],analysis_type:SysEnum.ReadableAnalysisType):
    if analysis_type == SysEnum.ReadableAnalysisType.General:
      case_number = first_row[0]
    else:
      case_number = first_row[1]
    return case_number

  def is_active_row(self,row:str) -> bool:
    """有効な行か（空行ではないか）"""
    if row:
      # csvの出力によっては全て空白が入ることもある
      is_active_row = functools.reduce(lambda x,y:x or y, row) # 空行ではないか
      return is_active_row
    else:
      return False

  def is_active_block(self,block:List[str]) -> bool:
    """有効なブロックか（空行ではないか）"""
    if block:
      # csvの出力によっては全て空白が入ることもある
      return self.is_active_row(block[0])
    else:
      return False


if __name__ == "__main__":
  parser = StorySeparater("./MainAnalysis.story.csv")
  parser.separate()
