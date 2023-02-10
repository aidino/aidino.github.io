---
layout: libdoc/page
title: Deep Learning - Computer Vision
permalink: /dl-computer-vision
category: Notes
description: "Reusable code snippets for computer vision and deep learning."
order: 1
---
{:toc}

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

Tải dữ liệu về, show file structure để có cái nhìn tổng quan về dữ liệu mới tải

```python
def download_data(url, filename):
        """ Download data from url and extract it to filename
        Args:
            url (str): Link to download data
            filename (str): Name of file to extract data to
        Returns:
            str: Path to extracted data directory
        """
        # Download data
        data_dir = tf.keras.utils.get_file(filename, url, extract=True, cache_dir=".")
        # Remove .zip extension
        data_dir, _ = os.path.splitext(data_dir)
        print("Data downloaded and extracted to: ", data_dir)
        return data_dir
```

```python
def print_tree(data_dir, level = 0, index = 0):
        """ Print out a tree structure of data_dir
        Args:
            data_dir (str): Path to data directory
            level (int, optional): Level of directory. Defaults to 0.
        """    
        
        indent = ' ' * 6 * level
        num_files = len(glob.glob(f'{data_dir}/*'))
        print(f'{indent}{os.path.basename(data_dir)}/ ({num_files} files)')
        subindent = ' ' * 6 * (level + 1)
        subfolders =  glob.glob(f'{data_dir}/*')
        if index == 10:
            print(f'{indent}...')
        max_print = len(subfolders) if len(subfolders) <= 10 else 10
        for idx in range(max_print+1):
            if idx >= len(subfolders):
                return
            subfolder = subfolders[idx]
            if os.path.isdir(subfolder):
                DataManager.print_tree(subfolder, level + 1, idx)
```

```python
def get_all_files(data_dir):
        """ Get all files in data_dir
        Args:
            data_dir (str): Path to data directory
        Returns:
            list: List of all files in data_dir
        """        
        
        filepaths = []
        for dirpath, dirnames, filenames in os.walk(data_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)
        return filepaths
```
## 2. Prepare data

Visualize, visualize and visualize ...

Hiển thị các ảnh ngẫu nhiên, các lớp, sau đó chuẩn bị phân chia vào các dataset tương ứng, chuẩn bị sẵn sàng để đưa vào model

```python
def view_random_images(data_dir, n_samples = 5, seed = 42):
        """ Show num_images random images from target_dir

        Parameters:
            data_dir (str): Path to target directory
            num_images (int, optional): Number of images to show. Defaults to 5.
            seed (int, optional): Seed for random number generator. Defaults to 42.
        
        Returns:
            Numpy Array: Array of random images directory
        """
        
        np.random.seed(seed)
        # Get all the images in data_path
        all_images = [image_path for image_path in Path(data_dir).rglob("*.*")]
        # Get random images
        random_images = np.random.choice(all_images, size=n_samples, replace=False)
        # Plot random images
        ncols = 5
        nrows = math.ceil(n_samples/ncols)
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 3+1))
        axes = axes.ravel()
        # turn off all the axis
        for i in range(nrows * ncols):
            axes[i].axis('off')
        
        for i, image_path in enumerate(random_images):
            image = plt.imread(image_path)
            axes[i].imshow(image)
            axes[i].set_title(image_path.parent.name + "\n" + str(image.shape))
            
        return random_images
```

```python
def view_sample(dataset, class_names, n_sample = 5):
        """ View sample images from dataset (dataset get from tensorflow_datasets)

        Args:
            dataset (Dataset): Dataset from tensorflow_datasets
            class_names (list): List of class names
            n_sample (int, optional): Number of sample images to show. Defaults to 5.
        """        
        
        samples = dataset.take(n_sample)
        ncols = 5
        nrows = math.ceil(n_sample/ncols)
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 3+1))
        axes = axes.ravel()
        # turn off all the axis
        for i in range(nrows * ncols):
            axes[i].axis('off')

        for i, (image, label) in enumerate(samples):
            axes[i].imshow(image)
            axes[i].set_title(f"{class_names[label.numpy()]} \n {image.shape}")
```

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

