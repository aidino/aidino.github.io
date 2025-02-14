---
layout: post
title: "Winning a Kaggle Competition in Python"
date: 2025-01-20 17:00:00 +0700
categories: machine learning in python
---


## Kaggle competitions process

[Slide]({{site.baseurl}}/files/Winning_a_Kaggle_Competition_in_Python_C1.pdf)

### Competitions overview

#### Explore train data

```python
# Import pandas
import pandas as pd

# Read train data
train = pd.read_csv('train.csv')

# Look at the shape of the data
print('Train shape:', train.shape)

# Look at the head() of the data
print(train.head())
```

```bash
<script.py> output:
    Train shape: (15500, 5)
           id        date  store  item  sales
    0  100000  2017-12-01      1     1     19
    1  100001  2017-12-02      1     1     16
    2  100002  2017-12-03      1     1     31
    3  100003  2017-12-04      1     1      7
    4  100004  2017-12-05      1     1     20
```

#### Explore test data

```python
import pandas as pd

# Read the test data
test = pd.read_csv('test.csv')
# Print train and test columns
print('Train columns:', train.columns.tolist())
print('Test columns:', test.columns.tolist())

# Read the sample submission file
sample_submission = pd.read_csv('sample_submission.csv')

# Look at the head() of the sample submission
print(sample_submission.head())
```

```bash
script.py> output:
    Train columns: ['id', 'date', 'store', 'item', 'sales']
    Test columns: ['id', 'date', 'store', 'item']
       id  sales
    0   0     52
    1   1     52
    2   2     52
    3   3     52
    4   4     52
```

### Public vs Private leaderboard

![]({{site.baseurl}}/images/kaggle1.png)


#### Train XGBoost models

```python
import xgboost as xgb

# Create DMatrix on train data
dtrain = xgb.DMatrix(data=train[['store', 'item']],
                     label=train['sales'])

# Define xgboost parameters
params = {'objective': 'reg:linear',
          'max_depth': 15,
          'verbosity': 0}

# Train xgboost model
xg_depth_15 = xgb.train(params=params, dtrain=dtrain)
```

#### Explore overfitting XGBoost

```python
from sklearn.metrics import mean_squared_error

dtrain = xgb.DMatrix(data=train[['store', 'item']])
dtest = xgb.DMatrix(data=test[['store', 'item']])

# For each of 3 trained models
for model in [xg_depth_2, xg_depth_8, xg_depth_15]:
    # Make predictions
    train_pred = model.predict(dtrain)     
    test_pred = model.predict(dtest)          
    
    # Calculate metrics
    mse_train = mean_squared_error(train['sales'], train_pred)                  
    mse_test = mean_squared_error(test['sales'], test_pred)
    print('MSE Train: {:.3f}. MSE Test: {:.3f}'.format(mse_train, mse_test))
```

```bash
<script.py> output:
    MSE Train: 631.275. MSE Test: 558.522
    MSE Train: 183.771. MSE Test: 337.337
    MSE Train: 134.984. MSE Test: 355.534
```

---
## Dive into the Competition

[Slide]({{site.baseurl}}/files/Winning_a_Kaggle_Competition_in_Python_C2.pdf)

### Understand the problem

#### Define a competition metric

- **Mean Squared Error (MSE) for the regression problem:**

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mi>M</mi>
  <mi>S</mi>
  <mi>E</mi>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mi>N</mi>
  </mfrac>
  <munderover>
    <mo data-mjx-texclass="OP">&#x2211;</mo>
    <mrow>
      <mi>i</mi>
      <mo>=</mo>
      <mn>1</mn>
    </mrow>
    <mrow>
      <mi>N</mi>
    </mrow>
  </munderover>
  <mrow>
    <mo stretchy="false">(</mo>
    <msub>
      <mi>y</mi>
      <mi>i</mi>
    </msub>
    <mo>&#x2212;</mo>
    <msub>
      <mrow>
        <mover>
          <mi>y</mi>
          <mo stretchy="false">^</mo>
        </mover>
      </mrow>
      <mi>i</mi>
    </msub>
    <msup>
      <mo stretchy="false">)</mo>
      <mn>2</mn>
    </msup>
  </mrow>
</math>


```python
import numpy as np

# Import MSE from sklearn
from sklearn.metrics import mean_squared_error

# Define your own MSE function
def own_mse(y_true, y_pred):
  	# Raise differences to the power of 2
    squares = np.power(y_true - y_pred, 2)
    # Find mean over all observations
    err = np.mean(squares)
    return err

print('Sklearn MSE: {:.5f}. '.format(mean_squared_error(y_regression_true, y_regression_pred)))
print('Your MSE: {:.5f}. '.format(own_mse(y_regression_true, y_regression_pred)))
```

```bash
Sklearn MSE: 0.15418. 
Your MSE: 0.15418. 
```

- **Logarithmic Loss (LogLoss) for the binary classification problem:**

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mi>L</mi>
  <mi>o</mi>
  <mi>g</mi>
  <mi>L</mi>
  <mi>o</mi>
  <mi>s</mi>
  <mi>s</mi>
  <mo>=</mo>
  <mo>&#x2212;</mo>
  <mfrac>
    <mn>1</mn>
    <mi>N</mi>
  </mfrac>
  <munderover>
    <mo data-mjx-texclass="OP">&#x2211;</mo>
    <mrow>
      <mi>i</mi>
      <mo>=</mo>
      <mn>1</mn>
    </mrow>
    <mrow>
      <mi>N</mi>
    </mrow>
  </munderover>
  <mrow>
    <mo stretchy="false">(</mo>
    <msub>
      <mi>y</mi>
      <mi>i</mi>
    </msub>
    <mi>ln</mi>
    <mo data-mjx-texclass="NONE">&#x2061;</mo>
    <msub>
      <mi>p</mi>
      <mi>i</mi>
    </msub>
    <mo>+</mo>
    <mo stretchy="false">(</mo>
    <mn>1</mn>
    <mo>&#x2212;</mo>
    <msub>
      <mi>y</mi>
      <mi>i</mi>
    </msub>
    <mo stretchy="false">)</mo>
    <mi>ln</mi>
    <mo data-mjx-texclass="NONE">&#x2061;</mo>
    <mo stretchy="false">(</mo>
    <mn>1</mn>
    <mo>&#x2212;</mo>
    <msub>
      <mi>p</mi>
      <mi>i</mi>
    </msub>
    <mo stretchy="false">)</mo>
    <mo stretchy="false">)</mo>
  </mrow>
</math>

```python
import numpy as np

# Import log_loss from sklearn
from sklearn.metrics import log_loss

# Define your own LogLoss function
# prob_pred: probability predicted
def own_logloss(y_true, prob_pred):
  	# Find loss for each observation
    terms = y_true * np.log(prob_pred) + (1 - y_true) * np.log(1 - prob_pred)
    # Find mean over all observations
    err = np.mean(terms) 
    return -err

print('Sklearn LogLoss: {:.5f}'.format(log_loss(y_classification_true, y_classification_pred)))
print('Your LogLoss: {:.5f}'.format(own_logloss(y_classification_true, y_classification_pred)))
```

```bash
<script.py> output:
    Sklearn LogLoss: 1.10801
    Your LogLoss: 1.10801
```

### Initial EDA

#### EDA statistics

```python
# Shapes of train and test data
print('Train shape:', train.shape)
print('Test shape:', test.shape)

# Train head()
print(train.head())
```

```bash
<script.py> output:
    Train shape: (20000, 8)
    Test shape: (9914, 7)
       id  fare_amount          pickup_datetime  pickup_longitude  pickup_latitude  dropoff_longitude  dropoff_latitude  passenger_count
    0   0          4.5  2009-06-15 17:26:21 UTC           -73.844           40.721            -73.842            40.712                1
    1   1         16.9  2010-01-05 16:52:16 UTC           -74.016           40.711            -73.979            40.782                1
    2   2          5.7  2011-08-18 00:35:00 UTC           -73.983           40.761            -73.991            40.751                2
    3   3          7.7  2012-04-21 04:30:42 UTC           -73.987           40.733            -73.992            40.758                1
    4   4          5.3  2010-03-09 07:51:00 UTC           -73.968           40.768            -73.957            40.784                1
```

```python
# Shapes of train and test data
print('Train shape:', train.shape)
print('Test shape:', test.shape)

# Train head()
print(train.head())

# Describe the target variable
print(train.fare_amount.describe())

# Train distribution of passengers within rides
print(train.passenger_count.value_counts())
```

```bash
count    20000.000
    mean        11.303
    std          9.542
    min         -3.000
    25%          6.000
    50%          8.500
    75%         12.500
    max        180.000
    Name: fare_amount, dtype: float64
    1    13999
    2     2912
    5     1327
    3      860
    4      420
    6      407
    0       75
    Name: passenger_count, dtype: int64
```

#### EDA plots I

```python

```

### Local validation
### Validation usage

---
## Feature Engineering

[Slide]({{site.baseurl}}/files/Winning_a_Kaggle_Competition_in_Python_C3.pdf)

### Feature engineering
### Categorical features
### Target encoding
### Missing data

---
## Modeling

[Slide]({{site.baseurl}}/files/Winning_a_Kaggle_Competition_in_Python_C4.pdf)

### Baseline model
### Hyperparameter tuning
### Model ensembling
### Final tips


---
## NOTE:

Chào bạn, việc lựa chọn thuật toán phù hợp cho các cuộc thi Kaggle là một yếu tố quan trọng để đạt được kết quả tốt. Dưới đây là một số thuật toán thường được sử dụng làm baseline và các thuật toán nên thử để cải thiện kết quả:

### Các thuật toán Baseline thường được sử dụng

* **Linear Regression (Hồi quy tuyến tính)**: Đây là một thuật toán đơn giản và dễ hiểu, thường được sử dụng làm baseline cho các bài toán hồi quy.
* **Logistic Regression (Hồi quy Logistic)**: Tương tự như Linear Regression, nhưng được sử dụng cho các bài toán phân loại nhị phân (binary classification).
* **Decision Tree (Cây quyết định)**: Một thuật toán đơn giản, dễ trực quan hóa, nhưng có thể bị overfitting nếu không được kiểm soát tốt.
* **Random Forest (Rừng ngẫu nhiên)**: Một thuật toán mạnh mẽ, thường được sử dụng làm baseline cho các bài toán phân loại. Random Forest là một tập hợp các cây quyết định, giúp giảm thiểu overfitting và cải thiện độ chính xác.

### Các thuật toán nên thử để cải thiện kết quả

* **Gradient Boosting Machines (GBM)**: Đây là một họ các thuật toán boosting mạnh mẽ, bao gồm XGBoost, LightGBM và CatBoost. GBM thường cho kết quả rất tốt trong các cuộc thi Kaggle.
* **Neural Networks (Mạng nơ-ron)**: Mạng nơ-ron có thể học các biểu diễn phức tạp của dữ liệu và thường được sử dụng cho các bài toán phức tạp như xử lý ảnh và xử lý ngôn ngữ tự nhiên.
* **Support Vector Machines (SVM)**: SVM là một thuật toán mạnh mẽ trong việc tìm ra ranh giới quyết định tối ưu giữa các lớp.
* **k-Nearest Neighbors (k-NN)**: Một thuật toán đơn giản, dựa trên khoảng cách giữa các điểm dữ liệu. k-NN có thể hiệu quả trong một số trường hợp nhất định.

### Các yếu tố khác cần xem xét

* **Đặc điểm của dữ liệu**: Loại dữ liệu (số, văn bản, ảnh, ...) và cấu trúc của dữ liệu sẽ ảnh hưởng đến việc lựa chọn thuật toán.
* **Kích thước dữ liệu**: Với dữ liệu lớn, các thuật toán phức tạp như Neural Networks có thể hiệu quả hơn, nhưng đòi hỏi nhiều tài nguyên tính toán hơn.
* **Thời gian và tài nguyên**: Một số thuật toán đòi hỏi nhiều thời gian huấn luyện và tài nguyên tính toán hơn các thuật toán khác.

### Lời khuyên

* **Bắt đầu với một baseline**: Hãy thử một số thuật toán đơn giản trước để thiết lập một baseline.
* **Thử nghiệm và so sánh**: Thử nghiệm nhiều thuật toán khác nhau và so sánh kết quả của chúng trên tập validation để chọn ra thuật toán tốt nhất.
* **Tối ưu hóa siêu tham số**: Điều chỉnh các siêu tham số của thuật toán để đạt được kết quả tốt nhất.
* **Ensemble learning**: Kết hợp kết quả của nhiều mô hình khác nhau để cải thiện độ chính xác.
