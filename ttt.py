'''Tensorboard���ݿ��ӻ�--step-����x��
��һ����run listener
��cmd�����뵽logs�ļ���֮��(dir���������ʾĿ¼directory)
�������tensorboard --logdir ·������ ������һ����������
������б������������²�������site-packages�ļ�����, ɾ��tensorboard--2.0.0dist-info
Ȼ������վ�����ȸ�������򿪣������������localhost:�˿ں�
�ڶ�����build summary
�ڴ����н���build summary
��������feed���ݽ�ȥ--������feed scalar/single-image/multi-images
'''
#import-step0
import datetime
import tensorflow as tf
import io #�������ģ��
import matplotlib.pyplot as plt
from tensorflow.keras import datasets,optimizers,layers,Sequential
'''
keras.metrics��������api�������Լ�׼ȷ��acc����ʧֵloss�ļ��㡣
��ֱ���metrics.Accuracy( )��metrics.Mean( )��
���忴��һ��chapter
'''
#��������׶�-step0
def preprocess(x,y):
    x = tf.cast(x,dtype=tf.float32)/255.
    y = tf.cast(y,dtype=tf.int32)
    return x,y
#������������image_grid��plot_to_imageʵ���˽�����ͼƬ�����һ����ʾ(��ʱ������⣬����ֱ����)
def plot_to_image(figure):#��figure������
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
#Ѱ������
batchsize = 128
(x,y),(x_val,y_val)=datasets.mnist.load_data()
print('Datasets:',x.shape,y.shape,x.min(),x.max(),y.min(),y.max())#0 255 0 9
#(60k,28,28,) (60k)
db = tf.data.Dataset.from_tensor_slices((x,y))
db = db.map(preprocess).shuffle(18888).batch(batchsize).repeat(10)
'''repeat�Ĺ��ܾ��ǽ����������ظ����,�൱�ڶ�һ��epoch���ж��ѵ��,������дforѭ��'''
ds_val = tf.data.Dataset.from_tensor_slices((x_val,y_val))
ds_val = ds_val.map(preprocess).shuffle(18888).batch(batchsize,drop_remainder=True)
'''����drop_remaindar
   ���ڱ�ʾ�Ƿ�������һ��batch����������ﲻ��batch_sizeʱ������������'''
net = Sequential([
    layers.Dense(256,activation='relu'),
    layers.Dense(128,activation='relu'),
    layers.Dense(64,activation='relu'),
    layers.Dense(32,activation='relu'),
    l