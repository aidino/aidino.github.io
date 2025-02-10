---
layout: post
title: "Dimensionality Reduction in Python"
date: 2025-01-20 09:00:00 +0700
categories: machine learning in python
---

High-dimensional datasets can be overwhelming and leave you not knowing where to start. Typically, you’d visually explore a new dataset first, but when you have too many dimensions the classical approaches will seem insufficient. Fortunately, there are visualization techniques designed specifically for high dimensional data and you’ll be introduced to these in this course. After exploring the data, you’ll often find that many features hold little information because they don’t show any variance or because they are duplicates of other features. 


## Exploring High Dimensional Data

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C1.pdf)

### Feature selection vs. feature extraction

Cả *Feature Selection* (lựa chọn đặc trưng) và *Feature Extraction* (khai thác đặc trưng) đều là các kỹ thuật quan trọng trong tiền xử lý dữ liệu và xây dựng mô hình học máy. Mục tiêu chung của chúng là cải thiện hiệu suất của mô hình bằng cách giảm số lượng đặc trưng đầu vào, nhưng cách thức thực hiện của chúng khác nhau.

**1. Feature Selection (Lựa chọn đặc trưng):**

*   **Định nghĩa:** *Feature Selection* là quá trình *chọn ra* một tập con các đặc trưng *quan trọng nhất* từ tập đặc trưng ban đầu, *bỏ qua* các đặc trưng *ít quan trọng* hoặc *không liên quan*.  Các đặc trưng được chọn sẽ được sử dụng để huấn luyện mô hình.
*   **Mục tiêu:**
    *   Cải thiện độ chính xác của mô hình.
    *   Giảm độ phức tạp của mô hình, giúp mô hình dễ hiểu và dễ diễn giải hơn.
    *   Giảm thời gian huấn luyện mô hình.
    *   Tránh hiện tượng *overfitting* (quá khớp).
*   **Phương pháp:**
    *   *Filter Methods* (Phương pháp lọc):  Dựa trên các tiêu chí thống kê (ví dụ: tương quan, *chi-square*) để đánh giá mức độ quan trọng của từng đặc trưng độc lập với mô hình.  Ví dụ: *Correlation Coefficient*, *ANOVA*.
    *   *Wrapper Methods* (Phương pháp bao bọc):  Sử dụng một mô hình học máy cụ thể để đánh giá tập con các đặc trưng.  Ví dụ: *Recursive Feature Elimination (RFE)*, *Forward Selection*, *Backward Elimination*.
    *   *Embedded Methods* (Phương pháp nhúng):  Tích hợp việc lựa chọn đặc trưng vào quá trình huấn luyện mô hình.  Ví dụ: *LASSO*, *Ridge Regression*, *Decision Tree*.

**2. Feature Extraction (Khai thác đặc trưng):**

*   **Định nghĩa:** *Feature Extraction* là quá trình *tạo ra* các đặc trưng *mới* từ tập đặc trưng ban đầu bằng cách *biến đổi* hoặc *kết hợp* các đặc trưng hiện có.  Các đặc trưng mới này sẽ được sử dụng để huấn luyện mô hình.
*   **Mục tiêu:**
    *   Giảm chiều dữ liệu (dimensionality reduction), giúp mô hình xử lý dữ liệu hiệu quả hơn.
    *   Khám phá các đặc trưng ẩn, có thể không được biểu diễn trực tiếp trong dữ liệu ban đầu.
    *   Cải thiện hiệu suất của mô hình bằng cách tạo ra các đặc trưng phù hợp hơn.
*   **Phương pháp:**
    *   *Principal Component Analysis (PCA)*:  Tìm các thành phần chính (principal components) là tổ hợp tuyến tính của các đặc trưng ban đầu, và giữ lại các thành phần chính quan trọng nhất.
    *   *Linear Discriminant Analysis (LDA)*:  Tìm các tổ hợp tuyến tính của các đặc trưng ban đầu để tối đa hóa sự khác biệt giữa các lớp.
    *   *Independent Component Analysis (ICA)*:  Phân tách tín hiệu thành các thành phần độc lập.
    *   *Autoencoders*:  Sử dụng mạng nơ-ron để học biểu diễn nén của dữ liệu.

**Tóm tắt:**

| Đặc điểm         | Feature Selection                               | Feature Extraction                               |
| ---------------- | --------------------------------------------- | ----------------------------------------------- |
| Mục tiêu         | Chọn đặc trưng quan trọng nhất, loại bỏ đặc trưng không liên quan | Tạo đặc trưng mới từ đặc trưng ban đầu            |
| Cách thức thực hiện | Chọn một tập con các đặc trưng hiện có       | Biến đổi hoặc kết hợp các đặc trưng hiện có   |
| Kết quả          | Tập con các đặc trưng ban đầu                 | Tập các đặc trưng mới                             |

**Ví dụ:**

*   **Feature Selection:**  Trong bài toán dự đoán giá nhà, bạn có thể chọn các đặc trưng như diện tích, số phòng ngủ, vị trí, và loại bỏ các đặc trưng ít quan trọng hơn như màu sơn tường.
*   **Feature Extraction:**  Trong bài toán nhận dạng khuôn mặt, bạn có thể sử dụng PCA để giảm chiều dữ liệu của ảnh khuôn mặt và tạo ra các đặc trưng mới đại diện cho khuôn mặt.

#### Example: Visually detecting redundant features

```python
# Create a pairplot and color the points using the 'Gender' feature
sns.pairplot(ansur_df_1, hue='Gender', diag_kind='hist')

# Show the plot
plt.show()
```

![]({{site.baseurl}}/images/redundant_feature.svg)

```python
# Remove one of the redundant features
reduced_df = ansur_df_1.drop('stature_m', axis=1)

# Create a pairplot and color the points using the 'Gender' feature
sns.pairplot(reduced_df, hue='Gender')

# Show the plot
plt.show()
```

![]({{site.baseurl}}/images/redundant_feature_1.svg)


### t-SNE visualization of high-dimensional data (Trực quan hóa dữ liệu nhiều chiều bằng t-SNE)

Dữ liệu trong các bài toán học máy thường có nhiều chiều (high-dimensional), ví dụ như ảnh (mỗi pixel là một chiều), văn bản (mỗi từ là một chiều), hoặc dữ liệu gen.  Việc trực quan hóa dữ liệu nhiều chiều để hiểu cấu trúc và phân bố của dữ liệu là một thách thức.  t-SNE (t-distributed Stochastic Neighbor Embedding) là một thuật toán giảm chiều dữ liệu (dimensionality reduction) và trực quan hóa dữ liệu rất hiệu quả, đặc biệt cho dữ liệu nhiều chiều.

**Ý tưởng chính của t-SNE:**

t-SNE chuyển đổi dữ liệu nhiều chiều thành dữ liệu hai hoặc ba chiều (thường là hai chiều để dễ dàng hiển thị trên mặt phẳng) sao cho các điểm dữ liệu *gần nhau* trong không gian nhiều chiều cũng *gần nhau* trong không gian hai chiều, và ngược lại.  Nói cách khác, t-SNE cố gắng *bảo toàn cấu trúc lân cận* của dữ liệu.

**Các bước chính của t-SNE:**

1.  **Tính toán độ tương tự (Similarity Calculation):**  t-SNE tính toán độ tương tự giữa các điểm dữ liệu trong không gian nhiều chiều.  Nó sử dụng một phân bố Gaussian để đo lường xác suất một điểm dữ liệu sẽ chọn một điểm dữ liệu khác làm "hàng xóm" của nó.

2.  **Chuyển đổi sang không gian chiều thấp (Dimensionality Reduction):**  t-SNE sử dụng một phân bố t-Student để mô hình hóa khoảng cách giữa các điểm dữ liệu trong không gian chiều thấp.  Mục tiêu là *tối thiểu hóa sự khác biệt* giữa phân bố xác suất trong không gian nhiều chiều và phân bố t-Student trong không gian chiều thấp.  Việc tối thiểu hóa này thường được thực hiện bằng thuật toán *gradient descent*.

3.  **Trực quan hóa (Visualization):**  Dữ liệu hai chiều (hoặc ba chiều) kết quả có thể được vẽ trên biểu đồ để trực quan hóa.

**Ưu điểm của t-SNE:**

*   Hiệu quả trong việc trực quan hóa dữ liệu nhiều chiều.
*   Bảo toàn cấu trúc lân cận của dữ liệu, giúp phát hiện các cụm, nhóm trong dữ liệu.
*   Có thể xử lý dữ liệu có kích thước lớn.

**Nhược điểm của t-SNE:**

*   Tốn kém tính toán, đặc biệt cho dữ liệu rất lớn.
*   Kết quả có thể khác nhau mỗi lần chạy do tính ngẫu nhiên của thuật toán.
*   Khó diễn giải ý nghĩa của các trục trong không gian chiều thấp.  t-SNE chỉ tập trung vào bảo toàn cấu trúc lân cận, không bảo toàn cấu trúc tổng thể của dữ liệu.
*   Không phù hợp cho các bài toán mà khoảng cách giữa các điểm dữ liệu có ý nghĩa quan trọng.

**Ứng dụng của t-SNE:**

*   Phân cụm dữ liệu (Clustering):  Giúp trực quan hóa kết quả phân cụm.
*   Phát hiện bất thường (Anomaly Detection):  Giúp phát hiện các điểm dữ liệu bất thường.
*   Xử lý ảnh và video:  Trực quan hóa các đặc trưng của ảnh và video.
*   Xử lý ngôn ngữ tự nhiên:  Trực quan hóa các biểu diễn vector của từ hoặc văn bản.

**Lưu ý khi sử dụng t-SNE:**

*   Nên thử nhiều lần chạy với các tham số khác nhau (ví dụ: *perplexity*) để có cái nhìn tổng quan về dữ liệu.
*   Không nên diễn giải ý nghĩa của các trục trong không gian chiều thấp.
*   t-SNE chỉ là một công cụ trực quan hóa, không phải là một thuật toán phân cụm.

#### Example - Fitting t-SNE to the ANSUR data

```python
from sklearn.manifold import TSNE

# Non-numerical columns in the dataset
non_numeric = ['Branch', 'Gender', 'Component']

# Drop the non-numerical columns from df
df_numeric = df.drop(non_numeric, axis=1)

# Create a t-SNE model with learning rate 50
m = TSNE(learning_rate=50)

# Fit and transform the t-SNE model on the numeric dataset
tsne_features = m.fit_transform(df_numeric)
print(tsne_features.shape)
```

#### t-SNE visualisation of dimensionality

```python
df['x'] = tsne_features[:,0]
df['y'] = tsne_features[:,1]

# Color the points by Army Branch
sns.scatterplot(x="x", y="y", hue='Component', data=df)
# Show the plot
plt.show()
```

![]({{site.baseurl}}/images/redundant_feature_2.svg)


```python
# Color the points by Army Branch
sns.scatterplot(x="x", y="y", hue='Branch', data=df)

# Show the plot
plt.show()
```

![]({{site.baseurl}}/images/redundant_feature_3.svg)

```python

# Color the points by Gender
sns.scatterplot(x="x", y="y", hue='Gender', data=df)

# Show the plot
plt.show()
```

![]({{site.baseurl}}/images/redundant_feature_4.svg)

---
## Feature Selection I - Selecting for Feature Information

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C2.pdf)

### The curse of dimensionality (Lời nguyền chiều cao)

"Lời nguyền chiều cao" (The Curse of Dimensionality) là một thuật ngữ trong học máy mô tả các vấn đề phát sinh khi làm việc với dữ liệu có số chiều (số lượng đặc trưng - features) *quá lớn*.  Nó đề cập đến sự gia tăng độ phức tạp và giảm hiệu suất của các thuật toán học máy khi số chiều của dữ liệu tăng lên.

**Các vấn đề do Lời nguyền chiều cao gây ra:**

1.  **Sự thưa thớt của dữ liệu (Data Sparsity):**  Trong không gian nhiều chiều, các điểm dữ liệu trở nên "thưa thớt" hơn.  Để đạt được cùng một độ "đặc" của dữ liệu (ví dụ: để một mô hình học máy có đủ dữ liệu để học), bạn cần một lượng dữ liệu *lớn hơn theo cấp số nhân* khi số chiều tăng lên.  Điều này thường không khả thi trong thực tế.

2.  **Khoảng cách giữa các điểm dữ liệu (Distance between Data Points):**  Trong không gian nhiều chiều, khoảng cách giữa các điểm dữ liệu có xu hướng *tăng lên*.  Điều này có thể làm cho các thuật toán dựa trên khoảng cách (ví dụ: k-NN, clustering) hoạt động kém hiệu quả.  Các điểm dữ liệu có thể trông "gần nhau" hơn so với thực tế, và việc phân biệt giữa chúng trở nên khó khăn hơn.

3.  **Quá khớp (Overfitting):**  Với số chiều lớn, mô hình học máy có nhiều "tự do" hơn để "học thuộc lòng" dữ liệu huấn luyện.  Điều này dẫn đến *overfitting*, khi mô hình hoạt động rất tốt trên dữ liệu huấn luyện nhưng lại kém trên dữ liệu kiểm tra.  Mô hình quá phức tạp và không khái quát hóa tốt cho dữ liệu mới.

4.  **Tăng chi phí tính toán (Increased Computational Cost):**  Khi số chiều tăng lên, chi phí tính toán (ví dụ: thời gian huấn luyện mô hình, bộ nhớ cần thiết) cũng tăng lên đáng kể.  Một số thuật toán có thể trở nên không khả thi khi xử lý dữ liệu có chiều cao.

5.  **Khó khăn trong trực quan hóa (Difficulty in Visualization):**  Việc trực quan hóa dữ liệu trở nên khó khăn hơn khi số chiều vượt quá 2 hoặc 3.  Các phương pháp trực quan hóa thông thường không thể hiển thị dữ liệu một cách đầy đủ và chính xác.

**Các phương pháp giảm thiểu ảnh hưởng của Lời nguyền chiều cao:**

1.  **Lựa chọn đặc trưng (Feature Selection):**  Chọn ra một tập con các đặc trưng *quan trọng nhất* và loại bỏ các đặc trưng *ít quan trọng* hoặc *không liên quan*.

2.  **Khai thác đặc trưng (Feature Extraction):**  Tạo ra các đặc trưng *mới* từ các đặc trưng ban đầu bằng cách biến đổi hoặc kết hợp chúng.  Ví dụ: *Principal Component Analysis (PCA)*.

3.  **Chuẩn hóa dữ liệu (Regularization):**  Sử dụng các kỹ thuật chuẩn hóa (ví dụ: L1, L2 regularization) để giảm độ phức tạp của mô hình và tránh overfitting.

4.  **Giảm chiều dữ liệu (Dimensionality Reduction):**  Sử dụng các thuật toán giảm chiều dữ liệu (ví dụ: PCA, t-SNE) để giảm số chiều của dữ liệu trong khi vẫn giữ lại thông tin quan trọng.

5.  **Sử dụng các thuật toán phù hợp:**  Một số thuật toán học máy ít bị ảnh hưởng bởi Lời nguyền chiều cao hơn các thuật toán khác.

### Features with missing values or little variance

=> Giảm chiều dữ liệu bằng cách loại bỏ các features chứa nhiều dữ liệu bị thiếu và phương sai không đủ.

#### Finding a good variance threshold

```python
# Create the boxplot
head_df.boxplot()
plt.show()
```
![]({{site.baseurl}}/images/redundant_feature_6.svg)

```python
# Normalize the data
normalized_df = head_df / head_df.mean()
normalized_df.boxplot()
plt.show()
```

![]({{site.baseurl}}/images/redundant_feature_7.svg)

Print the variances of the normalized data.

```python
# Normalize the data
normalized_df = head_df / head_df.mean()
# Print the variances of the normalized data
print(normalized_df.var())
```

```bash
<script.py> output:
    headbreadth          1.679e-03
    headcircumference    1.030e-03
    headlength           1.868e-03
    tragiontopofhead     2.640e-03
    n_hairs              1.003e-08
    measurement_error    0.000e+00
    dtype: float64
```

#### Features with low variance

```python
from sklearn.feature_selection import VarianceThreshold

# Create a VarianceThreshold feature selector
sel = VarianceThreshold(threshold=0.001)

# Fit the selector to normalized head_df
sel.fit(head_df / head_df.mean())

# Create a boolean mask
mask = sel.get_support()

# Apply the mask to create a reduced DataFrame
reduced_df = head_df.loc[:, mask]

print(f"Dimensionality reduced from {head_df.shape[1]} to {reduced_df.shape[1]}.")
```

```bash
<script.py> output:
    Dimensionality reduced from 6 to 4.
```

#### Removing features with many missing values

```python
# Create a boolean mask on whether each feature less than 50% missing values.
mask = school_df.isna().sum() / len(school_df) < 0.5

# Create a reduced dataset by applying the mask
reduced_df = school_df.loc[:, mask]

print(school_df.shape)
print(reduced_df.shape)
```

```bash
<script.py> output:
    (131, 21)
    (131, 19)
```

### Pairwise correlation

#### Visualizing the correlation matrix

```python
# Create the correlation matrix
corr = ansur_df.corr()

# Draw a heatmap of the correlation matrix
sns.heatmap(corr,  cmap=cmap, center=0, linewidths=1, annot=True, fmt=".2f")
plt.show()
```

![]({{site.baseurl}}/images/corr1.svg)

```python
# Create the correlation matrix
corr = ansur_df.corr()

# Generate a mask for the upper triangle 
mask = np.triu(np.ones_like(corr, dtype=bool))

# Add the mask to the heatmap
sns.heatmap(corr, mask=mask, cmap=cmap, center=0, linewidths=1, annot=True, fmt=".2f")
plt.show()
```

Output:

```bash
<script.py> output:
    [[ True  True  True  True  True]
     [False  True  True  True  True]
     [False False  True  True  True]
     [False False False  True  True]
     [False False False False  True]]
```

![]({{site.baseurl}}/images/corr2.svg)

### Removing highly correlated features

#### Filtering out highly correlated features

```python
# Calculate the correlation matrix and take the absolute value
corr_df = ansur_df.corr().abs()

# Create a True/False mask and apply it
mask = np.triu(np.ones_like(corr_df, dtype=bool))
tri_df = corr_df.mask(mask)

# List column names of highly correlated features (r > 0.95)
to_drop = [c for c in tri_df.columns if any(tri_df[c] >  0.95)]

# Drop the features in the to_drop list
reduced_df = ansur_df.drop(to_drop, axis=1)

print(f"The reduced_df DataFrame has {reduced_df.shape[1]} columns.")
```

```bash
The reduced_df DataFrame has 88 columns.
```

#### Nuclear energy and pool drownings

```python
# Print the first five lines of weird_df
print(weird_df.head())
```

```bash
<script.py> output:
       pool_drownings  nuclear_energy
    0             421           728.3
    1             465           753.9
    2             494           768.8
    3             538           780.1
    4             430           763.7
```

```python
# Put nuclear energy production on the x-axis and the number of pool drownings on the y-axis
sns.scatterplot(x='nuclear_energy', y='pool_drownings', data=weird_df)
plt.show()
```

![]({{site.baseurl}}/images/corr3.svg)



---
## Feature Selection II - Selecting for Model Accuracy

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C3.pdf)

### Selecting features for model performance
### Tree-based feature selection
### Regularized linear regression
### Combining feature selectors

---
## Feature Extraction

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C4.pdf)

### Feature extraction
### Principal component analysis
### PCA applications
### Principal Component selection
