# Poetry-Generation
# :sunny:项目介绍:sunny:  
## 本项目是基于Paddlenlp模型和Flask框架的古诗词在线生成
### :blush:一、模型介绍：[Paddlenlp](https://github.com/PaddlePaddle/PaddleNLP#readme)
#### Paddlenlp能够直接获取适合的格式,不用再对通过其他途径获得的数据进行比较繁琐的处理同样也便于后续对数据的处理
### :stuck_out_tongue:二、实现功能：随机古诗生成和藏头诗生成（实际多种生成方法）
### :sunglasses:三、文件简解
### Static:html中css等静态文件.
### templates:flask模板文件,主要是前端的界面.
#### 1.Check_poetry.ipynb
##### Jupyter notebook文件.这里主要是用来测试集成的功能,只有几行调用,详细看Generate_poetry.py.
#### 2.Generate_poetry.py
##### 请关注87行载入生成模型处，第93行model.load('./final.pdparams')需要参数文件  
##### 本项目文件尚未上传该文件,后面给出获取文件的两种方式.
#### 3.Poetry-show.py
##### 两个函数,poetry-show函数先打印诗句，再返回一个诗句列表例如["飞流直下三千尺","疑是银河落九天"],便于后续传入前端界面.
#### 4.app.py
##### Flask框架应用函数
#### 5.model.py
##### 模型构造
#### 6.剩下几个.py都非常简单
# :sunny:版本:sunny:
### :green_apple:python 3.7
### :cherries:Flask 2.2.3
### :lemon:paddlenlp2.0.1
### :tangerine:numpy1.19.3
# :sunny:运行:sunny:
## :dragon_face:pdparams获取
### 1.[百度网盘](https://pan.baidu.com/s/1bA_i8NeaFni2xFY8HRrLyg?pwd=star 提取码：star)
### 2.Paddle Ai studio平台,每天可获取算力卡,找到关于bert生成古诗词的项目,运行就好了（选择1.0算力/小时的大概需要6~7个小时）,同样在checkpoint中获取pdparams.
### 3.安装依赖后直接运行model.py/Generate-poetry.py/然后找check-poetry notebook文件测试是否能生成古诗词
### 4.若还想集成到网站上，则需要flask框架
# :crystal_ball:网页上输入random则返回随机诗句,输入文字则作为藏头词:crystal_ball:
