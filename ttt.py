'''Tensorboard数据可视化--step-代表x轴
第一步：run listener
打开cmd，进入到logs文件夹之下(dir命令可以显示目录directory)
输入命令：tensorboard --logdir 路径名称 来创建一个监听窗口
如果不行报错，我们做如下操作：在site-packages文件夹下, 删掉tensorboard--2.0.0dist-info
然后复制网站，到谷歌浏览器打开，如果不行输入localhost:端口号
第二步：build summary
在代码中进行build summary
第三步：feed数据进去--可以是feed scalar/single-image/multi-images
'''
#import-step0
import datetime
import tensorflow as tf
import io #输入输出模块
import matplotlib.pyplot as plt
from tensorflow.keras import datasets,optimizers,layers,Sequential
'''
keras.metrics中有两个api函数可以简化准确率acc和损失值loss的计算。
其分别是metrics.Accuracy( )和metrics.Mean( )。
具体看下一个chapter
'''
#函数定义阶段-step0
def preprocess(x,y):
    x = tf.cast(x,dtype=tf.float32)/255.
    y = tf.cast(y,dtype=tf.int32)
    return x,y
#以下两个函数image_grid和plot_to_image实现了将多张图片组合在一起显示(暂时不用理解，可以直接套)
def plot_to_image(figure):#将figure画出来
    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    plt.close(figure)
    buf.seek(0)
    image = tf.image.decode_png(buf.getvalue(),channels=4)
    image = tf.expand_dims(image,0)
    return image
def image_grid(images):#25-->5*5
    figure = plt.figure(figsize=(10,10))
    for i in range(25):
        plt.subplot(5,5,i+1,title='name')
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i],cmap=plt.cm.binary)
    return figure
#寻找数据
batchsize = 128
(x,y),(x_val,y_val)=datasets.mnist.load_data()
print('Datasets:',x.shape,y.shape,x.min(),x.max(),y.min(),y.max())#0 255 0 9
#(60k,28,28,) (60k)
db = tf.data.Dataset.from_tensor_slices((x,y))
db = db.map(preprocess).shuffle(18888).batch(batchsize).repeat(10)
'''repeat的功能就是将整个数据重复多次,相当于对一个epoch进行多次训练,不用再写for循环'''
ds_val = tf.data.Dataset.from_tensor_slices((x_val,y_val))
ds_val = ds_val.map(preprocess).shuffle(18888).batch(batchsize,drop_remainder=True)
'''参数drop_remaindar
   用于标示是否对于最后一个batch如果数据量达不到batch_size时保留还是抛弃'''
net = Sequential([
    layers.Dense(256,activation='relu'),
    layers.Dense(128,activation='relu'),
    layers.Dense(64,activation='relu'),
    layers.Dense(32,activation='relu'),
    l