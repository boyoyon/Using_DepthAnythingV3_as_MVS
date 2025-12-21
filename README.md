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
<img src="images/workaround1.svg"><br>
<br>
侵食サイズ:5 で境界付近の点群の汚れは取れた。<br>
(テストソース)<br>
・single_step_erode_rgb_depth_to_pcd.py <br>
　座標変換のバグを修正。<br>
　引数の指定も面倒だったので変更した。<br>
　(DepthAnythingV3実行結果のフォルダ)　(フレーム番号) を指定する。<br> 
<img src="images/erode_5.gif"><br>

ただ複数の点群(.ply)を合成するとこんな感じ･･･<br>
(テストソース)<br>
・o3d_display_multiple_plys.py<br>
・引数で PLYファイルへのワイルドカード(*.ply)を指定する<br>
<img src="images/erode_and_composite.png"><br>
<br>
対策2) 位置合わせ：ICPを実施。<br>
(テストソース)<br>
・test_ICP.py<br>
・引数 (PLYファイル1) (PLYファイル2)<br>
　きれいにはつなぎ合わせられず･･･(手動でつなぎ合わせるか･･･)<br>
<br>
　課題3) 位置合わせがうまくいった場合でも色合い、明るさの不連続が目立つ。<br>

<img src="images/ICP.svg"><br>
<br>
対策2') 位置合わせ：手動で位置合わせ。<br>
(テストソース)<br>
・manually_register.py<br>
・引数 (PLYファイル1) (PLYファイル2)<br>
　キー 1/2/3 で回転,　キー 4/5/6 で平行移動,　Shiftキーで逆方向<br>
　あっちを合わせれば、こっちがずれる･･･で気が変になりそうになる<br>
<img src="images/manually_register.gif"><br>
<br>
さらなる改善を思いつくまで一旦終了･･･<br>
<br>


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
