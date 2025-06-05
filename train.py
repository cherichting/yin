import matplotlib.pyplot as plt
import tensorflow as tf
import matplotlib
import pathlib
import random
import os



def get_paths_labels(data_root):

    all_image_paths = list(data_root.glob('*/*')) #所有文件
    all_image_paths = [str(path) for path in all_image_paths] #所有文件字符串
    random.shuffle(all_image_paths)         #随机打乱
    label_names = sorted(item.name for item in data_root.glob('*/') if item.is_dir())   #如果是目录获取名称，即获取中文名
    label_to_index = dict((name, index) for index, name in enumerate(label_names))    #获取文件名称和文件内容
    all_image_labels = [label_to_index[pathlib.Path(path).parent.name] for path in all_image_paths]   #获取标签
    print(all_image_paths, all_image_labels, label_names)
    return all_image_paths, all_image_labels, label_names

def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [image_height, image_width])
    image /= 255.0
    return image


def load_and_preprocess_image(path):

    image = tf.io.read_file(path)
    return preprocess_image(image)


def create_dataset(images, labels):

    image_ds = tf.data.Dataset.from_tensor_slices(images)
    image_ds = image_ds.map(load_and_preprocess_image, num_parallel_calls=AUTOTUNE)
    label_ds = tf.data.Dataset.from_tensor_slices(labels)
    image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))
    return image_label_ds



data_root = pathlib.Path("./train")

image_height, image_width = 300, 300
AUTOTUNE = tf.data.experimental.AUTOTUNE


all_image_paths, all_image_labels, label_names = get_paths_labels(data_root)
image_label_ds = create_dataset(all_image_paths, all_image_labels)


images_count = len(all_image_paths)
batch_size = 128


train_ds = image_label_ds.take(tf.cast(images_count * 0.8, "int64"))
val_ds = image_label_ds.skip(tf.cast(images_count * 0.8, "int64"))
train_ds = train_ds.shuffle(buffer_size=tf.cast(images_count * 0.8, "int64"))
val_ds = val_ds.shuffle(buffer_size=tf.cast(images_count * 0.2, "int64"))
train_ds = train_ds.repeat()
val_ds = val_ds.repeat()
train_ds = train_ds.batch(batch_size=batch_size)
val_ds = val_ds.batch(batch_size=batch_size)


mobile_net = tf.keras.applications.MobileNetV2(input_shape=(image_height, image_width, 3), include_top=False)
mobile_net.trainable = False
# 构建Keras中Sequential模型
model = tf.keras.Sequential([
    mobile_net, # 核心层
    tf.keras.layers.GlobalAveragePooling2D(), # 施加全局平均值池化
    tf.keras.layers.Dense(len(label_names), activation='softmax')# 全连接层
     ])
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categori'
                                                         'cal_crossentropy', metrics=["accuracy"])
model.summary()

checkpoint_save_path = "./ricew.ckpt"

if os.path.exists(checkpoint_save_path + '.index'):
    print('-------------加载模型-----------------')
    model.load_weights(checkpoint_save_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path, save_weights_only=True,
                                                 save_best_only=True)

train_per_epoch = tf.math.ceil(images_count * 0.8 / batch_size).numpy()
val_per_epoch = tf.math.ceil(images_count * 0.2 / batch_size).numpy()
history = model.fit(train_ds, epochs=5, steps_per_epoch=train_per_epoch, validation_data=val_ds,
                    validation_steps=val_per_epoch,
                    callbacks=[cp_callback])


# 确保中文显示正常
matplotlib.rcParams['font.family'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 获取训练和验证集的准确率和损失率数据
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

# 创建一个大的图形
plt.figure(figsize=(16, 6))

# 绘制准确率图表
plt.subplot(1, 2, 1)
plt.plot(acc, 'o-', label='训练集准确率')
plt.plot(val_acc, 's-', label='验证集准确率')
plt.title('训练集和验证集的准确率', fontsize=20)
plt.xlabel('迭代次数', fontsize=16)
plt.ylabel('准确率', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylim(min(min(acc), min(val_acc)) - 0.05, max(max(acc), max(val_acc)) + 0.05)
plt.legend(loc='best', fontsize=14)

# 绘制损失率图表
plt.subplot(1, 2, 2)
plt.plot(loss, 'o-', label='训练集损失')
plt.plot(val_loss, 's-', label='验证集损失')
plt.title('训练集和验证集的损失率', fontsize=20)
plt.xlabel('迭代次数', fontsize=16)
plt.ylabel('损失率', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylim(min(min(loss), min(val_loss)) - 0.05, max(max(loss), max(val_loss)) + 0.05)
plt.legend(loc='best', fontsize=14)

# 自动调整布局，防止文字重叠
plt.tight_layout()

# 显示图形
plt.show()