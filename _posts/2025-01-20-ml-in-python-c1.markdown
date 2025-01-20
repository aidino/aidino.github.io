---
layout: post
title: "Suppervised Learning with scikit-learn"
date: 2025-01-20 00:00:00 +0700
categories: machine learning in python
---

### Classification

Hãy tưởng tượng bạn là một người nông dân trồng táo và cam. Bạn muốn tạo ra một hệ thống tự động giúp phân loại quả khi thu hoạch. Đây chính là một **classification problem** (bài toán phân loại), và chúng ta có thể giải quyết nó bằng **supervised learning** (học có giám sát).

**1. Thu thập và chuẩn bị dữ liệu:**

Đầu tiên, bạn cần thu thập dữ liệu về táo và cam, ví dụ như:
    - **Màu sắc (Color):** Đỏ, cam, xanh
    - **Hình dạng (Shape):** Tròn, dài
    - **Kích thước (Size):** Nhỏ, vừa, lớn

Dựa trên kinh nghiệm, bạn biết rằng táo thường có màu đỏ, hình tròn, kích thước vừa phải, trong khi cam thường có màu cam, hình tròn và kích thước lớn hơn. Đây chính là **nhãn (label)** cho mỗi loại quả.

**2. Chia dữ liệu thành tập huấn luyện (training set) và tập kiểm tra (test set):**

Bạn sẽ sử dụng phần lớn dữ liệu (ví dụ 80%) để **huấn luyện (train)** mô hình, phần còn lại (20%) để **kiểm tra (test)** hiệu quả của mô hình. Việc này giống như việc bạn dạy cho mô hình cách phân biệt táo và cam dựa trên tập huấn luyện, sau đó kiểm tra xem nó học được tốt như thế nào trên tập kiểm tra.

**3. Xây dựng và huấn luyện mô hình:**

Giả sử bạn chọn **Decision Tree** (cây quyết định) làm mô hình. Mô hình này sẽ học cách phân loại quả dựa trên các quy tắc đơn giản, ví dụ:

- Nếu màu sắc là đỏ thì có khả năng cao là táo.
- Nếu màu sắc là cam và kích thước lớn thì có khả năng cao là cam.

Quá trình huấn luyện mô hình chính là quá trình tìm ra các quy tắc này từ dữ liệu huấn luyện.

**4. Dự đoán và đánh giá:**

Sau khi huấn luyện xong, bạn có thể sử dụng mô hình để **dự đoán (predict)** nhãn cho các quả mới. Ví dụ, nếu bạn đưa vào một quả có màu cam, hình tròn và kích thước lớn, mô hình sẽ dự đoán đó là cam.

Để đánh giá hiệu quả của mô hình, bạn so sánh nhãn dự đoán với nhãn thực tế trong tập kiểm tra. Các chỉ số thường được sử dụng là **accuracy** (độ chính xác), **precision** (độ chuẩn xác), **recall** (độ phủ).

**5. Độ phức tạp của mô hình (Model Complexity) và hiệu suất (Performance):**

Độ phức tạp của mô hình liên quan đến số lượng quy tắc và độ phức tạp của các quy tắc đó. Mô hình quá đơn giản có thể không đủ khả năng học được các đặc trưng quan trọng, dẫn đến **underfitting** (kém khớp). Ngược lại, mô hình quá phức tạp có thể học thuộc lòng dữ liệu huấn luyện, dẫn đến **overfitting** (quá khớp) và kém hiệu quả trên dữ liệu mới.

**Ví dụ:**

- **Mô hình đơn giản:** Chỉ dựa trên màu sắc để phân loại. Mô hình này có thể phân loại sai những quả cam có màu xanh.
- **Mô hình phức tạp:** Dựa trên rất nhiều đặc trưng, bao gồm cả những đặc trưng không liên quan như trọng lượng của cuống quả. Mô hình này có thể hoạt động tốt trên tập huấn luyện nhưng kém hiệu quả trên tập kiểm tra.


**6. Example: k-Nearest Neighbors**

- Train/test split + computing accuracy

```python
# Import the module
from sklearn.model_selection import train_test_split

X = churn_df.drop("churn", axis=1).values
y = churn_df["churn"].values

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
knn = KNeighborsClassifier(n_neighbors=5)

# Fit the classifier to the training data
knn.fit(X_train, y_train)

# Print the accuracy
print(knn.score(X_test, y_test))
```
- Overfitting and underfitting

```python
# Create neighbors
neighbors = np.arange(1, 13)
train_accuracies = {}
test_accuracies = {}

for neighbor in neighbors:
  
	# Set up a KNN Classifier
	knn = KNeighborsClassifier(n_neighbors=neighbor)
  
	# Fit the model
	knn.fit(X_train, y_train)
  
	# Compute accuracy
	train_accuracies[neighbor] = knn.score(X_train, y_train)
	test_accuracies[neighbor] = knn.score(X_test, y_test)
print(neighbors, '\n', train_accuracies, '\n', test_accuracies)
```

- Visualizing model complexity

```python
# Add a title
plt.title("KNN: Varying Number of Neighbors")

# Plot training accuracies
plt.plot(train_accuracies.keys(), train_accuracies.values(), label="Training Accuracy")

# Plot test accuracies
plt.plot(test_accuracies.keys(), test_accuracies.values(), label="Testing Accuracy")

plt.legend()
plt.xlabel("Number of Neighbors")
plt.ylabel("Accuracy")

# Display the plot
plt.show()
```

---
### Regression

Bạn là chủ một doanh nghiệp và muốn biết liệu việc chi tiêu cho quảng cáo (**advertising expenditure**) có thực sự hiệu quả trong việc tăng doanh số (**sales values**) hay không. Đây là lúc **hồi quy (regression)** trong học máy phát huy tác dụng. Cụ thể, chúng ta sẽ sử dụng **hồi quy tuyến tính (linear regression)** để xây dựng mô hình dự đoán doanh số dựa trên chi phí quảng cáo.

**1. Dữ liệu và mô hình:**

Giả sử bạn có dữ liệu về chi phí quảng cáo và doanh số tương ứng trong quá khứ. Mô hình hồi quy tuyến tính sẽ tìm kiếm một mối quan hệ tuyến tính giữa hai đại lượng này, có dạng:

  **Doanh số = a * Chi phí quảng cáo + b**

Trong đó, **a** và **b** là các hệ số mà mô hình cần tìm ra sao cho phù hợp nhất với dữ liệu. 

**Ví dụ:** Nếu a = 2 và b = 100, nghĩa là cứ mỗi đồng chi cho quảng cáo, doanh số tăng thêm 2 đồng, và ngay cả khi không quảng cáo, doanh số vẫn đạt 100 đồng.

**2. Đánh giá mô hình:**

Để đánh giá mô hình, chúng ta sử dụng các chỉ số như:

- **R-squared (R bình phương):** Đo lường tỷ lệ biến động của doanh số được giải thích bởi mô hình. R-squared càng cao (tối đa là 1), mô hình càng tốt.
- **Root Mean Squared Error (RMSE - Sai số bình phương trung bình căn bậc hai):** Đo lường mức độ sai lệch giữa doanh số dự đoán và doanh số thực tế. RMSE càng thấp, mô hình càng chính xác.

**3. K-fold cross-validation:**

Để đảm bảo mô hình không bị **overfitting** (quá khớp) với dữ liệu hiện có, chúng ta sử dụng kỹ thuật **k-fold cross-validation**. 

**Ví dụ:** Với 5-fold cross-validation, dữ liệu được chia thành 5 phần bằng nhau. Mô hình được huấn luyện 5 lần, mỗi lần sử dụng 4 phần để huấn luyện và 1 phần để kiểm tra. Kết quả cuối cùng là trung bình của 5 lần đánh giá.

**4. Regularization (Chính quy hóa):**

**Regularization** là một kỹ thuật giúp ngăn chặn overfitting bằng cách thêm vào mô hình một "hình phạt" cho các hệ số lớn. Điều này khuyến khích mô hình tìm ra các mối quan hệ đơn giản hơn, từ đó tăng khả năng tổng quát hóa cho dữ liệu mới.

**Example: Creating feature**

```python
import numpy as np

# Create X from the radio column's values
X = sales_df['radio'].values

# Create y from the sales column's values
y = sales_df['sales'].values

# Reshape X
X = X.reshape(-1, 1)

# Check the shape of the features and targets
print(X.shape, y.shape)
```

**Example: Building a linear regression model**

```python
# Import LinearRegression
from sklearn.linear_model import LinearRegression

# Create the model
reg = LinearRegression()

# Fit the model to the data
reg.fit(X, y)

# Make predictions
predictions = reg.predict(X)

print(predictions[:5])
```

**Example: Visualizing a linear regression model**

```python
# Import matplotlib.pyplot
import matplotlib.pyplot as plt

# Create scatter plot
plt.scatter(X, y, color="blue")

# Create line plot
plt.plot(X, predictions, color="red")
plt.xlabel("Radio Expenditure ($)")
plt.ylabel("Sales ($)")

# Display the plot
plt.show()
```

**Example: Fit and predict for regression**

```python
# Create X and y arrays
X = sales_df.drop("sales", axis=1).values
y = sales_df["sales"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Instantiate the model
reg = LinearRegression()

# Fit the model to the data
reg.fit(X_train, y_train)

# Make predictions
y_pred = reg.predict(X_test)
print("Predictions: {}, Actual Values: {}".format(y_pred[:2], y_test[:2]))
```

**Example: Regression performance**

```python
# Import mean_squared_error
from sklearn.metrics import mean_squared_error

# Compute R-squared
r_squared = reg.score(X_test, y_test)

# Compute RMSE
rmse = mean_squared_error(y_test, y_pred, squared=False)

# Print the metrics
print("R^2: {}".format(r_squared))
print("RMSE: {}".format(rmse))
```

**Example: Cross-validation for R-squared**

```python
# Import the necessary modules
from sklearn.model_selection import cross_val_score, KFold

# Create a KFold object
kf = KFold(n_splits=6, shuffle=True, random_state=5)

reg = LinearRegression()

# Compute 6-fold cross-validation scores
cv_scores = cross_val_score(reg, X, y, cv=kf)

# Print scores
print(cv_scores)
```

**Example: Analyzing cross-validation metrics**
```python
# Print the mean
print(np.mean(cv_results))

# Print the standard deviation
print(np.std(cv_results))

# Print the 95% confidence interval
print(np.quantile(cv_results, [0.025, 0.975]))
```

#### Regularized regression

Để hiểu rõ hơn về cách thức hoạt động của Ridge và Lasso regression, chúng ta hãy cùng xem xét công thức toán học của chúng với LaTeX markdown.

**1. Hồi quy tuyến tính (Linear Regression):**

Mục tiêu của hồi quy tuyến tính là tìm ra các hệ số  **w = (w<sub>1</sub>, w<sub>2</sub>, ..., w<sub>n</sub>)** sao cho mô hình dự đoán $\hat{y}$ gần với giá trị thực tế $y$ nhất có thể. Hàm mất mát thường được sử dụng là **Mean Squared Error (MSE):**

$$
MSE = \frac{1}{m} \sum_{i=1}^{m} (y_i - \hat{y}_i)^2 
$$

Trong đó:

- $m$ là số lượng điểm dữ liệu
- $y_i$ là giá trị thực tế của điểm dữ liệu thứ $i$
- $\hat{y}_i$ là giá trị dự đoán của điểm dữ liệu thứ $i$, được tính bằng: $\hat{y}_i = w_0 + w_1 x_{i1} + w_2 x_{i2} + ... + w_n x_{in}$

**2. Ridge Regression:**

Ridge regression thêm vào hàm MSE một hình phạt L2, tỷ lệ với bình phương của các hệ số:

```math
Ridge Loss = MSE + \lambda \sum_{j=1}^{n} w_j^2
```

Trong đó:

- $\lambda$ là **tham số chính quy hóa (regularization parameter)**, điều chỉnh mức độ "co lại" của các hệ số. $\lambda$ càng lớn, hình phạt càng mạnh, các hệ số càng bị co lại về gần 0.

**3. Lasso Regression:**

Lasso regression thêm vào hàm MSE một hình phạt L1, tỷ lệ với giá trị tuyệt đối của các hệ số:

```
Lasso Loss = MSE + \lambda \sum_{j=1}^{n} |w_j|
```

**4. Ảnh hưởng của hình phạt:**

- **Ridge regression:** Hình phạt L2 khiến các hệ số bị "co lại" về gần 0, nhưng không hoàn toàn bằng 0. Điều này giúp giảm ảnh hưởng của các biến ít quan trọng, đồng thời giữ lại tất cả các biến trong mô hình.
- **Lasso regression:** Hình phạt L1 có thể khiến một số hệ số bị "triệt tiêu" về 0, từ đó loại bỏ hoàn toàn những biến không quan trọng. Điều này giúp đơn giản hóa mô hình và tăng khả năng diễn giải.

**5. Lựa chọn tham số $\lambda$:**

Tham số $\lambda$ đóng vai trò quan trọng trong việc điều chỉnh mức độ chính quy hóa. Giá trị của $\lambda$ thường được xác định bằng kỹ thuật **cross-validation**, nhằm tìm ra giá trị tối ưu giúp mô hình đạt hiệu quả tốt nhất trên dữ liệu mới.

**Tóm lại:**

Công thức toán học của Ridge và Lasso regression cho thấy rõ sự khác biệt trong cách thức chúng thêm hình phạt vào hàm mất mát. Ridge sử dụng hình phạt L2, co lại các hệ số về gần 0, trong khi Lasso sử dụng hình phạt L1, triệt tiêu một số hệ số về 0. Việc hiểu rõ cơ chế hoạt động này giúp bạn lựa chọn phương pháp phù hợp cho từng bài toán cụ thể.
