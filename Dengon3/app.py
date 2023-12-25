# Flaskとその他の必要なライブラリをインポートします
from flask import Flask, render_template, request, session, redirect, url_for
import os
import signal

import subprocess
import time

# Flaskアプリケーションを作成します
app = Flask(__name__)
# セッションの秘密鍵を設定します。これはセッションデータを安全に暗号化するために使用されます
app.secret_key = os.urandom(24)

# ルートURL('/')にアクセスしたときの処理を定義します
@app.route('/', methods=['GET', 'POST'])
def index():
    f = open('execution_count.txt', 'w', encoding='UTF-8')
    f.write('0')
    f = open('real1_count.txt', 'w', encoding='UTF-8')
    f.write('0')
    f = open('real2_count.txt', 'w', encoding='UTF-8')
    f.write('0')
    # POSTリクエストの場合（フォームからデータが送信された場合）
    if request.method == 'POST':
        # セッションにプレイヤーの数とゲームのテーマを保存します
        session['num_players'] = request.form.get('num_players')
        # 現在のプレイヤーを1に設定します
        session['current_player'] = 1

        return redirect(url_for('subject')) # リダイレクト実行，画面遷移
    
    # GETリクエストの場合（ページが初めてロードされた場合）、index.htmlを表示します
    return render_template('index.html')



@app.route('/subject', methods=['GET', 'POST'])
def subject():
    # POSTリクエストの場合（フォームからデータが送信された場合）
    if request.method == 'POST':
        session['game'] = [{'type': 'theme', 'content': request.form.get('theme')}]
        return redirect(url_for('capture')) # リダイレクト実行，画面遷移
    
    return render_template('subject.html')



# 下3つのはplay.htmlの処理をうまく動作させるため。

@app.route('/start_hands_py', methods=['POST'])
def start_hands_py():
    if request.method == 'POST':
        subprocess.run(['python', 'hands.py'])
    return render_template('play.html', last_turn=session['game'][-1])

@app.route('/start_hands2_py', methods=['POST'])
def start_hands2_py():
    subprocess.run(['python', 'hands2.py'])
    return render_template('play.html', last_turn=session['game'][-1])

@app.route('/start_Add2_py', methods=['POST'])
def start_Add2_py():
    subprocess.run(['python', 'Add2.py'])
    return render_template('play.html', last_turn=session['game'][-1])


# 下3つのはcapture.htmlの処理をうまく動作させるため。

@app.route('/capture_start_hands_py', methods=['POST'])
def capture_start_hands_py():
    if request.method == 'POST':
        subprocess.run(['python', 'hands.py'])
    return render_template('capture.html', last_turn=session['game'][-1])

@app.route('/capture_start_hands2_py', methods=['POST'])
def capture_start_hands2_py():
    subprocess.run(['python', 'hands2.py'])
    return render_template('capture.html', last_turn=session['game'][-1])

@app.route('/capture_start_Add2_py', methods=['POST'])
def capture_start_Add2_py():
    subprocess.run(['python', 'Add2.py'])
    return render_template('capture.html', last_turn=session['game'][-1])


# キャプチャ画面(/capture)にアクセスしたときの処理を定義

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    # POSTリクエストの場合（フォームからデータが送信された場合）
    if request.method == 'POST':
        # フォームから送信された内容を取得します
        content = request.form.get('content')
        # ゲームのセッションに新しいターンのデータを追加します
        session['game'].append({'type': 'image' if len(session['game']) % 2 else 'description'})
        # 現在のプレイヤーを更新します（プレイヤーの数で割った余り+1）
        session['current_player'] = session['current_player'] % int(session['num_players']) + 1
        # 全プレイヤーが1回ずつプレイしたら、結果を表示する画面にリダイレクトします
        if len(session['game']) > int(session['num_players']):
            return redirect(url_for('reveal'))
        
        if (len(session['game']) % 2 == 0):
            return redirect(url_for('change')) # リダイレクト実行，画面遷移
    
    return render_template('capture.html', last_turn=session['game'][-1])



# プレイ画面(/play)にアクセスしたときの処理を定義

@app.route('/change', methods=['GET', 'POST'])
def change():
    # POSTリクエストの場合（フォームからデータが送信された場合）
    if request.method == 'POST':
        # フォームから送信された内容を取得します
        content = request.form.get('content')
        # ゲームのセッションに新しいターンのデータを追加します
        session['game'].append({'type': 'image' if len(session['game']) % 2 else 'description', 'content': content})
        # 現在のプレイヤーを更新します（プレイヤーの数で割った余り+1）
        session['current_player'] = session['current_player'] % int(session['num_players']) + 1
        # 全プレイヤーが1回ずつプレイしたら、結果を表示する画面にリダイレクトします
        if len(session['game']) > int(session['num_players']):
            return redirect(url_for('reveal'))
        
        if (len(session['game']) % 2 == 1):
            return redirect(url_for('play'))

            # return redirect(url_for('play'))
    # GETリクエストの場合（ページが初めてロードされた場合）、play.htmlを表示します
    return render_template('change.html', last_turn=session['game'][-1])


# プレイ画面(/play)にアクセスしたときの処理を定義

@app.route('/play', methods=['GET', 'POST'])
def play():
    # POSTリクエストの場合（フォームからデータが送信された場合）
    if request.method == 'POST':
        # フォームから送信された内容を取得します
        content = request.form.get('content')
        # ゲームのセッションに新しいターンのデータを追加します
        session['game'].append({'type': 'image' if len(session['game']) % 2 else 'description'})
        # 現在のプレイヤーを更新します（プレイヤーの数で割った余り+1）
        session['current_player'] = session['current_player'] % int(session['num_players']) + 1
        # 全プレイヤーが1回ずつプレイしたら、結果を表示する画面にリダイレクトします
        if len(session['game']) > int(session['num_players']):
            return redirect(url_for('reveal'))
        if (len(session['game']) % 2 == 0):
            return redirect(url_for('change'))
    # GETリクエストの場合（ページが初めてロードされた場合）、play.htmlを表示します
    return render_template('play.html', last_turn=session['game'][-1])



# 結果を表示する画面(/reveal)にアクセスしたときの処理を定義します
@app.route('/reveal', methods=['GET', 'POST'])
def reveal():
    # POSTリクエストの場合（フォームからデータが送信された場合）
    if request.method == 'POST':
        f = open('execution_count.txt', 'w', encoding='UTF-8')
        f.write('0')
        return redirect(url_for('real'))
    # reveal.htmlを表示し、ゲームのセッションデータを渡します
    return render_template('reveal.html', game=session['game'])

@app.route('/real', methods=['GET', 'POST'])
def real():
    # POSTリクエストの場合（フォームからデータが送信された場合）
    if request.method == 'POST':
        f = open('real1_count.txt', 'w', encoding='UTF-8')
        f.write('0')
        f = open('real2_count.txt', 'w', encoding='UTF-8')
        f.write('0')
    # reveal.htmlを表示し、ゲームのセッションデータを渡します
    return render_template('real.html', game=session['game'])


@app.route("/reset", methods=["POST"])
def reset():
    # ここでデータリセットの処理を行う
    session.pop('game', None)
    f = open('execution_count.txt', 'w', encoding='UTF-8')
    f.write('0')
    f = open('real1_count.txt', 'w', encoding='UTF-8')
    f.write('0')
    f = open('real2_count.txt', 'w', encoding='UTF-8')
    f.write('0')
    return redirect(url_for('index'))  # リセット後にメインページにリダイレクト

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # ここでデータリセットの処理を行う
    session.clear()  # セッションをクリア
    return redirect(url_for('subject'))  # リセット後にメインページにリダイレクト


# このスクリプトが直接実行されたとき（python app.pyというコマンドで実行されたとき）に、Flaskサーバーを起動します
if __name__ == '__main__':
    app.run(debug=True)
