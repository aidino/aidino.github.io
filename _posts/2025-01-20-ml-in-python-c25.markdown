---
layout: post
title: "Winning a Kaggle Competition in Python"
date: 2025-01-20 17:00:00 +0700
categories: machine learning in python
---

Learn how to approach and win competitions on Kaggle.


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
# Calculate the ride distance
train['distance_km'] = haversine_distance(train)

# Draw a scatterplot
plt.scatter(x=train['fare_amount'], y=train['distance_km'], alpha=0.5)
plt.xlabel('Fare amount')
plt.ylabel('Distance, km')
plt.title('Fare amount based on the distance')

# Limit on the distance
plt.ylim(0, 50)
plt.show()
```

![]({{site.baseurl}}/images/eda1.svg)

#### EDA plots II

```python
# Create hour feature
train['pickup_datetime'] = pd.to_datetime(train.pickup_datetime)
train['hour'] = train.pickup_datetime.dt.hour

# Find median fare_amount for each hour
hour_price = train.groupby('hour', as_index=False)['fare_amount'].median()

# Plot the line plot
plt.plot(hour_price['hour'], hour_price['fare_amount'], marker='o')
plt.xlabel('Hour of the day')
plt.ylabel('Median fare amount')
plt.title('Fare amount based on day time')
plt.xticks(range(24))
plt.show()
```

![]({{site.baseurl}}/images/eda2.svg)

### Local validation

#### K-fold cross-validation

```python
# Import KFold
from sklearn.model_selection import KFold

# Create a KFold object
kf = KFold(n_splits=3, shuffle=True, random_state=123)

# Loop through each split
fold = 0
for train_index, test_index in kf.split(train):
    # Obtain training and testing folds
    cv_train, cv_test = train.iloc[train_index], train.iloc[test_index]
    print('Fold: {}'.format(fold))
    print('CV train shape: {}'.format(cv_train.shape))
    print('Medium interest listings in CV train: {}\n'.format(sum(cv_train.interest_level == 'medium')))
    fold += 1
```

```bash
<script.py> output:
    Fold: 0
    CV train shape: (666, 9)
    Medium interest listings in CV train: 175
    
    Fold: 1
    CV train shape: (667, 9)
    Medium interest listings in CV train: 165
    
    Fold: 2
    CV train shape: (667, 9)
    Medium interest listings in CV train: 162
```

#### Stratified K-fold

```python
# Import StratifiedKFold
from sklearn.model_selection import StratifiedKFold

# Create a StratifiedKFold object
str_kf = StratifiedKFold(n_splits=3, shuffle=True, random_state=123)

# Loop through each split
fold = 0
for train_index, test_index in str_kf.split(train, train['interest_level']):
    # Obtain training and testing folds
    cv_train, cv_test = train.iloc[train_index], train.iloc[test_index]
    print('Fold: {}'.format(fold))
    print('CV train shape: {}'.format(cv_train.shape))
    print('Medium interest listings in CV train: {}\n'.format(sum(cv_train.interest_level == 'medium')))
    fold += 1
```

```bash
<script.py> output:
    Fold: 0
    CV train shape: (666, 9)
    Medium interest listings in CV train: 167
    
    Fold: 1
    CV train shape: (667, 9)
    Medium interest listings in CV train: 167
    
    Fold: 2
    CV train shape: (667, 9)
    Medium interest listings in CV train: 168
```

### Validation usage

#### Time K-fold

```python
from sklearn.model_selection import TimeSeriesSplit

# Create TimeSeriesSplit object
time_kfold = TimeSeriesSplit(n_splits=3)

# Sort train data by date
train = train.sort_values("date")

# Iterate through each split
fold = 0
for train_index, test_index in time_kfold.split(train):
    cv_train, cv_test = train.iloc[train_index], train.iloc[test_index]
    
    print('Fold :', fold)
    print('Train date range: from {} to {}'.format(cv_train.date.min(), cv_train.date.max()))
    print('Test date range: from {} to {}\n'.format(cv_test.date.min(), cv_test.date.max()))
    fold += 1
```

```bash
<script.py> output:
    Fold : 0
    Train date range: from 2017-12-01 to 2017-12-08
    Test date range: from 2017-12-08 to 2017-12-16
    
    Fold : 1
    Train date range: from 2017-12-01 to 2017-12-16
    Test date range: from 2017-12-16 to 2017-12-24
    
    Fold : 2
    Train date range: from 2017-12-01 to 2017-12-24
    Test date range: from 2017-12-24 to 2017-12-31
```

#### Overall validation score

```python
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

# Sort train data by date
train = train.sort_values('date')

# Initialize 3-fold time cross-validation
kf = TimeSeriesSplit(n_splits=3)

# Get MSE scores for each cross-validation split
mse_scores = get_fold_mse(train, kf)

print('Mean validation MSE: {:.5f}'.format(np.mean(mse_scores)))
print('MSE by fold: {}'.format(mse_scores))
print('Overall validation MSE: {:.5f}'.format(np.mean(mse_scores) + np.std(mse_scores)))
```

```bash
<script.py> output:
    Mean validation MSE: 955.49186
    MSE by fold: [890.30336, 961.65797, 1014.51424]
    Overall validation MSE: 1006.38784
```

---
## Feature Engineering

[Slide]({{site.baseurl}}/files/Winning_a_Kaggle_Competition_in_Python_C3.pdf)

### Feature engineering

#### Arithmetical features

```python
# Look at the initial RMSE
print('RMSE before feature engineering:', get_kfold_rmse(train))

# Find the total area of the house
train['TotalArea'] = train['TotalBsmtSF'] + train['FirstFlrSF'] + train['SecondFlrSF']
print('RMSE with total area:', get_kfold_rmse(train))

# Find the area of the garden
train['GardenArea'] = train['LotArea'] - train['FirstFlrSF']
print('RMSE with garden area:', get_kfold_rmse(train))

# Find total number of bathrooms
train['TotalBath'] = train['FullBath'] + train['HalfBath']
print('RMSE with number of bathrooms:', get_kfold_rmse(train))
```

```bash
<script.py> output:
    RMSE before feature engineering: 36029.39
    RMSE with total area: 35073.2
    RMSE with garden area: 34413.55
    RMSE with number of bathrooms: 34506.78
```

#### Date features

```python
# Concatenate train and test together
taxi = pd.concat([train, test])

# Convert pickup date to datetime object
taxi['pickup_datetime'] = pd.to_datetime(taxi['pickup_datetime'])

# Create a day of week feature
taxi['dayofweek'] = taxi['pickup_datetime'].dt.dayofweek

# Create an hour feature
taxi['hour'] = taxi['pickup_datetime'].dt.hour

# Split back into train and test
new_train = taxi[taxi['id'].isin(train['id'])]
new_test = taxi[taxi['id'].isin(test['id'])]
```

### Categorical features

#### Label encoding

```python
# Concatenate train and test together
houses = pd.concat([train, test])

# Label encoder
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

# Create new features
houses['RoofStyle_enc'] = le.fit_transform(houses['RoofStyle'])
houses['CentralAir_enc'] = le.fit_transform(houses['CentralAir'])

# Look at new features
print(houses[['RoofStyle', 'RoofStyle_enc', 'CentralAir', 'CentralAir_enc']].head())
```

```bash
<script.py> output:
      RoofStyle  RoofStyle_enc CentralAir  CentralAir_enc
    0     Gable              1          Y               1
    1     Gable              1          Y               1
    2     Gable              1          Y               1
    3     Gable              1          Y               1
    4     Gable              1          Y               1
```

#### One-Hot encoding

The problem with label encoding is that it implicitly assumes that there is a ranking dependency between the categories. 

```python
# Concatenate train and test together
houses = pd.concat([train, test])

# Label encode binary 'CentralAir' feature
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
houses['CentralAir_enc'] = le.fit_transform(houses['CentralAir'])

# Create One-Hot encoded features
ohe = pd.get_dummies(houses['RoofStyle'], prefix='RoofStyle')

# Concatenate OHE features to houses
houses = pd.concat([houses, ohe], axis=1)

# Look at OHE features
print(houses[[col for col in houses.columns if 'RoofStyle' in col]].head(3))
```

```bash
<script.py> output:
      RoofStyle  RoofStyle_Flat  RoofStyle_Gable  RoofStyle_Gambrel  RoofStyle_Hip  RoofStyle_Mansard  RoofStyle_Shed
    0     Gable               0                1                  0              0                  0               0
    1     Gable               0                1                  0              0                  0               0
    2     Gable               0                1                  0              0                  0               0
```

### Target encoding - Đối tượng địa lý

Áp dụng cho những features có >= 10 categories

#### Mean target encoding

First of all, you will create a function that implements mean target encoding. Remember that you need to develop the two following steps:

- Calculate the mean on the train, apply to the test
- Split train into K folds. Calculate the out-of-fold mean for each fold, apply to this particular fold

Each of these steps will be implemented in a separate function: `test_mean_target_encoding()` and `train_mean_target_encoding()`, respectively.

The final function `mean_target_encoding()` takes as arguments: the train and test DataFrames, the name of the categorical column to be encoded, the name of the target column and a smoothing parameter alpha (alpha is usually from 5 -> 10). It returns two values: a new feature for train and test DataFrames, respectively.

```python
def test_mean_target_encoding(train, test, target, categorical, alpha=5):
    # Calculate global mean on the train data
    global_mean = train[target].mean()
    
    # Group by the categorical feature and calculate its properties
    train_groups = train.groupby(categorical)
    category_sum = train_groups[target].sum()
    category_size = train_groups.size()
    
    # Calculate smoothed mean target statistics
    train_statistics = (category_sum + global_mean * alpha) / (category_size + alpha)
    
    # Apply statistics to the test data and fill new categories
    test_feature = test[categorical].map(train_statistics).fillna(global_mean)
    return test_feature.values
```

```python
def train_mean_target_encoding(train, target, categorical, alpha=5):
    # Create 5-fold cross-validation
    kf = KFold(n_splits=5, random_state=123, shuffle=True)
    train_feature = pd.Series(index=train.index)
    
    # For each folds split
    for train_index, test_index in kf.split(train):
        cv_train, cv_test = train.iloc[train_index], train.iloc[test_index]
      
        # Calculate out-of-fold statistics and apply to cv_test
        cv_test_feature = test_mean_target_encoding(cv_train, cv_test, target, categorical, alpha)
        
        # Save new feature for this particular fold
        train_feature.iloc[test_index] = cv_test_feature       
    return train_feature.values
```

```python
def mean_target_encoding(train, test, target, categorical, alpha=5):
  
    # Get the train feature
    train_feature = train_mean_target_encoding(train, target, categorical, alpha)
  
    # Get the test feature
    test_feature = test_mean_target_encoding(train, test, target, categorical, alpha)
    
    # Return new features to add to the model
    return train_feature, test_feature
```

#### K-fold cross-validation

You will work with a binary classification problem on a subsample from Kaggle playground competition. The objective of this competition is to predict whether a famous basketball player Kobe Bryant scored a basket or missed a particular shot.

Train data is available in your workspace as bryant_shots DataFrame. It contains data on 10,000 shots with its properties and a target variable `shot\_made\_flag` -- whether shot was scored or not.

One of the features in the data is `game_id` -- a particular game where the shot was made. There are 541 distinct games. So, you deal with a high-cardinality categorical feature. Let's encode it using a target mean!

Suppose you're using 5-fold cross-validation and want to evaluate a mean target encoded feature on the local validation.

```python
# Create 5-fold cross-validation
kf = KFold(n_splits=5, random_state=123, shuffle=True)

# For each folds split
for train_index, test_index in kf.split(bryant_shots):
    cv_train, cv_test = bryant_shots.iloc[train_index], bryant_shots.iloc[test_index]

    # Create mean target encoded feature
    cv_train['game_id_enc'], cv_test['game_id_enc'] = mean_target_encoding(train=cv_train,
                                                                           test=cv_test,
                                                                           target='shot_made_flag',
                                                                           categorical='game_id',
                                                                           alpha=5)
    # Look at the encoding
    print(cv_train[['game_id', 'shot_made_flag', 'game_id_enc']].sample(n=1))
```

```bash
<script.py> output:
           game_id  shot_made_flag  game_id_enc
    7106  20500532             0.0        0.362
           game_id  shot_made_flag  game_id_enc
    5084  20301100             0.0        0.568
           game_id  shot_made_flag  game_id_enc
    6687  20500228             0.0        0.481
           game_id  shot_made_flag  game_id_enc
    5046  20301075             0.0        0.252
           game_id  shot_made_flag  game_id_enc
    4662  20300515             1.0        0.453
```

#### Beyond binary classification

Of course, binary classification is just a single special case. Target encoding could be applied to any target variable type:

- For **binary classification** usually mean target encoding is used
- For **regression** mean could be changed to median, quartiles, etc.
- For **multi-class classification** with N classes we create N features with target mean for each category in one vs. all fashion
The `mean_target_encoding()` function you've created could be used for any target type specified above. Let's apply it for the regression problem on the example of House Prices Kaggle competition.

Your goal is to encode a categorical feature "RoofStyle" using mean target encoding. The train and test DataFrames are already available in your workspace.

```python
# Create mean target encoded feature
train['RoofStyle_enc'], test['RoofStyle_enc'] = mean_target_encoding(train=train,
                                                                     test=test,
                                                                     target='SalePrice',
                                                                     categorical='RoofStyle',
                                                                     alpha=10)

# Look at the encoding
print(test[['RoofStyle', 'RoofStyle_enc']].drop_duplicates())
```

```bash
<script.py> output:
         RoofStyle  RoofStyle_enc
    0        Gable     171565.948
    1          Hip     217594.645
    98     Gambrel     164152.950
    133       Flat     188703.563
    362    Mansard     180775.939
    1053      Shed     188267.663
```

### Missing data

####  Find missing data

```python
# Read DataFrame
twosigma = pd.read_csv('twosigma_train.csv')

# Find the number of missing values in each column
print(twosigma.isnull().sum())
```

```bash
<script.py> output:
    id                 0
    bathrooms          0
    bedrooms           0
    building_id       13
    latitude           0
    longitude          0
    manager_id         0
    price             32
    interest_level     0
    dtype: int64
```

```python
# Look at the columns with the missing values
print(twosigma[['building_id', 'price']].head())
```

```bash
                         building_id   price
    0  53a5b119ba8f7b61d4e010512e0dfc85  3000.0
    1  c5c8a357cba207596b04d1afd1e4f130  5465.0
    2  c3ba40552e2120b0acfc3cb5730bb2aa  2850.0
    3  28d9ad350afeaab8027513a3e52ac8d5  3275.0
    4                               NaN  3350.0
```

#### Impute missing data

You've found that "price" and "building_id" columns have missing values in the Rental Listing Inquiries dataset. So, before passing the data to the models you need to impute these values.

Numerical feature "price" will be encoded with a mean value of non-missing prices.

Imputing categorical feature "building_id" with the most frequent category is a bad idea, because it would mean that all the apartments with a missing "building_id" are located in the most popular building. The better idea is to impute it with a new category.

```python
# Import SimpleImputer
from sklearn.impute import SimpleImputer

# Create mean imputer
mean_imputer = SimpleImputer(strategy='mean')

# Price imputation
rental_listings[['price']] = mean_imputer.fit_transform(rental_listings[['price']])
```

```python
# Import SimpleImputer
from sklearn.impute import SimpleImputer

# Create constant imputer
constant_imputer = SimpleImputer(strategy='constant', fill_value='MISSING')

# building_id imputation
rental_listings[['building_id']] = constant_imputer.fit_transform(rental_listings[['building_id']])
```

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
