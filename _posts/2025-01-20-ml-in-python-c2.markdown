---
layout: post
title: "[Project]Sowing Success: How Machine Learning Helps Farmers Select the Best Crops"
date: 2025-01-20 00:00:00 +0700
categories: machine learning in python
---

Measuring essential soil metrics such as nitrogen, phosphorous, potassium levels, and pH value is an important aspect of assessing soil condition. However, it can be an expensive and time-consuming process, which can cause farmers to prioritize which metrics to measure based on their budget constraints.

Farmers have various options when it comes to deciding which crop to plant each season. Their primary objective is to maximize the yield of their crops, taking into account different factors. One crucial factor that affects crop growth is the condition of the soil in the field, which can be assessed by measuring basic elements such as nitrogen and potassium levels. Each crop has an ideal soil condition that ensures optimal growth and maximum yield.

A farmer reached out to you as a machine learning expert for assistance in selecting the best crop for his field. They've provided you with a dataset called `soil_measures.csv`, which contains:

- `"N"`: Nitrogen content ratio in the soil
- `"P"`: Phosphorous content ratio in the soil
- `"K"`: Potassium content ratio in the soil
- `"pH"` value of the soil
- `"crop"`: categorical values that contain various crops (target variable).

Each row in this dataset represents various measures of the soil in a particular field. Based on these measurements, the crop specified in the `"crop"` column is the optimal choice for that field.  

In this project, you will build multi-class classification models to predict the type of `"crop"` and identify the single most importance feature for predictive performance.

### Vietnamese

Việc đo lường các chỉ số đất quan trọng như hàm lượng nitơ (`nitrogen`), phốt pho (`phosphorous`), kali (`potassium`) và giá trị `pH` là một khía cạnh quan trọng trong việc đánh giá điều kiện đất. Tuy nhiên, đây có thể là một quá trình tốn kém và mất thời gian, khiến người nông dân phải ưu tiên các chỉ số cần đo lường dựa trên hạn chế ngân sách của họ.

Người nông dân có nhiều lựa chọn khi quyết định loại cây trồng nào sẽ trồng trong mỗi vụ. Mục tiêu chính của họ là tối đa hóa năng suất cây trồng, có tính đến các yếu tố khác nhau. Một yếu tố quan trọng ảnh hưởng đến sự phát triển của cây trồng là điều kiện đất đai trên đồng ruộng, có thể được đánh giá bằng cách đo lường các nguyên tố cơ bản như hàm lượng `nitrogen` và `potassium`. Mỗi loại cây trồng có một điều kiện đất lý tưởng để đảm bảo sự phát triển tối ưu và năng suất tối đa.

Một người nông dân đã liên hệ với bạn với tư cách là một chuyên gia về `machine learning` để được hỗ trợ trong việc lựa chọn loại cây trồng tốt nhất cho cánh đồng của mình. Họ đã cung cấp cho bạn một tập dữ liệu có tên là `soil_measures.csv`, chứa:

- `"N"`: Tỷ lệ hàm lượng `nitrogen` trong đất
- `"P"`: Tỷ lệ hàm lượng `phosphorous` trong đất
- `"K"`: Tỷ lệ hàm lượng `potassium` trong đất
- Giá trị `"pH"` của đất
- `"crop"`: các giá trị phân loại chứa các loại cây trồng khác nhau (biến mục tiêu).

Mỗi hàng trong tập dữ liệu này đại diện cho các phép đo khác nhau của đất trong một cánh đồng cụ thể. Dựa trên các phép đo này, loại cây trồng được chỉ định trong cột `"crop"` là lựa chọn tối ưu cho cánh đồng đó.

Trong dự án này, bạn sẽ xây dựng các mô hình phân loại đa lớp (`multi-class classification models`) để dự đoán loại `"crop"` và xác định tính năng quan trọng nhất (`feature`) cho hiệu suất dự đoán.

### Table of contents
1. [EDA (Exploratory data analysis)](#EDAExploratorydataanalysis)
2. [Spliting data](#Splitingdata)
3. [Evaluate feature performance](#Evaluatefeatureperformance)


```python
# All required libraries are imported here for you.
import pandas as pd # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn import metrics # type: ignore

# Load the dataset
crops = pd.read_csv("data/soil_measures.csv")

```

###  1. <a name='EDAExploratorydataanalysis'></a>EDA (Exploratory data analysis)


```python
crops.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>N</th>
      <th>P</th>
      <th>K</th>
      <th>ph</th>
      <th>crop</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>90</td>
      <td>42</td>
      <td>43</td>
      <td>6.502985</td>
      <td>rice</td>
    </tr>
    <tr>
      <th>1</th>
      <td>85</td>
      <td>58</td>
      <td>41</td>
      <td>7.038096</td>
      <td>rice</td>
    </tr>
    <tr>
      <th>2</th>
      <td>60</td>
      <td>55</td>
      <td>44</td>
      <td>7.840207</td>
      <td>rice</td>
    </tr>
    <tr>
      <th>3</th>
      <td>74</td>
      <td>35</td>
      <td>40</td>
      <td>6.980401</td>
      <td>rice</td>
    </tr>
    <tr>
      <th>4</th>
      <td>78</td>
      <td>42</td>
      <td>42</td>
      <td>7.628473</td>
      <td>rice</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Check for missing values
crops.isna().sum().sort_values()
```




    N       0
    P       0
    K       0
    ph      0
    crop    0
    dtype: int64




```python
# Check for crop types
crops['crop'].unique()
```




    array(['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
           'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
           'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
           'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'],
          dtype=object)



###  2. <a name='Splitingdata'></a>Spliting data


```python
# Features and target variables
X = crops.drop("crop", axis=1) 
y = crops["crop"]
# Use train_test_split()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

```




    ((1760, 4), (440, 4), (1760,), (440,))



###  3. <a name='Evaluatefeatureperformance'></a>Evaluate feature performance



```python
# Create a dictionary to store each features predictive performance
features_dict = {}
# Loop through the features
for feature in ["N", "P", "K", "ph"]:
    log_reg = LogisticRegression(multi_class="multinomial")
    log_reg.fit(X_train[[feature]], y_train)
    y_pred = log_reg.predict(X_test[[feature]])
    feature_performance = metrics.f1_score(y_test, y_pred, average="weighted")
    features_dict[feature]=feature_performance
    print(f"F1-score for {feature}: {feature_performance}")
    
```

    F1-score for N: 0.09149868209906838
    F1-score for P: 0.14761942909728204
    F1-score for K: 0.23896974566001802
    F1-score for ph: 0.04532731061152114


    /Users/ngohongthai/miniconda3/lib/python3.10/site-packages/sklearn/linear_model/_logistic.py:458: ConvergenceWarning: lbfgs failed to converge (status=1):
    STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
    
    Increase the number of iterations (max_iter) or scale the data as shown in:
        https://scikit-learn.org/stable/modules/preprocessing.html
    Please also refer to the documentation for alternative solver options:
        https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
      n_iter_i = _check_optimize_result(
    /Users/ngohongthai/miniconda3/lib/python3.10/site-packages/sklearn/linear_model/_logistic.py:458: ConvergenceWarning: lbfgs failed to converge (status=1):
    STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
    
    Increase the number of iterations (max_iter) or scale the data as shown in:
        https://scikit-learn.org/stable/modules/preprocessing.html
    Please also refer to the documentation for alternative solver options:
        https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
      n_iter_i = _check_optimize_result(
    /Users/ngohongthai/miniconda3/lib/python3.10/site-packages/sklearn/linear_model/_logistic.py:458: ConvergenceWarning: lbfgs failed to converge (status=1):
    STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
    
    Increase the number of iterations (max_iter) or scale the data as shown in:
        https://scikit-learn.org/stable/modules/preprocessing.html
    Please also refer to the documentation for alternative solver options:
        https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
      n_iter_i = _check_optimize_result(



```python
features_dict
```




    {'N': 0.09149868209906838,
     'P': 0.14761942909728204,
     'K': 0.23896974566001802,
     'ph': 0.04532731061152114}




```python
highest_key = max(features_dict, key=features_dict.get)
```


```python
best_predictive_feature={}
highest_key = max(features_dict, key=features_dict.get)
best_predictive_feature[highest_key]=features_dict[highest_key]
```


```python
best_predictive_feature
```




    {'K': 0.23896974566001802}




```python

```
