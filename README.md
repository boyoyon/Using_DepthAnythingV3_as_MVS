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
多視点画像の深度画像を点群にしてまとめてみたが･･･(VGGTの時よりひどい結果に)<br>
(いつか改善するかも知れないので)備忘録として･･･<br>
・背景との境界が汚くなるので, 点群に透明度を持たせるか?<br>
・ICPか何かで位置合わせをしないと･･･<br>
　　：<br>
<br>
入力画像<br>
<img src="images/InputImages.png"><br>
<br>
点群の貼り合わせ結果<br>
<img src="images/Rgbd2Pcd.gif"><br>
<br>
カラーキーでPLYをフィルター<br>
<img src="images/filteredPLY.gif"><br>
<br>
1枚1枚の点群はどれほど悪くない。合成前に点群の縁(へり)のゴミを削ればよさそう。<br>
点群の縁(へり)はどうやって抽出するんだろう･･･<br>
<img src="images/Rgbd2Pcd_0001.gif"><br>
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
●ワークフロー
</p>
<img src="images/workflow.svg">
<p>
　・Processed RGB画像群 ･･･ AIモデルの解像度にリサイズされたRGB画像群<br>
　・Depth画像群　　　　 ･･･ 推定された奥行画像群<br>
　・Conf画像群　　　　　･･･ ピクセル毎の推定確度(今のところ使用せず)<br>
　・内部パラメータ群　　･･･ 推定されたカメラ内部パラメータ<br>
　・外部パラメータ群　　･･･ 推定されたカメラ外部パラメータ<br>
</p>
<p>
[0] 本github/src内のスクリプトを<br>
　　Depth-Anything-3-main/src 配下にコピーする<br>
<br>
[1] Depth Anything V3の推論を実行する<br>
　　python ExecDA3.py (画像群へのワイルドカード)<br>
　　(例) python ExecDA3.py input/*.png<br>
　　実行結果は result* フォルダに出力される。<br>
<br>
[2] Depth Anything V3の推論結果から点群を作成する<br>
　　python Rgbd2Pcd.py (推論結果を格納したフォルダ)<br>
　　(例) python Rgbd2Pcd.py result<br>
<br>
[3] 点群を表示する<br>
　　python o3d_display_ply.py (点群ファイル)<br>
</p>

    </body>
</html>
