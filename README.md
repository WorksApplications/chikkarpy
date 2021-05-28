# chikkarpy
[![PyPi version](https://img.shields.io/pypi/v/chikkarpy.svg)](https://pypi.python.org/pypi/chikkarpy/)
[![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![test](https://github.com/t-yamamura/chikkarpy/actions/workflows/test.yaml/badge.svg)](https://github.com/t-yamamura/chikkarpy/actions/workflows/test.yaml)
[![](https://img.shields.io/github/license/t-yamamura/chikkarpy.svg)](https://github.com/t-yamamura/chikkarpy/blob/master/LICENSE)

chikkarpyは[chikkar](https://github.com/WorksApplications/chikkar)のPython版です。 
chikkarpy は [Sudachi 同義語辞書](https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md)を利用し、[SudachiPy](https://github.com/WorksApplications/SudachiPy)の出力に同義語展開を追加するために開発されたライブラリです。
単体でも同義語辞書の検索ツールとして利用できます。

chikkarpy is a Python version of [chikkar](https://github.com/WorksApplications/chikkar).
chikkarpy is developed to utilize the [Sudachi synonym dictionary](https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md) and add synonym expansion to the output of [SudachiPy](https://github.com/WorksApplications/SudachiPy).
This library alone can be used as a search tool for our synonym dictionaries.

## 利用方法 Usage
## TL;DR
```bash
$ pip install chikkarpy

$ echo "閉店" | chikkarpy
閉店    クローズ,close,店仕舞い
```

## Step 1. chikkarpyのインストール Install chikkarpy
```bash
$ pip install chikkarpy
```

## Step 2. 使用方法 Usage
### コマンドライン Command Line
```bash
$ echo "閉店" | chikkarpy
閉店    クローズ,close,店仕舞い
```
chikkarpyは入力された単語を見て一致する同義語のリストを返します。
chikkarpy looks at a headword of synonym dictionary by the entered word and returns a list of matching synonyms.

同義語辞書内の曖昧性フラグが`1`の見出し語をトリガーにすることはできません。
You cannot use a headword with an ambiguity flag of `1` in a synonym dictionary as a search trigger.

出力は`クエリ\t同義語リスト`の形式です。
The output is in the form of a `query \t synonym list`.

デフォルトの [Sudachi 同義語辞書](https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md) の見出し語は、
SudachiPyの正規化形 (`normalized_form()`) で登録されています。

The headwords in the Sudachi synonym dictionary are registered in SudachiPy's normalized form, `normalized_form()`.

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
When you use your user dictionary, you should specify the binary dictionary to read with `-d`.
(For building a binary dictionary, see [Building a Dictionary](#辞書の作成-Build-a-dictionary).)

複数辞書を読み込む場合は順番に注意してください。
When reading multiple dictionaries, pay attention to the order.

以下の場合，**user2 > user > system** の順で同義語を検索して見つかった時点で検索結果を返します。
In the following cases, the synonyms are searched in the order of **user2 > user > system**, and the search results are returned which are first found.

```bash
chikkarpy -d system.dic user.dic user2.dic
```

また、出力はデフォルトで**体言**のみです。
Also, the output is **noun** only by default.

**用言**も出力したい場合は`-ev`を有効にしてください。
When you want to output **verb** as well, please enable `-ev`.

```bash
$ echo "開放" | chikkarpy
開放	オープン,open
$ echo "開放" | chikkarpy -ev
開放	開け放す,開く,オープン,open
```

### Python ライブラリ / Python library
使用例 Example of use

```python
from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary

chikkar = Chikkar()

# デフォルトのシステム同義語辞書を使う場合，Dictionaryの引数は省略可能 You may omit the ``Dictionary`` arguments if you want to use the system synonym dictionary
system_dic = Dictionary()
chikkar.add_dictionary(system_dic)

print(chikkar.find("閉店"))
# => ['クローズ', 'close', '店仕舞い']

print(chikkar.find("閉店", group_ids=[5])) # グループIDによる検索 Search by group ID
# => ['クローズ', 'close', '店仕舞い']

print(chikkar.find("開放"))
# => ['オープン', 'open']

chikkar.enable_verb() # 用言の出力制御（デフォルトは体言のみ出力） Output control of verbs (default is to output only nouns)
print(chikkar.find("開放"))
# => ['開け放す', '開く', 'オープン', 'open']
```

`chikkar.add_dictionary()`で複数の辞書を読み込ませる場合は順番に注意してください。
最後に読み込んだ辞書を優先して検索します。
また、`enable_trie`を`False`に設定した辞書では、同義語を検索するときに見出し語よりもグループIDを優先して検索します。

When you read multiple dictionaries with `chikkar.add_dictionary()`, pay attention to the order.
Priority is given to the last read dictionary.
If ``enable_trie`` is ``False``, a search by synonym group IDs takes precedence over a search by the headword.

```python
chikkar = Chikkar()

system_dic = Dictionary(enable_trie=False)
user_dic = Dictionary(user_dict_path, enable_trie=True)
user2_dic = Dictionary(user_dict_path, enable_trie=True)

chikkar.add_dictionary(system_dic)
chikkar.add_dictionary(user_dic)
chikkar.add_dictionary(user2_dic)
```


## 辞書の作成 Build a dictionary

新しく辞書を追加する場合は、利用前にバイナリ形式辞書の作成が必要です。
Before using new dictionary, you need to create a binary format dictionary.

同義語辞書のフォーマットは[Sudachi 同義語辞書](https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md)に従ってください。
Follow the [Sudachi Synonym Dictionary](https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md) for the format of the synonym dictionary.

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
Run `scripts/lint.sh` to check if your code is formatted correctly.

`flake8` `flake8-import-order` `flake8-builtins` が必要です。
You need packages `flake8` `flake8-import-order` `flake8-builtins`.

### Test

`scripts/test.sh` を実行してテストしてください。
Run `scripts/test.sh` to run the tests.

## Contact

chikkarpyは[WAP Tokushima Laboratory of AI and NLP](http://nlp.worksap.co.jp/)によって開発されています。
chikkarpy is developed by WAP Tokushima Laboratory of AI and NLP.

開発者やユーザーの方々が質問したり議論するためのSlackワークスペースを用意しています。
Open an issue, or come to our Slack workspace for questions and discussion.
- https://sudachi-dev.slack.com/  ([招待を受ける/Get invitation](https://join.slack.com/t/sudachi-dev/shared_invite/enQtMzg2NTI2NjYxNTUyLTMyYmNkZWQ0Y2E5NmQxMTI3ZGM3NDU0NzU4NGE1Y2UwYTVmNTViYjJmNDI0MWZiYTg4ODNmMzgxYTQ3ZmI2OWU))
