---
layout: post
title: "Extreme Gradient Boosting with XGBoost"
date: 2025-01-20 07:00:00 +0700
categories: machine learning in python
---

XGBoost (Extreme Gradient Boosting) là một thuật toán *gradient boosting* (tăng cường gradient) được tối ưu hóa về tốc độ và hiệu suất. Nó được phát triển bởi Tianqi Chen và được sử dụng rộng rãi trong các cuộc thi học máy (như Kaggle) nhờ khả năng đạt độ chính xác cao.

## Classification with XGBoost

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C1.pdf)

### Introducing XGBoost

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


### When should I use XGBoost?


---
## Regression with XGBoost

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C2.pdf)

### Regression review

### Objective (loss) functions and base learners

### Regularization and base learners in XGBoost

---
## Fine-tuning your XGBoost model

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C3.pdf)

### Why tune your model?

### Overview of XGBoost's hyperparameters

### Review of grid search and random search

### Limits of grid search and random search


---
## Using XGBoost in pipelines

[Slide]({{site.baseurl}}/files/Extreme_Gradient_Boosting_with_XGBoost_C4.pdf)

### Review of pipelines using sklearn

### Incorporating XGBoost into pipelines

### Tuning XGBoost hyperparameters
