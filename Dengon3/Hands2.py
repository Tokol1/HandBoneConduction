import cv2  # OpenCVライブラリ
import mediapipe as mp  # MediaPipeライブラリ
import numpy as np  # NumPyライブラリ
import os  # OSライブラリ

# MediaPipeのモデルをロード
mp_drawing = mp.solutions.drawing_utils  # 描画ユーティリティ
mp_hands = mp.solutions.hands  # 手の骨格検出モデル

# プログラムが実行された回数を保持するファイルのパス
real2_count_file = 'real2_count.txt'

# プログラムが実行された回数を読み込む
if os.path.exists(real2_count_file):
    with open(real2_count_file, 'r') as f:
        real2_count = int(f.read())
else:
    real2_count = 0

# カメラのキャプチャ開始
# (0)がPCの内蔵カメラ、(1)が外付けカメラ。
# ノートPCなら(0)で良い。
cap = cv2.VideoCapture(1)

# 手の骨格検出モデルの設定と初期化
with mp_hands.Hands(
    min_detection_confidence=0.5,  # 検出信頼度の閾値
    min_tracking_confidence=0.5) as hands:  # トラッキング信頼度の閾値
  while cap.isOpened():  # カメラがオープンしている間
    success, image = cap.read()  # カメラから画像を読み込む
    if not success:  # 画像が読み込めなかった場合
      print("Ignoring empty camera frame.")  # エラーメッセージを出力
      continue  # 次のループへ

    # RGBに変換
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False  # 画像を書き込み不可に設定
    results = hands.process(image)  # 手の骨格検出を実行

    # 描画の準備
    image.flags.writeable = True  # 画像を書き込み可能に設定
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # BGRに変換
    h, w, _ = image.shape  # 画像の高さと幅を取得
    image_blank = np.zeros([h, w, 3], dtype=np.uint8)  # 黒い背景画像を作成

    # 骨格の描画
    if results.multi_hand_landmarks:  # 骨格が検出された場合
      for hand_landmarks in results.multi_hand_landmarks:  # 各手に対して
        mp_drawing.draw_landmarks(
            image_blank,  # 描画対象の画像
            hand_landmarks,  # 骨格の情報
            mp_hands.HAND_CONNECTIONS)  # 骨格の接続情報

    # 画像の表示
    cv2.imshow('Hands', image_blank)  # 画像を表示
    
    # スペースキーを押したときにシャッターを切る
    if cv2.waitKey(5) & 0xFF == 32:  # スペースキーが押された場合
      output_path = f'static/pictures/real2_{real2_count}.jpg'

      # 画像のサイズを半分にする
      image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))

      cv2.imwrite("static/pictures/image2.jpg", image_blank) # キャプチャ実行 
      cv2.imwrite(output_path, image) # 背景が写っている画像の保存
      break
    if cv2.waitKey(5) & 0xFF == 27:  # Escキーが押された場合
      break  # ループを抜ける

# 実行回数を更新して保存
real2_count = real2_count + 2
with open(real2_count_file, 'w') as f:
    f.write(str(real2_count))

# キャプチャの終了
cap.release()