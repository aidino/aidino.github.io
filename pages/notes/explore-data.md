---
layout: libdoc/page
title: 1 - Explore data
permalink: /explore-data
category: Notes
description: "Reusable code for exploring data"
order: 1
---
{:toc}
- *Code:* 
<br>

### Image datasource

#### Download data

```bash
!wget https://storage.googleapis.com/mlep-public/course_1/week2/kagglecatsanddogs_3367a.zip
```

#### Extrax 

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

#### Check file-type in a folder
```python
import os
import glob

folder_path = "path/to/folder"  # replace with your folder path
# get a list of file extensions in the folder
extensions = [os.path.splitext(file)[1] for file in glob.glob(folder_path + "/*")]
# remove duplicates and sort the extensions alphabetically
extensions = sorted(set(extensions))
# print the extensions
for extension in extensions:
    print(extension)

```

#### Clean data folder

```python
import os
import imghdr

def clean_data(folder_path, allowed_extensions):
    """
    Delete files that have a size of 0 or are not of the allowed file types.

    Args:
        folder_path (str): The path to the folder.
        allowed_extensions (list): A list of allowed file extensions.
    """
    # iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # check if the file has a size of 0 or is not of an allowed file type
        if os.path.getsize(file_path) == 0 or not file_name.lower().endswith(tuple(allowed_extensions)) or imghdr.what(file_path) is None:
            os.remove(file_path)  # delete the file

```
**or**

```python
!find ./tmp/data/ -size 0 -exec rm {} +
!find ./tmp/data/ -type f ! -name "*.jpg" -exec rm {} +
```


#### Move 

```python
import shutil
raw_birds_dir = './tmp/data/CUB_200_2011/images'
base_birds_dir = os.path.join(base_dir,'PetImages/Bird')
os.mkdir(base_birds_dir)

for subdir in os.listdir(raw_birds_dir):
  subdir_path = os.path.join(raw_birds_dir, subdir)
  for image in os.listdir(subdir_path):
    shutil.move(os.path.join(subdir_path, image), os.path.join(base_birds_dir))

print(f"There are {len(os.listdir(base_birds_dir))} images of birds")
```

####  Display sample

```python
from IPython.display import Image, display

print("Sample cat image:")
display(Image(filename=f"{os.path.join(base_cats_dir, os.listdir(base_cats_dir)[0])}")
```

####  Train/evaluate split

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

#### View random image in folder

```python
from IPython.display import Image, display
print("Sample cat image:")
display(Image(filename=f"{os.path.join(base_cats_dir, os.listdir(base_cats_dir)[0])}")
```

View random image using `IPython`

```python
import os
import random
from IPython.display import display, Image

def view_sample_images(folder_path, n):
    """
    Display n sample images from a folder using IPython.display.
    
    Arguments:
    folder_path -- the path to the folder containing the images
    n -- the number of sample images to display
    
    Returns:
    None
    """
    # Get a list of all the image file names in the folder
    file_names = os.listdir(folder_path)
    image_file_names = [f for f in file_names if f.endswith('.jpg') or f.endswith('.png')]
    
    # Randomly select n image file names
    sample_image_file_names = random.sample(image_file_names, n)
    
    # Display each image
    for file_name in sample_image_file_names:
        image_path = os.path.join(folder_path, file_name)
        display(Image(filename=image_path))

```

View random image using `matplotlib`

```python
import matplotlib.pyplot as plt
import os
import random

def view_sample_images(folder_path, n):
    """
    Display n sample images from a folder using Matplotlib.
    
    Arguments:
    folder_path -- the path to the folder containing the images
    n -- the number of sample images to display
    
    Returns:
    None
    """
    # Get a list of all the image file names in the folder
    file_names = os.listdir(folder_path)
    image_file_names = [f for f in file_names if f.endswith('.jpg') or f.endswith('.png')]
    
    # Randomly select n image file names
    sample_image_file_names = random.sample(image_file_names, n)
    
    # Calculate the number of rows and columns needed to display the images
    rows = n // 5 + 1
    cols = min(n, 5)
    
    # Create a figure with the appropriate number of subplots
    fig, axs = plt.subplots(rows, cols, figsize=(15, 3 * rows))
    
    # Load and display each image in a subplot
    for i, file_name in enumerate(sample_image_file_names):
        image_path = os.path.join(folder_path, file_name)
        image = plt.imread(image_path)
        row = i // 5
        col = i % 5
        axs[row, col].imshow(image)
        axs[row, col].axis('off')
    
    # Remove any unused subplots
    for i in range(n, rows * cols):
        row = i // 5
        col = i % 5
        axs[row, col].axis('off')
    
    plt.show()
```

```python
view_sample_images('/path/to/folder', 20)
```

#### Visualize the dataset

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

#### Check for data augmentation effects

```python
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img, load_img

# Displays transformations on random images of birds in the training partition
def display_transformations(gen):
  train_birds_dir = "./tmp/data/train/birds"
  random_index = random.randint(0, len(os.listdir(train_birds_dir)))
  sample_image = load_img(f"{os.path.join(train_birds_dir, os.listdir(train_birds_dir)[random_index])}", target_size=(150, 150))
  sample_array = img_to_array(sample_image)
  sample_array = sample_array[None, :]

	# Display 4 images
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

#### Check for class imbalance

```python
import seaborn as sns
sns.countplot(x=train_generator.classes)
```

---

### Dataframe

#### Split CSV file

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

#### Check for missing value

```python
print(df.isnull().sum())
```

#### Check for class imbalance

```python
sns.countplot(x='label', data=df)
```

#### Text processing

```python
stop_words = set(stopwords.words('english'))
df['text'] = df['text'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word.lower() not in stop_words]))
```

#### Visualize the dataset

```python
all_words = ' '.join([text for text in df['text']])
wordcloud = WordCloud(width=800, height=500, random_state=42, max_font_size=100).generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()
```

---

### Other dataset

#### Load dataset
```python
df = pd.read_csv('path/to/dataset.csv')
```

#### Check for missing values
```python
print(df.isnull().sum())
```

#### Check for data 
```python
print(df.describe())
```

#### Check for correlations
```python
corr = df.corr()
sns.heatmap(corr, annot=True, cmap="YlGnBu")
```

#### Visualize the dataset
```python
sns.pairplot(df)
```

#### Check for outliers
```python
sns.boxplot(x='column_name', data=df)
```

#### Check for class imbalance
```python
sns.countplot(x='label', data=df)
```