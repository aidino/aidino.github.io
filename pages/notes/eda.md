---
layout: libdoc/page
title: EDA - Exploratory Data Analysis.
permalink: /eda
category: Notes
description: "Reusable code snippets for computer vision and deep learning."
order: 1
---
{:toc}
- *Code:* 
<br>



# Khái niệm

**EDA (Exploratory Data Analysis)** là một giai đoạn quan trọng trong quá trình xử lý dữ liệu và phân tích trong machine learning. Nó bao gồm việc khám phá, phân tích và trực quan hóa dữ liệu để hiểu rõ hơn về dữ liệu và chuẩn bị cho việc xây dựng mô hình dự đoán.

Các bước thực hiện EDA trong machine learning thường bao gồm:

1. Tải dữ liệu và xem tổng quan về dữ liệu: Đây là bước đầu tiên để hiểu về dữ liệu, bao gồm kiểm tra kích thước tập dữ liệu, số lượng các thuộc tính, kiểu dữ liệu, giá trị bị thiếu,...
2. Khám phá dữ liệu: Bao gồm các thống kê cơ bản như min, max, mean, median, mode, variance, std,.. Đồng thời xem xét phân bố của các thuộc tính bằng histogram, boxplot, scatter plot,.. Nếu có quá nhiều thuộc tính thì cần ưu tiên phân tích các thuộc tính có mối liên quan đến bài toán cần giải quyết.
3. Xử lý dữ liệu: Bao gồm các bước xử lý thiếu dữ liệu, xử lý dữ liệu bị nhiễu, chuẩn hóa dữ liệu, rút trích đặc trưng,...
4. Tìm kiếm mối liên hệ giữa các thuộc tính: Các thuộc tính có thể có mối liên hệ với nhau và ảnh hưởng đến kết quả của mô hình. Do đó, cần phân tích mối tương quan giữa các thuộc tính để chọn ra những thuộc tính có ảnh hưởng nhất đến kết quả.
5. Trực quan hóa dữ liệu: Sử dụng biểu đồ và đồ thị để trực quan hóa dữ liệu và giúp người phân tích hiểu rõ hơn về dữ liệu.

Các kết quả từ quá trình EDA sẽ giúp xác định được các vấn đề cần giải quyết và tối ưu hóa mô hình dự đoán. Nó cũng giúp tăng độ chính xác của mô hình và đưa ra dự đoán chính xác hơn trên tập dữ liệu mới.

# Example

## EDA in Computer vision

### Load Dataset

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load the dataset
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_generator = train_datagen.flow_from_directory(
        'path/to/train/directory',
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        subset='training')
valid_generator = train_datagen.flow_from_directory(
        'path/to/train/directory',
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        subset='validation')
```

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# No data augmentation for now, only normalizing pixel values
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Point to the imbalanced directory
train_generator = train_datagen.flow_from_directory(
        'path/to/train/directory/train',
        target_size=(224, 224),
        batch_size=32,
        class_mode='sparse')

validation_generator = test_datagen.flow_from_directory(
        'path/to/train/directory/eval',
        target_size=(224, 224),
        batch_size=32,
        class_mode='sparse')
```

### Visualize the dataset

```python
images, labels = next(train_generator)
fig, axs = plt.subplots(4, 8, figsize=(12, 6))
fig.subplots_adjust(hspace = .1, wspace=.1)
axs = axs.ravel()
for i in np.arange(0, 32):
    axs[i].imshow(images[i])
    axs[i].axis('off')
plt.show()
```

### Check for class imbalance

```python
import seaborn as sns
sns.countplot(x=train_generator.classes)
```

### Check for data augmentation effects

```python
# Check for data augmentation effects
train_datagen_aug = ImageDataGenerator(
  rescale=1./255, 
  rotation_range=30, 
  zoom_range=0.2, 
  horizontal_flip=True)

train_generator_aug = train_datagen_aug.flow_from_directory(
        'path/to/train/directory',
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        subset='training')

images_aug, labels_aug = next(train_generator_aug)
fig, axs = plt.subplots(4, 8, figsize=(12, 6))
fig.subplots_adjust(hspace = .1, wspace=.1)
axs = axs.ravel()
for i in np.arange(0, 32):
    axs[i].imshow(images_aug[i])
    axs[i].axis('off')
plt.show()
```

**Data augmentation example**

```python
# Now applying image augmentation
train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=50,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)


test_datagen = ImageDataGenerator(rescale=1./255)

# Still pointing to directory with full dataset
train_generator = train_datagen.flow_from_directory(
        'path/to/train/directory/train',
        target_size=(224, 224),
        batch_size=32,
        class_mode='sparse')

validation_generator = test_datagen.flow_from_directory(
        'path/to/train/directory/eval',
        target_size=(224, 224),
        batch_size=32,
        class_mode='sparse')
```

**Display**

```python
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img, load_img

# Displays transformations on random images of birds in the training partition
def display_transformations(gen):
  train_birds_dir = "./tmp/data/train/birds"
  random_index = random.randint(0, len(os.listdir(train_birds_dir)))
  sample_image = load_img(f"{os.path.join(train_birds_dir, os.listdir(train_birds_dir)[random_index])}", target_size=(150, 150))
  sample_array = img_to_array(sample_image)
  sample_array = sample_array[None, :]

  for iteration, array in zip(range(4), gen.flow(sample_array, batch_size=1)):
    array = np.squeeze(array)
    img = array_to_img(array)
    print(f"\nTransformation number: {iteration}\n")
    display(img)

# An example of an ImageDataGenerator
sample_gen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=50,
        width_shift_range=0.25,
        height_shift_range=0.25,
        shear_range=0.2,
        zoom_range=0.25,
        horizontal_flip=True)

display_transformations(sample_gen)
```



## EDA for NLP

### Libraries

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
```

### Load dataset

```python
df = pd.read_csv('path/to/dataset.csv')
```

### Check for missing value

```python
print(df.isnull().sum())
```

### Check for class imbalance

```python
sns.countplot(x='label', data=df)
```

### Text processing

```python
stop_words = set(stopwords.words('english'))
df['text'] = df['text'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word.lower() not in stop_words]))
```

### Visualize the dataset

```python
all_words = ' '.join([text for text in df['text']])
wordcloud = WordCloud(width=800, height=500, random_state=42, max_font_size=100).generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()
```

## EDA for other datasets

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('path/to/dataset.csv')

# Check for missing values
print(df.isnull().sum())

# Check for data distribution
print(df.describe())

# Check for correlations
corr = df.corr()
sns.heatmap(corr, annot=True, cmap="YlGnBu")

# Visualize the dataset
sns.pairplot(df)

# Check for outliers
sns.boxplot(x='column_name', data=df)

# Check for class imbalance
sns.countplot(x='label', data=df)

```

