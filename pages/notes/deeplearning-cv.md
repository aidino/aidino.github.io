---
layout: libdoc/page
title: Deep Learning - Computer Vision
permalink: /dl-computer-vision
unlisted: true
category: Notes
description: "Reusable code snippets for computer vision and deep learning."
order: 1
---
{:toc}
- *Code:* 
<br>

## 0. Getting setup
Import các thư viện cần thiết, hiển thị một số thông số quan trọng về môi trường chạy như: tensorflow version, keras version, có GPU hay không? ...

### Import libraries

```python
import os
import glob
import sys
import platform
import itertools
import datetime
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers.experimental import preprocessing
from pathlib import Path
from sklearn.metrics import confusion_matrix, classification_report

# Sử dụng trong file notebook để auto reload những thay đổi có trong file helper (nếu có)
%reload_ext autoreload
%autoreload 2

# Ignore warning
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings('ignore')
```



### Print env info

```python
print("#-------------- ENVIRONMENT ---------------#")
print(f"Python Platform: {platform.platform()}")
print(f"Python {sys.version}")
print(f"Tensor Flow Version: {tf.__version__}")
print(f"Keras Version: {tensorflow.keras.__version__}")

gpus = tf.config.list_physical_devices('GPU')
print("GPU is", "available" if len(gpus)>0 else "NOT AVAILABLE")
for gpu in gpus:
    print("\t Name:", gpu.name)
print("#-------------------------------------------#")
```



## 1.Get data

#### Tải dữ liệu về, show file structure để có cái nhìn tổng quan về dữ liệu mới tải

```bash
!wget https://storage.googleapis.com/mlep-public/course_1/week2/kagglecatsanddogs_3367a.zip
```

```python
# Extrax data
cats_and_dogs_zip = './content/kagglecatsanddogs_3367a.zip'
caltech_birds_tar = './content/CUB_200_2011.tar'
base_dir = './tmp/data'

with zipfile.ZipFile(cats_and_dogs_zip, 'r') as my_zip:
  my_zip.extractall(base_dir)
  
with tarfile.open(caltech_birds_tar, 'r') as my_tar:
  my_tar.extractall(base_dir)
```

#### Move data

```python
raw_birds_dir = './tmp/data/CUB_200_2011/images'
base_birds_dir = os.path.join(base_dir,'PetImages/Bird')
os.mkdir(base_birds_dir)

for subdir in os.listdir(raw_birds_dir):
  subdir_path = os.path.join(raw_birds_dir, subdir)
  for image in os.listdir(subdir_path):
    shutil.move(os.path.join(subdir_path, image), os.path.join(base_birds_dir))

print(f"There are {len(os.listdir(base_birds_dir))} images of birds")
```

#### Display sample

```python
from IPython.display import Image, display

print("Sample cat image:")
display(Image(filename=f"{os.path.join(base_cats_dir, os.listdir(base_cats_dir)[0])}")
```

#### Train/evaluate split

```python
train_eval_dirs = ['train/cats', 'train/dogs', 'train/birds',
                   'eval/cats', 'eval/dogs', 'eval/birds']

for dir in train_eval_dirs:
  if not os.path.exists(os.path.join(base_dir, dir)):
    os.makedirs(os.path.join(base_dir, dir))
```

#### Move to destination

```python
def move_to_destination(origin, destination, percentage_split):
  num_images = int(len(os.listdir(origin))*percentage_split)
  for image_name, image_number in zip(sorted(os.listdir(origin)), range(num_images)):
    shutil.move(os.path.join(origin, image_name), destination)
    
# Move 70% of the images to the train dir
move_to_destination(base_cats_dir, os.path.join(base_dir, 'train/cats'), 0.7)
move_to_destination(base_dogs_dir, os.path.join(base_dir, 'train/dogs'), 0.7)
move_to_destination(base_birds_dir, os.path.join(base_dir, 'train/birds'), 0.7)

# Move the remaining images to the eval dir
move_to_destination(base_cats_dir, os.path.join(base_dir, 'eval/cats'), 1)
move_to_destination(base_dogs_dir, os.path.join(base_dir, 'eval/dogs'), 1)
move_to_destination(base_birds_dir, os.path.join(base_dir, 'eval/birds'), 1)
```

#### Copy with limit

```python
# Very similar to the one used before but this one copies instead of moving
def copy_with_limit(origin, destination, percentage_split):
  num_images = int(len(os.listdir(origin))*percentage_split)
  for image_name, image_number in zip(sorted(os.listdir(origin)), range(num_images)):
    shutil.copy(os.path.join(origin, image_name), destination)
    
# Perform the copying
copy_with_limit(os.path.join(base_dir, 'train/cats'), os.path.join(base_dir, 'imbalanced/train/cats'), 1)
copy_with_limit(os.path.join(base_dir, 'train/dogs'), os.path.join(base_dir, 'imbalanced/train/dogs'), 0.2)
copy_with_limit(os.path.join(base_dir, 'train/birds'), os.path.join(base_dir, 'imbalanced/train/birds'), 0.1)

# Print number of available images
print(f"There are {len(os.listdir(os.path.join(base_dir, 'imbalanced/train/cats')))} images of cats for training")
print(f"There are {len(os.listdir(os.path.join(base_dir, 'imbalanced/train/dogs')))} images of dogs for training")
print(f"There are {len(os.listdir(os.path.join(base_dir, 'imbalanced/train/birds')))} images of birds for training\n")

```

#### Clean data folder

```python
!find ./tmp/data/ -size 0 -exec rm {} +
!find ./tmp/data/ -type f ! -name "*.jpg" -exec rm {} +
```

## 2. Prepare data

#### Visualize, visualize and visualize ...

```python
from IPython.display import Image, display
print("Sample cat image:")
display(Image(filename=f"{os.path.join(base_cats_dir, os.listdir(base_cats_dir)[0])}")
```



Hiển thị các ảnh ngẫu nhiên, các lớp, sau đó chuẩn bị phân chia vào các dataset tương ứng, chuẩn bị sẵn sàng để đưa vào model

```python
train_dir = data_dir + "/train"
test_dir = data_dir + "/test"

train_data = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=image_size,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

test_data = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    image_size=image_size,
    batch_size=BATCH_SIZE,
    label_mode='categorical',
    shuffle=False
)
```

## 3. Experiments

### Build models

```python
base_model = tf.keras.applications.EfficientNetB0(include_top=False)
base_model.trainable = False

inputs = tf.keras.layers.Input(shape=(image_size[0], image_size[1], 3), name='input_layer')
data_augmentation = ModelHelper.data_augmentation_layer()

x = data_augmentation(inputs)
x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D(name='global_average_pooling_layer')(x)
outputs = tf.keras.layers.Dense(len(class_names), activation='softmax', name='output_layer')(x)
model = tf.keras.Model(inputs, outputs)

model.compile(
    loss='categorical_crossentropy', 
    optimizer=tf.keras.optimizers.Adam(learning_rate), 
    metrics=['accuracy'])

history_0 = model.fit(
    train_data,
    epochs = initial_epochs,
    validation_data = test_data,
    validation_steps = int(0.15 * len(test_data)),
    callbacks=[checkpoint]
)
```

Fine-turning model

```python
# Setting up for fine-tuning last 5 layers of base model
base_model.trainable = True
for layer in base_model.layers[:-5]:
    layer.trainable = False
ModelHelper.print_trainable_info(base_model)
```

#### Full example

```python
# In another way
from tensorflow.keras import layers, models, optimizers

def create_model():
  # A simple CNN architecture based on the one found here: https://www.tensorflow.org/tutorials/images/classification
  model = models.Sequential([
  layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
  layers.MaxPooling2D((2, 2)),
  layers.Conv2D(64, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.Conv2D(64, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.Conv2D(128, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.Flatten(),
  layers.Dense(512, activation='relu'),
  layers.Dense(3, activation='softmax')
  ])
  # Compile the model
  model.compile(
      loss=tf.keras.losses.SparseCategoricalCrossentropy(),
      optimizer=optimizers.Adam(),
      metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
  )
  return model

---

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# No data augmentation for now, only normalizing pixel values
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Point to the imbalanced directory
train_generator = train_datagen.flow_from_directory(
        './tmp/data/imbalanced/train',
        target_size=(150, 150),
        batch_size=32,
        class_mode='sparse')

validation_generator = test_datagen.flow_from_directory(
        './tmp/data/imbalanced/eval',
        target_size=(150, 150),
        batch_size=32,
        class_mode='sparse')

print(f"labels for each class in the train generator are: {train_generator.class_indices}")
print(f"labels for each class in the validation generator are: {validation_generator.class_indices}")

imbalanced_history = imbalanced_model.fit(
    train_generator,
    steps_per_epoch=100,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=80)

def get_training_metrics(history):
  
  # This is needed depending on if you used the pretrained model or you trained it yourself
  if not isinstance(history, pd.core.frame.DataFrame):
    history = history.history
  
  acc = history['sparse_categorical_accuracy']
  val_acc = history['val_sparse_categorical_accuracy']

  loss = history['loss']
  val_loss = history['val_loss']

  return acc, val_acc, loss, val_loss

def plot_train_eval(history):
  acc, val_acc, loss, val_loss = get_training_metrics(history)

  acc_plot = pd.DataFrame({"training accuracy":acc, "evaluation accuracy":val_acc})
  acc_plot = sns.lineplot(data=acc_plot)
  acc_plot.set_title('training vs evaluation accuracy')
  acc_plot.set_xlabel('epoch')
  acc_plot.set_ylabel('sparse_categorical_accuracy')
  plt.show()

  print("")

  loss_plot = pd.DataFrame({"training loss":loss, "evaluation loss":val_loss})
  loss_plot = sns.lineplot(data=loss_plot)
  loss_plot.set_title('training vs evaluation loss')
  loss_plot.set_xlabel('epoch')
  loss_plot.set_ylabel('loss')
  plt.show()

plot_train_eval(imbalanced_history)

---
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, balanced_accuracy_score

# Use the validation generator without shuffle to easily compute additional metrics
val_gen_no_shuffle = test_datagen.flow_from_directory(
    './tmp/data/imbalanced/eval',
    target_size=(150, 150),
    batch_size=32,
    class_mode='sparse',
    shuffle=False)

# Get the true labels from the generator
y_true = val_gen_no_shuffle.classes
# Use the model to predict (will take a couple of minutes)
predictions_imbalanced = imbalanced_model.predict(val_gen_no_shuffle)
# Get the argmax (since softmax is being used)
y_pred_imbalanced = np.argmax(predictions_imbalanced, axis=1)
# Print accuracy score
print(f"Accuracy Score: {accuracy_score(y_true, y_pred_imbalanced)}")
# Print balanced accuracy score
print(f"Balanced Accuracy Score: {balanced_accuracy_score(y_true, y_pred_imbalanced)}")

imbalanced_cm = confusion_matrix(y_true, y_pred_imbalanced)
ConfusionMatrixDisplay(imbalanced_cm, display_labels=['birds', 'cats', 'dogs']).plot(values_format="d")

misclassified_birds = (imbalanced_cm[0, 1] + imbalanced_cm[0, 2])/np.sum(imbalanced_cm, axis=1)[0]
misclassified_cats = (imbalanced_cm[1, 0] + imbalanced_cm[1, 2])/np.sum(imbalanced_cm, axis=1)[1]
misclassified_dogs = (imbalanced_cm[2, 0] + imbalanced_cm[2, 1])/np.sum(imbalanced_cm, axis=1)[2]

print(f"Proportion of misclassified birds: {misclassified_birds*100:.2f}%")
print(f"Proportion of misclassified cats: {misclassified_cats*100:.2f}%")
print(f"Proportion of misclassified dogs: {misclassified_dogs*100:.2f}%")
```



### Data augmentation layer

```python
from tensorflow.keras.layers.experimental import preprocessing

preprocessing_layers = Sequential([
            preprocessing.RandomFlip("horizontal"),
            preprocessing.RandomRotation(0.2),
            preprocessing.RandomZoom(0.2),
            preprocessing.RandomHeight(0.2),
            preprocessing.RandomWidth(0.2),
            ], name="data_augmentation")
```

### Print model info

```python
def print_trainable_info(model):
        """ In ra summary của model

        Args:
            model (Model): Model
        """    
        print(
            "STT".ljust(6) 
            + "Name".ljust(30) 
            + "Shape".ljust(30)
            +  "Trainable".ljust(15)
            + "dtype".ljust(15)
            + "Policy".ljust(15))
        print("-"*109)
        info = list()
        for i, layer in enumerate(model.layers):
            info_dict = {}
            info_dict['STT'] = i
            info_dict['Name'] = layer.name
            info_dict['Shape'] = layer.output_shape
            info_dict['Trainable'] = layer.trainable
            info_dict['Policy'] = layer.dtype_policy
            info_dict['dtype'] = layer.dtype
            info.append(info_dict)
        for d in reversed(info):
            print(
                str(d['STT']).ljust(6) 
                + d['Name'].ljust(30) 
                + str(d['Shape']).ljust(30) 
                + str(d['Trainable']).ljust(15)
                + str(d['dtype']).ljust(15)
                + str(d['Policy']).ljust(15)) 
```

### Callbacks

#### tensorboard callback

```python
log_dir = dir_name + "/" + experiment_name + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
```

#### learning rate callback

```python
lr_schedule = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-4 * 10**(epoch/20))
```

#### checkpoint callback

```python
checkpoint_path = dir_name + "/" + experiment_name +  "/cp.ckpt"
# Tạo ModelCheckpoint callback chỉ để lưu các trọn số của mô hình 
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    save_best_only=True, # đặt là True để chỉ lưu những mô hình tốt nhất thay vì một mô hình mỗi epoch
    monitor='val_loss')
print(f"Saving model checkpoints to: {checkpoint_path}")
```

#### early stopping callback

```python
tf.keras.callbacks.EarlyStopping(
  monitor="val_loss", # theo dõi phép đo val loss
  patience=3) # nếu val loss giảm trong 3 epoch liên tiếp, hãy ngừng huấn luyện
```

#### reduce learning rate callback

```python
tf.keras.callbacks.ReduceLROnPlateau(
  monitor="val_loss", 
  factor=0.2, # nhân learning rate với 0.2 (giảm 5 lần)
  patience=2,
  verbose=1, # in ra khi nào learning rate giảm
  min_lr=1e-7)
```

## 4. Evaluation

```python
def plot_loss_curves(results):
        """ Vẽ đồ thị loss và accuracy của model

        Args:
            results (dict): dictionary chứa loss và accuracy của model. Ví dụ:
                {"loss": [...],
                "accuracy": [...],
                "val_loss": [...],
                "val_accuracy": [...]}
        """
        loss = results["loss"]
        test_loss = results["val_loss"]

        accuracy = results["accuracy"]
        test_accuracy = results["val_accuracy"]

        epochs = range(len(results["loss"]))

        plt.figure(figsize=(15, 7))

        # Plot loss
        plt.subplot(1, 2, 1)
        plt.plot(epochs, loss, label="train_loss")
        plt.plot(epochs, test_loss, label="test_loss")
        plt.title("Loss")
        plt.xlabel("Epochs")
        plt.legend()

        # Plot accuracy
        plt.subplot(1, 2, 2)
        plt.plot(epochs, accuracy, label="train_accuracy")
        plt.plot(epochs, test_accuracy, label="test_accuracy")
        plt.title("Accuracy")
        plt.xlabel("Epochs")
        plt.legend()
```

```python
def make_confusion_matrix(y_true, y_pred, classes=None, figsize=(10, 10), text_size=15, norm=False, savefig=False): 
        """ Tạo confusion matrix để đánh giá model dựa trên y_true và y_pred 
        
        Nếu classes được truyền vào, confusion matrix sẽ được gán nhãn, 
        nếu không, giá trị class sẽ được gán nhãn bằng số nguyên

        Args:
            y_true: Mảng chứa nhãn thực tế (phải có cùng kích thước với y_pred).
            y_pred: Mảng chứa nhãn dự đoán (phải có cùng kích thước với y_true).
            classes: Mảng chứa nhãn của các class (ví dụ: dạng string). Nếu `None`, nhãn sẽ là số nguyên.
            figsize: Kích thước của figure (default=(10, 10)).
            text_size: Kích thước của chữ (default=15).
            norm: normalize values hay không (default=False).
            savefig: Lưu figure hay không (default=False).
        
        Returns:
            Một labelled confusion matrix được vẽ để so sánh y_true và y_pred.

        Example usage:
            make_confusion_matrix(y_true=test_labels, # ground truth test labels
                                y_pred=y_preds, # predicted labels
                                classes=class_names, # array of class label names
                                figsize=(15, 15),
                                text_size=10)
        """  
        # Create the confustion matrix
        cm = confusion_matrix(y_true, y_pred)
        cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] # normalize it
        n_classes = cm.shape[0] # find the number of classes we're dealing with

        # Plot the figure and make it pretty
        fig, ax = plt.subplots(figsize=figsize)
        cax = ax.matshow(cm, cmap=plt.cm.Blues) # colors will represent how 'correct' a class is, darker == better
        fig.colorbar(cax)

        # Are there a list of classes?
        if classes:
            labels = classes
        else:
            labels = np.arange(cm.shape[0])
        
        # Label the axes
        ax.set(title="Confusion Matrix",
                xlabel="Predicted label",
                ylabel="True label",
                xticks=np.arange(n_classes), # create enough axis slots for each class
                yticks=np.arange(n_classes), 
                xticklabels=labels, # axes will labeled with class names (if they exist) or ints
                yticklabels=labels)
        
        # Make x-axis labels appear on bottom
        ax.xaxis.set_label_position("bottom")
        ax.xaxis.tick_bottom()
        # set the rotation for the x axis tick labels to 45 degrees
        ax.tick_params(axis="x", rotation=45)

        # Set the threshold for different colors
        threshold = (cm.max() + cm.min()) / 2.

        # Plot the text on each cell
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if norm:
                plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
                    horizontalalignment="center",
                    color="white" if cm[i, j] > threshold else "black",
                    size=text_size)
            else:
                plt.text(j, i, f"{cm[i, j]}",
                    horizontalalignment="center",
                    color="white" if cm[i, j] > threshold else "black",
                    size=text_size)

        # Save the figure to the current working directory
        if savefig:
            fig.savefig("confusion_matrix.png")
```

```python
def plot_learning_rate_and_loss(history, epochs):
        # Vẽ biểu đồ learning rate với loss
        lrs = 1e-4 * (10 ** (np.arange(epochs)/20))
        plt.figure(figsize=(10, 7))
        plt.semilogx(lrs, history["loss"]) # muốn trục x (learning rate) theo thang log
        plt.xlabel("Learning Rate")
        plt.ylabel("Loss")
        plt.title("Learning rate vs. loss")
```

```python
def compare_historys(original_history, new_history, initial_epochs=5):
        """ So sánh 2 history của model
            Thường là so sánh history của model gốc với history của model sau khi fine-tuning

        Args:
            original_history (dict): History của model gốc
            new_history (dict): History của model mới
            initial_epochs (int, optional): Số epochs ban đầu của model gốc. Defaults to 5.
        """
        
        # Get original history measurements
        acc = original_history.history["accuracy"]
        loss = original_history.history["loss"]

        val_acc = original_history.history["val_accuracy"]
        val_loss = original_history.history["val_loss"]

        # Combine original history with new history
        total_acc = acc + new_history.history["accuracy"]
        total_loss = loss + new_history.history["loss"]

        total_val_acc = val_acc + new_history.history["val_accuracy"]
        total_val_loss = val_loss + new_history.history["val_loss"]

        # Make plots
        plt.figure(figsize=(8, 8))
        plt.subplot(2, 1, 1)
        plt.plot(total_acc, label='Training Accuracy')
        plt.plot(total_val_acc, label='Validation Accuracy')
        plt.plot([initial_epochs-1, initial_epochs-1], plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(2, 1, 2)
        plt.plot(total_loss, label='Training Loss')
        plt.plot(total_val_loss, label='Validation Loss')
        plt.plot([initial_epochs-1, initial_epochs-1], plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.xlabel('epoch')
        plt.show()
```

```python
def prepare_for_evaluation(model, test_dataset):
        """ Chuẩn bị dữ liệu cho việc đánh giá model

        Args:
            model (Model): Model đã được train
            test_dataset (Dataset): Dataset dùng để test

        Returns:
            (y_true, y_pred, classes): Nhãn thực tế, nhãn dự đoán, tên các lớp
        """
        
        pred_probs = model.predict(test_dataset)
        y_pred = pred_probs.argmax(axis=1)
        y_true = []
        for _, labels in test_dataset.unbatch(): # dữ liệu kiểm tra và lấy ảnh, nhãn
            y_true.append(labels.numpy().argmax()) # nối chỉ mục có giá trị lớn nhất (nhãn ở định dạng one-hot)
        return y_true, y_pred, pred_probs, test_dataset.class_names
```

```python
def plot_f1_score(y_true, y_pred, classes):
        """ In ra classification report của model

        Args:
            y_true (list): Ground truth labels
            y_pred (list): Predicted labels
            classes (list): Tên các class
        """
        classification_report_dict = classification_report(y_true, y_pred, target_names=classes, output_dict=True)
        class_f1_scores = {}
        for key, value in classification_report_dict.items():
            if key in classes:
                class_f1_scores[key] = value['f1-score']
        f1_scores = pd.DataFrame({"class_name": list(class_f1_scores.keys()), 
                          "f1-score": list(class_f1_scores.values())}).sort_values(by='f1-score', ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 25))
        scores = ax.barh(range(len(f1_scores)), f1_scores["f1-score"].values)
        ax.set_yticks(range(len(f1_scores)))
        ax.set_yticklabels(list(f1_scores["class_name"]))
        ax.set_xlabel("f1-score")
        ax.set_title(f"F1-Scores for {len(classes)} Different Classes")
        ax.invert_yaxis(); # đảo ngược thứ tự

        def autolabel(rects): # Phiên bản đã sửa của: https://matplotlib.org/examples/api/barchart_demo.html
            """
            Attach a text label above each bar displaying its height (it's value).
            """
            for rect in rects:
                width = rect.get_width()
                ax.text(1.03*width, rect.get_y() + rect.get_height()/1.5,
                        f"{width:.2f}",
                        ha='center', va='bottom')

        autolabel(scores)
```



```python
def create_predict_dataframe(y_true, y_pred, pred_probs ,classes, filepaths):
        """ Tạo dataframe chứa thông tin ảnh, nhãn thực tế, nhãn dự đoán, xác suất dự đoán, tên lớp

        Args:
            model (Model): Model đã được train
            test_dataset (Dataset): Dataset dùng để test
            test_dir (str): Đường dẫn thư mục chứa ảnh test

        Returns:
            DataFrame: Dataframe chứa thông tin ảnh, nhãn thực tế, nhãn dự đoán, xác suất dự đoán, tên lớp
            
        Example:
            ```python
            filepaths = [filepath.numpy() for filepath in test_dataset.list_files(test_dir + "/*/*.jpg", shuffle=False)]
            pred_df = Evaluation.create_predict_dataframe(y_true, y_pred, pred_probs ,classes, filepaths)
```

        """        
        pred_df = pd.DataFrame({"img_path": filepaths,
                        "pred_conf": pred_probs.max(axis=1), # lấy giá trị xác suất dự đoán lớn nhất
                        "y_true_classname": [classes[i] for i in y_true],
                        "y_pred_classname": [classes[i] for i in y_pred]})
        # 3. Dự đoán có đúng không?
        pred_df["pred_correct"] = pred_df["y_true_classname"] == pred_df["y_pred_classname"]
        
        return pred_df
```

```python
def get_top_wrong_df(y_true, y_pred, pred_probs ,classes, filepaths, n = 100):
        """ Lấy n ảnh dự đoán sai có xác suất dự đoán cao nhất

        Args:
            model (Model): Model đã được train
            test_dataset (Dataset): Dataset dùng để test
            test_dir (str): Đường dẫn thư mục chứa ảnh test
            n (int, optional): Số ảnh dự đoán sai có xác suất dự đoán cao nhất. Defaults to 100.

        Returns:
            DataFrame: Dataframe chứa thông tin ảnh, nhãn thực tế, nhãn dự đoán, xác suất dự đoán, tên lớp
            
        Example:
            ```python
            filepaths = [filepath.numpy() for filepath in test_dataset.list_files(test_dir + "/*/*.jpg", shuffle=False)]
            top_wrongs = Evaluation.get_top_wrong_df(y_true, y_pred, pred_probs , classes, filepaths, n = 100)
```
        """        
        
        pred_df = create_predict_dataframe(y_true, y_pred, pred_probs ,classes, filepaths)
        return pred_df[pred_df["pred_correct"] == False].sort_values("pred_conf", ascending=False)[:n]
```

```python
def load_and_prep_image(filename, img_shape, scale=False):
        """
        Đọc một ảnh từ filename, biến nó thành một tensor và reshape thành
        (224, 224, 3).

        Args:
            filename (str): string filename của ảnh mục tiêu
            img_shape (int): kích thước để resize ảnh mục tiêu, mặc định là 224
            scale (bool): có co giãn các giá trị pixel thành range(0, 1) không, mặc định là True
        Returns:
            image (Tensor): ảnh đã được xử lý thành tensor
        """
        # Đọc trong ảnh
        img = tf.io.read_file(filename)
        # Giải mã nó thành một tensor
        img = tf.io.decode_image(img)
        # Thay đổi kích thước ảnh
        img = tf.image.resize(img, img_shape)
        if scale:
            # Co giãn ảnh (nhận tất cả các giá trị từ 0 đến 1)
            return img/255.
        else:
            return img  
```



```python
def plot_predicted(imagepaths, y_trues, y_preds, pred_probs ,image_size):
        # Create the figure and axes objects
        ncols = 5
        nrows = math.ceil(len(imagepaths)/ncols)
        
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 3+1))
        axes = axes.ravel()
        
        for i in ncols*nrows:
            axes[i].axis('off')

        # Iterate over the test images
        for i, imagepath in enumerate(imagepaths):
            # Read the image
            image = tf.keras.preprocessing.image.load_img(imagepath, target_size=image_size)
            # Convert the image to a numpy array
            image = tf.keras.preprocessing.image.img_to_array(image)
            # Normalize the image
            image = image/255
            # Plot the image on the current axis
            axes[i].imshow(image)
            axes[i].set_title(f"True: {y_trues[i]}, \n Pred: {y_preds[i]}, \n Prob: {pred_probs[i]}", fontsize=15, color='r')

        # Add a tight layout to the figure
        plt.tight_layout()
```

```python
# Example
    # foie gras có f1 score thấp nhất, thử hiển thị ngẫu nhiên môt số ảnh trong class này
    # foie_gras_dir = test_dir + "/foie_gras"
    # random_foie_gras = np.random.choice(os.listdir(foie_gras_dir), size=20, replace=False)
    # random_foie_gras_paths = [foie_gras_dir + "/" + foie_gras for foie_gras in random_foie_gras]
    # random_foie_gras_paths
    # Evaluation.predict_and_plot(model, random_foie_gras_paths, class_names, image_size, true_class='foie_gras', scale = False)
    def predict_and_plot(model, image_paths, class_names, image_shape, true_class=None, scale = False):
        ncols = 5
        nrows = math.ceil(len(image_paths)/ncols)
        
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 3+1))
        axes = axes.ravel()
        
        for i in range(ncols*nrows):
            axes[i].axis('off')
            
        for i, image_name in enumerate(image_paths):
            # Đọc trong ảnh
            img = tf.io.read_file(image_name)
            # Giải mã nó thành một tensor
            img = tf.io.decode_image(img)
            # Thay đổi kích thước ảnh
            img = tf.image.resize(img, image_shape)
            
            if scale:
                # Co giãn ảnh (nhận tất cả các giá trị từ 0 đến 1)
                # Với pretrained model là EfficientNetB0, không cần co giãn ảnh
                img = img/255.
                axes[i].imshow(img)
            else:
                axes[i].imshow(img/255.)
                
            pred_prob = model.predict(tf.expand_dims(img, axis=0))
            pred_class = class_names[np.argmax(pred_prob)]
            
            if true_class is None:
                axes[i].set_title(f"Pred: {pred_class}, \n Prob: {pred_prob.max():.2f}", fontsize=15)
            else:
                if true_class == pred_class:
                    axes[i].set_title(f"True: {true_class}, \n Pred: {pred_class}, \n Prob: {pred_prob.max():.2f}", fontsize=15, color='g')
                else:
                    axes[i].set_title(f"True: {true_class}, \n Pred: {pred_class}, \n Prob: {pred_prob.max():.2f}", fontsize=15, color='r')
            # Add a tight layout to the figure
            plt.tight_layout()
```

