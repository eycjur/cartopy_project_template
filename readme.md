# Cartopy Project Template
cartopyの環境をローカルに構築する

## Advance Preparation
### pyenvのインストール
python本体のバージョン管理ツール
- mac
```bash
brew install pyenv
echo '
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
' >> ~/.bashrc
source ~/.bashrc
## ターミナルを再起動
```

- wsl
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
source ~/.bashrc
## ターミナルを再起動
```

### pythonのインストール
pyenvを利用してpython3.9.4をインストールする

```bash
## インストールできるバージョンの一覧
pyenv install --list
pyenv install 3.9.4
pyenv global 3.9.4
## インストールされているバージョンの確認
pyenv versions
python -V
```

### poetryのインストール
パッケージ管理ツール

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source $HOME/.poetry/bin
## ターミナルを再起動

## プロジェクト内に仮想環境を作成するように設定
poetry config virtualenvs.in-project true
poetry config --list
```

## Installation
```bash
git clone https://github.com/eycjur/cartopy_project_template.git
poetry  install
```

以下のファイルをカレントディレクトリにおいてください
- anl_p125_hgt.2012011012
- cluster_data.csv


## Quick Start
### juyter notebook形式で実行
- vscodeを利用する場合
1. vscodeを利用する場合は拡張機能で`@recommended`で検索して表示されるものを入れる
1. jra55.ipynbを開くと、jupyter notebook形式で実行できる

- ブラウザで行う場合
1. ターミナルで`make jupyter`を実行
1. ブラウザで http://localhost:8888/lab を開き、jra55.ipynbを開く

### スクリプト形式で実行
```bash
poetry shell  ## 仮想環境に入る
python jra55.py
# outputディレクトリ内に各種画像が出力される
```

## Warning
poetry以外のパッケージ管理ツールを利用する場合には依存関係がめんどくさいので、以下のバージョンを指定してインストールしてください。  
情報源が少ないのでいくつかのバージョンを試してみて上手くいったものを採用しています。
- cartopy==0.19.0.post1
- Shapely==1.6.0

## Reference
poetryの使い方
- [pythonでのプロジェクト作成に関するツールの使い方まとめ](https://qiita.com/eycjur/items/38459af60ea6f989a068)

参考にしたもの
- [ubuntu 20.04 / 18.04 に pyenv をインストール](https://zenn.dev/neruo/articles/install-pyenv-on-ubuntu)
- [cartopyのバージョンに関するissue](https://github.com/SciTools/iris/issues/4468##issuecomment-997997068)
