import tensorflow as tf
import numpy as np
# 这是一个提交
tf.compat.v1.disable_eager_execution()
#一共有1个添加神经层、一个输入层、10个隐藏层、1个输出层
#添加神经层 常见的参数有weights，biases和激励函数
#定义神经层的函数 参数为 输入值、输入的大小、 输出的大小 和激励函数，这里默认为None
def add_layer(inputs, in_size, out_size, activation_function=None, n_layer=1):
    layer_name = 'layer%s'%n_layer  #这里的%s就是一个字符，不知道在问我
    with tf.name_scope('layer'):
    #定义成一个in_size行， out_size列的随机变量矩阵
        with tf.name_scope('Weights'):
            Weights = tf.Variable(tf.compat.v1.random_normal([in_size, out_size]))
            #用来显示直方图信息  图的名字 收集的源(collection)
            tf.compat.v1.summary.histogram(layer_name + '/weights', Weights)
    #biases不推荐为0
        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
            tf.compat.v1.summary.histogram(layer_name + 'biases', biases)
    #matmul是矩阵乘法 y = weights * inputs + biases Wx_plus_b是预测值
        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.matmul(inputs, Weights) + biases
        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)
        tf.compat.v1.summary.histogram(layer_name+'/outputs',outputs)
        return outputs


#导入数据
x_data = np.linspace(-1, 1, 300, dtype=np.float32)[:,np.newaxis]#列扩展
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise # y = x ** 2 + noise
#这里的None代表无论输入有多少都可以，因为输入只有一个特征，所以这里是1。
with tf.name_scope('inputs'):
    xs = tf.compat.v1.placeholder(tf.float32, [None, 1], name='x_in')
    ys = tf.compat.v1.placeholder(tf.float32, [None, 1], name='y_in')
#定义隐藏层  自带tf.nn.relu
l1 = add_layer(xs, 1, 10, activation_function=tf.compat.v1.nn.relu, n_layer=1)
#定义输出层。此时的输入就是隐藏层的输出——l1，输入有10层（隐藏层的输出层），输出有1层。
prediction = add_layer(l1, 10, 1, activation_function=None, n_layer=2)
#计算预测值prediction和真实值的误差，对二者差的平方求和再取平均,也叫损失值
#axis称为“坍塌维度”，当[0]是表示0维坍塌，即原来的n行变1行，即按行进行sum
#[1]是表示1维坍塌,即原来的n列变1列，即按列进行sum   eduction_indices
#比如[[1,4,9,16]，[1,4,9,16]]  [0]-->[2,8,18,32]  [1]-->[30,30]
with tf.name_scope('loss'):
    loss = tf.compat.v1.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), axis=[1]))
    #tf.summary.scalar(tags, values, collections=None, name=None) 标量统计结果
    tf.compat.v1.summary.scalar('loss', loss)
#提高机器学习的准确性，tf.train.GradientDescentOptimizer()中的值通常都小于1，这里取0.1
with tf.name_scope('train'):
    train_step = tf.compat.v1.train.GradientDescentOptimizer(0.1).minimize(loss)
#初始化
init = tf.compat.v1.global_variables_initializer()
x_data = np.linspace(-1, 1, 300, dtype=np.float32)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise # y = x ** 2 - 0.5 + noise
#获取session，并运行init 给所有训练图合并
Sess = tf.compat.v1.Session()
Sess.run(init)
merged = tf.compat.v1.summary.merge_all()
writer = tf.compat.v1.summary.FileWriter('logs/', Sess.graph)

for i in range(1000):
    Sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        #得run merged才能进行运行这个图形
        rs = Sess.run(merged, feed_dict={xs: x_data, ys: y_data})
        #把运行的结果添加到summary中
        writer.add_summary(rs, i)



