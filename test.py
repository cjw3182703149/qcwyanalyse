import tensorflow as tf
import numpy as np
tf.compat.v1.disable_eager_execution()
#一共有1个添加神经层、一个输入层、10个隐藏层、1个输出层
#添加神经层 常见的参数有weights，biases和激励函数
#定义神经层的函数 参数为 输入值、输入的大小、 输出的大小 和激励函数，这里默认为None
def add_layer(inputs, in_size, out_size, activation_function=None):
    #定义成一个in_size行， out_size列的随机变量矩阵
    Weights = tf.Variable(tf.compat.v1.random_normal(in_size, out_size))
    #biases不推荐为0
    biases = tf.Variable(tf.zeros[1, out_size] + 0.1)
    #matmul是矩阵乘法 y = weights * inputs + biases Wx_plus_b是预测值
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

#导入数据
x_data = np.linspace(-1, 1, 300, dtype=np.dtype32)[:,np.newaxis]#列扩展
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise # y = x ** 2 + noise
#这里的None代表无论输入有多少都可以，因为输入只有一个特征，所以这里是1。
xs = tf.compat.v1.placeholder(tf.float32, [None, 1])
ys = tf.compat.v1.placeholder(tf.float32, [None, 1])
#定义隐藏层  自带tf.nn.relu
l1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)
#定义输出层。此时的输入就是隐藏层的输出——l1，输入有10层（隐藏层的输出层），输出有1层。
prediction = add_layer(l1, 10, 1, activation_function=None)
#计算预测值prediction和真实值的误差，对二者差的平方求和再取平均,也叫损失值
#reduction_indices称为“坍塌维度”，当[0]是表示0维坍塌，即原来的n行变1行，即按行进行sum
#[1]是表示1维坍塌,即原来的n列变1列，即按列进行sum
#比如[[1,4,9,16]，[1,4,9,16]]  [0]-->[2,8,18,32]  [1]-->[30,30]
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))











