# flaskモジュールからFlaskクラスをインポート
from flask import Flask, render_template, request, redirect
# sqlite3をインポート
import sqlite3
# Flaskクラスをインスタンス化してapp変数に代入
app = Flask(__name__)

# ここにコードを書く





# スクリプトとして直接実行した場合
if __name__ == "__main__":
    # FlaskのWEBアプリケーションを起動　本番環境ではdebug=False
    app.run(debug=True)