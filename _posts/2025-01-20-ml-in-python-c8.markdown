---
layout: post
title: "Extreme Gradient Boosting with XGBoost"
date: 2025-01-20 07:00:00 +0700
categories: machine learning in python
---

XGBoost (Extreme Gradient Boosting) là một thuật toán *gradient boosting* (tăng cường gradient) được tối ưu hóa về tốc độ và hiệu suất. Nó được phát triển bởi Tianqi Chen và được sử dụng rộng rãi trong các cuộc thi học máy (như Kaggle) nhờ khả năng đạt độ chính xác cao.

### Table of content


- [1. Classification with XGBoost](#1-classification-with-xgboost)
  - [1.1. Introducing XGBoost](#11-introducing-xgboost)
    - [1.1.1. Example - Measuring accuracy](#111-example---measuring-accuracy)
    - [1.1.2. Example - Measuring AUC](#112-example---measuring-auc)
  - [1.2. When should I use XGBoost?](#12-when-should-i-use-xgboost)
- [2. Regression with XGBoost](#2-regression-with-xgboost)
  - [2.1. Objective (loss) functions and base learners](#21-objective-loss-functions-and-base-learners)
    - [2.1.1. Example - Trees as base learners example: Scikit-learn API](#211-example---trees-as-base-learners-example-scikit-learn-api)
    - [2.1.2. Example - Linear base learners example: learning API only](#212-example---linear-base-learners-example-learning-api-only)
    - [2.1.3. Example - Evaluating model quality](#213-example---evaluating-model-quality)
  - [2.2. Regularization and base learners in XGBoost](#22-regularization-and-base-learners-in-xgboost)
    - [2.2.1. Example - Using regularization in XGBoost](#221-example---using-regularization-in-xgboost)
    - [2.2.2. Example - Visualizing individual XGBoost trees](#222-example---visualizing-individual-xgboost-trees)
    - [2.2.3. Visualizing feature importances: What features are most important in my dataset](#223-visualizing-feature-importances-what-features-are-most-important-in-my-dataset)
- [3. Fine-tuning your XGBoost model](#3-fine-tuning-your-xgboost-model)
  - [3.1. Why tune your model?](#31-why-tune-your-model)
    - [3.1.1. Example - Tuning the number of boosting rounds](#311-example---tuning-the-number-of-boosting-rounds)
    - [3.1.2. Example - Automated boosting round selection using early\_stopping](#312-example---automated-boosting-round-selection-using-early_stopping)
  - [3.2. Overview of XGBoost's hyperparameters](#32-overview-of-xgboosts-hyperparameters)
    - [3.2.1. Example - Tuning eta (learning rate)](#321-example---tuning-eta-learning-rate)
    - [3.2.2. Example - Tuning max\_depth](#322-example---tuning-max_depth)
    - [3.2.3. Example - Tuning colsample\_bytree](#323-example---tuning-colsample_bytree)
  - [3.3. Review of grid search and random search](#33-review-of-grid-search-and-random-search)
    - [3.3.1. Example - Grid search with XGBoost](#331-example---grid-search-with-xgboost)
    - [3.3.2. Example - Random search with XGBoost](#332-example---random-search-with-xgboost)
  - [3.4. Limits of grid search and random search](#34-limits-of-grid-search-and-random-search)
- [4. Using XGBoost in pipelines](#4-using-xgboost-in-pipelines)
  - [4.1. Review of pipelines using sklearn](#41-review-of-pipelines-using-sklearn)
    - [4.1.1. Example1 - Encoding categorical columns I: LabelEncoder](#411-example1---encoding-categorical-columns-i-labelencoder)
    - [4.1.2. Example2 - Encoding categorical columns II: OneHotEncoder](#412-example2---encoding-categorical-columns-ii-onehotencoder)
    - [4.1.3. Example 3 - Encoding categorical columns III: DictVectorizer](#413-example-3---encoding-categorical-columns-iii-dictvectorizer)
    - [4.1.4. Example 4 - Preprocessing within a pipeline](#414-example-4---preprocessing-within-a-pipeline)
  - [4.2. Incorporating XGBoost into pipelines](#42-incorporating-xgboost-into-pipelines)
    - [4.2.1. Example 1: Cross-validating your XGBoost model](#421-example-1-cross-validating-your-xgboost-model)
    - [4.2.2. Example 2: Kidney disease case study I: Categorical Imputer](#422-example-2-kidney-disease-case-study-i-categorical-imputer)
    - [4.2.3. Example 3: Kidney disease case study II: Feature Union](#423-example-3-kidney-disease-case-study-ii-feature-union)
    - [4.2.4. Example 4: Kidney disease case study III: Full pipeline](#424-example-4-kidney-disease-case-study-iii-full-pipeline)
  - [4.3. Tuning XGBoost hyperparameters](#43-tuning-xgboost-hyperparameters)
    - [4.3.1. Example - Bringing it all together](#431-example---bringing-it-all-together)



##  1. <a name='ClassificationwithXGBoost'></a>Classification with XGBoost

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C1.pdf)

###  1.1. <a name='IntroducingXGBoost'></a>Introducing XGBoost

**XGBoost (Extreme Gradient Boosting - Tăng cường Gradient Cực hạn)**

XGBoost (Extreme Gradient Boosting) là một thuật toán *gradient boosting* (tăng cường gradient) được tối ưu hóa về tốc độ và hiệu suất. Nó được phát triển bởi Tianqi Chen và được sử dụng rộng rãi trong các cuộc thi học máy (như Kaggle) nhờ khả năng đạt độ chính xác cao.

**Những điểm mạnh của XGBoost:**

*   **Tốc độ:** XGBoost được thiết kế để tối ưu hóa tốc độ huấn luyện. Nó sử dụng các kỹ thuật song song hóa và bộ nhớ đệm để tăng tốc độ tính toán.
*   **Hiệu suất:** XGBoost thường đạt độ chính xác cao hơn so với các thuật toán *gradient boosting* khác.  Điều này là do nó sử dụng các kỹ thuật *regularization* (điều chuẩn) để tránh *overfitting* (học quá khớp).
*   **Khả năng xử lý dữ liệu thiếu:** XGBoost có thể xử lý dữ liệu bị thiếu một cách hiệu quả.
*   **Hỗ trợ nhiều ngôn ngữ:** XGBoost có sẵn các thư viện cho nhiều ngôn ngữ lập trình, như Python, R, Java, Scala, C++,...
*   **Tính năng quan trọng:** XGBoost cung cấp thông tin về mức độ quan trọng của các thuộc tính (feature importance), giúp hiểu rõ hơn về dữ liệu.

**Cách thức hoạt động (tóm tắt):**

XGBoost cũng hoạt động dựa trên nguyên tắc *gradient boosting*, nhưng có một số cải tiến quan trọng:

1.  **Chính quy hóa (Regularization):** XGBoost sử dụng cả L1 và L2 *regularization* để kiểm soát độ phức tạp của mô hình và tránh *overfitting*.  Điều này giúp mô hình khái quát hóa tốt hơn trên dữ liệu mới.

2.  **Tối ưu hóa hàm mục tiêu:** XGBoost tối ưu hóa một hàm mục tiêu bao gồm cả thành phần *loss* (đo lường sai số) và thành phần *regularization*.

3.  **Gradient Boosting:** XGBoost xây dựng các cây quyết định một cách tuần tự. Mỗi cây mới được thêm vào để sửa chữa những sai sót của các cây trước đó.  Tuy nhiên, thay vì chỉ sử dụng gradient của hàm *loss*, XGBoost sử dụng gradient bậc hai (hessian) để tối ưu hóa tốt hơn.

4.  **Xử lý dữ liệu thiếu:** XGBoost có khả năng xử lý dữ liệu bị thiếu bằng cách học cách "điền" giá trị thiếu trong quá trình huấn luyện.

**Các tham số quan trọng của XGBoost:**

*   `n_estimators`: Số lượng cây (boosting rounds).
*   `learning_rate`: Tốc độ học.
*   `max_depth`: Độ sâu tối đa của cây.
*   `gamma`: Tham số *regularization* cho số lượng nút lá.
*   `reg_alpha`: L1 *regularization*.
*   `reg_lambda`: L2 *regularization*.
*   `subsample`: Tỉ lệ mẫu được sử dụng cho mỗi cây.
*   `colsample_bytree`: Tỉ lệ thuộc tính được sử dụng cho mỗi cây.

**Ví dụ (sử dụng Python và thư viện `xgboost`):**

```python
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Create arrays for the features and the target: X, y
X, y = churn_data.iloc[:,:-1], churn_data.iloc[:,-1]

# Create the training and test sets
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.2, random_state=123)

# Instantiate the XGBClassifier: xg_cl
xg_cl = xgb.XGBClassifier(objective='binary:logistic', n_estimators=10, seed=123)

# Fit the classifier to the training set
xg_cl.fit(X_train, y_train)

# Predict the labels of the test set: preds
preds = xg_cl.predict(X_test)

# Compute the accuracy: accuracy
accuracy = float(np.sum(preds==y_test))/y_test.shape[0]
print("accuracy: %f" % (accuracy))
```

**Tóm lại:**

*   XGBoost là một thuật toán *gradient boosting* mạnh mẽ và hiệu quả, được tối ưu hóa về tốc độ và hiệu suất.
*   Nó được sử dụng rộng rãi trong các bài toán học máy nhờ khả năng đạt độ chính xác cao.
*   XGBoost có nhiều tham số cần được điều chỉnh (tuned) để đạt được kết quả tốt nhất.

####  1.1.1. <a name='Example-Measuringaccuracy'></a>Example - Measuring accuracy

```python
import xgboost as xgb
import pandas as pd
churn_data = pd.read_csv("classification_data.csv")

# Create arrays for the features and the target: X, y
X, y = churn_data.iloc[:,:-1], churn_data.iloc[:,-1]

# Create the DMatrix from X and y: churn_dmatrix
churn_dmatrix = xgb.DMatrix(data=X, label=y)

# Create the parameter dictionary: params
params = {"objective":"reg:logistic", "max_depth":3}

# Perform cross-validation: cv_results
cv_results = xgb.cv(dtrain=churn_dmatrix, params=params, 
                  nfold=3, num_boost_round=5, 
                  metrics="error", as_pandas=True, seed=123)

# Print cv_results
print(cv_results)

# Print the accuracy
print(((1-cv_results["test-error-mean"]).iloc[-1]))

## Result: 0.751480015401492
```

####  1.1.2. <a name='Example-MeasuringAUC'></a>Example - Measuring AUC

```python
# Perform cross_validation: cv_results
cv_results = xgb.cv(dtrain=churn_dmatrix, params=params, 
                  nfold=3, num_boost_round=5, 
                  metrics="auc", as_pandas=True, seed=123)

# Print cv_results
print(cv_results)

# Print the AUC
print((cv_results["test-auc-mean"]).iloc[-1])

### Result: 0.8261911413597645
```

###  1.2. <a name='WhenshouldIuseXGBoost'></a>When should I use XGBoost?

**Khi nào nên sử dụng Stochastic Gradient Boosting (SGB)**

SGB là một lựa chọn tuyệt vời trong nhiều tình huống, đặc biệt khi:

1.  **Dữ liệu lớn:** Khi bạn có một tập dữ liệu lớn, việc huấn luyện Gradient Boosting truyền thống có thể tốn kém về mặt tính toán. SGB, với khả năng lấy mẫu ngẫu nhiên, giúp giảm đáng kể thời gian huấn luyện.

2.  **Nguy cơ overfitting:** Nếu bạn lo lắng về việc mô hình có thể bị overfitting (học quá khớp), SGB là một lựa chọn tốt. Việc lấy mẫu ngẫu nhiên giúp mô hình khái quát hóa tốt hơn, giảm nguy cơ học thuộc lòng dữ liệu huấn luyện.

3.  **Cải thiện hiệu suất:** Trong nhiều trường hợp, SGB có thể mang lại hiệu suất tốt hơn so với Gradient Boosting truyền thống, đặc biệt khi dữ liệu có nhiều nhiễu hoặc có cấu trúc phức tạp.

4.  **Khám phá dữ liệu:** SGB có thể được sử dụng để khám phá dữ liệu và tìm hiểu các mối quan hệ tiềm ẩn. Việc lấy mẫu ngẫu nhiên giúp mô hình tập trung vào các khía cạnh khác nhau của dữ liệu.

**Khi nào không nên sử dụng Stochastic Gradient Boosting (SGB)**

Tuy nhiên, SGB không phải là lúc nào cũng là lựa chọn tối ưu. Cân nhắc không sử dụng SGB khi:

1.  **Dữ liệu nhỏ:** Nếu bạn có một tập dữ liệu nhỏ, việc lấy mẫu ngẫu nhiên có thể làm giảm hiệu suất của mô hình. Trong trường hợp này, Gradient Boosting truyền thống có thể là lựa chọn tốt hơn.

2.  **Yêu cầu độ chính xác tuyệt đối:** Mặc dù SGB thường cho kết quả tốt, nhưng đôi khi nó có thể không đạt được độ chính xác tuyệt đối như Gradient Boosting truyền thống trên một số tập dữ liệu nhất định.

3.  **Khả năng diễn giải:** Mô hình SGB thường khó diễn giải hơn so với Gradient Boosting truyền thống, do nó được xây dựng trên các mẫu ngẫu nhiên. Nếu khả năng diễn giải là yếu tố quan trọng, hãy cân nhắc các lựa chọn khác.

4.  **Tài nguyên hạn chế:** Mặc dù SGB giúp giảm thời gian huấn luyện so với Gradient Boosting truyền thống, nhưng nó vẫn có thể yêu cầu tài nguyên tính toán đáng kể, đặc biệt khi số lượng cây lớn.

**Lời khuyên**

*   Hãy thử cả Gradient Boosting truyền thống và SGB trên tập dữ liệu của bạn để xem mô hình nào hoạt động tốt hơn.
*   Điều chỉnh các siêu tham số (hyperparameters) của SGB, như `subsample`, `learning_rate`, và `n_estimators`, để đạt được hiệu suất tốt nhất.
*   Sử dụng cross-validation để đánh giá mô hình một cách khách quan.


---
##  2. <a name='RegressionwithXGBoost'></a>Regression with XGBoost

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C2.pdf)

###  2.1. <a name='Objectivelossfunctionsandbaselearners'></a>Objective (loss) functions and base learners


Trong XGBoost, việc lựa chọn *objective function* (hàm mục tiêu) và *base learner* (mô hình cơ sở) là rất quan trọng, ảnh hưởng trực tiếp đến hiệu suất và khả năng của mô hình.

**1. Objective Function (Hàm Mục Tiêu):**

*   *Objective function* là một hàm toán học đo lường "mức độ tốt" của mô hình.  Trong XGBoost, *objective function* bao gồm hai thành phần chính:
    *   *Loss function* (hàm mất mát): Đo lường sai số giữa dự đoán của mô hình và giá trị thực tế.
    *   *Regularization term* (thành phần điều chuẩn):  Kiểm soát độ phức tạp của mô hình, giúp tránh *overfitting* (học quá khớp).

*   XGBoost cố gắng tối thiểu hóa *objective function* trong quá trình huấn luyện.

*   **Các loại Objective Function phổ biến:**
    *   **Đối với bài toán hồi quy (Regression):**
        *   `reg:squarederror`: *Mean Squared Error (MSE)* - Sai số bình phương trung bình.
        *   `reg:logistic`: *Logistic loss* - Thường được dùng cho hồi quy logistic.
        *   `reg:absoluteerror`: *Mean Absolute Error (MAE)* - Sai số tuyệt đối trung bình.
    *   **Đối với bài toán phân loại (Classification):**
        *   `binary:logistic`: *Logistic loss* - Cho bài toán phân loại nhị phân.
        *   `multi:softmax`: *Softmax loss* - Cho bài toán phân loại đa lớp (trả về xác suất cho mỗi lớp).
        *   `multi:softprob`: *Softmax loss* - Giống `multi:softmax` nhưng trả về xác suất cho mỗi lớp.

**2. Base Learners (Mô hình Cơ sở):**

*   *Base learner* là mô hình học máy yếu được sử dụng để xây dựng mô hình XGBoost.  XGBoost kết hợp nhiều *base learners* để tạo ra một mô hình mạnh mẽ hơn.

*   **Các loại Base Learners phổ biến:**
    *   `gbtree` (Tree Booster): Sử dụng cây quyết định làm *base learner*.  Đây là loại *base learner* phổ biến nhất trong XGBoost.
    *   `gblinear` (Linear Booster): Sử dụng mô hình tuyến tính làm *base learner*.  Thường được dùng khi dữ liệu có mối quan hệ tuyến tính.
    *   `dart` (DART Booster):  Một biến thể của `gbtree` với cơ chế *dropout*, giúp tăng tính đa dạng của các cây và giảm overfitting.

**Ví dụ:**

Giả sử bạn muốn xây dựng một mô hình XGBoost để dự đoán giá nhà (bài toán hồi quy). Bạn có thể chọn:

*   *Objective function*: `reg:squarederror` (MSE) để đo lường sai số giữa giá nhà dự đoán và giá nhà thực tế.
*   *Base learner*: `gbtree` (cây quyết định) vì cây quyết định có thể học được các mối quan hệ phức tạp giữa các thuộc tính và giá nhà.

**Cách lựa chọn Objective Function và Base Learner:**

Việc lựa chọn *objective function* và *base learner* phụ thuộc vào bài toán cụ thể và đặc điểm của dữ liệu.

*   **Loại bài toán:**  Bài toán hồi quy hay phân loại sẽ quyết định loại *objective function* phù hợp.
*   **Đặc điểm dữ liệu:**  Dữ liệu có mối quan hệ tuyến tính hay phi tuyến tính sẽ ảnh hưởng đến việc lựa chọn *base learner*.
*   **Mục tiêu:**  Đôi khi, việc tối ưu một độ đo cụ thể (ví dụ: F1-score) đòi hỏi một *objective function* riêng biệt.

**Tóm lại:**

*   *Objective function* đo lường "mức độ tốt" của mô hình và bao gồm *loss function* và *regularization term*.
*   *Base learner* là mô hình học máy yếu được sử dụng để xây dựng mô hình XGBoost.
*   Việc lựa chọn *objective function* và *base learner* phù hợp là rất quan trọng để đạt được hiệu suất tốt nhất.  Cần xem xét loại bài toán, đặc điểm dữ liệu và mục tiêu cụ thể.
  

####  2.1.1. <a name='Example-Treesasbaselearnersexample:Scikit-learnAPI'></a>Example - Trees as base learners example: Scikit-learn API

```python
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

boston_data = pd.read_csv("boston_housing.csv")
X, y = boston_data.iloc[:,:-1],boston_data.iloc[:,-1]
# Create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Instantiate the XGBRegressor: xg_reg
xg_reg = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=10, seed=123)

# Fit the regressor to the training set
xg_reg.fit(X_train, y_train)

# Predict the labels of the test set: preds
preds = xg_reg.predict(X_test)

# Compute the rmse: rmse
rmse = np.sqrt(mean_squared_error(preds, y_test))
print("RMSE: %f" % (rmse))
```

####  2.1.2. <a name='Example-Linearbaselearnersexample:learningAPIonly'></a>Example - Linear base learners example: learning API only

```python
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

boston_data = pd.read_csv("boston_housing.csv")
X, y = boston_data.iloc[:,:-1],boston_data.iloc[:,-1]
# Create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Convert the training and testing sets into DMatrixes: DM_train, DM_test
DM_train = xgb.DMatrix(data=X_train, label=y_train)
DM_test =  xgb.DMatrix(data=X_test, label=y_test)

# Create the parameter dictionary: params
params = {"booster":"gblinear","objective":"reg:squarederror"}

# Train the model: xg_reg
xg_reg = xgb.train(params = params, dtrain=DM_train, num_boost_round=5)

# Predict the labels of the test set: preds
preds = xg_reg.predict(DM_test)

# Compute and print the RMSE
rmse = np.sqrt(mean_squared_error(y_test,preds))
print("RMSE: %f" % (rmse))
```

####  2.1.3. <a name='Example-Evaluatingmodelquality'></a>Example - Evaluating model quality

```python
# Create the DMatrix: housing_dmatrix
housing_dmatrix = xgb.DMatrix(data=X, label=y)

# Create the parameter dictionary: params
params = {"objective":"reg:squarederror", "max_depth":4}

# Perform cross-validation: cv_results
cv_results = xgb.cv(dtrain=housing_dmatrix, params=params, nfold=4, num_boost_round=5, metrics='mae', as_pandas=True, seed=123)

# Print cv_results
print(cv_results)

# Extract and print final boosting round metric
print((cv_results["test-mae-mean"]).tail(1))
```

###  2.2. <a name='RegularizationandbaselearnersinXGBoost'></a>Regularization and base learners in XGBoost

####  2.2.1. <a name='Example-UsingregularizationinXGBoost'></a>Example - Using regularization in XGBoost

```python
# Create the DMatrix: housing_dmatrix
housing_dmatrix = xgb.DMatrix(data=X, label=y)

reg_params = [1, 10, 100]

# Create the initial parameter dictionary for varying l2 strength: params
params = {"objective":"reg:squarederror","max_depth":3}

# Create an empty list for storing rmses as a function of l2 complexity
rmses_l2 = []

# Iterate over reg_params
for reg in reg_params:

    # Update l2 strength
    params["lambda"] = reg
    
    # Pass this updated param dictionary into cv
    cv_results_rmse = xgb.cv(dtrain=housing_dmatrix, params=params, nfold=2, num_boost_round=5, metrics="rmse", as_pandas=True, seed=123)
    
    # Append best rmse (final round) to rmses_l2
    rmses_l2.append(cv_results_rmse["test-rmse-mean"].tail(1).values[0])

# Look at best rmse per l2 param
print("Best rmse as a function of l2:")
print(pd.DataFrame(list(zip(reg_params, rmses_l2)), columns=["l2", "rmse"]))
```

####  2.2.2. <a name='Example-VisualizingindividualXGBoosttrees'></a>Example - Visualizing individual XGBoost trees

```python
# Create the DMatrix: housing_dmatrix
housing_dmatrix = xgb.DMatrix(data=X, label=y)

# Create the parameter dictionary: params
params = {"objective":"reg:squarederror", "max_depth":2}

# Train the model: xg_reg
xg_reg = xgb.train(params=params, dtrain=housing_dmatrix, num_boost_round=10)

# Plot the first tree
xgb.plot_tree(xg_reg, num_trees=0)
plt.show()

# Plot the fifth tree
xgb.plot_tree(xg_reg, num_trees=4)
plt.show()

# Plot the last tree sideways
xgb.plot_tree(xg_reg, num_trees=9 ,rankdir="LR")
plt.show()
```

**Plot the first tree**
![]({{site.baseurl}}/images/tree1.svg)

**Plot the fifth tree**
![]({{site.baseurl}}/images/tree2.svg)

**Plot the last tree sideways**
![]({{site.baseurl}}/images/tree3.svg)

####  2.2.3. <a name='Visualizingfeatureimportances:Whatfeaturesaremostimportantinmydataset'></a>Visualizing feature importances: What features are most important in my dataset

```python
# Create the DMatrix: housing_dmatrix
housing_dmatrix = xgb.DMatrix(data=X, label=y)

# Create the parameter dictionary: params
params = params = {"objective":"reg:squarederror", "max_depth":4}

# Train the model: xg_reg
xg_reg = xg_reg = xgb.train(params=params, dtrain=housing_dmatrix, num_boost_round=10)

# Plot the feature importances
xgb.plot_importance(xg_reg)
plt.show()
```

**Plot the feature importances**
![]({{site.baseurl}}/images/important_feature_xgboost.svg)

---
##  3. <a name='Fine-tuningyourXGBoostmodel'></a>Fine-tuning your XGBoost model

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C3.pdf)

###  3.1. <a name='Whytuneyourmodel'></a>Why tune your model?

####  3.1.1. <a name='Example-Tuningthenumberofboostingrounds'></a>Example - Tuning the number of boosting rounds

```python
# Create the DMatrix: housing_dmatrix
housing_dmatrix = xgb.DMatrix(data=X, label=y)

# Create the parameter dictionary for each tree: params 
params = {"objective":"reg:squarederror", "max_depth":3}

# Create list of number of boosting rounds
num_rounds = [5, 10, 15]

# Empty list to store final round rmse per XGBoost model
final_rmse_per_round = []

# Iterate over num_rounds and build one model per num_boost_round parameter
for curr_num_rounds in num_rounds:

    # Perform cross-validation: cv_results
    cv_results = xgb.cv(dtrain=housing_dmatrix, params=params, nfold=3, num_boost_round=curr_num_rounds, metrics="rmse", as_pandas=True, seed=123)
    
    # Append final round RMSE
    final_rmse_per_round.append(cv_results["test-rmse-mean"].tail().values[-1])

# Print the resultant DataFrame
num_rounds_rmses = list(zip(num_rounds, final_rmse_per_round))
print(pd.DataFrame(num_rounds_rmses,columns=["num_boosting_rounds","rmse"]))
```

####  3.1.2. <a name='Example-Automatedboostingroundselectionusingearly_stopping'></a>Example - Automated boosting round selection using early_stopping

```python
# Create your housing DMatrix: housing_dmatrix
housing_dmatrix = xgb.DMatrix(data=X, label=y)

# Create the parameter dictionary for each tree: params
params = {"objective":"reg:squarederror", "max_depth":4}

# Perform cross-validation with early stopping: cv_results
cv_results = xgb.cv(dtrain=housing_dmatrix, 
                    params=params, metrics='rmse', 
                    nfold=3,
                    early_stopping_rounds=10,
                    num_boost_round=50, 
                    as_pandas=True, 
                    seed=123)

# Print cv_results
print(cv_results)
```

###  3.2. <a name='OverviewofXGBoostshyperparameters'></a>Overview of XGBoost's hyperparameters

- Common tree tunable parameters
    - `learning rate`: learning rate/eta
    - `gamma`: min loss reduction to create new tree split
    - `lambda`: L2 reg on leaf weights
    - `alpha`: L1 reg on leaf weights
    - `max_depth`: max depth per tree
    - `subsample`: % samples used per tree
    - `colsample_bytree`: % features used per tree

- Linear tunable parameters
    - `lambda`: L2 reg on weights
    - `alpha`: L1 reg on weights
    - `lambda_bias`: L2 reg term on bias

You can also tune the number of estimators used for both base model types

####  3.2.1. <a name='Example-Tuningetalearningrate'></a>Example - Tuning eta (learning rate)

```python
# Create your housing DMatrix: housing_dmatrix
housing_dmatrix = xgb.DMatrix(data=X, label=y)

# Create the parameter dictionary for each tree (boosting round)
params = {"objective":"reg:squarederror", "max_depth":3}

# Create list of eta values and empty list to store final round rmse per xgboost model
eta_vals = [0.001, 0.01, 0.1]
best_rmse = []

# Systematically vary the eta 
for curr_val in eta_vals:

    params["eta"] = curr_val
    
    # Perform cross-validation: cv_results
    cv_results = xgb.cv(
                    dtrain=housing_dmatrix,
                    nfold=3,
                    params=params,
                    num_boost_round=10,
                    early_stopping_rounds=5,
                    metrics='rmse',
                    as_pandas=True,
                    seed=123
    )
    
    
    
    # Append the final round rmse to best_rmse
    best_rmse.append(cv_results["test-rmse-mean"].tail().values[-1])

# Print the resultant DataFrame
print(pd.DataFrame(list(zip(eta_vals, best_rmse)), columns=["eta","best_rmse"]))


### Output
<script.py> output:
         eta   best_rmse
    0  0.001  195736.403
    1  0.010  179932.184
    2  0.100   79759.412
```

####  3.2.2. <a name='Example-Tuningmax_depth'></a>Example - Tuning max_depth

```python
# Create your housing DMatrix
housing_dmatrix = xgb.DMatrix(data=X,label=y)

# Create the parameter dictionary
params = {"objective":"reg:squarederror"}

# Create list of max_depth values
max_depths = [2, 5, 10, 20]
best_rmse = []

# Systematically vary the max_depth
for curr_val in max_depths:

    params["max_depth"] = curr_val
    
    # Perform cross-validation
    cv_results = xgb.cv(
                dtrain=housing_dmatrix,
                nfold=2,
                params=params,
                metrics='rmse',
                early_stopping_rounds=5,
                num_boost_round=10,
                seed=123,
                as_pandas=True
    )
    
    
    
    # Append the final round rmse to best_rmse
    best_rmse.append(cv_results["test-rmse-mean"].tail().values[-1])

# Print the resultant DataFrame
print(pd.DataFrame(list(zip(max_depths, best_rmse)),columns=["max_depth","best_rmse"]))

### Output
<script.py> output:
       max_depth  best_rmse
    0          2  37957.469
    1          5  35596.600
    2         10  36065.547
    3         20  36739.576
```

####  3.2.3. <a name='Example-Tuningcolsample_bytree'></a>Example - Tuning colsample_bytree

```python
# Create your housing DMatrix
housing_dmatrix = xgb.DMatrix(data=X,label=y)

# Create the parameter dictionary
params={"objective":"reg:squarederror","max_depth":3}

# Create list of hyperparameter values: colsample_bytree_vals
colsample_bytree_vals = [0.1, 0.5, 0.8, 1]
best_rmse = []

# Systematically vary the hyperparameter value 
for curr_val in colsample_bytree_vals:

    params['colsample_bytree'] = curr_val
    
    # Perform cross-validation
    cv_results = xgb.cv(dtrain=housing_dmatrix, params=params, nfold=2,
                 num_boost_round=10, early_stopping_rounds=5,
                 metrics="rmse", as_pandas=True, seed=123)
    
    # Append the final round rmse to best_rmse
    best_rmse.append(cv_results["test-rmse-mean"].tail().values[-1])

# Print the resultant DataFrame
print(pd.DataFrame(list(zip(colsample_bytree_vals, best_rmse)), columns=["colsample_bytree","best_rmse"]))

### Output
<script.py> output:
       colsample_bytree  best_rmse
    0               0.1  50033.735
    1               0.5  35656.186
    2               0.8  36399.002
    3               1.0  35836.044
```

###  3.3. <a name='Reviewofgridsearchandrandomsearch'></a>Review of grid search and random search

####  3.3.1. <a name='Example-GridsearchwithXGBoost'></a>Example - Grid search with XGBoost

```python
# Create the parameter grid: gbm_param_grid
gbm_param_grid = {
    'colsample_bytree': [0.3, 0.7],
    'n_estimators': [50],
    'max_depth': [2, 5]
}

# Instantiate the regressor: gbm
gbm = xgb.XGBRegressor()

# Perform grid search: grid_mse
grid_mse = GridSearchCV(
            estimator=gbm,
            param_grid=gbm_param_grid,
            scoring='neg_mean_squared_error',
            cv=4,
            verbose=1
)


# Fit grid_mse to the data
grid_mse.fit(X, y)

# Print the best parameters and lowest RMSE
print("Best parameters found: ", grid_mse.best_params_)
print("Lowest RMSE found: ", np.sqrt(np.abs(grid_mse.best_score_)))
```

Output:

```bash
Fitting 4 folds for each of 4 candidates, totalling 16 fits
Best parameters found:  {'colsample_bytree': 0.3, 'max_depth': 5, 'n_estimators': 50}
Lowest RMSE found:  29916.017850830365
```

####  3.3.2. <a name='Example-RandomsearchwithXGBoost'></a>Example - Random search with XGBoost

```python
# Create the parameter grid: gbm_param_grid 
gbm_param_grid = {
    'n_estimators': [25],
    'max_depth': range(2, 12)
}

# Instantiate the regressor: gbm
gbm = xgb.XGBRegressor(n_estimators=10)

# Perform random search: grid_mse
randomized_mse = RandomizedSearchCV(
                   estimator=gbm,
                   param_distributions=gbm_param_grid,
                   scoring='neg_mean_squared_error',
                   n_iter=5,
                   cv=4,
                   verbose=1
)


# Fit randomized_mse to the data
randomized_mse.fit(X, y)

# Print the best parameters and lowest RMSE
print("Best parameters found: ", randomized_mse.best_params_)
print("Lowest RMSE found: ", np.sqrt(np.abs(randomized_mse.best_score_)))
```

Output:

```bash
Fitting 4 folds for each of 5 candidates, totalling 20 fits
Best parameters found:  {'n_estimators': 25, 'max_depth': 6}
Lowest RMSE found:  31412.365221128253
```

###  3.4. <a name='Limitsofgridsearchandrandomsearch'></a>Limits of grid search and random search

Trong Machine Learning, *grid search* (tìm kiếm lưới) và *random search* (tìm kiếm ngẫu nhiên) là hai phương pháp phổ biến được sử dụng để *tune hyperparameters* (điều chỉnh siêu tham số) của mô hình. Tuy nhiên, cả hai phương pháp này đều có những hạn chế nhất định.

**1. Grid Search (Tìm Kiếm Lưới):**

*   **Ưu điểm:**
    *   Đơn giản, dễ thực hiện.
    *   Tìm kiếm toàn diện trong không gian tham số được định nghĩa.

*   **Hạn chế:**
    *   **Tốn kém tính toán:**  Số lượng kết hợp tham số tăng theo cấp số nhân với số lượng tham số.  Ví dụ, nếu bạn có 3 tham số, mỗi tham số có 10 giá trị, bạn cần đánh giá 10 * 10 * 10 = 1000 mô hình.  Điều này có thể rất tốn kém về thời gian và tài nguyên tính toán, đặc biệt khi không gian tìm kiếm lớn.
    *   **Không hiệu quả với không gian tham số lớn:**  Khi số lượng tham số hoặc số lượng giá trị cho mỗi tham số lớn, *grid search* trở nên không khả thi.
    *   **Khó xác định phạm vi tìm kiếm:**  Việc xác định phạm vi giá trị cho mỗi tham số có thể khó khăn. Nếu phạm vi quá nhỏ, bạn có thể bỏ lỡ các giá trị tối ưu. Nếu phạm vi quá lớn, *grid search* sẽ tốn kém hơn.

**2. Random Search (Tìm Kiếm Ngẫu Nhiên):**

*   **Ưu điểm:**
    *   Ít tốn kém tính toán hơn *grid search*, đặc biệt khi không gian tham số lớn.
    *   Có thể tìm kiếm các giá trị tối ưu "ẩn" mà *grid search* có thể bỏ lỡ.

*   **Hạn chế:**
    *   **Không đảm bảo tìm được giá trị tối ưu:** Vì tìm kiếm ngẫu nhiên, không có gì đảm bảo rằng bạn sẽ tìm thấy giá trị tối ưu, hoặc thậm chí một giá trị đủ tốt.
    *   **Khó kiểm soát:**  Khó kiểm soát quá trình tìm kiếm.  Có thể lãng phí tài nguyên vào việc đánh giá các kết hợp tham số không hiệu quả.
    *   **Vẫn tốn kém nếu không gian tìm kiếm quá lớn:** Mặc dù ít tốn kém hơn *grid search*, *random search* vẫn có thể tốn kém nếu không gian tìm kiếm quá lớn.

**So sánh Grid Search và Random Search:**

*   *Grid search* tìm kiếm *toàn diện* trong không gian tham số được định nghĩa, nhưng tốn kém tính toán.
*   *Random search* tìm kiếm *ngẫu nhiên* trong không gian tham số, ít tốn kém hơn nhưng không đảm bảo tìm được giá trị tối ưu.

**Các phương pháp khác:**

Ngoài *grid search* và *random search*, còn có các phương pháp khác hiệu quả hơn, đặc biệt khi không gian tìm kiếm lớn, như:

*   **Bayesian Optimization (Tối Ưu Hóa Bayesian):**  Sử dụng mô hình Bayesian để ước lượng hàm mục tiêu và chọn các giá trị tham số tiếp theo một cách thông minh.
*   **Hyperopt:** Một thư viện Python để tối ưu hóa siêu tham số, hỗ trợ nhiều thuật toán tìm kiếm khác nhau, bao gồm cả Bayesian Optimization.
*   **Scikit-optimize:** Một thư viện Python khác để tối ưu hóa siêu tham số, cũng hỗ trợ Bayesian Optimization.

**Tóm lại:**

*   *Grid search* và *random search* là các phương pháp cơ bản để điều chỉnh siêu tham số, nhưng có những hạn chế nhất định.
*   *Grid search* tốn kém tính toán, đặc biệt khi không gian tham số lớn.
*   *Random search* ít tốn kém hơn, nhưng không đảm bảo tìm được giá trị tối ưu.
*   Các phương pháp như Bayesian Optimization có thể hiệu quả hơn, đặc biệt khi không gian tìm kiếm lớn.  Việc lựa chọn phương pháp phù hợp phụ thuộc vào bài toán cụ thể và nguồn lực có sẵn.


---
##  4. <a name='UsingXGBoostinpipelines'></a>Using XGBoost in pipelines

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C4.pdf)

###  4.1. <a name='Reviewofpipelinesusingsklearn'></a>Review of pipelines using sklearn

####  4.1.1. <a name='Example1-EncodingcategoricalcolumnsI:LabelEncoder'></a>Example1 - Encoding categorical columns I: LabelEncoder

```python
# Import LabelEncoder
from sklearn.preprocessing import LabelEncoder

# Fill missing values with 0
df.LotFrontage = df.LotFrontage.fillna(0)

# Create a boolean mask for categorical columns
categorical_mask = (df.dtypes == object)

# Get list of categorical column names
categorical_columns = df.columns[categorical_mask].tolist()

# Print the head of the categorical columns
print(df[categorical_columns].head())

# Create LabelEncoder object: le
le = LabelEncoder()

# Apply LabelEncoder to categorical columns
df[categorical_columns] = df[categorical_columns].apply(lambda x: le.fit_transform(x))

# Print the head of the LabelEncoded categorical columns
print(df[categorical_columns].head())
```

####  4.1.2. <a name='Example2-EncodingcategoricalcolumnsII:OneHotEncoder'></a>Example2 - Encoding categorical columns II: OneHotEncoder

```python
# Import OneHotEncoder
from sklearn.preprocessing import OneHotEncoder

# Create OneHotEncoder: ohe
ohe = OneHotEncoder(sparse=False)

# Apply OneHotEncoder to categorical columns - output is no longer a dataframe: df_encoded
df_encoded = ohe.fit_transform(df)

# Print first 5 rows of the resulting dataset - again, this will no longer be a pandas dataframe
print(df_encoded[:5, :])

# Print the shape of the original DataFrame
print(df.shape)

# Print the shape of the transformed array
print(df_encoded.shape)
```

####  4.1.3. <a name='Example3-EncodingcategoricalcolumnsIII:DictVectorizer'></a>Example 3 - Encoding categorical columns III: DictVectorizer

```python
# Import DictVectorizer
from sklearn.feature_extraction import DictVectorizer

# Convert df into a dictionary: df_dict
df_dict = df.to_dict("records")

# Create the DictVectorizer object: dv
dv = DictVectorizer(sparse=False)

# Apply dv on df: df_encoded
df_encoded = dv.fit_transform(df_dict)

# Print the resulting first five rows
print(df_encoded[:5,:])

# Print the vocabulary
print(dv.vocabulary_)
```

####  4.1.4. <a name='Example4-Preprocessingwithinapipeline'></a>Example 4 - Preprocessing within a pipeline

```python
# Import necessary modules
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

# Fill LotFrontage missing values with 0
X.LotFrontage = X.LotFrontage.fillna(0)

# Setup the pipeline steps: steps
steps = [("ohe_onestep", DictVectorizer(sparse=False)),
         ("xgb_model", xgb.XGBRegressor())]

# Create the pipeline: xgb_pipeline
xgb_pipeline = Pipeline(steps)

# Fit the pipeline
xgb_pipeline.fit(X.to_dict('records'),y)
```

###  4.2. <a name='IncorporatingXGBoostintopipelines'></a>Incorporating XGBoost into pipelines

####  4.2.1. <a name='Example1:Cross-validatingyourXGBoostmodel'></a>Example 1: Cross-validating your XGBoost model

```python
# Import necessary modules
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

# Fill LotFrontage missing values with 0
X.LotFrontage = X.LotFrontage.fillna(0)

# Setup the pipeline steps: steps
steps = [("ohe_onestep", DictVectorizer(sparse=False)),
         ("xgb_model", xgb.XGBRegressor(max_depth=2, objective="reg:squarederror"))]

# Create the pipeline: xgb_pipeline
xgb_pipeline = Pipeline(steps)

# Cross-validate the model
cross_val_scores = cross_val_score(
                    xgb_pipeline, 
                    X.to_dict('records'), 
                    y, 
                    scoring='neg_mean_squared_error', 
                    cv=10)

# Print the 10-fold RMSE
print("10-fold RMSE: ", np.mean(np.sqrt(np.abs(cross_val_scores))))
```

Output:

```bash
<script.py> output:
    10-fold RMSE:  27683.04157118635
```

####  4.2.2. <a name='Example2:KidneydiseasecasestudyI:CategoricalImputer'></a>Example 2: Kidney disease case study I: Categorical Imputer

```python
# Import necessary modules
from sklearn_pandas import DataFrameMapper
from sklearn.impute import SimpleImputer

# Check number of nulls in each feature column
nulls_per_column = X.isnull().sum()
print(nulls_per_column)

# Create a boolean mask for categorical columns
categorical_feature_mask = X.dtypes == object

# Get list of categorical column names
categorical_columns = X.columns[categorical_feature_mask].tolist()

# Get list of non-categorical column names
non_categorical_columns = X.columns[~categorical_feature_mask].tolist()

# Apply numeric imputer
numeric_imputation_mapper = DataFrameMapper(
                                            [([numeric_feature], SimpleImputer(strategy="median")) for numeric_feature in non_categorical_columns],
                                            input_df=True,
                                            df_out=True
                                           )

# Apply categorical imputer
categorical_imputation_mapper = DataFrameMapper(
                                                [(category_feature, SimpleImputer(strategy="median")) for category_feature in categorical_columns],
                                                input_df=True,
                                                df_out=True
                                               )
```

####  4.2.3. <a name='Example3:KidneydiseasecasestudyII:FeatureUnion'></a>Example 3: Kidney disease case study II: Feature Union

```python
# Import FeatureUnion
from sklearn.pipeline import FeatureUnion

# Combine the numeric and categorical transformations
numeric_categorical_union = FeatureUnion([
                                          ("num_mapper", numeric_imputation_mapper),
                                          ("cat_mapper", categorical_imputation_mapper)
                                         ])
```

####  4.2.4. <a name='Example4:KidneydiseasecasestudyIII:Fullpipeline'></a>Example 4: Kidney disease case study III: Full pipeline

```python
# Create full pipeline
pipeline = Pipeline([
                     ("featureunion", numeric_categorical_union),
                     ("dictifier", Dictifier()),
                     ("vectorizer", DictVectorizer(sort=False)),
                     ("clf", xgb.XGBClassifier(max_depth=3))
                    ])

# Perform cross-validation
cross_val_scores = cross_val_score(pipeline, X, y, scoring="roc_auc", cv=3)

# Print avg. AUC
print("3-fold AUC: ", np.mean(cross_val_scores))
```

Output:

```bash
<script.py> output:
    3-fold AUC:  0.998237712755785
```

###  4.3. <a name='TuningXGBoosthyperparameters'></a>Tuning XGBoost hyperparameters

####  4.3.1. <a name='Example-Bringingitalltogether'></a>Example - Bringing it all together

```python
# Create the parameter grid
gbm_param_grid = {
    'clf__learning_rate': np.arange(0.05, 1, 0.05),
    'clf__max_depth': np.arange(3, 10, 1),
    'clf__n_estimators': np.arange(50, 200, 50)
}

# Perform RandomizedSearchCV
randomized_roc_auc = RandomizedSearchCV(
                        estimator=pipeline,
                        param_distributions=gbm_param_grid,
                        n_iter=2,
                        cv=2,
                        scoring="roc_auc",
                        verbose=1)

# Fit the estimator
randomized_roc_auc.fit(X, y)

# Compute metrics
print(randomized_roc_auc.best_score_)
print(randomized_roc_auc.best_estimator_)
```

Output:

```bash
0.9970133333333333
Pipeline(steps=[('featureunion',
                 FeatureUnion(transformer_list=[('num_mapper',
                                                 DataFrameMapper(df_out=True,
                                                                 features=[(['age'],
                                                                            SimpleImputer(strategy='median')),
                                                                           (['bp'],
                                                                            SimpleImputer(strategy='median')),
                                                                           (['sg'],
                                                                            SimpleImputer(strategy='median')),
                                                                           (['al'],
                                                                            SimpleImputer(strategy='median')),
                                                                           (['su'],
                                                                            SimpleImputer(strategy='median')),
                                                                           (['bgr'],
                                                                            SimpleImputer(s...
                               gamma=0, gpu_id=-1, grow_policy='depthwise',
                               importance_type=None, interaction_constraints='',
                               learning_rate=0.25, max_bin=256,
                               max_cat_to_onehot=4, max_delta_step=0,
                               max_depth=7, max_leaves=0, min_child_weight=1,
                               missing=nan, monotone_constraints='()',
                               n_estimators=150, n_jobs=0, num_parallel_tree=1,
                               predictor='auto', random_state=0, reg_alpha=0,
                               reg_lambda=1, ...))])

<script.py> output:
    Fitting 2 folds for each of 2 candidates, totalling 4 fits
    0.9965333333333333
    Pipeline(steps=[('featureunion',
                     FeatureUnion(transformer_list=[('num_mapper',
                                                     DataFrameMapper(df_out=True,
                                                                     features=[(['age'],
                                                                                SimpleImputer(strategy='median')),
                                                                               (['bp'],
                                                                                SimpleImputer(strategy='median')),
                                                                               (['sg'],
                                                                                SimpleImputer(strategy='median')),
                                                                               (['al'],
                                                                                SimpleImputer(strategy='median')),
                                                                               (['su'],
                                                                                SimpleImputer(strategy='median')),
                                                                               (['bgr'],
                                                                                SimpleImputer(s...
                                   gamma=0, gpu_id=-1, grow_policy='depthwise',
                                   importance_type=None, interaction_constraints='',
                                   learning_rate=0.9500000000000001, max_bin=256,
                                   max_cat_to_onehot=4, max_delta_step=0,
                                   max_depth=4, max_leaves=0, min_child_weight=1,
                                   missing=nan, monotone_constraints='()',
                                   n_estimators=100, n_jobs=0, num_parallel_tree=1,
                                   predictor='auto', random_state=0, reg_alpha=0,
                                   reg_lambda=1, ...))])
```