# ライブラリインポート
import cv2
import numpy as np
import os


# プログラムが実行された回数を保持するファイルのパス
execution_count_file = 'execution_count.txt'

# プログラムが実行された回数を読み込む
if os.path.exists(execution_count_file):
    with open(execution_count_file, 'r') as f:
        execution_count = int(f.read())
else:
    execution_count = 0


# 画像の読み込み
pic1 = cv2.imread('static/pictures/image1.jpg', cv2.IMREAD_COLOR)  # 画像1をカラーで読み込む
pic2 = cv2.imread('static/pictures/image2.jpg', cv2.IMREAD_COLOR)  # 画像2をカラーで読み込む

# 二値化処理
pic2gray = cv2.imread('static/pictures/image2.jpg', cv2.IMREAD_GRAYSCALE)  # 画像2をグレースケールで読み込む
ret, thresh = cv2.threshold(pic2gray, 5, 255, cv2.THRESH_BINARY)  # 二値化処理を適用

# 輪郭抽出
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)  # 輪郭を抽出
max_cnt = max(contours, key=lambda x: cv2.contourArea(x))  # 最大の輪郭を取得

# マスク画像の作成
pic2thresh = cv2.drawContours(pic2gray, [max_cnt], -1, 255, -1)  # 最大の輪郭に基づいてマスク画像を作成
# cv2.imwrite('pic2thresh2.jpg', np.array(pic2thresh))  # マスク画像を保存

# 画像合成前処理
pic2[pic2thresh < 255] = [0, 0, 0]  # マスク画像の白い部分以外を黒くする
pic1[pic2thresh == 255] = [0, 0, 0]  # マスク画像の白い部分を黒くする
# cv2.imwrite('pic2thres3.jpg', np.array(pic1))  # 処理後の画像を保存

# 画像合成
pic3 = cv2.add(pic1, pic2)  # 画像1と画像2を合成

# 画像のサイズを半分にする
pic3 = cv2.resize(pic3, (pic3.shape[1] // 2, pic3.shape[0] // 2))

# 合成画像を保存
output_path = f'static/pictures/Add_{execution_count}.jpg'
cv2.imwrite(output_path, np.array(pic3))

# 実行回数を更新して保存
execution_count = execution_count + 2
with open(execution_count_file, 'w') as f:
    f.write(str(execution_count))

print(f"合成画像を保存しました: {output_path}")