# pyresp

## 概要

- RESP出力ファイル操作用のpythonライブラリ
- storyファイルやlastファイルを各値テーブルごとにcsvに分割し、pandasなどによるデータ操作を簡易にするためのライブラリ

## インストール方法

```MSDOS
pip install git+https://github.com/riku-sakamoto/pyresp
```

## 主要関数

|関数名|説明|
|-----|-----|
|sepearate_story_csv|storyファイルを各テーブルごとのcsvに分割する|


## 使用例

```python
import pyresp
story_path = "./MainAnalysis.story.csv"
out_dir = "./out_story"
pyresp.sepearate_story_csv(story_path,out_dir)
```

--- 
