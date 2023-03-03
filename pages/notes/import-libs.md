---
layout: libdoc/page
title: 0 - Import libraries
permalink: /import-libs
category: Notes
description: "Useful libraries"
order: 0
---
{:toc}
- *Code:* 
<br>



## 0. Import useful libraries

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



**Print env info**

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

