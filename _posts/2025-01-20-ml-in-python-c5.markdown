---
layout: post
title: "Linear Classifiers in Python"
date: 2025-01-20 04:00:00 +0700
categories: machine learning in python
---

Learn the details of linear classifiers like logistic regression and SVM.


### Table of contents

1. [Applying logistic regression and SVM](#ApplyinglogisticregressionandSVM)
   * 1.1. [**scikit-learn refresher**](#scikit-learnrefresher)
   * 1.2. [**Applying logistic regression and SVM**](#ApplyinglogisticregressionandSVM-1)
2. [Loss functions](#Lossfunctions)
3. [Logistic regression](#Logisticregression)
   * 3.1. [**Logistic regression and regularization**](#Logisticregressionandregularization)
   * 3.2. [**Logistic regression and probabilities**](#Logisticregressionandprobabilities)
   * 3.3. [**Multi-class logistic regression**](#Multi-classlogisticregression)
   * 3.4. [**Support Vector Machines**](#SupportVectorMachines)
4. [Logistic regression](#Logisticregression-1)

---
###  1. <a name='ApplyinglogisticregressionandSVM'></a>Applying logistic regression and SVM

[Slide]({{site.baseurl}}/files/linears_classifiers_in_python_c1.pdf)

####  1.1. <a name='scikit-learnrefresher'></a>**scikit-learn refresher**

- **KNN classification**

**K-Nearest Neighbors (KNN)** là một thuật toán học máy thuộc nhóm **học có giám sát (supervised learning)**, được sử dụng cho cả bài toán **phân loại (classification)** và **hồi quy (regression)**. Ở đây, chúng ta sẽ tập trung vào KNeighborsClassifier cho bài toán phân loại.

**Ý tưởng chính:**

KNN dựa trên ý tưởng về sự tương đồng giữa các điểm dữ liệu. Giả sử bạn có một tập dữ liệu đã được gán nhãn (training data). Khi bạn muốn phân loại một điểm dữ liệu mới (test data), KNN sẽ tìm ra **K** điểm dữ liệu gần nhất với nó trong tập huấn luyện, và gán cho điểm dữ liệu mới nhãn phổ biến nhất trong số K điểm gần nhất đó.

**Ví dụ:**

Hãy tưởng tượng bạn có một rổ trái cây gồm táo và cam. Bạn muốn phân loại một quả mới vào rổ. KNN sẽ làm như sau:

1. **Tìm K quả gần nhất:** Nó sẽ tìm ra K quả táo hoặc cam gần nhất với quả mới dựa trên các đặc điểm như màu sắc, kích thước, v.v.
2. **Đếm nhãn:** Nó sẽ đếm xem trong K quả gần nhất có bao nhiêu quả là táo, bao nhiêu quả là cam.
3. **Gán nhãn:** Nếu số lượng táo nhiều hơn, quả mới sẽ được phân loại là táo. Ngược lại, nếu số lượng cam nhiều hơn, quả mới sẽ được phân loại là cam.

**KNeighborsClassifier trong scikit-learn:**

Đây là lớp (class) trong thư viện scikit-learn của Python, cung cấp công cụ để sử dụng thuật toán KNN cho bài toán phân loại. Bạn có thể tùy chỉnh các tham số như số lượng hàng xóm (K), cách tính khoảng cách, v.v.

**Ưu điểm của KNN:**

* **Dễ hiểu và dễ cài đặt:** Ý tưởng của KNN rất trực quan và việc triển khai cũng khá đơn giản.
* **Không cần huấn luyện mô hình:** KNN không cần trải qua quá trình huấn luyện phức tạp như các thuật toán khác.
* **Linh hoạt:** Có thể sử dụng cho nhiều loại dữ liệu khác nhau.

**Nhược điểm của KNN:**

* **Tốn kém bộ nhớ:** KNN cần lưu trữ toàn bộ dữ liệu huấn luyện để tính khoảng cách.
* **Chậm:** Việc tìm K điểm gần nhất có thể tốn thời gian, đặc biệt khi dữ liệu lớn.
* **Dễ bị ảnh hưởng bởi nhiễu:** Nếu dữ liệu có nhiều điểm nhiễu, kết quả phân loại có thể bị sai lệch.


```python
from sklearn.neighbors import KNeighborsClassifier

# Create and fit the model
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

# Predict on the test features, print the results
pred = knn.predict(X_test)[0]
print("Prediction for test example 0:", pred)
print("Score:", knn.score(X_test, y_test))
```

####  1.2. <a name='ApplyinglogisticregressionandSVM-1'></a>**Applying logistic regression and SVM**

**Logistic Regression** là một thuật toán học máy thuộc nhóm **học có giám sát (supervised learning)**, được sử dụng cho bài toán **phân loại (classification)**. Mặc dù có tên "regression" (hồi quy), nhưng thực chất đây là một thuật toán phân loại.

**Ý tưởng chính:**

Logistic Regression dự đoán xác suất một điểm dữ liệu thuộc về một lớp nào đó. Ví dụ, trong bài toán phân loại email spam/không spam, Logistic Regression sẽ dự đoán xác suất một email là spam hay không phải spam.

**Cách thức hoạt động:**

1. **Hàm sigmoid:** Logistic Regression sử dụng hàm sigmoid để chuyển đổi kết quả đầu ra của một phương trình tuyến tính thành xác suất trong khoảng từ 0 đến 1.
2. **Phương trình tuyến tính:** Đầu tiên, thuật toán sẽ tính một tổ hợp tuyến tính của các đặc trưng đầu vào, giống như trong Linear Regression:
   z = w0 + w1*x1 + w2*x2 + ... + wn*xn
   Trong đó:
      * z là kết quả tuyến tính
      * w0, w1, ..., wn là các hệ số cần tìm
      * x1, x2, ..., xn là các đặc trưng đầu vào
3. **Chuyển đổi sang xác suất:** Kết quả z được đưa qua hàm sigmoid để chuyển đổi thành xác suất:
   p = 1 / (1 + exp(-z))
   Trong đó:
      * p là xác suất
      * exp là hàm mũ tự nhiên
4. **Phân loại:** Nếu xác suất p lớn hơn một ngưỡng (thường là 0.5), điểm dữ liệu sẽ được phân loại vào lớp dương (ví dụ: email spam). Ngược lại, nếu p nhỏ hơn ngưỡng, điểm dữ liệu sẽ được phân loại vào lớp âm (ví dụ: email không phải spam).

**LogisticRegression trong scikit-learn:**

Đây là lớp (class) trong thư viện scikit-learn của Python, cung cấp công cụ để sử dụng thuật toán Logistic Regression. Bạn có thể tùy chỉnh các tham số như cách tối ưu hóa, регуляризация (L1 hoặc L2), v.v.

**Ưu điểm của Logistic Regression:**

* **Dễ hiểu và dễ cài đặt:** Ý tưởng của Logistic Regression khá đơn giản và việc triển khai cũng không quá phức tạp.
* **Hiệu quả:** Logistic Regression thường cho kết quả tốt trên các tập dữ liệu nhỏ và vừa.
* **Xác suất:** Cho phép dự đoán xác suất thuộc về một lớp, giúp đánh giá mức độ tin cậy của dự đoán.

**Nhược điểm của Logistic Regression:**

* **Giả định tuyến tính:** Logistic Regression giả định rằng các đặc trưng đầu vào có mối quan hệ tuyến tính với nhau. Nếu dữ liệu không thỏa mãn giả định này, hiệu suất có thể giảm.
* **Nhạy cảm với ngoại lệ:** Logistic Regression có thể bị ảnh hưởng bởi các điểm dữ liệu ngoại lệ.

---

**Support Vector Machine (SVM)** là một thuật toán học máy thuộc nhóm **học có giám sát (supervised learning)**, được sử dụng cho bài toán **phân loại (classification)** và **hồi quy (regression)**. Trong bài giải thích này, chúng ta sẽ tập trung vào SVM cho bài toán phân loại.

**Ý tưởng chính:**

SVM tìm một **siêu phẳng (hyperplane)** "tối ưu" để phân chia dữ liệu thành các lớp khác nhau. "Tối ưu" ở đây có nghĩa là siêu phẳng đó có khoảng cách lớn nhất đến các điểm dữ liệu gần nhất của mỗi lớp (margin).

**Cách thức hoạt động:**

1. **Tìm siêu phẳng:** SVM sẽ tìm một siêu phẳng (đường thẳng trong không gian 2D, mặt phẳng trong không gian 3D, v.v.) sao cho khoảng cách từ siêu phẳng đó đến các điểm dữ liệu gần nhất của mỗi lớp là lớn nhất.
2. **Điểm hỗ trợ (support vectors):** Các điểm dữ liệu gần nhất với siêu phẳng được gọi là "điểm hỗ trợ". Chúng đóng vai trò quan trọng trong việc xác định vị trí của siêu phẳng.
3. **Kernel trick:** Trong trường hợp dữ liệu không thể phân tách tuyến tính, SVM sử dụng một kỹ thuật gọi là "kernel trick" để ánh xạ dữ liệu vào một không gian chiều cao hơn, nơi mà nó có thể được phân tách tuyến tính.
4. **Phân loại:** Dựa vào vị trí của một điểm dữ liệu mới so với siêu phẳng, SVM sẽ phân loại điểm đó vào lớp tương ứng.

**Các loại kernel phổ biến:**

* **Linear:** Kernel tuyến tính, được sử dụng khi dữ liệu có thể phân tách tuyến tính.
* **Polynomial:** Kernel đa thức, tạo ra các siêu phẳng phức tạp hơn.
* **RBF (Radial Basis Function):** Kernel Gauss, tạo ra các siêu phẳng linh hoạt và phù hợp với nhiều loại dữ liệu.

**Ưu điểm của SVM:**

* **Hiệu quả:** SVM thường hoạt động rất hiệu quả trên các tập dữ liệu vừa và nhỏ.
* **Tổng quát hóa tốt:** SVM có khả năng tổng quát hóa tốt, ít bị overfitting.
* **Linh hoạt:** Có thể sử dụng các kernel khác nhau để xử lý nhiều loại dữ liệu.

**Nhược điểm của SVM:**

* **Tốn kém tính toán:** SVM có thể tốn kém tính toán trên các tập dữ liệu lớn.
* **Khó hiểu:** Ý tưởng của SVM có thể khó hiểu đối với người mới bắt đầu.
* **Nhạy cảm với tham số:** Hiệu suất của SVM phụ thuộc vào việc lựa chọn đúng các tham số như loại kernel, hệ số, v.v.

---

**LinearSVC** là một thuật toán học máy thuộc nhóm **học có giám sát (supervised learning)**, được sử dụng cho bài toán **phân loại (classification)**. Nó là một dạng của **Support Vector Machine (SVM)**, nhưng được tối ưu hóa cho trường hợp dữ liệu có thể phân tách tuyến tính.

**Ý tưởng chính:**

LinearSVC tìm một **siêu phẳng (hyperplane)** tốt nhất để phân chia dữ liệu thành các lớp khác nhau. "Tốt nhất" ở đây có nghĩa là siêu phẳng đó có khoảng cách lớn nhất đến các điểm dữ liệu gần nhất của mỗi lớp (margin).

**Cách thức hoạt động:**

1. **Tìm siêu phẳng:** LinearSVC sẽ tìm một siêu phẳng (đường thẳng trong không gian 2D, mặt phẳng trong không gian 3D, v.v.) sao cho khoảng cách từ siêu phẳng đó đến các điểm dữ liệu gần nhất của mỗi lớp là lớn nhất.
2. **Phân loại:** Dựa vào vị trí của một điểm dữ liệu mới so với siêu phẳng, LinearSVC sẽ phân loại điểm đó vào lớp tương ứng.

**LinearSVC trong scikit-learn:**

Đây là lớp (class) trong thư viện scikit-learn của Python, cung cấp công cụ để sử dụng thuật toán LinearSVC. Bạn có thể tùy chỉnh các tham số như cách tối ưu hóa, hàm mất mát, v.v.

**Ưu điểm của LinearSVC:**

* **Hiệu quả:** LinearSVC thường hoạt động rất hiệu quả trên các tập dữ liệu lớn.
* **Đơn giản:** Dễ hiểu và dễ cài đặt.
* **Phù hợp với dữ liệu tuyến tính:** Rất tốt cho dữ liệu có thể phân tách tuyến tính.

**Nhược điểm của LinearSVC:**

* **Không phù hợp với dữ liệu phi tuyến tính:** Nếu dữ liệu không thể phân tách tuyến tính, LinearSVC có thể không hoạt động tốt.
* **Nhạy cảm với nhiễu:** LinearSVC có thể bị ảnh hưởng bởi các điểm dữ liệu nhiễu.

**So sánh với SVC:**

* **SVC:** Là một lớp tổng quát hơn của SVM, có thể sử dụng các kernel (hàm) khác nhau để xử lý dữ liệu phi tuyến tính. Tuy nhiên, SVC thường chậm hơn LinearSVC trên dữ liệu lớn.
* **LinearSVC:** Là một phiên bản tối ưu hóa của SVC cho trường hợp kernel tuyến tính, nhanh hơn và hiệu quả hơn trên dữ liệu lớn.


**Example**

```python
from sklearn import datasets
digits = datasets.load_digits()
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target)

# Apply logistic regression and print scores
lr = LogisticRegression()
lr.fit(X_train, y_train)
print(lr.score(X_train, y_train))
print(lr.score(X_test, y_test))

# Apply SVM and print scores
svm = SVC()
svm.fit(X_train, y_train)
print(svm.score(X_train, y_train))
print(svm.score(X_test, y_test))
```

Sentiment analysis for movie reviews

```python
# Instantiate logistic regression and train
lr = LogisticRegression()
lr.fit(X, y)

# Predict sentiment for a glowing review
review1 = "LOVED IT! This movie was amazing. Top 10 this year."
review1_features = get_features(review1)
print("Review:", review1)
print("Probability of positive review:", lr.predict_proba(review1_features)[0,1])

# Predict sentiment for a poor review
review2 = "Total junk! I'll never watch a film by that director again, no matter how good the reviews."
review2_features = get_features(review2)
print("Review:", review2)
print("Probability of positive review:", lr.predict_proba(review2_features)[0,1])
```

---
###  2. <a name='Lossfunctions'></a>Loss functions

[Slide]({{site.baseurl}}/files/linears_classifiers_in_python_c2.pdf)

---
###  3. <a name='Logisticregression'></a>Logistic regression

[Slide]({{site.baseurl}}/files/linears_classifiers_in_python_c3.pdf)

####  3.1. <a name='Logisticregressionandregularization'></a>**Logistic regression and regularization**

- **Regularized logistic regression**

```python
# Train and validaton errors initialized as empty list
train_errs = list()
valid_errs = list()

# Loop over values of C_value
for C_value in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
    # Create LogisticRegression object and fit
    lr = LogisticRegression(C=C_value)
    lr.fit(X_train, y_train)
    
    # Evaluate error rates and append to lists
    train_errs.append( 1.0 - lr.score(X_train, y_train) )
    valid_errs.append( 1.0 - lr.score(X_valid, y_valid) )
    
# Plot results
plt.semilogx(C_values, train_errs, C_values, valid_errs)
plt.legend(("train", "validation"))
plt.show()
```

- **Logistic regression and feature selection**

```python
# Specify L1 regularization
lr = LogisticRegression(solver='liblinear', penalty='l1')

# Instantiate the GridSearchCV object and run the search
searcher = GridSearchCV(lr, {'C':[0.001, 0.01, 0.1, 1, 10]})
searcher.fit(X_train, y_train)

# Report the best parameters
print("Best CV params", searcher.best_params_)

# Find the number of nonzero coefficients (selected features)
best_lr = searcher.best_estimator_
coefs = best_lr.coef_
print("Total number of features:", coefs.size)
print("Number of selected features:", np.count_nonzero(coefs))
```

- **Identifying the most positive and negative words**

```python
# Get the indices of the sorted cofficients
inds_ascending = np.argsort(lr.coef_.flatten()) 
inds_descending = inds_ascending[::-1]

# Print the most positive words
print("Most positive words: ", end="")
for i in range(5):
    print(vocab[inds_descending[i]], end=", ")
print("\n")

# Print most negative words
print("Most negative words: ", end="")
for i in range(5):
    print(vocab[inds_ascending[i]], end=", ")
print("\n")
```

####  3.2. <a name='Logisticregressionandprobabilities'></a>**Logistic regression and probabilities**

- **Regularization and probabilities**

```python
# Set the regularization strength
model = LogisticRegression(C=0.1)

# Fit and plot
model.fit(X,y)
plot_classifier(X,y,model,proba=True)

# Predict probabilities on training points
prob = model.predict_proba(X)
print("Maximum predicted probability", np.max(prob))
```

- **Visualizing easy and difficult examples**

```python
lr = LogisticRegression()
lr.fit(X,y)

# Get predicted probabilities
proba = lr.predict_proba(X)

# Sort the example indices by their maximum probability
proba_inds = np.argsort(np.max(proba,axis=1))

# Show the most confident (least ambiguous) digit
show_digit(proba_inds[-1], lr)

# Show the least confident (most ambiguous) digit
show_digit(proba_inds[0], lr)

```

####  3.3. <a name='Multi-classlogisticregression'></a>**Multi-class logistic regression**

- **Fitting multi-class logistic regression**

```python
# Fit one-vs-rest logistic regression classifier
lr_ovr = LogisticRegression(multi_class='ovr')
lr_ovr.fit(X_train, y_train)

print("OVR training accuracy:", lr_ovr.score(X_train, y_train))
print("OVR test accuracy    :", lr_ovr.score(X_test, y_test))

# Fit softmax classifier
lr_mn = LogisticRegression(multi_class='multinomial')
lr_mn.fit(X_train, y_train)

print("Softmax training accuracy:", lr_mn.score(X_train, y_train))
print("Softmax test accuracy    :", lr_mn.score(X_test, y_test))
```

####  3.4. <a name='SupportVectorMachines'></a>**Support Vector Machines**


---
###  4. <a name='Logisticregression-1'></a>Logistic regression

[Slide]({{site.baseurl}}/files/linears_classifiers_in_python_c4.pdf)

- **Effect of removing examples**

```python
# Train a linear SVM
svm = SVC(kernel="linear")
svm.fit(X, y)
plot_classifier(X, y, svm, lims=(11,15,0,6))

# Make a new data set keeping only the support vectors
print("Number of original examples", len(X))
print("Number of support vectors", len(svm.support_))
X_small = X[svm.support_]
y_small = y[svm.support_]

# Train a new SVM using only the support vectors
svm_small = SVC(kernel="linear")
svm_small.fit(X_small, y_small)
plot_classifier(X_small, y_small, svm_small, lims=(11,15,0,6))
```

- **GridSearchCV warm-up**

```python
# Instantiate an RBF SVM
svm = SVC()

# Instantiate the GridSearchCV object and run the search
parameters = {'gamma':[0.00001, 0.0001, 0.001, 0.01, 0.1]}
searcher = GridSearchCV(svm, parameters)
searcher.fit(X, y)

# Report the best parameters
print("Best CV params", searcher.best_params_)
```

- **Using SGDClassifier**

Với **SGDClassifier** thì có thể  chuyển đổi qua lại giữa **LogisticRegression** và **LinearSVM** chỉ cần thay đổi tham số `loss`

```python
from sklearn.linear_model import SGDClassifier
logreg = SGDClassifier(loss='log_loss')
linsvm = SGDClassifier(loss='hinge')
```

Ngoài ra, **SGDClassifier** còn có regulation `alpha` = 1/C

```python
# We set random_state=0 for reproducibility 
linear_classifier = SGDClassifier(random_state=0)

# Instantiate the GridSearchCV object and run the search
parameters = {'alpha':[0.00001, 0.0001, 0.001, 0.01, 0.1, 1], 
             'loss':['log_loss', 'hinge']}
searcher = GridSearchCV(linear_classifier, parameters, cv=10)
searcher.fit(X_train, y_train)

# Report the best parameters and the corresponding score
print("Best CV params", searcher.best_params_)
print("Best CV accuracy", searcher.best_score_)
print("Test accuracy of best grid search hypers:", searcher.score(X_test, y_test))
```