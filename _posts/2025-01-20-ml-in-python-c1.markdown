---
layout: post
title: "Suppervised Learning with scikit-learn"
date: 2025-01-20 00:00:00 +0700
categories: machine learning in python
---

### Table of contents

1. [Classification](#Classification)
2. [Regression](#Regression)
	* 2.1. [Regularized regression](#Regularizedregression)
3. [Fine-Tuning Your Model](#Fine-TuningYourModel)
	* 3.1. [Đánh giá mô hình Machine Learning (Evaluating Machine Learning Model)](#nhgimhnhMachineLearningEvaluatingMachineLearningModel)
	* 3.2. [Phân tích hiệu quả mô hình phân loại (Analyzing Classification Model Performance)](#PhntchhiuqumhnhphnloiAnalyzingClassificationModelPerformance)
	* 3.3. [Tối ưu hóa mô hình (Optimizing Models)](#TiuhamhnhOptimizingModels)
	* 3.4. [ Logistic Regression: Mô hình phân loại "đa năng"](#LogisticRegression:Mhnhphnloianng)
4. [Preprocessing and Pipelines](#PreprocessingandPipelines)
	* 4.1. [Xử lý dữ liệu thiếu (Impute missing values)](#XldliuthiuImputemissingvalues)
	* 4.2. [Chuyển đổi dữ liệu phân loại (Convert categorical data)](#ChuynidliuphnloiConvertcategoricaldata)
	* 4.3. [Chuẩn hóa dữ liệu (Scale data)](#ChunhadliuScaledata)
	* 4.4. [Đánh giá nhiều mô hình (Evaluate multiple models)](#nhginhiumhnhEvaluatemultiplemodels)
	* 4.5. [Xây dựng pipeline (Build pipelines)](#XydngpipelineBuildpipelines)
	* 4.6. [Example: Preprocessing data](#Example:Preprocessingdata)
	* 4.7. [Example: Handling missing data](#Example:Handlingmissingdata)
	* 4.8. [Example: Centering and Scaling](#Example:CenteringandScaling)
	* 4.9. [Example: Evaluating multiple models](#Example:Evaluatingmultiplemodels)


###  1. <a name='Classification'></a>Classification

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
###  2. <a name='Regression'></a>Regression

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

####  2.1. <a name='Regularizedregression'></a>Regularized regression

**1. Giới thiệu**

Trong học máy, mục tiêu của chúng ta thường là tìm mô hình dự đoán tốt nhất cho dữ liệu. Tuy nhiên, đôi khi mô hình quá phức tạp, dẫn đến hiện tượng overfitting (quá khớp). Overfitting xảy ra khi mô hình học quá tốt trên tập huấn luyện, đến mức nó ghi nhớ cả nhiễu và không khái quát hóa tốt cho dữ liệu mới.

Để giải quyết overfitting, chúng ta có thể sử dụng các kỹ thuật regularization (chính quy hóa). Ridge và Lasso regularization là hai kỹ thuật phổ biến giúp ngăn chặn overfitting bằng cách thêm một penalty term vào hàm mất mát.

**2. Ridge Regularization**

Ridge regularization thêm penalty term là tổng bình phương của các hệ số vào hàm mất mát. Điều này buộc mô hình giảm giá trị của các hệ số, làm cho mô hình đơn giản hơn và ít bị overfitting hơn.

**Công thức:**

Hàm mất mát với Ridge regularization:  Loss function + λ * Σ(β<sub>j</sub><sup>2</sup>)

Trong đó:

*  Loss function: Hàm mất mát ban đầu (ví dụ: Mean Squared Error)
*  λ: Tham số điều chỉnh mức độ regularization. λ càng lớn, penalty càng mạnh.
*  β<sub>j</sub>: Hệ số của biến thứ j

**Ưu điểm:**

* Giảm overfitting hiệu quả.
* Hoạt động tốt khi có nhiều biến tương quan với nhau.

**Nhược điểm:**

* Không loại bỏ hoàn toàn các biến không quan trọng, chỉ làm giảm giá trị của chúng.

**3. Lasso Regularization**

Lasso regularization thêm penalty term là tổng giá trị tuyệt đối của các hệ số vào hàm mất mát. Điều này buộc một số hệ số về bằng 0, hiệu quả loại bỏ các biến không quan trọng khỏi mô hình.

**Công thức:**

Hàm mất mát với Lasso regularization: Loss function + λ * Σ(\|β<sub>j</sub>\|)

Trong đó:

*  Loss function: Hàm mất mát ban đầu
*  λ: Tham số điều chỉnh mức độ regularization
*  β<sub>j</sub>: Hệ số của biến thứ j

**Ưu điểm:**

* Giảm overfitting hiệu quả.
* Thực hiện feature selection (lựa chọn đặc trưng) bằng cách loại bỏ các biến không quan trọng.

**Nhược điểm:**

* Có thể hoạt động kém khi có nhiều biến tương quan với nhau.
* Có thể loại bỏ một số biến quan trọng nếu λ quá lớn.

**4. So sánh Ridge và Lasso**

| Đặc điểm | Ridge | Lasso |
|---|---|---|
| Penalty term | Tổng bình phương hệ số | Tổng giá trị tuyệt đối hệ số |
| Tác động lên hệ số | Giảm giá trị hệ số | Buộc một số hệ số về 0 |
| Feature selection | Không | Có |
| Ưu điểm | Xử lý tốt biến tương quan | Loại bỏ biến không quan trọng |
| Nhược điểm | Không loại bỏ hoàn toàn biến | Có thể loại bỏ biến quan trọng |


**5. Trường hợp sử dụng**

* **Ridge:** Thích hợp khi có nhiều biến dự đoán và chúng có thể tương quan với nhau.
* **Lasso:** Thích hợp khi cần lựa chọn các biến quan trọng nhất trong mô hình, đặc biệt khi có nhiều biến không cần thiết.

**6. Ví dụ minh họa**

Giả sử chúng ta đang xây dựng mô hình dự đoán giá nhà dựa trên các biến như diện tích, số phòng ngủ, khoảng cách đến trung tâm thành phố, ...

* Nếu chúng ta sử dụng **Ridge regularization**, mô hình sẽ giảm giá trị của các hệ số tương ứng với các biến ít quan trọng (ví dụ: màu sơn tường). 
* Nếu chúng ta sử dụng **Lasso regularization**, mô hình có thể loại bỏ hoàn toàn các biến không quan trọng (ví dụ: số lượng cây trong vườn).

**7. Kết luận**

Cả Ridge và Lasso regularization đều là những kỹ thuật hữu ích để ngăn chặn overfitting trong học máy. Việc lựa chọn phương pháp nào phụ thuộc vào đặc điểm của dữ liệu và mục tiêu của mô hình.

**Example: Ridge**

```python
# Import Ridge
from sklearn.linear_model import Ridge
alphas = [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
ridge_scores = []
for alpha in alphas:
  
  # Create a Ridge regression model
  ridge = Ridge(alpha=alpha)
  
  # Fit the data
  ridge.fit(X_train, y_train)
  
  # Obtain R-squared
  score = ridge.score(X_test, y_test)
  ridge_scores.append(score)
print(ridge_scores)

```

**Example: Lasso regression for feature importance**

```python
# Import Lasso
from sklearn.linear_model import Lasso

# Instantiate a lasso regression model
lasso = Lasso(alpha=0.3)

# Fit the model to the data
lasso.fit(X, y)

# Compute and print the coefficients
lasso_coef = lasso.coef_
print(lasso_coef)
plt.bar(sales_columns, lasso_coef)
plt.xticks(rotation=45)
plt.show()
```

###  3. <a name='Fine-TuningYourModel'></a>Fine-Tuning Your Model

Để hiểu rõ hiệu quả của một mô hình Machine Learning, chúng ta cần **đánh giá (evaluate)** nó. Giống như việc chấm điểm bài kiểm tra, chúng ta cần các **thước đo (metrics)** để xem mô hình hoạt động tốt ra sao.

####  3.1. <a name='nhgimhnhMachineLearningEvaluatingMachineLearningModel'></a>Đánh giá mô hình Machine Learning (Evaluating Machine Learning Model)

Tưởng tượng bạn huấn luyện một mô hình để phân loại ảnh mèo và chó. Làm sao biết mô hình "học" tốt đến đâu? 

Chúng ta dùng các **thước đo (metrics)** như **độ chính xác (accuracy)**: tỷ lệ ảnh được phân loại đúng. 

Tuy nhiên, độ chính xác đôi khi chưa đủ. Nếu có rất ít ảnh mèo, mô hình luôn đoán "chó" vẫn có thể đạt độ chính xác cao nhưng lại phân loại sai hết ảnh mèo. Vì vậy, ta cần thêm các thước đo khác như:

* **Precision**: Trong số ảnh được dự đoán là mèo, có bao nhiêu ảnh thực sự là mèo?
* **Recall**: Trong số ảnh thực sự là mèo, mô hình dự đoán đúng bao nhiêu ảnh?
* **F1-score**: Kết hợp precision và recall để đánh giá tổng thể.

Để dễ hình dung, ta dùng **ma trận nhầm lẫn (confusion matrix)**:

![](https://glassboxmedicine.com/wp-content/uploads/2019/02/confusion-matrix.png?w=816)

Ma trận này cho thấy số lượng dự đoán đúng và sai của từng loại. Từ đó, ta tính được các metrics trên. **Scikit-learn** là một thư viện Python cung cấp các hàm tính toán các metrics này một cách dễ dàng.

####  3.2. <a name='PhntchhiuqumhnhphnloiAnalyzingClassificationModelPerformance'></a>Phân tích hiệu quả mô hình phân loại (Analyzing Classification Model Performance)

Ngoài các metrics, ta có thể dùng **đường cong ROC (Receiver Operating Characteristic curve)** và **AUC (Area Under the Curve)** để phân tích mô hình.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Roc_curve.svg/220px-Roc_curve.svg.png)

Đường cong ROC biểu diễn mối quan hệ giữa **tỷ lệ dương tính thật (True Positive Rate)** và **tỷ lệ dương tính giả (False Positive Rate)**. AUC là diện tích dưới đường cong ROC, càng gần 1 thì mô hình càng tốt.

####  3.3. <a name='TiuhamhnhOptimizingModels'></a>Tối ưu hóa mô hình (Optimizing Models)

Giống như việc điều chỉnh các nút vặn trên radio để bắt sóng tốt nhất, ta cần **tối ưu hóa (optimize)** mô hình bằng cách điều chỉnh các **siêu tham số (hyperparameters)**. 

Ví dụ, với mô hình cây quyết định, siêu tham số có thể là độ sâu tối đa của cây. Ta có thể thử nghiệm nhiều giá trị khác nhau để tìm ra giá trị tốt nhất.

**Scikit-learn** cung cấp các công cụ như **GridSearchCV** và **RandomizedSearchCV** để tự động tìm kiếm siêu tham số tối ưu.

Tóm lại, việc đánh giá, phân tích và tối ưu hóa mô hình là các bước quan trọng để đảm bảo mô hình hoạt động hiệu quả và đáng tin cậy.

**Example: confusion_matrix, classification_report**
```python
# Import confusion matrix
from sklearn.metrics import confusion_matrix, classification_report

knn = KNeighborsClassifier(n_neighbors=6)

# Fit the model to the training data
knn.fit(X_train, y_train)

# Predict the labels of the test data: y_pred
y_pred = knn.predict(X_test)

# Generate the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

```

####  3.4. <a name='LogisticRegression:Mhnhphnloianng'></a> Logistic Regression: Mô hình phân loại "đa năng"

Logistic Regression (Hồi quy Logistic) là một thuật toán mạnh mẽ trong học máy, được sử dụng rộng rãi cho các bài toán **phân loại (classification)**. Mặc dù có tên gọi là "hồi quy", nhưng thực chất nó lại được dùng để dự đoán **xác suất** một đối tượng thuộc về một lớp nào đó.

**Hoạt động của Logistic Regression**

Hãy tưởng tượng bạn muốn dự đoán liệu một email có phải là spam hay không. Logistic Regression sẽ phân tích các đặc trưng của email (ví dụ: nội dung, người gửi,...) và đưa ra một xác suất từ 0 đến 1. Nếu xác suất cao hơn một ngưỡng nào đó (ví dụ: 0.5), email sẽ được phân loại là spam.

Để làm được điều này, Logistic Regression sử dụng **hàm sigmoid**. Hàm sigmoid có dạng hình chữ "S", nhận đầu vào là một giá trị bất kỳ và  biến đổi nó thành một giá trị nằm trong khoảng từ 0 đến 1. 

![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Logistic-curve.svg/220px-Logistic-curve.svg.png)

Giá trị đầu ra của hàm sigmoid được hiểu là xác suất. Ví dụ, nếu hàm sigmoid trả về giá trị 0.8, có nghĩa là mô hình dự đoán email có 80% khả năng là spam.

**Ưu điểm của Logistic Regression**

* **Đơn giản và dễ hiểu**: Logistic Regression là một mô hình tương đối đơn giản, dễ dàng triển khai và diễn giải.
* **Hiệu quả**: Logistic Regression hoạt động tốt trên nhiều bài toán phân loại, đặc biệt là các bài toán phân loại nhị phân (hai lớp).
* **Diễn giải được**: Ta có thể hiểu được tầm quan trọng của từng đặc trưng bằng cách xem xét hệ số của chúng trong mô hình.

**Ứng dụng của Logistic Regression**

Logistic Regression được ứng dụng trong nhiều lĩnh vực, bao gồm:

* **Nhận dạng hình ảnh**: Phân loại ảnh (ví dụ: mèo/chó, xe hơi/xe máy).
* **Xử lý ngôn ngữ tự nhiên**: Phân loại văn bản (ví dụ: spam/không spam, tích cực/tiêu cực).
* **Y tế**: Dự đoán bệnh (ví dụ: ung thư/không ung thư).
* **Tài chính**: Đánh giá rủi ro tín dụng.
* **Marketing**: Dự đoán khả năng khách hàng mua hàng.

**Ví dụ minh họa**

Giả sử bạn muốn xây dựng mô hình dự đoán liệu một khách hàng có nhấp vào quảng cáo hay không. Bạn có thể sử dụng Logistic Regression với các đặc trưng như tuổi, giới tính, sở thích của khách hàng. Mô hình sẽ phân tích các đặc trưng này và đưa ra xác suất khách hàng nhấp vào quảng cáo.

**Tóm lại**, Logistic Regression là một mô hình phân loại linh hoạt và hiệu quả, được ứng dụng rộng rãi trong nhiều lĩnh vực. Nó là một công cụ mạnh mẽ cho bất kỳ ai muốn khám phá thế giới của học máy.

**Example:**

- Building a logistic regression model

```python
# Import LogisticRegression
from sklearn.linear_model import LogisticRegression

# Instantiate the model
logreg = LogisticRegression()

# Fit the model
logreg.fit(X_train, y_train)

# Predict probabilities
y_pred_probs = logreg.predict_proba(X_test)[:, 1]

print(y_pred_probs[:10])
```

- The ROC curve

```python
# Import roc_curve
from sklearn.metrics import roc_curve

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_probs)

plt.plot([0, 1], [0, 1], 'k--')

# Plot tpr against fpr
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Diabetes Prediction')
plt.show()
```

- ROC AUC

```python
# Import roc_auc_score
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

# Calculate roc_auc_score
print(roc_auc_score(y_test, y_pred_probs))

# Calculate the confusion matrix
print(confusion_matrix(y_test, y_pred))

# Calculate the classification report
print(classification_report(y_test, y_pred))
```

- `GridSearchCV`

```python
# Import GridSearchCV
from sklearn.model_selection import GridSearchCV

# Set up the parameter grid
# create 20 evenly spaced values ranging from 0.00001 to 1.
param_grid = {"alpha": np.linspace(0.00001, 1, 20)}

# Instantiate lasso_cv
lasso_cv = GridSearchCV(lasso, param_grid, cv=kf)

# Fit to the training data
lasso_cv.fit(X_train, y_train)
print("Tuned lasso paramaters: {}".format(lasso_cv.best_params_))
print("Tuned lasso score: {}".format(lasso_cv.best_score_))
```

- `RandomizedSearchCV`

```python
# Create the parameter space
params = {"penalty": ["l1", "l2"],
         "tol": np.linspace(0.0001, 1.0, 50),
         "C": np.linspace(0.1, 1.0, 50),
         "class_weight": ["balanced", {0:0.8, 1:0.2}]}

# Instantiate the RandomizedSearchCV object
logreg_cv = RandomizedSearchCV(logreg, params, cv=kf)

# Fit the data to the model
logreg_cv.fit(X_train, y_train)

# Print the tuned parameters and score
print("Tuned Logistic Regression Parameters: {}".format(logreg_cv.best_params_))
print("Tuned Logistic Regression Best Accuracy Score: {}".format(logreg_cv.best_score_))
```

###  4. <a name='PreprocessingandPipelines'></a>Preprocessing and Pipelines

Trước khi huấn luyện mô hình Machine Learning, chúng ta cần **tiền xử lý dữ liệu (preprocess data)**. Hãy tưởng tượng dữ liệu như những nguyên liệu thô, cần được sơ chế và chuẩn bị trước khi "nấu" thành món ăn (mô hình).

####  4.1. <a name='XldliuthiuImputemissingvalues'></a>Xử lý dữ liệu thiếu (Impute missing values)

Dữ liệu thực tế thường có **giá trị thiếu (missing values)**, giống như những chỗ trống trong bảng dữ liệu. Ta cần "lấp đầy" những chỗ trống này để mô hình hoạt động hiệu quả.

Một số phương pháp phổ biến:

* **Thay thế bằng giá trị trung bình/trung vị (Mean/Median imputation)**: Điền vào chỗ trống bằng giá trị trung bình hoặc trung vị của cột dữ liệu.
* **Thay thế bằng KNN (K-Nearest Neighbors imputation)**: Dựa vào các điểm dữ liệu gần nhất để dự đoán giá trị thiếu.

Ví dụ: Nếu cột "tuổi" có giá trị thiếu, ta có thể thay thế bằng tuổi trung bình của những người có đặc điểm tương đồng.

####  4.2. <a name='ChuynidliuphnloiConvertcategoricaldata'></a>Chuyển đổi dữ liệu phân loại (Convert categorical data)

**Dữ liệu phân loại (categorical data)** là dữ liệu dạng nhãn, ví dụ: màu sắc (đỏ, xanh, vàng), giới tính (nam, nữ). Mô hình Machine Learning thường yêu cầu dữ liệu dạng số, nên ta cần chuyển đổi dữ liệu phân loại.

Một số phương pháp phổ biến:

* **One-hot encoding**: Tạo các cột mới, mỗi cột đại diện cho một giá trị của biến phân loại. 
* **Label encoding**: Gán mỗi giá trị của biến phân loại một số nguyên.

Ví dụ: Biến "màu sắc" có thể được chuyển đổi thành ba cột mới: "đỏ", "xanh", "vàng".

####  4.3. <a name='ChunhadliuScaledata'></a>Chuẩn hóa dữ liệu (Scale data)

Các biến trong dữ liệu có thể có **thang đo (scale)** khác nhau, ví dụ: tuổi (0-100) và thu nhập (hàng triệu đồng). **Chuẩn hóa dữ liệu (data scaling)** giúp đưa các biến về cùng một thang đo, tránh trường hợp biến có giá trị lớn hơn chi phối mô hình.

Một số phương pháp phổ biến:

* **Standardization**: Biến đổi dữ liệu sao cho có trung bình bằng 0 và độ lệch chuẩn bằng 1.
* **Normalization**: Biến đổi dữ liệu về khoảng giá trị từ 0 đến 1.

####  4.4. <a name='nhginhiumhnhEvaluatemultiplemodels'></a>Đánh giá nhiều mô hình (Evaluate multiple models)

Để chọn ra mô hình tốt nhất, ta cần so sánh hiệu quả của nhiều mô hình **học có giám sát (supervised learning)** khác nhau, ví dụ: **Logistic Regression, Decision Tree, Support Vector Machine**.

Ta có thể sử dụng các **thước đo (metrics)** như **độ chính xác (accuracy), precision, recall, F1-score** để đánh giá và so sánh các mô hình.

####  4.5. <a name='XydngpipelineBuildpipelines'></a>Xây dựng pipeline (Build pipelines)

**Pipeline** giúp kết hợp các bước tiền xử lý dữ liệu và huấn luyện mô hình thành một quy trình duy nhất. Điều này giúp đơn giản hóa code và tránh lỗi.

Ví dụ: Một pipeline có thể bao gồm các bước: impute missing values -> convert categorical data -> scale data -> train Logistic Regression model.

**Scikit-learn** cung cấp các công cụ mạnh mẽ để xây dựng pipeline.

**Tóm lại**, tiền xử lý dữ liệu và đánh giá mô hình là những bước quan trọng trong quy trình Machine Learning. Bằng cách áp dụng các kỹ thuật này, ta có thể xây dựng mô hình hiệu quả và đáng tin cậy hơn.

####  4.6. <a name='Example:Preprocessingdata'></a>Example: Preprocessing data

- Creating dummy variables

```python
# Create music_dummies
music_dummies = pd.get_dummies(music_df, drop_first=True)

# Print the new DataFrame's shape
print("Shape of music_dummies: {}".format(music_dummies.shape))
```

- Regression with categorical features

```python
# Create X and y
X = music_dummies.drop("popularity", axis=1).values
y = music_dummies["popularity"].values

# Instantiate a ridge model
ridge = Ridge(alpha=0.2)

# Perform cross-validation
scores = cross_val_score(ridge, X, y, cv=kf, scoring="neg_mean_squared_error")

# Calculate RMSE
rmse = np.sqrt(scores*-1)
print("Average RMSE: {}".format(np.mean(rmse)))
print("Standard Deviation of the target array: {}".format(np.std(y)))
```

####  4.7. <a name='Example:Handlingmissingdata'></a>Example: Handling missing data

- Dropping missing data

```python
# Print missing values for each column
print(music_df.isna().sum().sort_values())

# Remove values where less than 5% are missing
music_df = music_df.dropna(subset=["genre", "popularity", "loudness", "liveness", "tempo"])

# Convert genre to a binary feature
music_df["genre"] = np.where(music_df["genre"] == "Rock", 1, 0)

print(music_df.isna().sum().sort_values())
print("Shape of the `music_df`: {}".format(music_df.shape))
```

- Pipeline 

```python
# Import modules
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Instantiate an imputer
imputer = SimpleImputer()

# Instantiate a knn model
knn = KNeighborsClassifier(n_neighbors=3)

# Build steps for the pipeline
steps = [("imputer", imputer), 
         ("knn", knn)]

# Create the pipeline
pipeline = Pipeline(steps)

# Fit the pipeline to the training data
pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = pipeline.predict(X_test)

# Print the confusion matrix
print(confusion_matrix(y_test, y_pred))

```

####  4.8. <a name='Example:CenteringandScaling'></a>Example: Centering and Scaling

- Centering and scaling for regression

```python
# Import StandardScaler
from sklearn.preprocessing import StandardScaler

# Create pipeline steps
steps = [("scaler", StandardScaler()),
         ("lasso", Lasso(alpha=0.5))]

# Instantiate the pipeline
pipeline = Pipeline(steps)
pipeline.fit(X_train, y_train)

# Calculate and print R-squared
print(pipeline.score(X_test, y_test)) #0.6193523316282489
```

- Centering and scaling for classification

```python
# Build the steps
steps = [("scaler", StandardScaler()),
         ("logreg", LogisticRegression())]
pipeline = Pipeline(steps)

# Create the parameter space
parameters = {"logreg__C": np.linspace(0.001, 1.0, 20)}
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=21)

# Instantiate the grid search object
cv = GridSearchCV(pipeline, param_grid=parameters)

# Fit to the training data
cv.fit(X_train, y_train)
print(cv.best_score_, "\n", cv.best_params_)

```

####  4.9. <a name='Example:Evaluatingmultiplemodels'></a>Example: Evaluating multiple models

- Visualizing regression model performance

```python
models = {"Linear Regression": LinearRegression(), "Ridge": Ridge(alpha=0.1), "Lasso": Lasso(alpha=0.1)}
results = []

# Loop through the models' values
for model in models.values():
  kf = KFold(n_splits=6, random_state=42, shuffle=True)
  
  # Perform cross-validation
  cv_scores = cross_val_score(model, X_train, y_train, cv=kf)
  
  # Append the results
  results.append(cv_scores)

# Create a box plot of the results
plt.boxplot(results, labels=models.keys())
plt.show()
```

- Predicting on the test set

```python
# Import mean_squared_error
from sklearn.metrics import mean_squared_error

for name, model in models.items():
  
  # Fit the model to the training data
  model.fit(X_train_scaled, y_train)
  
  # Make predictions on the test set
  y_pred = model.predict(X_test_scaled)
  
  # Calculate the test_rmse
  test_rmse = mean_squared_error(y_test, y_pred, squared=False)
  print("{} Test Set RMSE: {}".format(name, test_rmse))
```

- Visualizing classification model performance

```python
# Create models dictionary
models = {"Logistic Regression": LogisticRegression(), "KNN": KNeighborsClassifier(), "Decision Tree Classifier": DecisionTreeClassifier()}
results = []

# Loop through the models' values
for model in models.values():
  
  # Instantiate a KFold object
  kf = KFold(n_splits=6, random_state=12, shuffle=True)
  
  # Perform cross-validation
  cv_results = cross_val_score(model, X_train_scaled, y_train, cv=kf)
  results.append(cv_results)
plt.boxplot(results, labels=models.keys())
plt.show()
```

- Pipeline for predicting song popularity

```python
# Create steps
steps = [("imp_mean", SimpleImputer()), 
         ("scaler", StandardScaler()), 
         ("logreg", LogisticRegression())]

# Set up pipeline
pipeline = Pipeline(steps)
params = {"logreg__solver": ["newton-cg", "saga", "lbfgs"],
         "logreg__C": np.linspace(0.001, 1.0, 10)}

# Create the GridSearchCV object
tuning = GridSearchCV(pipeline, param_grid=params)
tuning.fit(X_train, y_train)
y_pred = tuning.predict(X_test)

# Compute and print performance
print("Tuned Logistic Regression Parameters: {}, Accuracy: {}".format(tuning.best_params_, tuning.score(X_test, y_test)))
```