# chikkarpy
[![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![test](https://github.com/t-yamamura/chikkarpy/actions/workflows/test.yaml/badge.svg)](https://github.com/t-yamamura/chikkarpy/actions/workflows/test.yaml)
[![](https://img.shields.io/github/license/t-yamamura/chikkarpy.svg)](https://github.com/t-yamamura/chikkarpy/blob/master/LICENSE)

chikkarpyは[chikkar](https://github.com/WorksApplications/chikkar)のPython版です。 
chikkarpy is a Python version of chikkar.

chikkarpy は [Sudachi 同義語辞書](https://github.com/WorksApplications/SudachiDict/)を利用し、[SudachiPy](https://github.com/WorksApplications/SudachiPy)の出力に同義語展開を追加するために開発されたライブラリです。

単体でも同義語辞書の検索ツールとして利用できます。

## 利用方法 Ussage
## TL;DR
```
$ pip install chikkarpy

$ echo "閉店" | chikkarpy
閉店    クローズ,close,店仕舞い
```

## Step 1. chikkarpyのインストール
```
$ pip install chikkarpy
```
## Step 2. 使用方法
### コマンドライン
```
$ echo "閉店" | chikkarpy
閉店    クローズ,close,店仕舞い
```
chikkarpyは入力された単語を見て一致する同義語のリストを返します。
同義語辞書内の曖昧性フラグが`1`の見出し語をトリガーにすることはできません。
出力は`クエリ\t同義語リスト`の形式です。

### python ライブラリ
使用例
```
from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary

chikkar = Chikkar()

system_dic = Dictionary("system.dic", False)
chikkar.add_dictionary(system_dic)

print(chikkar.find("閉店"))
# => ['クローズ', 'close', '店仕舞い']

print(chikkar.find("閉店", group_ids=[5])) # グループIDによる検索
# => ['クローズ', 'close', '店仕舞い']

print(chikkar.find("開放"))
# => ['オープン', 'open']

chikkar.enable_verb() # 用言の出力制御（デフォルトは体言のみ出力）
print(chikkar.find("開放"))
# => ['開け放す', '開く', 'オープン', 'open']

```


## 辞書の作成 Build a dictionary

新しく辞書を追加する場合は、利用前にバイナリ形式辞書の作成が必要です。
Before using new dictionary, you need to create a binary format dictionary.

```
$ chikkarpy build -i synonym_dict.csv -o system.dic 
```
