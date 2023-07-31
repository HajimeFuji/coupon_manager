import sqlite3
from flask import Flask, render_template, request, redirect, session
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
        # couponテーブルからレコードを全て選択
        c.execute("select id, coupon_name, shop_name, expiration from coupon where user_flag = ?", (user_id,))
        coupon_list = []
        for row in c.fetchall():
            print("-------------")
            print(row)
            print("-------------")
            coupon_list.append({"coupon_name": row[1], "shop_name": row[2], "expiration": row[3]})
        c.close()
        print(coupon_list)
        return render_template("list.html", user_name = user_name, coupon_list = coupon_list)
    else:
        return redirect("/")



# 404ページを返す
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)