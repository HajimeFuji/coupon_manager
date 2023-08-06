import sqlite3
from flask import Flask, render_template, request, redirect, session
from datetime import datetime
app = Flask(__name__)

# セッション情報を暗号化するために必要
app.secret_key = "sunabaco"

@app.route("/")
def top_page():
    return render_template("index.html")

# ログイン入力情報からidを取得する
@app.route("/", methods=["POST"])
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("coupon_manager.db")
    c = conn.cursor()
    c.execute("select id from users where user_name = ? and password = ?", (name, password))
    user_id = c.fetchone()
    c.close()
    if user_id is None:
        return render_template("index.html")
    else:
        session["user_id"] = user_id
        return redirect("/list")

# 新規登録（時間あったら実装）
# @app.route("/regist", methods=["POST"])
# def regist_post():
#     name = request.form.get("name")
#     password = request.form.get("password")
#     conn = sqlite3.connect("coupon_manager.db")
#     c = conn.cursor()
#     c.execute("insert into users values (null, ?, ?)", (name, password))
#     conn.commit()
#     c.close()
#     return redirect("/")

# DBのテーブル情報をリストとして返す
@app.route("/list")
def coupon_list():
    if "user_id" in session:
        # セッション情報からログインユーザーのidを取得する
        user_id = session["user_id"][0]
        print(user_id)
        conn = sqlite3.connect("coupon_manager.db")
        c = conn.cursor()
        # ログインユーザーの名前を取得
        c.execute("select user_name from users where id = ?", (user_id,))
        user_name = c.fetchone()[0]
        # couponテーブルからレコードを全て選択（order by expirationで日付を昇順にソート）
        c.execute("select id, coupon_name, shop_name, expiration from coupon where user_flag = ? order by expiration", (user_id,))
        coupon_list = []
        for row in c.fetchall():
            print("-------------")
            print(row)
            print("-------------")
            coupon_list.append({"id": row[0], "coupon_name": row[1], "shop_name": row[2], "expiration": row[3]})
        c.close()
        print(coupon_list)
        return render_template("list.html", user_name = user_name, coupon_list = coupon_list)
    else:
        return redirect("/")

# リストにクーポンを追加する
@app.route("/add", methods=["GET"])
def add_get():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/login")

@app.route("/add", methods=["POST"])
def add_coupon():
    if "user_id" in session:
        user_flag = session["user_id"][0]
        shop_name = request.form.get("shop_name")
        coupon_name = request.form.get("coupon_name")
        expiration = request.form.get("expiration")
        conn = sqlite3.connect("coupon_manager.db")
        c = conn.cursor()
        c.execute("insert into coupon values (null, ?, ?, ?, ?)", (coupon_name, shop_name, expiration, user_flag))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login")

# リスト内のクーポンを削除する
@app.route("/del/<int:id>")
def del_task(id):
    if "user_id" in session:
        conn = sqlite3.connect("coupon_manager.db")
        c = conn.cursor()
        c.execute("delete from coupon where id = ?", (id,))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login")

# ログアウトする
@app.route("/logout")
def logout():
    # セッションを削除してログアウト
    session.pop("user_id", None)
    return redirect("/")

# クーポンの内容を編集
# ①編集画面を開く
@app.route("/edit/<int:id>")
def edit_get(id):
    if "user_id" in session:
        conn = sqlite3.connect("coupon_manager.db")
        c = conn.cursor()
        c.execute("select id, coupon_name, shop_name, expiration from coupon where id = ?", (id,))
        item = c.fetchone()
        c.close()
        coupon_info = {"id": id, "coupon_name": item[1], "shop_name": item[2], "expiration": item[3]}
        print(coupon_info)
        return render_template("edit.html", coupon_info = coupon_info)
    else:
        return redirect("/login")

# ②編集内容を反映する
@app.route("/edit", methods=["POST"])
def update_coupon():
    if "user_id" in session:
        coupon_id = request.form.get("coupon_id")
        # request.form.get()は文字列型で取得されるため、数値型に変換
        coupon_id = int(coupon_id)
        # 変更後のクーポン情報を取得
        shop_name = request.form.get("shop_name")
        coupon_name = request.form.get("coupon_name")
        expiration = request.form.get("expiration")
        conn = sqlite3.connect("coupon_manager.db")
        c = conn.cursor()
        c.execute("update coupon set coupon_name = ?, shop_name = ?, expiration = ? where id = ?", (coupon_name, shop_name, expiration, coupon_id))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login")

# 404ページを返す
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)