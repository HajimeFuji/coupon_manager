# flaskモジュールからflaskクラスをインポート
from flask import Flask,render_template,request,redirect
# sqlite3をインポート
import sqlite3
# Flaskクラスをインスタント化してapp変数に代入
app = Flask(__name__)

@app.route("/")
def index():
    # テンプレートを表示する
    return render_template("base.html")

@app.route("/add")
def add_get():
    return render_template("add.html")

@app.route("/add",methods=["post"]) 
def add_post():
    # 入力フォームからデータを取得する
    task = request.form.get("task")
    print(task)
    # 2.データベースに接続する
    conn = sqlite3.connect("myTask.db")
    # 3.データベースを操作するための準備
    c = conn.cursor()
    # 4.SQLを実行してDBにデータを送る
    c.execute("insert into task values (null,?)",(task,))
    # 5.データベースの更新(保存)をする
    conn.commit()
    # 6.データベースの接続を終了する
    c.close()
    # リダイレクトでルーティングに飛ばす
    return redirect("/list")

@app.route("/list")
def list_get():
    # conn = sqlite3.connect("myTask.db")
    # c = conn.cursor()
    # c.execute("select id,task from task")
    # # データを格納する配列を準備
    # task_list = []
    # # c.fetchall()で指定したDBレコードを条件取得する
    # for row in c.fetchall():
    #     # 取得したレコードを辞書型に変換して、task_listに追加する
    #     task_list.append({"id":row[0],"task":row[1]})
    # c.close()
    # print(task_list)    
    return render_template("list.html")
    #                                ↑task_list = task_list

# スクリプトとして直接実行した場合
if __name__ == "__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True, port=5002)