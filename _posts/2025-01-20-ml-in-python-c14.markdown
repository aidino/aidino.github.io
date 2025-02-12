---
layout: post
title: "Model Validation in Python"
date: 2025-01-20 13:00:00 +0700
categories: machine learning in python
---

Machine learning models are easier to implement now more than ever before. Without proper validation, the results of running new data through a model might not be as accurate as expected. Model validation allows analysts to confidently answer the question, how good is your model? We will answer this question for classification models using the complete set of tic-tac-toe endgame scenarios, and for regression models using fivethirtyeight’s ultimate Halloween candy power ranking dataset. In this course, we will cover the basics of model validation, discuss various validation techniques, and begin to develop tools for creating validated and high performing models.


---
## Basic Modeling in scikit-learn

[Slide]({{site.baseurl}}/files/Model_Validation_in_Python_C1.pdf)

### Regression models

#### Set parameters and fit a model

```python
# Set the number of trees
rfr.n_estimators = 100

# Add a maximum depth
rfr.max_depth = 6

# Set the random state
rfr.random_state = 1111

# Fit the model
rfr.fit(X_train, y_train)
```

#### Feature importances

```python
# Fit the model using X and y
rfr.fit(X_train, y_train)

# Print how important each column is to the model
for i, item in enumerate(rfr.feature_importances_):
      # Use i and item to print out the feature importance of each column
    print("{0:s}: {1:.2f}".format(X_train.columns[i], item))
```

```bash
<script.py> output:
    chocolate: 0.44
    fruity: 0.03
    caramel: 0.02
    peanutyalmondy: 0.05
    nougat: 0.01
    crispedricewafer: 0.03
    hard: 0.01
    bar: 0.02
    pluribus: 0.02
    sugarpercent: 0.17
    pricepercent: 0.19

```

### Classification models

#### Classification predictions

```python
# Fit the rfc model. 
rfc.fit(X_train, y_train)

# Create arrays of predictions
classification_predictions = rfc.predict(X_test)
probability_predictions = rfc.predict_proba(X_test)

# Print out count of binary predictions
print(pd.Series(classification_predictions).value_counts())

# Print the first value from probability_predictions
print('The first predicted probabilities are: {}'.format(probability_predictions[0]))
```

```bash
<script.py> output:
    1    563
    0    204
    dtype: int64
    The first predicted probabilities are: [0.26524423 0.73475577]
```

#### Reusing model parameters

```python
rfc = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=1111)

# Print the classification model
print(rfc)

# Print the classification model's random state parameter
print('The random state is: {}'.format(rfc.random_state))

# Print all parameters
print('Printing the parameters dictionary: {}'.format(rfc.get_params()))
```

```bash
<script.py> output:
    RandomForestClassifier(max_depth=6, n_estimators=50, random_state=1111)
    The random state is: 1111
    Printing the parameters dictionary: {'bootstrap': True, 'ccp_alpha': 0.0, 'class_weight': None, 'criterion': 'gini', 'max_depth': 6, 'max_features': 'auto', 'max_leaf_nodes': None, 'max_samples': None, 'min_impurity_decrease': 0.0, 'min_samples_leaf': 1, 'min_samples_split': 2, 'min_weight_fraction_leaf': 0.0, 'n_estimators': 50, 'n_jobs': None, 'oob_score': False, 'random_state': 1111, 'verbose': 0, 'warm_start': False}
```

#### Random forest classifier

```python
from sklearn.ensemble import RandomForestClassifier

# Create a random forest classifier
rfc = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=1111)

# Fit rfc using X_train and y_train
rfc.fit(X_train, y_train)

# Create predictions on X_test
predictions = rfc.predict(X_test)
print(predictions[0:5])

# Print model accuracy using score() and the testing data
print(rfc.score(X_test, y_test))
```

```bash
<script.py> output:
    [1 1 1 1 1]
    0.817470664928292
```

---
## Validation Basics

[Slide]({{site.baseurl}}/files/Model_Validation_in_Python_C2.pdf)

### Creating train, test, and validation datasets

#### Create one holdout set

```python
# Create dummy variables using pandas
X = pd.get_dummies(tic_tac_toe.iloc[:,0:9])
y = tic_tac_toe.iloc[:, 9]

# Create training and testing datasets. Use 10% for the test set
X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=0.1, random_state=1111)
```

#### Create two holdout sets

```python
# Create temporary training and final testing datasets
X_temp, X_test, y_temp, y_test  =\
    train_test_split(X, y, test_size=0.2, random_state=1111)

# Create the final training and validation datasets
X_train, X_val, y_train, y_val =\
    train_test_split(X_temp, y_temp, test_size=0.25, random_state=1111)
```

### Accuracy metrics: regression models


**1. Định nghĩa**

*   **MAE (Sai số tuyệt đối trung bình)**: Trung bình của giá trị tuyệt đối của sai số giữa giá trị dự đoán và giá trị thực tế.
*   **MSE (Sai số bình phương trung bình)**: Trung bình của bình phương sai số giữa giá trị dự đoán và giá trị thực tế.

**2. Công thức**

*   **MAE:**
    ```
    MAE = (1/n) * Σ |y_i - ŷ_i|
    ```
    Trong đó:
        *   n: số lượng dữ liệu
        *   y\_i: giá trị thực tế thứ i
        *   ŷ\_i: giá trị dự đoán thứ i
*   **MSE:**
    ```
    MSE = (1/n) * Σ (y_i - ŷ_i)^2
    ```
    Trong đó:
        *   n: số lượng dữ liệu
        *   y\_i: giá trị thực tế thứ i
        *   ŷ\_i: giá trị dự đoán thứ i

**3. Ví dụ**

Giả sử chúng ta có 5 dữ liệu dự đoán giá nhà như sau (đơn vị: triệu đồng):

| Giá nhà thực tế | Giá nhà dự đoán | Sai số (MAE) | Sai số (MSE) |
| :-------------- | :-------------- | :----------- | :----------- |
| 100             | 90              | 10           | 100          |
| 120             | 115             | 5            | 25           |
| 150             | 140             | 10           | 100          |
| 110             | 105             | 5            | 25           |
| 130             | 125             | 5            | 25           |

*   **MAE:** (10 + 5 + 10 + 5 + 5) / 5 = 7
*   **MSE:** (100 + 25 + 100 + 25 + 25) / 5 = 55

**4. Ưu nhược điểm**

| Đặc điểm | MAE                                                                                                                                                                                                                                                                                                              | MSE                                                                                                                                                                                                                                                                                                                      |
| :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ưu điểm  | *   Dễ hiểu và tính toán.                                                                                                                                                                                                                                                                                         | *   Khác biệt lớn hơn sẽ bị phạt nặng hơn, giúp mô hình tập trung vào việc giảm thiểu các lỗi lớn.                                                                                                                                                                                                                              |
| Nhược điểm | *   Không nhạy cảm với các giá trị ngoại lệ lớn.                                                                                                                                                                                                                                                                  | *   Dễ bị ảnh hưởng bởi các giá trị ngoại lệ lớn do sai số được bình phương.                                                                                                                                                                                                                                                        |
| Trường hợp sử dụng | *   Sử dụng khi muốn đánh giá sai số một cách tuyến tính và không quá quan trọng về việc phạt các lỗi lớn.                                                                                                                                                                                                               | *   Sử dụng khi muốn mô hình tập trung vào việc giảm thiểu các lỗi lớn, hoặc khi các giá trị ngoại lệ có thể gây ảnh hưởng lớn đến kết quả.                                                                                                                                                                                               |
| Độ nhạy cảm với giá trị ngoại lệ | Không nhạy cảm                                                                                                                                                                                                                                                                                         | Rất nhạy cảm                                                                                                                                                                                                                                                                                                                 |
| Tính chất toán học | Không khả vi tại điểm 0                                                                                                                                                                                                                                                                                       | Khả vi liên tục                                                                                                                                                                                                                                                                                                              |

**5. Kết luận**

*   **MAE** phù hợp khi bạn muốn một độ đo sai số đơn giản, dễ hiểu và ít bị ảnh hưởng bởi các giá trị ngoại lệ.
*   **MSE** phù hợp khi bạn muốn mô hình tập trung vào việc giảm thiểu các lỗi lớn và sẵn sàng "phạt" nặng các dự đoán sai lệch nhiều.

#### Mean absolute error

```python
from sklearn.metrics import mean_absolute_error

# Manually calculate the MAE
n = len(predictions)
mae_one = sum(abs(y_test - predictions)) / n
print('With a manual calculation, the error is {}'.format(mae_one))

# Use scikit-learn to calculate the MAE
mae_two = mean_absolute_error(predictions, y_test)
print('Using scikit-learn, the error is {}'.format(mae_two))
```

```bash
<script.py> output:
    With a manual calculation, the error is 5.9
    Using scikit-learn, the error is 5.9
```

#### Mean squared error

```python
from sklearn.metrics import mean_squared_error

n = len(predictions)
# Finish the manual calculation of the MSE
mse_one = sum((y_test - predictions)**2) / n
print('With a manual calculation, the error is {}'.format(mse_one))

# Use the scikit-learn function to calculate MSE
mse_two = mean_squared_error(predictions, y_test)
print('Using scikit-learn, the error is {}'.format(mse_two))
```

```bash
<script.py> output:
    With a manual calculation, the error is 49.1
    Using scikit-learn, the error is 49.1
```

### Classification metrics
### The bias-variance tradeoff


---
## Cross Validation

[Slide]({{site.baseurl}}/files/Model_Validation_in_Python_C3.pdf)

### The problems with holdout sets
### Cross-validation
### sklearn's cross_val_score()
### Leave-one-out-cross-validation (LOOCV)


---
## Selecting the best model with Hyperparameter tuning.

[Slide]({{site.baseurl}}/files/Model_Validation_in_Python_C4.pdf)

### Introduction to hyperparameter tuning
### RandomizedSearchCV
### Selecting your final model
