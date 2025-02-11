---
layout: post
title: "Machine Learning for Time Series Data in Python"
date: 2025-01-20 11:00:00 +0700
categories: machine learning in python
---

Time series data is ubiquitous. Whether it be stock market fluctuations, sensor data recording climate change, or activity in the brain, any signal that changes over time can be described as a time series. Machine learning has emerged as a powerful method for leveraging complexity in data in order to generate predictions and insights into the problem one is trying to solve. This course is an intersection between these two worlds of machine learning and time series data, and covers feature engineering, spectograms, and other advanced techniques in order to classify heartbeat sounds and predict stock prices.


##  Time Series and Machine Learning Primer

[Slide]({{site.baseurl}}/files/Machine_Learning_for_Time_Series_Data_in_Python_C1.pdf)

### Timeseries kinds and applications

#### Plotting a time series (I)

```python
# Plot the time series in each dataset
fig, axs = plt.subplots(2, 1, figsize=(5, 10))
data.iloc[:1000].plot(y='data_values', ax=axs[0])
data2.iloc[:1000].plot(y='data_values', ax=axs[1])
plt.show()
```

![]({{site.baseurl}}/images/time-serie1.svg)

#### Plotting a time series (II)

```python
# Plot the time series in each dataset
fig, axs = plt.subplots(2, 1, figsize=(5, 10))
data.iloc[:1000].plot(x='time', y='data_values', ax=axs[0])
data2.iloc[:1000].plot(x='time', y='data_values', ax=axs[1])
plt.show()
```

![]({{site.baseurl}}/images/time-serie2.svg)

### Machine learning basics

#### Fitting a simple model: classification

```python
from sklearn.svm import LinearSVC

# Construct data for the model
X = data[['petal length (cm)','petal width (cm)']]
y = data[['target']]

# Fit the model
model = LinearSVC()
model.fit(X, y)
```

#### Predicting using a classification model

```python
# Create input array
X_predict = targets[['petal length (cm)', 'petal width (cm)']]

# Predict with the model
predictions = model.predict(X_predict)
print(predictions)

# Visualize predictions and actual values
plt.scatter(X_predict['petal length (cm)'], X_predict['petal width (cm)'],
            c=predictions, cmap=plt.cm.coolwarm)
plt.title("Predicted class values")
plt.show()
```

#### Inspecting the regression data

```python

```

![]({{site.baseurl}}/images/time-serie3.svg)

### Machine learning and time series data

#### Inspecting the classification data

```python
import librosa as lr
from glob import glob

# List all the wav files in the folder
audio_files = glob(data_dir + '/*.wav')

# Read in the first audio file, create the time array
audio, sfreq = lr.load(audio_files[0])
time = np.arange(0, len(audio)) / sfreq

# Plot audio over time
fig, ax = plt.subplots()
ax.plot(time, audio)
ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
plt.show()
```

![]({{site.baseurl}}/images/time-serie4.svg)

#### Inspecting the regression data

```python
# Read in the data
data = pd.read_csv('prices.csv', index_col=0)

# Convert the index of the DataFrame to datetime
data.index = pd.to_datetime(data.index)
print(data.head())

# Loop through each column, plot its values over time
fig, ax = plt.subplots()
for column in data.columns:
    data[column].plot(ax=ax, label=column)
ax.legend()
plt.show()
```

![]({{site.baseurl}}/images/time-serie5.svg)

---
## Time Series as Inputs to a Model

[Slide]({{site.baseurl}}/files/Machine_Learning_for_Time_Series_Data_in_Python_C2.pdf)

### Classifying a time series

#### Many repetitions of sounds

```python
fig, axs = plt.subplots(3, 2, figsize=(15, 7), sharex=True, sharey=True)

# Calculate the time array
time = np.arange(normal.shape[0]) / sfreq

# Stack the normal/abnormal audio so you can loop and plot
stacked_audio = np.hstack([normal, abnormal]).T

# Loop through each audio file / ax object and plot
# .T.ravel() transposes the array, then unravels it into a 1-D vector for looping
for iaudio, ax in zip(stacked_audio, axs.T.ravel()):
    ax.plot(time, iaudio)
show_plot_and_make_titles()
```

![]({{site.baseurl}}/images/time-serie6.svg)

#### Invariance in time

```python
# Average across the audio files of each DataFrame
mean_normal = np.mean(normal, axis=1)
mean_abnormal = np.mean(abnormal, axis=1)

# Plot each average over time
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3), sharey=True)
ax1.plot(time, mean_normal)
ax1.set(title="Normal Data")
ax2.plot(time, mean_abnormal)
ax2.set(title="Abnormal Data")
plt.show()
```

![]({{site.baseurl}}/images/time-serie7.svg)

#### Build a classification model

```python
from sklearn.svm import LinearSVC

# Initialize and fit the model
model = LinearSVC()
model.fit(X_train, y_train)

# Generate predictions and score them manually
predictions = model.predict(X_test)
print(sum(predictions == y_test.squeeze()) / len(y_test))
```

### Improving features for classification
### The spectrogram


---
## Predicting Time Series Data

[Slide]({{site.baseurl}}/files/Machine_Learning_for_Time_Series_Data_in_Python_C3.pdf)

### Predicting data over time
### Advanced time series prediction
### Creating features over time


---
## Validating and Inspecting Time Series Models

[Slide]({{site.baseurl}}/files/Machine_Learning_for_Time_Series_Data_in_Python_C4.pdf)

### Creating features from the past
### Cross-validating time series data
### Stationarity and stability
