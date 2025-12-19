<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
<h1><center>Using DepthAnythingV3 as MVS</center></h1>
<h2>なにものか？</h2>
<p>
Depth Anything V3を使って多視点ステレオを行うプログラムです。<br>
<br>
<img src="images/workflow0.svg"><br>
入力するRGB画像群の例<br>
<img src="images/InputImages.png"><br>
<br>
Depth Anything V3を実行すると以下が得られる。<br>
・Processed RGB画像群 ･･･ AIモデルの解像度にリサイズされたRGB画像群<br>
・Depth画像群　　　　 ･･･ 各ピクセルの深度を推定したもの<br>
・Conf画像群　　　　　･･･ 各ピクセルの推定確度(今のところ使用せず)<br>
・内部パラメータ群　　･･･ ピクセル座標→カメラ座標の変換パラメータ群<br>
・外部パラメータ群　　･･･ カメラ座標→ワールド座標の変換パラメータ群<br>
<br>
Depth画像 / 内部パラメータ / 外部パラメータを使うとワールド座標に変換された点群が得られるが,<br>
各RGB画像には背景が写っており, <br>
<br>

<img src="images/Rgbd2Pcd.png"><br>
<br>
そのまま合成すると, こうなってしまう。<br>

<img src="images/Rgbd2Pcd.gif"><br>
<br>
後処理で背景色の点群を削除しても以下のようになる。<br>

<img src="images/filteredPLY.gif"><br>
<br>

課題1) 境界付近の点群が背景色に汚染されている。<br>
課題2) 位置合わせが不完全<br>
<br>
合成前でもこんな感じ<br>
<img src="images/Rgbd2Pcd_0001.gif">

<br>

対策1) ピクセル座標の段階で境界付近の点を削る。<br>
<img src="images/workaround1.svg">
<br>
つづく･･･<br>
<br>
対策2) レジストレーション：未着手<br>

</p>

<h2>環境構築方法</h2>
<p>
[1] Depth Anything V3をダウンロード～解凍する<br>
　　<a href="https://github.com/ByteDance-Seed/Depth-Anything-3">https://github.com/ByteDance-Seed/Depth-Anything-3</a><br>
　　Code --> Download ZIP<br>
<br>
　　Depth-Anything-3-main.zip を解凍する<br>
<br>
[2] Python実行環境を作成する<br>
　　conda create -n DA3 python=3.10<br>
　　conda activate DA3<br>
<br>
　　必要なモジュールをインストールする<br>
　　pip install -r requrements.txt
</p>
<h2>使い方</h2>

<p>
[0] 本github/src内のスクリプトを<br>
　　Depth-Anything-3-main/src 配下にコピーする<br>
<br>
[1] Depth Anything V3の推論を実行する<br>
　　python ExecDA3.py (画像群へのワイルドカード)<br>
　　(例) python ExecDA3.py input/*.png<br>
　　実行結果は result* フォルダに出力される。<br>
<br>
[2] 対策1)の侵食量を色々試して決める<br>
　　python trying_erode_level.py (RGB画像)<br>
　　※ (R,G,B)=(0,0,0)の領域をマスクと見なすので、そうなっていないRGB画像ではうまく動作しません。<br>
<img src="images/trying_erode_level.png"><br>
<br>

[3] Depth Anything V3の推論結果から点群を作成する<br>
　　python Rgbd2Pcd.py (推論結果を格納したフォルダ)<br>
　　(例) python Rgbd2Pcd.py result<br>

<br>
　　※ 対策1) はまだ適用されていません･･･<br>
　　　 対策2) も･･･<br>
<br>
[4] 点群を表示する<br>
　　python o3d_display_ply.py (点群ファイル)<br>
</p>
</body>
</html>
