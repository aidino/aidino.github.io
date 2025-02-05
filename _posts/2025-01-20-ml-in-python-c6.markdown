---
layout: post
title: "Machine Learning with Tree-Based Models in Python"
date: 2025-01-20 05:00:00 +0700
categories: machine learning in python
---

Decision trees are supervised learning models used for problems involving classification and regression. 

Tree models present a high flexibility that comes at a price: on one hand, trees are able to capture complex non-linear relationships; on the other hand, they are prone to memorizing the noise present in a dataset. By aggregating the predictions of trees that are trained differently, ensemble methods take advantage of the flexibility of trees while reducing their tendency to memorize noise. Ensemble methods are used across a variety of fields and have a proven track record of winning many machine learning competitions.

---
### Classification and Regression Trees

[Slide]({{site.baseurl}}/files/Machine_Learning_with_Tree_Based_Models_C1.pdf)

#### Decision tree for classification

**Decision Regions: CART vs. Linear Model (Vùng Quyết Định: CART so với Mô hình Tuyến tính)**

Trong Machine Learning, bài toán phân loại (classification) là việc gán một đối tượng vào một trong các lớp (categories) đã được định nghĩa trước.  *Decision regions* (vùng quyết định) là vùng không gian đặc trưng (feature space) mà tại đó, mô hình dự đoán một lớp cụ thể.  Nói cách khác, nếu một điểm dữ liệu rơi vào một vùng quyết định nào đó, mô hình sẽ dự đoán điểm dữ liệu đó thuộc lớp tương ứng với vùng đó.

**1. Mô hình Tuyến tính (Linear Models):**

Các mô hình tuyến tính, như *Logistic Regression* hay *Linear SVM*, tạo ra các *decision boundaries* (ranh giới quyết định) tuyến tính.  Điều này có nghĩa là ranh giới giữa các lớp có thể được biểu diễn bằng một đường thẳng (trong không gian 2D), một mặt phẳng (trong không gian 3D), hoặc một siêu phẳng (trong không gian nhiều chiều).

*   **Đặc điểm:**
    *   *Decision regions* thường được phân tách bởi các đường thẳng hoặc mặt phẳng.
    *   Mô hình tuyến tính hoạt động tốt khi các lớp có thể phân tách tuyến tính (linearly separable).
    *   Ví dụ: Nếu bạn có hai lớp và dữ liệu của chúng có thể được chia cắt bởi một đường thẳng duy nhất, thì mô hình tuyến tính có thể hoạt động tốt.
*   **Ưu điểm:**
    *   Dễ hiểu và dễ diễn giải (interpretable).
    *   Tính toán nhanh.
*   **Nhược điểm:**
    *   Không phù hợp với dữ liệu phức tạp, phi tuyến tính.  Nếu các lớp không thể phân tách tuyến tính, mô hình tuyến tính sẽ hoạt động kém.

**2. Cây Quyết Định (CART - Classification and Regression Trees):**

CART là một loại mô hình cây quyết định sử dụng một loạt các quy tắc "nếu-thì" (if-then rules) để phân chia dữ liệu thành các vùng quyết định.  Mỗi nút (node) trong cây đại diện cho một thuộc tính (feature), và mỗi nhánh (branch) đại diện cho một kết quả của phép kiểm tra thuộc tính đó.

*   **Đặc điểm:**
    *   *Decision regions* có dạng hình chữ nhật hoặc đa giác, tùy thuộc vào các phép chia được thực hiện bởi cây.
    *   CART có thể xử lý dữ liệu phi tuyến tính bằng cách tạo ra các ranh giới quyết định phức tạp hơn.
    *   Ví dụ: Để phân loại dữ liệu phức tạp, CART có thể chia không gian đặc trưng thành nhiều vùng nhỏ hơn, mỗi vùng tương ứng với một lớp.
*   **Ưu điểm:**
    *   Có thể xử lý dữ liệu phi tuyến tính.
    *   Dễ hiểu và dễ trực quan hóa.
*   **Nhược điểm:**
    *   Dễ bị quá khớp (overfitting) nếu cây quá phức tạp.  Cần các phương pháp điều chỉnh (regularization) để tránh overfitting.

**So sánh:**

| Đặc điểm        | Mô hình Tuyến tính (Linear Models) | Cây Quyết Định (CART) |
|-----------------|-----------------------------------|----------------------|
| Ranh giới quyết định | Tuyến tính (đường thẳng, mặt phẳng) | Phi tuyến tính (hình chữ nhật, đa giác) |
| Khả năng xử lý dữ liệu | Phân tách tuyến tính           | Phân tách tuyến tính và phi tuyến tính |
| Độ phức tạp     | Thấp                               | Cao (có thể phức tạp) |
| Khả năng diễn giải | Dễ                               | Dễ                   |
| Khả năng bị overfitting | Thấp                               | Cao (dễ bị overfitting nếu không điều chỉnh) |


- **Train your first classification tree**

```python
# Import DecisionTreeClassifier from sklearn.tree
from sklearn.tree import DecisionTreeClassifier

# Instantiate a DecisionTreeClassifier 'dt' with a maximum depth of 6
dt = DecisionTreeClassifier(max_depth=6, random_state=SEED)

# Fit dt to the training set
dt.fit(X_train, y_train)

# Predict test set labels
y_pred = dt.predict(X_test)
print(y_pred[0:5])
```

- **Evaluate the classification tree**

```python
# Import accuracy_score
from sklearn.metrics import accuracy_score

# Predict test set labels
y_pred = dt.predict(X_test)

# Compute test set accuracy  
acc = accuracy_score(y_pred, y_test)
print("Test set accuracy: {:.2f}".format(acc))
```

- **Logistic regression vs classification tree**

```python
# Import LogisticRegression from sklearn.linear_model
from sklearn.linear_model import  LogisticRegression

# Instatiate logreg
logreg = LogisticRegression(random_state=1)

# Fit logreg to the training set
logreg.fit(X_train, y_train)

# Define a list called clfs containing the two classifiers logreg and dt
clfs = [logreg, dt]

# Review the decision regions of the two classifiers
plot_labeled_decision_regions(X_test, y_test, clfs)
```
#### Classification tree Learning

**Information Gain (IG) trong mô hình Cây Quyết Định (Decision Tree)**

Trong Machine Learning, đặc biệt là khi xây dựng mô hình Cây Quyết Định (*Decision Tree*), *Information Gain (IG)* là một độ đo quan trọng được sử dụng để lựa chọn thuộc tính (feature) nào sẽ được sử dụng để phân chia dữ liệu tại mỗi nút (node) của cây.  Mục tiêu là chọn thuộc tính nào mang lại nhiều thông tin nhất về nhãn (label) của dữ liệu.

**Entropy:**

Để hiểu *Information Gain*, trước tiên cần hiểu khái niệm *Entropy*. *Entropy* là một độ đo sự hỗn loạn hay không chắc chắn của một tập dữ liệu.  Trong ngữ cảnh phân loại (*classification*), *Entropy* đo mức độ "không thuần nhất" của nhãn trong một tập dữ liệu.

*   Nếu một tập dữ liệu chứa toàn các đối tượng thuộc cùng một lớp, *Entropy* sẽ bằng 0 (hoàn toàn thuần nhất).
*   Nếu một tập dữ liệu chứa các đối tượng phân bố đều giữa các lớp, *Entropy* sẽ đạt giá trị cao nhất (hoàn toàn hỗn loạn).

Công thức tính *Entropy* cho một tập dữ liệu *S* với các lớp *c<sub>i</sub>* và xác suất *p<sub>i</sub>* của mỗi lớp:

**Entropy(S)** = -Σ (p<sub>i</sub> * log<sub>2</sub>(p<sub>i</sub>))


**Information Gain (IG):**

*Information Gain* của một thuộc tính *A* đối với một tập dữ liệu *S* được tính bằng cách lấy *Entropy* của tập dữ liệu ban đầu trừ đi *Entropy* sau khi tập dữ liệu được chia theo thuộc tính *A*.

**IG(S, A)** = **Entropy(S)** -Σ((\|S<sub>v</sub>\| / \|S\|) * Entropy(S<sub>v</sub>) )


Trong đó:

*   *S*: Tập dữ liệu ban đầu.
*   *A*: Thuộc tính được xem xét.
*   *v*: Các giá trị có thể của thuộc tính *A*.
*   *S<sub>v</sub>*: Tập con của *S* chứa các đối tượng có giá trị *v* cho thuộc tính *A*.
*   \|S\|: Kích thước của tập *S*.
*   \|S<sub>v</sub>\|: Kích thước của tập *S<sub>v</sub>*.

**Ý nghĩa của Information Gain:**

*   *Information Gain* càng cao, thuộc tính đó càng tốt để phân chia dữ liệu, vì nó làm giảm đáng kể sự hỗn loạn trong các tập con được tạo ra.
*   Thuộc tính có *Information Gain* cao nhất sẽ được chọn để phân chia dữ liệu tại nút hiện tại của cây quyết định.

**Ví dụ:**

Giả sử bạn có một tập dữ liệu về việc dự đoán khách hàng có mua sản phẩm hay không dựa trên các thuộc tính như "Độ tuổi", "Thu nhập", và "Giới tính".  Để xây dựng cây quyết định, bạn cần tính *Information Gain* cho từng thuộc tính này.  Thuộc tính nào có *Information Gain* cao nhất sẽ được chọn để phân chia dữ liệu đầu tiên.

**Tóm lại:**

*   *Information Gain* là một độ đo quan trọng trong việc xây dựng cây quyết định.
*   Nó giúp lựa chọn thuộc tính tốt nhất để phân chia dữ liệu tại mỗi nút của cây.
*   Thuộc tính có *Information Gain* cao nhất sẽ được ưu tiên sử dụng.  Việc sử dụng *Information Gain* giúp cây quyết định đạt được độ chính xác cao và tránh overfitting.


- **Using entropy as a criterion**

```python
# Import DecisionTreeClassifier from sklearn.tree
from sklearn.tree import DecisionTreeClassifier

# Instantiate dt_entropy, set 'entropy' as the information criterion
dt_entropy = DecisionTreeClassifier(max_depth=8, criterion='entropy', random_state=1)

# Fit dt_entropy to the training set
dt_entropy.fit(X_train, y_train)
```

#### Decision tree for regression

Trong Machine Learning, *Decision Tree* (Cây Quyết Định) không chỉ được sử dụng cho bài toán phân loại (*classification*) mà còn có thể áp dụng cho bài toán hồi quy (*regression*), nơi mục tiêu là dự đoán một giá trị liên tục (ví dụ: giá nhà, nhiệt độ, doanh thu).  *Decision Tree for Regression* (Cây Quyết Định cho Hồi Quy) hoạt động dựa trên nguyên tắc chia nhỏ không gian đặc trưng (feature space) thành các vùng nhỏ hơn và gán một giá trị trung bình (hoặc giá trị dự đoán khác) cho mỗi vùng.

**Cách thức hoạt động:**

1.  **Chọn thuộc tính tốt nhất:** Giống như trong bài toán phân loại, thuật toán sẽ chọn thuộc tính (feature) tốt nhất để phân chia dữ liệu tại mỗi nút (node) của cây. Tuy nhiên, thay vì sử dụng *Information Gain* hoặc *Gini Index*, trong hồi quy, chúng ta thường sử dụng các độ đo khác như *Mean Squared Error (MSE)* hoặc *Mean Absolute Error (MAE)* để đánh giá mức độ "hỗn loạn" của dữ liệu. Mục tiêu là giảm thiểu sai số dự đoán trong mỗi vùng.

2.  **Phân chia dữ liệu:** Dữ liệu sẽ được chia thành hai nhánh dựa trên giá trị của thuộc tính được chọn. Quá trình này tiếp tục cho đến khi đạt được một tiêu chí dừng nhất định, ví dụ:
    *   Độ sâu tối đa của cây.
    *   Số lượng mẫu tối thiểu trong một lá (leaf).
    *   Sai số dự đoán đủ nhỏ.

3.  **Gán giá trị dự đoán:** Mỗi lá (leaf) của cây sẽ đại diện cho một vùng trong không gian đặc trưng. Giá trị dự đoán cho một mẫu dữ liệu mới sẽ là giá trị trung bình (hoặc giá trị dự đoán khác) của các mẫu dữ liệu trong cùng một lá.

**Ví dụ:**

Giả sử chúng ta muốn dự đoán giá nhà dựa trên diện tích và số phòng.

1.  Thuật toán sẽ chọn thuộc tính nào (diện tích hay số phòng) giúp giảm thiểu *MSE* nhiều nhất khi phân chia dữ liệu.
2.  Giả sử "diện tích" được chọn. Dữ liệu sẽ được chia thành hai nhóm: diện tích lớn và diện tích nhỏ.
3.  Quá trình này tiếp tục cho đến khi cây đạt độ sâu tối đa hoặc số lượng mẫu trong một lá đạt ngưỡng.
4.  Khi dự đoán giá nhà cho một căn nhà mới, chúng ta sẽ "đi" theo các nhánh của cây dựa trên diện tích và số phòng của căn nhà đó cho đến khi đến một lá. Giá trị dự đoán sẽ là giá trị trung bình của giá nhà của các căn nhà trong lá đó.

**Ưu điểm của Decision Tree for Regression:**

*   **Dễ hiểu và trực quan:** Cây quyết định dễ dàng được biểu diễn và diễn giải.
*   **Xử lý dữ liệu phi tuyến tính:** Có thể mô hình hóa các mối quan hệ phức tạp, phi tuyến tính giữa các biến.
*   **Không yêu cầu chuẩn hóa dữ liệu:** Không cần chuẩn hóa dữ liệu đầu vào.

**Nhược điểm của Decision Tree for Regression:**

*   **Dễ bị overfitting:** Có thể tạo ra cây quá phức tạp, dẫn đến overfitting. Cần các phương pháp điều chỉnh (regularization) để tránh overfitting, ví dụ như *pruning* (cắt tỉa cây).
*   **Không ổn định:** Thay đổi nhỏ trong dữ liệu huấn luyện có thể dẫn đến sự thay đổi lớn trong cấu trúc của cây.

**Tóm lại:**

*Decision Tree for Regression* là một công cụ hữu ích cho bài toán hồi quy, đặc biệt khi dữ liệu có mối quan hệ phi tuyến tính. Tuy nhiên, cần chú ý đến vấn đề overfitting và sử dụng các phương pháp điều chỉnh để đảm bảo mô hình hoạt động tốt trên dữ liệu mới.

- **Train your first regression tree**

```python
# Import DecisionTreeRegressor from sklearn.tree
from sklearn.tree import DecisionTreeRegressor

# Instantiate dt
dt = DecisionTreeRegressor(max_depth=8,
             min_samples_leaf = 0.13,
            random_state=3)

# Fit dt to the training set
dt.fit(X_train, y_train)
```

- **Evaluate the regression tree**

```python
# Import mean_squared_error from sklearn.metrics as MSE
from sklearn.metrics import mean_squared_error as MSE

# Compute y_pred
y_pred = dt.predict(X_test)

# Compute mse_dt
mse_dt = MSE(y_pred, y_test)

# Compute rmse_dt
rmse_dt = mse_dt**(1/2)

# Print rmse_dt
print("Test set RMSE of dt: {:.2f}".format(rmse_dt))
```

---
### The Bias-Variance Tradeoff

[Slide]({{site.baseurl}}/files/Machine_Learning_with_Tree_Based_Models_C2.pdf)


Trong Machine Learning, mục tiêu chính là xây dựng một mô hình có khả năng *generalize* (khái quát hóa) tốt, tức là hoạt động tốt không chỉ trên dữ liệu huấn luyện mà còn trên dữ liệu mới, chưa từng gặp.  *Generalization Error* (Lỗi Khái quát) đo lường khả năng dự đoán của mô hình trên dữ liệu mới.  Lỗi này bao gồm hai thành phần chính: *Bias* (Độ lệch) và *Variance* (Phương sai).

**1. Bias (Độ lệch):**

*   *Bias* thể hiện mức độ sai lệch giữa dự đoán của mô hình và giá trị thực tế.  Mô hình có *high bias* (độ lệch cao) thường đưa ra các giả định quá đơn giản về dữ liệu, bỏ qua các đặc điểm phức tạp, dẫn đến *underfitting* (học chưa đủ).  Nói cách khác, mô hình *bias* cao thường "chệch" so với thực tế.
*   Ví dụ:  Cố gắng dự đoán giá nhà bằng một đường thẳng đơn giản khi dữ liệu thực tế phức tạp và phi tuyến tính sẽ dẫn đến *high bias*.

**2. Variance (Phương sai):**

*   *Variance* thể hiện mức độ biến động của dự đoán của mô hình khi dữ liệu huấn luyện thay đổi. Mô hình có *high variance* (phương sai cao) quá "nhạy cảm" với dữ liệu huấn luyện, học thuộc lòng cả nhiễu (noise) trong dữ liệu, dẫn đến *overfitting* (học quá khớp).  Mô hình *variance* cao hoạt động rất tốt trên dữ liệu huấn luyện nhưng lại kém trên dữ liệu mới.
*   Ví dụ: Xây dựng một cây quyết định quá sâu, học thuộc lòng cả dữ liệu huấn luyện, bao gồm cả nhiễu, sẽ dẫn đến *high variance*.

**Mối quan hệ giữa Bias và Variance:**

*   *High Bias, Low Variance:* Mô hình quá đơn giản, dự đoán kém cả trên dữ liệu huấn luyện và dữ liệu mới (underfitting).
*   *Low Bias, High Variance:* Mô hình quá phức tạp, dự đoán tốt trên dữ liệu huấn luyện nhưng kém trên dữ liệu mới (overfitting).
*   *Low Bias, Low Variance:* Mô hình tốt, dự đoán tốt trên cả dữ liệu huấn luyện và dữ liệu mới. Đây là mục tiêu chúng ta hướng tới.

**Hình minh họa:**

Hãy tưởng tượng bạn đang chơi trò ném phi tiêu.

*   *High Bias:* Phi tiêu của bạn liên tục trượt khỏi tâm bia một khoảng đều nhau.
*   *High Variance:* Phi tiêu của bạn rải rác khắp nơi trên bảng bia, không có xu hướng cụ thể.
*   *Low Bias, Low Variance:* Phi tiêu của bạn tập trung gần tâm bia.

**Giải quyết vấn đề Bias và Variance:**

*   *High Bias:* Sử dụng mô hình phức tạp hơn, thêm đặc trưng (feature), hoặc thử các thuật toán khác.
*   *High Variance:* Sử dụng nhiều dữ liệu huấn luyện hơn, đơn giản hóa mô hình (ví dụ: *pruning* cho cây quyết định), sử dụng các phương pháp điều chỉnh (regularization) như L1 hoặc L2 regularization, hoặc *dropout*.

**Tóm lại:**

*   *Bias* và *Variance* là hai thành phần quan trọng của *Generalization Error*.
*   *Bias* đo độ lệch của mô hình so với thực tế.
*   *Variance* đo độ biến động của mô hình khi dữ liệu huấn luyện thay đổi.
*   Mục tiêu là tìm sự cân bằng giữa *Bias* và *Variance* để đạt được mô hình có khả năng khái quát hóa tốt.  Đây được gọi là *Bias-Variance Tradeoff*.

**Example**

```python
### Instantiate the model

# Import train_test_split from sklearn.model_selection
from sklearn.model_selection import train_test_split

# Set SEED for reproducibility
SEED = 1

# Split the data into 70% train and 30% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

# Instantiate a DecisionTreeRegressor dt
dt = DecisionTreeRegressor(max_depth=4, min_samples_leaf=0.26, random_state=SEED)

### Evaluate the 10-fold CV error
# Compute the array containing the 10-folds CV MSEs
MSE_CV_scores = - cross_val_score(dt, X_train, y_train, cv=10, 
                       scoring='neg_mean_squared_error',
                       n_jobs=-1)

# Compute the 10-folds CV RMSE
RMSE_CV = (MSE_CV_scores.mean())**(1/2)

# Print RMSE_CV
print('CV RMSE: {:.2f}'.format(RMSE_CV))

```

#### Ensemble Learning

Trong Machine Learning, *Ensemble Learning* là một phương pháp sử dụng kết hợp nhiều mô hình học máy yếu (weak learners) để tạo ra một mô hình mạnh mẽ hơn (strong learner) có khả năng dự đoán chính xác hơn.  Ý tưởng cơ bản là "tập thể tốt hơn cá nhân".  Bằng cách kết hợp các mô hình khác nhau, chúng ta có thể tận dụng ưu điểm của từng mô hình và giảm thiểu nhược điểm của chúng.

**Các loại Ensemble Learning phổ biến:**

1.  **Bagging (Bootstrap Aggregating):**
    *   Tạo ra nhiều tập dữ liệu con bằng cách lấy mẫu có hoàn lại (sampling with replacement) từ dữ liệu huấn luyện ban đầu.
    *   Huấn luyện một mô hình học máy yếu trên mỗi tập dữ liệu con.
    *   Kết hợp các dự đoán của các mô hình bằng cách lấy trung bình (cho hồi quy) hoặc biểu quyết (cho phân loại).
    *   Ví dụ: *Random Forest* là một thuật toán *bagging* phổ biến, sử dụng nhiều cây quyết định.

2.  **Boosting:**
    *   Huấn luyện các mô hình học máy yếu một cách tuần tự.
    *   Mỗi mô hình sau được huấn luyện để sửa chữa những sai sót của các mô hình trước đó.
    *   Các mẫu dữ liệu bị dự đoán sai bởi các mô hình trước sẽ được gán trọng số cao hơn, để các mô hình sau tập trung vào chúng.
    *   Ví dụ: *AdaBoost*, *Gradient Boosting*, *XGBoost*, *LightGBM*, *CatBoost* là các thuật toán *boosting* phổ biến.

3.  **Stacking (Stacked Generalization):**
    *   Huấn luyện nhiều mô hình học máy yếu khác nhau.
    *   Sử dụng dự đoán của các mô hình này làm đầu vào cho một mô hình học máy khác (gọi là *meta-learner* hoặc *combiner*).
    *   *Meta-learner* học cách kết hợp các dự đoán của các mô hình yếu để đưa ra dự đoán cuối cùng.

**Lợi ích của Ensemble Learning:**

*   **Tăng độ chính xác:** Mô hình *ensemble* thường có độ chính xác cao hơn so với bất kỳ mô hình riêng lẻ nào.
*   **Giảm overfitting:** Bằng cách kết hợp các mô hình khác nhau, *ensemble learning* giúp giảm nguy cơ *overfitting*.
*   **Tăng tính ổn định:** Dự đoán của mô hình *ensemble* thường ổn định hơn, ít bị ảnh hưởng bởi nhiễu trong dữ liệu.

**Ví dụ:**

Hãy tưởng tượng bạn muốn dự đoán thời tiết ngày mai. Thay vì hỏi một người duy nhất, bạn hỏi nhiều người (mỗi người có một cách dự đoán riêng). Sau đó, bạn tổng hợp các dự đoán này lại để đưa ra dự đoán cuối cùng. Đây chính là ý tưởng của *ensemble learning*.

**Ứng dụng của Ensemble Learning:**

*Ensemble Learning* được sử dụng rộng rãi trong nhiều lĩnh vực, bao gồm:

*   Nhận dạng ảnh (image recognition)
*   Xử lý ngôn ngữ tự nhiên (natural language processing)
*   Dự đoán tài chính (financial forecasting)
*   Và nhiều lĩnh vực khác.

**Tóm lại:**

*   *Ensemble Learning* là một phương pháp mạnh mẽ để cải thiện độ chính xác và tính ổn định của mô hình học máy.
*   Bằng cách kết hợp nhiều mô hình yếu, chúng ta có thể tạo ra một mô hình mạnh mẽ hơn, có khả năng khái quát hóa tốt hơn.
*   *Bagging*, *Boosting*, và *Stacking* là ba loại *ensemble learning* phổ biến.

- **Example: Define the ensemble**

```python
# Set seed for reproducibility
SEED=1

# Instantiate lr
lr = LogisticRegression(random_state=SEED)

# Instantiate knn
knn = KNeighborsClassifier(n_neighbors=27)

# Instantiate dt
dt = DecisionTreeClassifier(min_samples_leaf=0.13, random_state=SEED)

# Define the list classifiers
classifiers = [('Logistic Regression', lr), ('K Nearest Neighbours', knn), ('Classification Tree', dt)]
```

- **Evaluate individual classifiers**

```python
# Iterate over the pre-defined list of classifiers
for clf_name, clf in classifiers:    
 
    # Fit clf to the training set
    clf.fit(X_train, y_train)    
   
    # Predict y_pred
    y_pred = clf.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_pred, y_test) 
   
    # Evaluate clf's accuracy on the test set
    print('{:s} : {:.3f}'.format(clf_name, accuracy))
    
```

- **Better performance with a Voting Classifier**

```python
# Import VotingClassifier from sklearn.ensemble
from sklearn.ensemble import VotingClassifier

# Instantiate a VotingClassifier vc
vc = VotingClassifier(estimators=classifiers)     

# Fit vc to the training set
vc.fit(X_train, y_train)   

# Evaluate the test set predictions
y_pred = vc.predict(X_test)

# Calculate accuracy score
accuracy = accuracy_score(y_pred, y_test)
print('Voting Classifier: {:.3f}'.format(accuracy))
```

---
### Bagging and Random Forests

[Slide]({{site.baseurl}}/files/Machine_Learning_with_Tree_Based_Models_C3.pdf)

- **Define the bagging classifier**

```python
# Import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier

# Import BaggingClassifier
from sklearn.ensemble import BaggingClassifier

# Instantiate dt
dt = DecisionTreeClassifier(random_state=1)

# Instantiate bc
bc = BaggingClassifier(base_estimator=dt, n_estimators=50, random_state=1)
```

- **Evaluate Bagging performance**

```python
# Fit bc to the training set
bc.fit(X_train, y_train)

# Predict test set labels
y_pred = bc.predict(X_test)

# Evaluate acc_test
acc_test = accuracy_score(y_pred, y_test)
print('Test set accuracy of bc: {:.2f}'.format(acc_test)) 
```

#### Out Of Bag Evaluation

Trong Machine Learning, đặc biệt là khi sử dụng các phương pháp *Ensemble Learning* như *Bagging* (ví dụ: *Random Forest*), *Out-of-Bag Evaluation (OOB Evaluation)* là một kỹ thuật thông minh để ước lượng hiệu suất của mô hình mà không cần sử dụng tập dữ liệu kiểm tra riêng biệt.

**Cách thức hoạt động:**

1.  **Bagging và Bootstraping:** Như đã biết, trong *Bagging*, chúng ta tạo ra nhiều tập dữ liệu con bằng cách lấy mẫu có hoàn lại (sampling with replacement) từ dữ liệu huấn luyện ban đầu.  Quá trình này được gọi là *bootstrapping*.

2.  **Dữ liệu Out-of-Bag:** Vì chúng ta lấy mẫu có hoàn lại, sẽ có một số mẫu dữ liệu không được chọn vào bất kỳ tập dữ liệu con nào. Những mẫu dữ liệu này được gọi là *out-of-bag (OOB)* data.  Trung bình, khoảng 37% dữ liệu sẽ là OOB data cho mỗi mô hình con.

3.  **Đánh giá mô hình:** Đối với mỗi mô hình con được huấn luyện trên một tập dữ liệu con, chúng ta có thể sử dụng các mẫu OOB tương ứng của nó để đánh giá hiệu suất của mô hình đó.  Nói cách khác, mỗi mô hình con sẽ được đánh giá trên một tập hợp các mẫu mà nó chưa từng "nhìn thấy" trong quá trình huấn luyện.

4.  **Tổng hợp kết quả:** Sau khi đánh giá tất cả các mô hình con trên dữ liệu OOB của chúng, chúng ta có thể tổng hợp kết quả để có được ước lượng tổng thể về hiệu suất của mô hình *ensemble*.  Ví dụ, trong bài toán phân loại, chúng ta có thể lấy biểu quyết (voting) từ các dự đoán của các mô hình con trên dữ liệu OOB để đưa ra dự đoán cuối cùng và so sánh với nhãn thực tế.

**Ưu điểm của OOB Evaluation:**

*   **Không cần dữ liệu kiểm tra riêng:** OOB Evaluation cho phép chúng ta ước lượng hiệu suất của mô hình mà không cần phải chia dữ liệu thành tập huấn luyện và tập kiểm tra riêng biệt. Điều này đặc biệt hữu ích khi chúng ta có ít dữ liệu.
*   **Đánh giá khách quan:** Vì các mẫu OOB không được sử dụng trong quá trình huấn luyện mô hình tương ứng, OOB Evaluation cung cấp một ước lượng khách quan về khả năng khái quát hóa của mô hình.
*   **Tiện lợi với Bagging:** OOB Evaluation là một phần tự nhiên của quá trình *Bagging*, do đó chúng ta không cần thêm bất kỳ bước nào khác để thực hiện đánh giá.

**Ví dụ:**

Trong *Random Forest*, mỗi cây quyết định sẽ được huấn luyện trên một tập con của dữ liệu, và khoảng 37% dữ liệu còn lại sẽ được sử dụng làm OOB samples cho cây đó. Bằng cách tổng hợp kết quả dự đoán của tất cả các cây trên OOB samples tương ứng, ta có thể đánh giá được độ chính xác của *Random Forest* mà không cần tách dữ liệu kiểm tra.

**Tóm lại:**

*   *Out-of-Bag Evaluation* là một kỹ thuật thông minh để đánh giá mô hình *ensemble* dựa trên dữ liệu không được sử dụng trong quá trình huấn luyện.
*   Nó đặc biệt hữu ích trong *Bagging* và giúp ước lượng khả năng khái quát hóa của mô hình mà không cần dữ liệu kiểm tra riêng biệt.


- **Prepare the ground**

```python
# Import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier

# Import BaggingClassifier
from sklearn.ensemble import BaggingClassifier

# Instantiate dt
dt = DecisionTreeClassifier(min_samples_leaf=8, random_state=1)

# Instantiate bc
bc = BaggingClassifier(base_estimator=dt, 
            n_estimators=50,
            oob_score=True, # important
            random_state=1)
```

- **OOB Score vs Test Set Score**

```python
# Fit bc to the training set 
bc.fit(X_train, y_train)

# Predict test set labels
y_pred = bc.predict(X_test)

# Evaluate test set accuracy
acc_test = accuracy_score(y_pred, y_test)

# Evaluate OOB accuracy
acc_oob = bc.oob_score_

# Print acc_test and acc_oob
print('Test set accuracy: {:.3f}, OOB accuracy: {:.3f}'.format(acc_test, acc_oob))
```

####  Random Forests

*Random Forests* là một thuật toán *ensemble learning* (học kết hợp) phổ biến và mạnh mẽ, được sử dụng cho cả bài toán phân loại (*classification*) và hồi quy (*regression*).  Nó hoạt động bằng cách xây dựng nhiều cây quyết định (*decision trees*) trên các tập con ngẫu nhiên của dữ liệu huấn luyện và kết hợp dự đoán của chúng để đưa ra dự đoán cuối cùng.

**Cách thức hoạt động:**

1.  **Bootstrap Sampling:** *Random Forests* sử dụng kỹ thuật *bootstrap sampling* để tạo ra nhiều tập dữ liệu con từ dữ liệu huấn luyện ban đầu.  *Bootstrap sampling* là quá trình lấy mẫu có hoàn lại (sampling with replacement), nghĩa là một mẫu dữ liệu có thể được chọn nhiều lần trong một tập dữ liệu con.

2.  **Feature Randomness:** Tại mỗi nút (node) của mỗi cây quyết định, thay vì xem xét tất cả các thuộc tính (features) để chọn thuộc tính tốt nhất để phân chia dữ liệu, *Random Forests* chỉ xem xét một tập con ngẫu nhiên của các thuộc tính.  Điều này giúp tăng tính đa dạng của các cây quyết định và giảm sự tương quan giữa chúng.

3.  **Xây dựng cây quyết định:** Mỗi cây quyết định được xây dựng trên một tập dữ liệu con được tạo ra bằng *bootstrap sampling* và sử dụng một tập con ngẫu nhiên của các thuộc tính tại mỗi nút.  Các cây quyết định thường được phát triển đầy đủ (không giới hạn độ sâu) để giảm *bias* (độ lệch).

4.  **Kết hợp dự đoán:**
    *   **Phân loại:** Trong bài toán phân loại, *Random Forests* kết hợp dự đoán của các cây quyết định bằng cách lấy biểu quyết (voting).  Lớp (class) nào được nhiều cây quyết định dự đoán nhất sẽ là dự đoán cuối cùng.
    *   **Hồi quy:** Trong bài toán hồi quy, *Random Forests* kết hợp dự đoán của các cây quyết định bằng cách lấy trung bình (averaging) các dự đoán.

**Ưu điểm của Random Forests:**

*   **Độ chính xác cao:** *Random Forests* thường đạt độ chính xác cao, đặc biệt trên dữ liệu phức tạp.
*   **Khả năng khái quát hóa tốt:** Do sử dụng *bootstrap sampling* và *feature randomness*, *Random Forests* ít bị *overfitting* (học quá khớp) hơn so với một cây quyết định đơn lẻ.
*   **Xử lý dữ liệu đa dạng:** Có thể xử lý cả dữ liệu số (numerical) và dữ liệu phân loại (categorical).
*   **Không yêu cầu chuẩn hóa dữ liệu:** Không cần chuẩn hóa dữ liệu đầu vào.
*   **Đánh giá tầm quan trọng của thuộc tính:** Có thể ước lượng tầm quan trọng của từng thuộc tính trong việc dự đoán.

**Nhược điểm của Random Forests:**

*   **Khó diễn giải:** Khó diễn giải hơn so với một cây quyết định đơn lẻ.
*   **Tốn kém tính toán:** Đòi hỏi nhiều tính toán hơn so với một cây quyết định đơn lẻ, đặc biệt khi có nhiều cây quyết định.
*   **Yêu cầu bộ nhớ lớn:** Lưu trữ nhiều cây quyết định có thể tốn kém bộ nhớ.

**Ứng dụng của Random Forests:**

*Random Forests* được sử dụng rộng rãi trong nhiều lĩnh vực, bao gồm:

*   Nhận dạng ảnh (image recognition)
*   Xử lý ngôn ngữ tự nhiên (natural language processing)
*   Dự đoán tài chính (financial forecasting)
*   Sinh học (biology)
*   Và nhiều lĩnh vực khác.

**Tóm lại:**

*   *Random Forests* là một thuật toán *ensemble learning* mạnh mẽ và linh hoạt.
*   Bằng cách kết hợp nhiều cây quyết định, *Random Forests* đạt được độ chính xác cao và khả năng khái quát hóa tốt.
*   Đây là một trong những thuật toán được sử dụng phổ biến nhất trong Machine Learning.

- **Train an RF regressor**

```python
# Import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

# Instantiate rf
rf = RandomForestRegressor(n_estimators=25,
            random_state=2)
            
# Fit rf to the training set    
rf.fit(X_train, y_train) 
```

- **Evaluate the RF regressor**

```python
# Import mean_squared_error as MSE
from sklearn.metrics import mean_squared_error as MSE

# Predict the test set labels
y_pred = rf.predict(X_test)

# Evaluate the test set RMSE
rmse_test = MSE(y_test, y_pred)**(1/2)

# Print rmse_test
print('Test set RMSE of rf: {:.2f}'.format(rmse_test))
```

- **Visualizing features importances**

```python
# Create a pd.Series of features importances
importances = pd.Series(data=rf.feature_importances_,
                        index= X_train.columns)

# Sort importances
importances_sorted = importances.sort_values()

# Draw a horizontal barplot of importances_sorted
importances_sorted.plot(kind='barh', color='lightgreen')
plt.title('Features Importances')
plt.show()
```

---
### Boosting

[Slide]({{site.baseurl}}/files/Machine_Learning_with_Tree_Based_Models_C4.pdf)

#### AdaBoost

AdaBoost (viết tắt của Adaptive Boosting) là một thuật toán *ensemble learning* (học kết hợp) thuộc nhóm *boosting*.  Nó được sử dụng cho cả bài toán phân loại (*classification*) và hồi quy (*regression*), mặc dù phổ biến hơn trong phân loại.  Ý tưởng chính của AdaBoost là huấn luyện một chuỗi các mô hình học máy yếu (weak learners), và mỗi mô hình sau sẽ tập trung vào việc sửa chữa những sai sót của các mô hình trước đó.

**Cách thức hoạt động:**

1.  **Khởi tạo trọng số:** Ban đầu, mỗi mẫu dữ liệu trong tập huấn luyện được gán một trọng số bằng nhau.

2.  **Huấn luyện mô hình yếu:** Huấn luyện một mô hình học máy yếu (ví dụ: cây quyết định với độ sâu nhỏ, *stump*) trên dữ liệu huấn luyện với trọng số hiện tại.

3.  **Tính toán sai số:** Tính toán sai số của mô hình yếu trên dữ liệu huấn luyện. Sai số này cho biết mô hình yếu dự đoán đúng hay sai các mẫu dữ liệu như thế nào, có tính đến trọng số của chúng.

4.  **Cập nhật trọng số:** Tăng trọng số của các mẫu dữ liệu bị dự đoán sai và giảm trọng số của các mẫu dữ liệu được dự đoán đúng.  Việc này làm cho các mẫu bị dự đoán sai trở nên "quan trọng" hơn trong các vòng lặp tiếp theo.

5.  **Tính toán hệ số của mô hình yếu:** Tính toán một hệ số cho mô hình yếu dựa trên sai số của nó. Mô hình nào có sai số thấp hơn sẽ có hệ số cao hơn, đóng góp nhiều hơn vào dự đoán cuối cùng.

6.  **Lặp lại:** Lặp lại các bước 2-5 cho đến khi đạt được một số lượng mô hình yếu nhất định hoặc sai số đạt ngưỡng.

7.  **Kết hợp dự đoán:** Kết hợp các dự đoán của các mô hình yếu bằng cách lấy trung bình có trọng số (weighted average) (cho hồi quy) hoặc biểu quyết có trọng số (weighted voting) (cho phân loại). Trọng số của mỗi mô hình yếu chính là hệ số đã được tính toán ở bước 5.

**Điểm khác biệt của AdaBoost so với Bagging:**

*   **Trọng số mẫu:** Trong khi *Bagging* lấy mẫu ngẫu nhiên có hoàn lại, *AdaBoost* gán trọng số cho từng mẫu dữ liệu và cập nhật trọng số này sau mỗi vòng lặp.
*   **Huấn luyện tuần tự:** Các mô hình yếu trong *AdaBoost* được huấn luyện tuần tự, mô hình sau phụ thuộc vào kết quả của mô hình trước. Trong khi đó, các mô hình trong *Bagging* được huấn luyện độc lập.

**Ưu điểm của AdaBoost:**

*   **Độ chính xác cao:** AdaBoost thường đạt độ chính xác cao, đặc biệt trên dữ liệu phức tạp.
*   **Khả năng thích ứng:** AdaBoost có khả năng thích ứng với dữ liệu, tập trung vào các mẫu dữ liệu khó.
*   **Ít bị overfitting:** AdaBoost ít bị overfitting hơn so với một số thuật toán khác, đặc biệt khi sử dụng các mô hình yếu đơn giản.

**Nhược điểm của AdaBoost:**

*   **Nhạy cảm với nhiễu:** AdaBoost có thể nhạy cảm với dữ liệu nhiễu.
*   **Khó diễn giải:** Khó diễn giải hơn so với một số thuật toán khác.
*   **Tính toán tốn kém:** Đòi hỏi nhiều tính toán hơn so với một số thuật toán khác.

**Ứng dụng của AdaBoost:**

AdaBoost được sử dụng trong nhiều lĩnh vực, bao gồm:

*   Nhận dạng khuôn mặt (face recognition)
*   Phân loại văn bản (text classification)
*   Phát hiện đối tượng (object detection)
*   Và nhiều lĩnh vực khác.

**Tóm lại:**

*   AdaBoost là một thuật toán *boosting* mạnh mẽ và hiệu quả.
*   Bằng cách huấn luyện một chuỗi các mô hình yếu và tập trung vào các mẫu dữ liệu khó, AdaBoost đạt được độ chính xác cao.
*   Đây là một trong những thuật toán *ensemble learning* được sử dụng phổ biến nhất.

- **Define the AdaBoost classifier**

```python
# Import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier

# Import AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier

# Instantiate dt
dt = DecisionTreeClassifier(max_depth=2, random_state=1)

# Instantiate ada
ada = AdaBoostClassifier(base_estimator=dt, n_estimators=180, random_state=1)
```

- **Train the AdaBoost classifier**

```python
# Fit ada to the training set
ada.fit(X_train, y_train)

# Compute the probabilities of obtaining the positive class
y_pred_proba = ada.predict_proba(X_test)[:, 1]
```

- **Evaluate the AdaBoost classifier**

```python
# Import roc_auc_score
from sklearn.metrics import roc_auc_score

# Evaluate test-set roc_auc_score
ada_roc_auc = roc_auc_score(y_test, y_pred_proba)

# Print roc_auc_score
print('ROC AUC score: {:.2f}'.format(ada_roc_auc))
```

#### Gradient Boosting

*Gradient Boosting* là một thuật toán *ensemble learning* (học kết hợp) thuộc nhóm *boosting*. Tương tự như AdaBoost, Gradient Boosting cũng xây dựng một chuỗi các mô hình học máy yếu (weak learners) một cách tuần tự, với mỗi mô hình sau cố gắng sửa chữa những sai sót của các mô hình trước đó. Tuy nhiên, điểm khác biệt chính là cách Gradient Boosting xác định "sai sót" và cách nó tối ưu hóa mô hình.

**Cách thức hoạt động:**

1.  **Khởi tạo:** Khởi tạo một mô hình dự đoán ban đầu (thường là một giá trị trung bình hoặc hằng số).

2.  **Tính toán phần dư (residuals):** Tính toán phần dư (residuals) giữa giá trị thực tế và dự đoán của mô hình hiện tại. Phần dư này chính là "sai sót" mà mô hình cần sửa chữa.

3.  **Huấn luyện mô hình yếu trên phần dư:** Huấn luyện một mô hình học máy yếu (ví dụ: cây quyết định với độ sâu nhỏ) trên phần dư. Mô hình này sẽ cố gắng dự đoán phần dư, hay nói cách khác, nó sẽ học cách "sửa sai" cho mô hình trước đó.

4.  **Cập nhật mô hình:** Cập nhật mô hình hiện tại bằng cách cộng thêm dự đoán của mô hình yếu vừa huấn luyện, nhân với một hệ số học (learning rate) nhỏ. Hệ số học này kiểm soát mức độ đóng góp của mô hình yếu vào mô hình tổng thể.

5.  **Lặp lại:** Lặp lại các bước 2-4 cho đến khi đạt được một số lượng mô hình yếu nhất định hoặc sai số đạt ngưỡng.

6.  **Kết hợp dự đoán:** Kết hợp các dự đoán của tất cả các mô hình yếu để đưa ra dự đoán cuối cùng.

**Điểm khác biệt chính của Gradient Boosting so với AdaBoost:**

*   **Cách xác định sai sót:** AdaBoost sử dụng trọng số mẫu để tập trung vào các mẫu bị dự đoán sai. Gradient Boosting sử dụng phần dư (residuals) để xác định sai sót.
*   **Cách tối ưu hóa:** AdaBoost tối ưu hóa bằng cách thay đổi trọng số mẫu. Gradient Boosting tối ưu hóa bằng cách sử dụng gradient descent (phương phápGradient).

**Các biến thể phổ biến của Gradient Boosting:**

Có nhiều biến thể của Gradient Boosting, bao gồm:

*   **XGBoost (Extreme Gradient Boosting):** Tối ưu hóa tốc độ và hiệu suất.
*   **LightGBM (Light Gradient Boosting Machine):** Sử dụng các kỹ thuật tối ưu hóa để tăng tốc độ huấn luyện và giảm mức sử dụng bộ nhớ.
*   **CatBoost (Categorical Boosting):** Xử lý tốt dữ liệu phân loại.

**Ưu điểm của Gradient Boosting:**

*   **Độ chính xác cao:** Gradient Boosting thường đạt độ chính xác rất cao, đặc biệt trên dữ liệu phức tạp.
*   **Khả năng khái quát hóa tốt:** Ít bị overfitting.
*   **Linh hoạt:** Có thể sử dụng nhiều loại mô hình yếu khác nhau.

**Nhược điểm của Gradient Boosting:**

*   **Khó diễn giải:** Khó diễn giải hơn so với một số thuật toán khác.
*   **Tính toán tốn kém:** Đòi hỏi nhiều tính toán hơn so với một số thuật toán khác.
*   **Nhạy cảm với tuning hyperparameters:** Yêu cầu điều chỉnh các siêu tham số (hyperparameters) cẩn thận.
*   


**Ứng dụng của Gradient Boosting:**

Gradient Boosting được sử dụng rộng rãi trong nhiều lĩnh vực, bao gồm:

*   Kaggle competitions
*   Dự đoán tài chính
*   Nhận dạng ảnh
*   Xử lý ngôn ngữ tự nhiên
*   Và nhiều lĩnh vực khác.

**Tóm lại:**

*   *Gradient Boosting* là một thuật toán *boosting* mạnh mẽ và hiệu quả.
*   Bằng cách sử dụng gradient descent để tối ưu hóa mô hình, Gradient Boosting đạt được độ chính xác rất cao.
*   Đây là một trong những thuật toán được sử dụng phổ biến nhất trong Machine Learning, đặc biệt trong các cuộc thi học máy.
  

- **Define the GB regressor**

```python
# Import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Instantiate gb
gb = GradientBoostingRegressor(max_depth=4, 
            n_estimators=200,
            random_state=2)
```

- **Train the GB regressor**

```python
# Fit gb to the training set
gb.fit(X_train, y_train)

# Predict test set labels
y_pred = gb.predict(X_test)
```

- **Evaluate the GB regressor**

```python
# Import mean_squared_error as MSE
from sklearn.metrics import mean_squared_error as MSE

# Compute MSE
mse_test = MSE(y_test, y_pred)

# Compute RMSE
rmse_test = mse_test**(1/2)

# Print RMSE
print('Test set RMSE of gb: {:.3f}'.format(rmse_test))
```

#### Stochastic Gradient Boosting (SGB)

*Stochastic Gradient Boosting (SGB)* là một biến thể của *Gradient Boosting* (Tăng cường Gradient) được giới thiệu để cải thiện hiệu suất và khả năng khái quát hóa của mô hình.  Điểm khác biệt chính của SGB so với Gradient Boosting "truyền thống" là việc sử dụng ngẫu nhiên trong quá trình huấn luyện.

**Cách thức hoạt động:**

SGB hoạt động tương tự như Gradient Boosting, nhưng có thêm một bước ngẫu nhiên:

1.  **Khởi tạo:** Khởi tạo một mô hình dự đoán ban đầu (thường là một giá trị trung bình hoặc hằng số).

2.  **Lấy mẫu ngẫu nhiên:** Thay vì sử dụng toàn bộ dữ liệu huấn luyện để tính toán gradient, SGB chỉ sử dụng một tập con ngẫu nhiên của dữ liệu huấn luyện.  Việc này được thực hiện ở mỗi bước huấn luyện của mỗi weak learner. Tỉ lệ mẫu được lấy gọi là *subsample ratio*.

3.  **Tính toán phần dư (residuals):** Tính toán phần dư (residuals) giữa giá trị thực tế và dự đoán của mô hình hiện tại, *chỉ trên tập con ngẫu nhiên*.

4.  **Huấn luyện mô hình yếu trên phần dư:** Huấn luyện một mô hình học máy yếu (ví dụ: cây quyết định với độ sâu nhỏ) trên phần dư, *sử dụng tập con ngẫu nhiên*.

5.  **Cập nhật mô hình:** Cập nhật mô hình hiện tại bằng cách cộng thêm dự đoán của mô hình yếu vừa huấn luyện, nhân với một hệ số học (learning rate) nhỏ.

6.  **Lặp lại:** Lặp lại các bước 2-5 cho đến khi đạt được một số lượng mô hình yếu nhất định hoặc sai số đạt ngưỡng.

7.  **Kết hợp dự đoán:** Kết hợp các dự đoán của tất cả các mô hình yếu để đưa ra dự đoán cuối cùng.

**Điểm khác biệt chính của SGB so với Gradient Boosting "truyền thống":**

*   **Sử dụng ngẫu nhiên:** SGB sử dụng một tập con ngẫu nhiên của dữ liệu huấn luyện ở mỗi bước, trong khi Gradient Boosting "truyền thống" sử dụng toàn bộ dữ liệu.

**Lợi ích của Stochastic Gradient Boosting:**

*   **Giảm overfitting:** Việc sử dụng ngẫu nhiên giúp giảm overfitting, do mỗi weak learner chỉ được huấn luyện trên một phần dữ liệu, tránh học thuộc lòng dữ liệu huấn luyện.
*   **Tăng tốc độ huấn luyện:** Huấn luyện trên tập con ngẫu nhiên nhanh hơn so với huấn luyện trên toàn bộ dữ liệu.
*   **Cải thiện khả năng khái quát hóa:** Mô hình SGB thường có khả năng khái quát hóa tốt hơn, do ít bị ảnh hưởng bởi nhiễu trong dữ liệu.

**Các tham số quan trọng trong SGB:**

*   `n_estimators`: Số lượng weak learners (ví dụ: số cây quyết định).
*   `learning_rate`: Hệ số học, kiểm soát mức độ đóng góp của mỗi weak learner.
*   `subsample`: Tỉ lệ mẫu được sử dụng ở mỗi bước huấn luyện.  Giá trị này nằm trong khoảng (0, 1].
*   `max_depth`: Độ sâu tối đa của cây quyết định (nếu weak learner là cây quyết định).

**Tóm lại:**

*   *Stochastic Gradient Boosting* là một biến thể của *Gradient Boosting* sử dụng ngẫu nhiên trong quá trình huấn luyện.
*   Việc sử dụng ngẫu nhiên giúp giảm overfitting, tăng tốc độ huấn luyện và cải thiện khả năng khái quát hóa của mô hình.
*   SGB là một thuật toán mạnh mẽ và được sử dụng rộng rãi trong Machine Learning.

- **Regression with SGB**

```python
# Import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Instantiate sgbr
sgbr = GradientBoostingRegressor(max_depth=4, 
            subsample=0.9,
            max_features=0.75,
            n_estimators=200,
            random_state=2)
```

- **Train the SGB regressor**

```python
# Fit sgbr to the training set
sgbr.fit(X_train, y_train)

# Predict test set labels
y_pred = sgbr.predict(X_test)
```

- **Evaluate the SGB regressor**

```python 
# Import mean_squared_error as MSE
from sklearn.metrics import mean_squared_error as MSE

# Compute test set MSE
mse_test = MSE(y_test, y_pred)

# Compute test set RMSE
rmse_test = mse_test**(1/2)

# Print rmse_test
print('Test set RMSE of sgbr: {:.3f}'.format(rmse_test))
```



---
### Model Tuning

[Slide]({{site.baseurl}}/files/Machine_Learning_with_Tree_Based_Models_C5.pdf)

