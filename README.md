# picross_solver
ピクロスを解くプログラムです。

## 前提
横方向のヒント数字を horizontal_hints  
縦方向のヒント数字を vertical_hints  
と定義する。  

![](https://github.com/TaroTsuyama/picross_solver/blob/main/img/img001.png?raw=true)

horizontal_hints は上から順に、vertical_hints は左から順に list に格納していく。  
図の例だと次のようになる。  
```python
horizontal_hints = [
    [1],
    [5],
    [3],
    [1,1],
    [1,1],
]

vertical_hints = [
    [1,1],
    [3],
    [3],
    [3],
    [1,1],
]
```

## 使い方
sample を見てね。

1.picross_solver.Picross のインスタンスを生成  
第一引数: horizontal_hints  
第二引数: vertical_hints  

2.solve メソッドを実行

3.show メソッドで結果を表示


### 使用例
sample1
![](https://github.com/TaroTsuyama/picross_solver/blob/main/img/sample1.png?raw=true)

sample2
![](https://github.com/TaroTsuyama/picross_solver/blob/main/img/sample2.png?raw=true)

sample3
![](https://github.com/TaroTsuyama/picross_solver/blob/main/img/sample3.png?raw=true)

## 注意点
現段階では 10x10 くらいのサイズまでが実用的な範囲。  
それより大きいものだと処理時間がとっても長くなります。  

10x10 でも物によっては何時間も掛かってしまう事があります。