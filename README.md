# RVEサイズ決定プログラム

## 入力形式(.xyz)
プログラムの入力には、3次元画像のVoxelサイズ(e.g. 1024\*1024\*1024 px^3)
と2値化画像の1-画素の座標の集合のみを含む。
```
1024 1024 1024
1 2 1
1 3 4
5 5 0
...
1010 800 801
1011 1 20
1011 2 60
```
