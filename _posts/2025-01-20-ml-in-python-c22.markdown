---
layout: post
title: "Image Processing in Python"
date: 2025-01-20 17:00:00 +0700
categories: machine learning in python
---

Images are everywhere! We live in a time where images contain lots of information, which is sometimes difficult to obtain. This is why image pre-processing has become a highly valuable skill, applicable in many use cases. In this course, you will learn to process, transform, and manipulate images at your will, even when they come in thousands. You will also learn to restore damaged images, perform noise reduction, smart-resize images, count the number of dots on a dice, apply facial detection, and much more, using scikit-image. After completing this course, you will be able to apply your knowledge to different domains such as machine learning and artificial intelligence, machine and robotic vision, space and medical image analysis, retailing, and many more. Take the step and dive into the wonderful world that is computer vision!


## Introducing Image Processing and scikit-image

[Slide]({{site.baseurl}}/files/Image_Processing_in_Python_C1.pdf)

**Helper function**

```python
from matplotlib import pyplot as plt

def show_image(image, title='Image', cmap_type='gray'):
    plt.imshow(image, cmap=cmap_type)
    plt.title(title)
    plt.axis('off')
    plt.show()
```

### Make images come alive with scikit-image

#### RGB to grayscale

```python
# Import the modules from skimage
from skimage import data, color

# Load the rocket image
rocket = data.rocket()

# Convert the image to grayscale
gray_scaled_rocket = color.rgb2gray(rocket)

# Show the original image
show_image(rocket, 'Original RGB image')

# Show the grayscale image
show_image(gray_scaled_rocket, 'Grayscale image')
```

![]({{site.baseurl}}/images/img_processing1.svg)

![]({{site.baseurl}}/images/img_processing2.svg)

### NumPy for images

#### Flipping out

```python

```

### Getting started with thresholding


## Filters, Contrast, Transformation and Morphology

[Slide]({{site.baseurl}}/files/Image_Processing_in_Python_C2.pdf)

### Jump into filtering
### Contrast enhancement
### Transformations
### Morphology


## Image restoration, Noise, Segmentation and Contours

[Slide]({{site.baseurl}}/files/Image_Processing_in_Python_C3.pdf)

### Image restoration
### Noise
### Superpixels & segmentation
### Finding contours


## Advanced Operations, Detecting Faces and Features

[Slide]({{site.baseurl}}/files/Image_Processing_in_Python_C4.pdf)

### Finding the edges with Canny
### Right around the corner
### Face detection
### Real-world applications
