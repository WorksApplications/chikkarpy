# chikkarpy
[![PyPi version](https://img.shields.io/pypi/v/chikkarpy.svg)](https://pypi.python.org/pypi/chikkarpy/)
[![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![test](https://github.com/t-yamamura/chikkarpy/actions/workflows/test.yaml/badge.svg)](https://github.com/t-yamamura/chikkarpy/actions/workflows/test.yaml)
[![](https://img.shields.io/github/license/t-yamamura/chikkarpy.svg)](https://github.com/t-yamamura/chikkarpy/blob/master/LICENSE)

chikkarpyは[chikkar](https://github.com/WorksApplications/chikkar)のPython版です。 
chikkarpy is a Python version of chikkar.

chikkarpy は [Sudachi 同義語辞書](https://github.com/WorksApplications/SudachiDict/blob/develop/src/main/text/synonyms.txt)を利用し、[SudachiPy](https://github.com/WorksApplications/SudachiPy)の出力に同義語展開を追加するために開発されたライブラリです。

単体でも同義語辞書の検索ツールとして利用できます。

## 利用方法 Usage
## TL;DR
```bash
$ pip install chikkarpy

$ echo "閉店" | chikkarpy
閉店    クローズ,close,店仕舞い
```

## Step 1. chikkarpyのインストール
```bash
$ pip install chikkarpy
```
## Step 2. 使用方法
### コマンドライン
```bash
$ echo "閉店" | chikkarpy
閉店    クローズ,close,店仕舞い
```
chikkarpyは入力された単語を見て一致する同義語のリストを返します。
同義語辞書内の曖昧性フラグが`1`の見出し語をトリガーにすることはできません。
出力は`クエリ\t同義語リスト`の形式です。

```bash
$ chikkarpy search -h
usage: chikkarpy search [-h] [-d [file [file ...]]] [-ev] [-o file] [-v]
                        [file [file ...]]

Search synonyms

positional arguments:
  file                  text written in utf-8

optional arguments:
  -h, --help            show this help message and exit
  -d [file [file ...]]  synonym dictionary (default: system synonym
                        dictionary)
  -ev                   Enable verb and adjective synonyms.
  -o file               the output file
  -v, --version         print chikkarpy version
```

自分で用意したユーザー辞書を使いたい場合は`-d`で読み込むバイナリ辞書を指定できます。
（バイナリ辞書のビルドは[辞書の作成](#辞書の作成-Build-a-dictionary)を参照してください。）
複数辞書を読み込む場合は順番に注意してください。
以下の場合，user2 > user > system の順で同義語を検索して見つかった時点で検索結果を返します。

```bash
chikkarpy -d system.dic user.dic user2.dic
```

また、出力はデフォルトで**体言**のみです。
**用言**も出力したい場合は`-ev`を有効にしてください。

```bash
$ echo "開放" | chikkarpy
開放	オープン,open
$ echo "開放" | chikkarpy -ev
開放	開け放す,開く,オープン,open
```


### python ライブラリ
使用例
```python
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

`chikkar.add_dictionary()`で複数の辞書を読み込ませる場合は順番に注意してください。
最後に読み込んだ辞書を優先して検索します。

## 辞書の作成 Build a dictionary

新しく辞書を追加する場合は、利用前にバイナリ形式辞書の作成が必要です。
Before using new dictionary, you need to create a binary format dictionary.

```bash
$ chikkarpy build -i synonym_dict.csv -o system.dic 
```

```bash
$ chikkarpy build -h
usage: chikkarpy build [-h] -i file [-o file] [-d string]

Build Synonym Dictionary

optional arguments:
  -h, --help  show this help message and exit
  -i file     dictionary file (csv)
  -o file     output file (default: synonym.dic)
  -d string   description comment to be embedded on dictionary
```

## 開発者向け

### Code Format

`scripts/lint.sh` を実行して、コードが正しいフォーマットかを確認してください。

`flake8` `flake8-import-order` `flake8-builtins` が必要です。

### Test

`scripts/test.sh` を実行してテストしてください。

## Contact

chikkarpyは[WAP Tokushima Laboratory of AI and NLP](http://nlp.worksap.co.jp/)によって開発されています。

開発者やユーザーの方々が質問したり議論するためのSlackワークスペースを用意しています。
- https://sudachi-dev.slack.com/  ([こちら](https://join.slack.com/t/sudachi-dev/shared_invite/enQtMzg2NTI2NjYxNTUyLTMyYmNkZWQ0Y2E5NmQxMTI3ZGM3NDU0NzU4NGE1Y2UwYTVmNTViYjJmNDI0MWZiYTg4ODNmMzgxYTQ3ZmI2OWU)から招待を受けてください)
