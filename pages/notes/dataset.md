---
layout: libdoc/page
title: 2 - Prepare dataset
permalink: /prepare-dataset
category: Notes
description: "Reusable code for preparing dataset"
order: 2
---
{:toc}
- *Code:* 
<br>

## Dataset for computer vision

Nếu data được sắp xếp trong các folder có dạng:

```bash
data/
  train/
    dogs/
      dog001.jpg
      dog002.jpg
      ...
    cats/
      cat001.jpg
      cat002.jpg
      ...
  test/
    dogs/
      dog101.jpg
      dog102.jpg
      ...
    cats/
      cat101.jpg
      cat102.jpg
```

Cách đưa vào dataset:

### With data augmentation

```python
import tensorflow as tf

# Define the path to the root directory
data_dir = "data/train"

# Define the batch size and image size
batch_size = 32
img_size = (224, 224)

# Create a data generator for data augmentation
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,  # Rescale the pixel values to [0, 1]
    rotation_range=20,  # Randomly rotate the images by up to 20 degrees
    zoom_range=0.2,  # Randomly zoom the images by up to 20%
    horizontal_flip=True,  # Randomly flip the images horizontally
    validation_split=0.2,  # Split the data into training and validation sets
)

# Create the training dataset with data augmentation
train_ds = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    shuffle=True,
    subset="training",
)

# Create the validation dataset
val_ds = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    shuffle=False,
    subset="validation",
)

# Define the path to the test directory
test_dir = "data/test"

# Create the test dataset
test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    seed=123,  # Set the random seed for reproducibility
    image_size=img_size,
    batch_size=batch_size,
)

# Print the number of batches in each dataset
print("Number of batches in the training set: %d" % len(train_ds))
print("Number of batches in the validation set: %d" % len(val_ds))
print("Number of batches in the test set: %d" % tf.data.experimental.cardinality(test_ds))

```

### Without data augmentation

```python
import tensorflow as tf

# Define the path to the root directory
data_dir = "data/train"

# Define the batch size and image size
batch_size = 32
img_size = (224, 224)

# Create the training dataset
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,  # Split the data into training and validation sets
    subset="training",
    seed=123,  # Set the random seed for reproducibility
    image_size=img_size,
    batch_size=batch_size,
)

# Create the validation dataset
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,  # Split the data into training and validation sets
    subset="validation",
    seed=123,  # Set the random seed for reproducibility
    image_size=img_size,
    batch_size=batch_size,
)

# Define the path to the test directory
test_dir = "data/test"

# Create the test dataset
test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    seed=123,  # Set the random seed for reproducibility
    image_size=img_size,
    batch_size=batch_size,
)

# Print the number of batches in each dataset
print("Number of batches in the training set: %d" % tf.data.experimental.cardinality(train_ds))
print("Number of batches in the validation set: %d" % tf.data.experimental.cardinality(val_ds))
print("Number of batches in the test set: %d" % tf.data.experimental.cardinality(test_ds))

```

## Dataset for NLP

```python
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Splitting the data into train and test sets
train_df, test_df = train_test_split(df, test_size=0.2)

# Splitting the train set further into train and validation sets
train_df, val_df = train_test_split(train_df, test_size=0.2)

# Creating TensorFlow datasets from dataframes
train_ds = tf.data.Dataset.from_tensor_slices((train_df['text'].values, train_df['label'].values))
train_ds = train_ds.shuffle(buffer_size=len(train_df))
train_ds = train_ds.batch(batch_size=32)

val_ds = tf.data.Dataset.from_tensor_slices((val_df['text'].values, val_df['label'].values))
val_ds = val_ds.batch(batch_size=32)

test_ds = tf.data.Dataset.from_tensor_slices((test_df['text'].values, test_df['label'].values))
test_ds = test_ds.batch(batch_size=32)
```



Một cách tiếp cận khác là chia tập dữ liệu lớn ra các tệp `csv` nhỏ để dễ dàng xử lý

```bash
data/
	train.csv
	validation.csv
	test.csv
```

**Code tách dữ liệu**

```python
import pandas as pd
from sklearn.model_selection import train_test_split

def split_csv_file(csv_path, train_size, val_size, test_size, seed=42):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)
    
    # Split the data into training, validation, and test sets
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=seed)
    train_df, val_df = train_test_split(train_df, test_size=val_size/(train_size+val_size), random_state=seed)
    
    # Write the training, validation, and test sets to separate CSV files
    train_df.to_csv("train.csv", index=False)
    val_df.to_csv("validation.csv", index=False)
    test_df.to_csv("test.csv", index=False)
    
    print("Split complete!")

split_csv_file("big_data.csv", train_size=0.6, val_size=0.2, test_size=0.2)
```

**Code đọc dữ liệu từ các file, đưa chúng vào dataset**

```python
import tensorflow as tf
import pandas as pd

# Define batch size and number of epochs
BATCH_SIZE = 32
NUM_EPOCHS = 10

# Load the CSV files into pandas DataFrames
train_df = pd.read_csv("train.csv")
val_df = pd.read_csv("validation.csv")
test_df = pd.read_csv("test.csv")

# Define function to preprocess text and labels
def preprocess_text(text):
    # TODO: Implement text preprocessing
    return text

def preprocess_label(label):
    # TODO: Implement label preprocessing
    return label

# Define TensorFlow datasets for training, validation, and test sets
train_dataset = tf.data.Dataset.from_tensor_slices((preprocess_text(train_df["text"]), preprocess_label(train_df["label"])))
val_dataset = tf.data.Dataset.from_tensor_slices((preprocess_text(val_df["text"]), preprocess_label(val_df["label"])))
test_dataset = tf.data.Dataset.from_tensor_slices((preprocess_text(test_df["text"]), preprocess_label(test_df["label"])))

# Apply shuffling and batching to the datasets
train_dataset = train_dataset.shuffle(len(train_df)).batch(BATCH_SIZE).repeat(NUM_EPOCHS)
val_dataset = val_dataset.batch(BATCH_SIZE)
test_dataset = test_dataset.batch(BATCH_SIZE)

# Prepare the datasets for training
train_dataset = train_dataset.prefetch(tf.data.experimental.AUTOTUNE)
val_dataset = val_dataset.prefetch(tf.data.experimental.AUTOTUNE)
test_dataset = test_dataset.prefetch(tf.data.experimental.AUTOTUNE)


model.fit(train_dataset, validation_data=val_dataset, epochs=NUM_EPOCHS)

```

