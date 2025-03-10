---
layout: post
title: "Dimensionality Reduction in Python"
date: 2025-01-20 09:00:00 +0700
categories: machine learning in python
---

High-dimensional datasets can be overwhelming and leave you not knowing where to start. Typically, you’d visually explore a new dataset first, but when you have too many dimensions the classical approaches will seem insufficient. Fortunately, there are visualization techniques designed specifically for high dimensional data and you’ll be introduced to these in this course. After exploring the data, you’ll often find that many features hold little information because they don’t show any variance or because they are duplicates of other features. 

### Table of content 

1. [Exploring High Dimensional Data](#ExploringHighDimensionalData)
	* 1.1. [Feature selection vs. feature extraction](#Featureselectionvs.featureextraction)
		* 1.1.1. [Example: Visually detecting redundant features](#Example:Visuallydetectingredundantfeatures)
	* 1.2. [t-SNE visualization of high-dimensional data (Trực quan hóa dữ liệu nhiều chiều bằng t-SNE)](#t-SNEvisualizationofhigh-dimensionaldataTrcquanhadliunhiuchiubngt-SNE)
		* 1.2.1. [Example - Fitting t-SNE to the ANSUR data](#Example-Fittingt-SNEtotheANSURdata)
		* 1.2.2. [t-SNE visualisation of dimensionality](#t-SNEvisualisationofdimensionality)
2. [Feature Selection I - Selecting for Feature Information](#FeatureSelectionI-SelectingforFeatureInformation)
	* 2.1. [The curse of dimensionality (Lời nguyền chiều cao)](#ThecurseofdimensionalityLinguynchiucao)
	* 2.2. [Features with missing values or little variance](#Featureswithmissingvaluesorlittlevariance)
		* 2.2.1. [Finding a good variance threshold](#Findingagoodvariancethreshold)
		* 2.2.2. [Features with low variance](#Featureswithlowvariance)
		* 2.2.3. [Removing features with many missing values](#Removingfeatureswithmanymissingvalues)
	* 2.3. [Pairwise correlation](#Pairwisecorrelation)
		* 2.3.1. [Visualizing the correlation matrix](#Visualizingthecorrelationmatrix)
	* 2.4. [Removing highly correlated features](#Removinghighlycorrelatedfeatures)
		* 2.4.1. [Filtering out highly correlated features](#Filteringouthighlycorrelatedfeatures)
		* 2.4.2. [Nuclear energy and pool drownings](#Nuclearenergyandpooldrownings)
3. [Feature Selection II - Selecting for Model Accuracy](#FeatureSelectionII-SelectingforModelAccuracy)
	* 3.1. [Selecting features for model performance](#Selectingfeaturesformodelperformance)
		* 3.1.1. [Example 1 - Building a diabetes classifier](#Example1-Buildingadiabetesclassifier)
		* 3.1.2. [Example 2 - Manual Recursive Feature Elimination](#Example2-ManualRecursiveFeatureElimination)
		* 3.1.3. [Example 3 - Automatic Recursive Feature Elimination](#Example3-AutomaticRecursiveFeatureElimination)
	* 3.2. [Tree-based feature selection](#Tree-basedfeatureselection)
		* 3.2.1. [Building a random forest model](#Buildingarandomforestmodel)
		* 3.2.2. [Random forest for feature selection](#Randomforestforfeatureselection)
		* 3.2.3. [Random forest for feature selection](#Randomforestforfeatureselection-1)
		* 3.2.4. [Recursive Feature Elimination with random forests](#RecursiveFeatureEliminationwithrandomforests)
	* 3.3. [Regularized linear regression](#Regularizedlinearregression)
		* 3.3.1. [Creating a LASSO regressor](#CreatingaLASSOregressor)
		* 3.3.2. [Lasso model results](#Lassomodelresults)
		* 3.3.3. [Adjusting the regularization strength](#Adjustingtheregularizationstrength)
	* 3.4. [Combining feature selectors](#Combiningfeatureselectors)
		* 3.4.1. [Creating a LassoCV regressor](#CreatingaLassoCVregressor)
		* 3.4.2. [Ensemble models for extra votes](#Ensemblemodelsforextravotes)
		* 3.4.3. [Combining 3 feature selectors](#Combining3featureselectors)
4. [Feature Extraction](#FeatureExtraction)
	* 4.1. [Feature extraction](#Featureextraction)
		* 4.1.1. [Manual feature extraction I](#ManualfeatureextractionI)
		* 4.1.2. [Manual feature extraction II](#ManualfeatureextractionII)
	* 4.2. [Principal component analysis](#Principalcomponentanalysis)
		* 4.2.1. [Calculating Principal Components](#CalculatingPrincipalComponents)
	* 4.3. [PCA applications](#PCAapplications)
		* 4.3.1. [Understanding the components](#Understandingthecomponents)
	* 4.4. [Principal Component selection](#PrincipalComponentselection)
		* 4.4.1. [Selecting the proportion of variance to keep](#Selectingtheproportionofvariancetokeep)
		* 4.4.2. [Choosing the number of components](#Choosingthenumberofcomponents)
		* 4.4.3. [PCA for image compression](#PCAforimagecompression)


##  1. <a name='ExploringHighDimensionalData'></a>Exploring High Dimensional Data

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C1.pdf)

###  1.1. <a name='Featureselectionvs.featureextraction'></a>Feature selection vs. feature extraction

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

####  1.1.1. <a name='Example:Visuallydetectingredundantfeatures'></a>Example: Visually detecting redundant features

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


###  1.2. <a name='t-SNEvisualizationofhigh-dimensionaldataTrcquanhadliunhiuchiubngt-SNE'></a>t-SNE visualization of high-dimensional data (Trực quan hóa dữ liệu nhiều chiều bằng t-SNE)

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

####  1.2.1. <a name='Example-Fittingt-SNEtotheANSURdata'></a>Example - Fitting t-SNE to the ANSUR data

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

####  1.2.2. <a name='t-SNEvisualisationofdimensionality'></a>t-SNE visualisation of dimensionality

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
##  2. <a name='FeatureSelectionI-SelectingforFeatureInformation'></a>Feature Selection I - Selecting for Feature Information

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C2.pdf)

###  2.1. <a name='ThecurseofdimensionalityLinguynchiucao'></a>The curse of dimensionality (Lời nguyền chiều cao)

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

###  2.2. <a name='Featureswithmissingvaluesorlittlevariance'></a>Features with missing values or little variance

=> Giảm chiều dữ liệu bằng cách loại bỏ các features chứa nhiều dữ liệu bị thiếu và phương sai không đủ.

####  2.2.1. <a name='Findingagoodvariancethreshold'></a>Finding a good variance threshold

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

####  2.2.2. <a name='Featureswithlowvariance'></a>Features with low variance

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

####  2.2.3. <a name='Removingfeatureswithmanymissingvalues'></a>Removing features with many missing values

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

###  2.3. <a name='Pairwisecorrelation'></a>Pairwise correlation

####  2.3.1. <a name='Visualizingthecorrelationmatrix'></a>Visualizing the correlation matrix

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

###  2.4. <a name='Removinghighlycorrelatedfeatures'></a>Removing highly correlated features

####  2.4.1. <a name='Filteringouthighlycorrelatedfeatures'></a>Filtering out highly correlated features

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

####  2.4.2. <a name='Nuclearenergyandpooldrownings'></a>Nuclear energy and pool drownings

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
##  3. <a name='FeatureSelectionII-SelectingforModelAccuracy'></a>Feature Selection II - Selecting for Model Accuracy

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C3.pdf)

###  3.1. <a name='Selectingfeaturesformodelperformance'></a>Selecting features for model performance

Phương pháp này sẽ sử dụng model để train với toàn bộ các feature, dựa vào hệ số `coef` (gần bằng 0) sẽ quyết định được feature nào ít ảnh hưởng tới kết quả,
qua đó sẽ lọai bỏ các tính năng ít quan trọng

####  3.1.1. <a name='Example1-Buildingadiabetesclassifier'></a>Example 1 - Building a diabetes classifier

```python
# Fit the scaler on the training features and transform these in one go
X_train_std = scaler.fit_transform(X_train)

# Fit the logistic regression model on the scaled training data
lr.fit(X_train_std, y_train)

# Scale the test features
X_test_std = scaler.transform(X_test)

# Predict diabetes presence on the scaled test set
y_pred = lr.predict(X_test_std)

# Prints accuracy metrics and feature coefficients
print(f"{accuracy_score(y_test, y_pred):.1%} accuracy on test set.")
print(dict(zip(X.columns, abs(lr.coef_[0]).round(2))))
```

Output

```bash
<script.py> output:
    79.6% accuracy on test set.
    {'pregnant': 0.05, 'glucose': 1.23, 'diastolic': 0.03, 'triceps': 0.24, 'insulin': 0.19, 'bmi': 0.38, 'family': 0.35, 'age': 0.34}
```

####  3.1.2. <a name='Example2-ManualRecursiveFeatureElimination'></a>Example 2 - Manual Recursive Feature Elimination

remove the feature with the lowest model coefficient

```python
# Remove the feature with the lowest model coefficient
X = diabetes_df[['pregnant', 'glucose', 'triceps', 'insulin', 'bmi', 'family', 'age']]

# Performs a 25-75% train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Scales features and fits the logistic regression model
lr.fit(scaler.fit_transform(X_train), y_train)

# Calculates the accuracy on the test set and prints coefficients
acc = accuracy_score(y_test, lr.predict(scaler.transform(X_test)))
print(f"{acc:.1%} accuracy on test set.") 
print(dict(zip(X.columns, abs(lr.coef_[0]).round(2))))
```

```bash 
80.6% accuracy on test set.
{'pregnant': 0.05, 'glucose': 1.24, 'triceps': 0.24, 'insulin': 0.2, 'bmi': 0.39, 'family': 0.34, 'age': 0.35}
```

Remove 2 more features with the lowest model coefficients.

```python
# Remove the 2 features with the lowest model coefficients
X = diabetes_df[['glucose', 'triceps', 'bmi', 'family', 'age']]

# Performs a 25-75% train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Scales features and fits the logistic regression model
lr.fit(scaler.fit_transform(X_train), y_train)

# Calculates the accuracy on the test set and prints coefficients
acc = accuracy_score(y_test, lr.predict(scaler.transform(X_test)))
print(f"{acc:.1%} accuracy on test set.") 
print(dict(zip(X.columns, abs(lr.coef_[0]).round(2))))
```

```bash
79.6% accuracy on test set.
{'glucose': 1.13, 'triceps': 0.25, 'bmi': 0.34, 'family': 0.34, 'age': 0.37}
```

Run the code and only keep the feature with the highest coefficient.

```python
# Only keep the feature with the highest coefficient
X = diabetes_df[['glucose']]

# Performs a 25-75% train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Scales features and fits the logistic regression model to the data
lr.fit(scaler.fit_transform(X_train), y_train)

# Calculates the accuracy on the test set and prints coefficients
acc = accuracy_score(y_test, lr.predict(scaler.transform(X_test)))
print(f"{acc:.1%} accuracy on test set.")  
print(dict(zip(X.columns, abs(lr.coef_[0]).round(2))))
```

```bash 
<script.py> output:
    75.5% accuracy on test set.
    {'glucose': 1.28}
```

####  3.1.3. <a name='Example3-AutomaticRecursiveFeatureElimination'></a>Example 3 - Automatic Recursive Feature Elimination

```python
from sklearn.feature_selection import RFE

# Create the RFE with a LogisticRegression estimator and 3 features to select
rfe = RFE(estimator=LogisticRegression(), n_features_to_select=3, verbose=1)

# Fits the eliminator to the data
rfe.fit(X_train, y_train)

# Print the features and their ranking (high = dropped early on)
print(dict(zip(X.columns, rfe.ranking_)))

# Print the features that are not eliminated
print(X.columns[rfe.support_])

# Calculates the test set accuracy
acc = accuracy_score(y_test, rfe.predict(X_test))
print(f"{acc:.1%} accuracy on test set.") 
```

```bash
Fitting estimator with 8 features.
Fitting estimator with 7 features.
Fitting estimator with 6 features.
Fitting estimator with 5 features.
Fitting estimator with 4 features.
{'pregnant': 5, 'glucose': 1, 'diastolic': 6, 'triceps': 3, 'insulin': 4, 'bmi': 1, 'family': 2, 'age': 1}
Index(['glucose', 'bmi', 'age'], dtype='object')
80.6% accuracy on test set
```

###  3.2. <a name='Tree-basedfeatureselection'></a>Tree-based feature selection

####  3.2.1. <a name='Buildingarandomforestmodel'></a>Building a random forest model

```python
# Perform a 75% training and 25% test data split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Fit the random forest model to the training data
rf = RandomForestClassifier(random_state=0)
rf.fit(X_train, y_train)

# Calculate the accuracy
acc = accuracy_score(rf.predict(X_test), y_test)

# Print the importances per feature
print(dict(zip(X.columns, rf.feature_importances_.round(2))))

# Print accuracy
print(f"{acc:.1%} accuracy on test set.") 
```

```bash
<script.py> output:
    {'pregnant': 0.07, 'glucose': 0.25, 'diastolic': 0.09, 'triceps': 0.09, 'insulin': 0.14, 'bmi': 0.12, 'family': 0.12, 'age': 0.13}
    79.6% accuracy on test set.
```

####  3.2.2. <a name='Randomforestforfeatureselection'></a>Random forest for feature selection

```python 
# Create a mask for features importances above the threshold
mask = rf.feature_importances_ > 0.15

# Prints out the mask
print(mask)
```

```bash 
[False  True False False False False False  True]
```

####  3.2.3. <a name='Randomforestforfeatureselection-1'></a>Random forest for feature selection

```python 
# Create a mask for features importances above the threshold
mask = rf.feature_importances_ > 0.15

# Apply the mask to the feature dataset X
reduced_X = X.loc[:, mask]

# prints out the selected column names
print(reduced_X.columns)
```

```bash 
Index(['glucose', 'age'], dtype='object')
```

####  3.2.4. <a name='RecursiveFeatureEliminationwithrandomforests'></a>Recursive Feature Elimination with random forests

```python 
from sklearn.feature_selection import RFE

# Wrap the feature eliminator around the random forest model
# Có thể bổ xung param: step=10 để tốc độ nhanh hơn, mỗi vòng lặp sẽ loại đi 10 features cho đến khi đến số lượng chỉ định. 
rfe = RFE(estimator=RandomForestClassifier(), n_features_to_select=2, verbose=1)

# Fit the model to the training data
rfe.fit(X_train, y_train)

# Create a mask using the support_ attribute of rfe
mask = rfe.support_

# Apply the mask to the feature dataset X and print the result
reduced_X = X.loc[:, mask]
print(reduced_X.columns)
```

```bash 
Fitting estimator with 8 features.
Fitting estimator with 7 features.
Fitting estimator with 6 features.
Fitting estimator with 5 features.
Fitting estimator with 4 features.
Fitting estimator with 3 features.
Index(['glucose', 'insulin'], dtype='object')
```

###  3.3. <a name='Regularizedlinearregression'></a>Regularized linear regression

####  3.3.1. <a name='CreatingaLASSOregressor'></a>Creating a LASSO regressor

```python
# Set the test size to 30% to get a 70-30% train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Fit the scaler on the training features and transform these in one go
X_train_std = scaler.fit_transform(X_train)

# Create the Lasso model
la = Lasso()

# Fit it to the standardized training data
la.fit(X_train_std, y_train)
```

####  3.3.2. <a name='Lassomodelresults'></a>Lasso model results

```python
# Transform the test set with the pre-fitted scaler
X_test_std = scaler.transform(X_test)

# Calculate the coefficient of determination (R squared) on X_test_std
r_squared = la.score(X_test_std, y_test)
print(f"The model can predict {r_squared:.1%} of the variance in the test set.")

# Create a list that has True values when coefficients equal 0
zero_coef = la.coef_ == 0

# Calculate how many features have a zero coefficient
n_ignored = sum(zero_coef)
print(f"The model has ignored {n_ignored} out of {len(la.coef_)} features.")
```

```bash
The model can predict 84.7% of the variance in the test set.
The model has ignored 82 out of 91 features.
```

####  3.3.3. <a name='Adjustingtheregularizationstrength'></a>Adjusting the regularization strength

```python 
# Find the highest alpha value with R-squared above 98%
la = Lasso(alpha=0.1, random_state=0)

# Fits the model and calculates performance stats
la.fit(X_train_std, y_train)
r_squared = la.score(X_test_std, y_test)
n_ignored_features = sum(la.coef_ == 0)

# Print peformance stats 
print(f"The model can predict {r_squared:.1%} of the variance in the test set.")
print(f"{n_ignored_features} out of {len(la.coef_)} features were ignored.")
```

```bash 
The model can predict 98.3% of the variance in the test set.
64 out of 91 features were ignored
```

###  3.4. <a name='Combiningfeatureselectors'></a>Combining feature selectors

####  3.4.1. <a name='CreatingaLassoCVregressor'></a>Creating a LassoCV regressor

```python
from sklearn.linear_model import LassoCV

# Create and fit the LassoCV model on the training set
lcv = LassoCV()
lcv.fit(X_train, y_train)
print(f'Optimal alpha = {lcv.alpha_:.3f}')

# Calculate R squared on the test set
r_squared = lcv.score(X_test, y_test)
print(f'The model explains {r_squared:.1%} of the test set variance')

# Create a mask for coefficients not equal to zero
lcv_mask = lcv.coef_ != 0
print(f'{sum(lcv_mask)} features out of {len(lcv_mask)} selected')
``` 

```bash 
Optimal alpha = 0.097
The model explains 87.4% of the test set variance
22 features out of 32 selected
``` 

####  3.4.2. <a name='Ensemblemodelsforextravotes'></a>Ensemble models for extra votes

```python 
from sklearn.feature_selection import RFE
from sklearn.ensemble import GradientBoostingRegressor

# Select 10 features with RFE on a GradientBoostingRegressor, drop 3 features on each step
rfe_gb = RFE(estimator=GradientBoostingRegressor(), 
             n_features_to_select=10, step=3, verbose=1)
rfe_gb.fit(X_train, y_train)

# Calculate the R squared on the test set
r_squared = rfe_gb.score(X_test, y_test)
print(f'The model can explain {r_squared:.1%} of the variance in the test set')

# Assign the support array to gb_mask
gb_mask = rfe_gb.support_
```

```bash 
Fitting estimator with 32 features.
Fitting estimator with 29 features.
Fitting estimator with 26 features.
Fitting estimator with 23 features.
Fitting estimator with 20 features.
Fitting estimator with 17 features.
Fitting estimator with 14 features.
Fitting estimator with 11 features.
The model can explain 85.2% of the variance in the test set
```

```python 
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor

# Select 10 features with RFE on a RandomForestRegressor, drop 3 features on each step
rfe_rf = RFE(estimator=RandomForestRegressor(), 
             n_features_to_select=10, step=3, verbose=1)
rfe_rf.fit(X_train, y_train)

# Calculate the R squared on the test set
r_squared = rfe_rf.score(X_test, y_test)
print(f'The model can explain {r_squared:.1%} of the variance in the test set')

# Assign the support array to rf_mask
rf_mask = rfe_rf.support_
```

```bash 
<script.py> output:
    Fitting estimator with 32 features.
    Fitting estimator with 29 features.
    Fitting estimator with 26 features.
    Fitting estimator with 23 features.
    Fitting estimator with 20 features.
    Fitting estimator with 17 features.
    Fitting estimator with 14 features.
    Fitting estimator with 11 features.
    The model can explain 84.4% of the variance in the test set
```

####  3.4.3. <a name='Combining3featureselectors'></a>Combining 3 feature selectors

```python 
# Sum the votes of the three models
votes = np.sum([lcv_mask, rf_mask, gb_mask], axis=0)

# Create a mask for features selected by all 3 models
meta_mask = votes == 3

# Apply the dimensionality reduction on X
X_reduced = X.loc[:, meta_mask]

# Plug the reduced dataset into a linear regression pipeline
X_train, X_test, y_train, y_test = train_test_split(X_reduced, y, test_size=0.3, random_state=0)
lm.fit(scaler.fit_transform(X_train), y_train)
r_squared = lm.score(scaler.transform(X_test), y_test)
print(f'The model can explain {r_squared:.1%} of the variance in the test set using {len(lm.coef_)} features.')
```

```bash
<script.py> output:
    The model can explain 86.7% of the variance in the test set using 7 features.
```

---
##  4. <a name='FeatureExtraction'></a>Feature Extraction

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C4.pdf)

###  4.1. <a name='Featureextraction'></a>Feature extraction

####  4.1.1. <a name='ManualfeatureextractionI'></a>Manual feature extraction I

```python
# Calculate the price from the quantity sold and revenue
sales_df['price'] = sales_df['revenue'] / sales_df['quantity']

# Drop the quantity and revenue features
reduced_df = sales_df.drop(['quantity', 'revenue'], axis=1)

print(reduced_df.head())
```

####  4.1.2. <a name='ManualfeatureextractionII'></a>Manual feature extraction II

```python 
# Calculate the mean height
height_df['height'] = height_df[['height_1', 'height_2', 'height_3']].mean(axis=1)

# Drop the 3 original height features
reduced_df = height_df.drop(['height_1', 'height_2', 'height_3'], axis=1)

print(reduced_df.head())
```

###  4.2. <a name='Principalcomponentanalysis'></a>Principal component analysis

####  4.2.1. <a name='CalculatingPrincipalComponents'></a>Calculating Principal Components

```python 
# Create a pairplot to inspect ansur_df
sns.pairplot(ansur_df)

plt.show()
```

![]({{site.baseurl}}/images/pca1.svg)

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Create the scaler
scaler = StandardScaler()
ansur_std = scaler.fit_transform(ansur_df)

# Create the PCA instance and fit and transform the data with pca
pca = PCA()
pc = pca.fit_transform(ansur_std)
pc_df = pd.DataFrame(pc, columns=['PC 1', 'PC 2', 'PC 3', 'PC 4'])

# Create a pairplot of the principal component DataFrame
sns.pairplot(pc_df)
plt.show()
```

![]({{site.baseurl}}/images/pca2.svg)


###  4.3. <a name='PCAapplications'></a>PCA applications

####  4.3.1. <a name='Understandingthecomponents'></a>Understanding the components

```python 
# Build the pipeline
pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=2))])

# Fit it to the dataset and extract the component vectors
pipe.fit(poke_df)
vectors = pipe['reducer'].components_.round(2)

# Print feature effects
print('PC 1 effects = ' + str(dict(zip(poke_df.columns, vectors[0]))))
print('PC 2 effects = ' + str(dict(zip(poke_df.columns, vectors[1]))))
```

```bash
PC 1 effects = {'HP': 0.39, 'Attack': 0.44, 'Defense': 0.36, 'Sp. Atk': 0.46, 'Sp. Def': 0.45, 'Speed': 0.34}
PC 2 effects = {'HP': 0.08, 'Attack': -0.01, 'Defense': 0.63, 'Sp. Atk': -0.31, 'Sp. Def': 0.24, 'Speed': -0.67}
```

###  4.4. <a name='PrincipalComponentselection'></a>Principal Component selection

####  4.4.1. <a name='Selectingtheproportionofvariancetokeep'></a>Selecting the proportion of variance to keep

```python
# Pipe a scaler to PCA selecting 80% of the variance
pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=0.8))])

# Fit the pipe to the data
pipe.fit(ansur_df)

print(f'{len(pipe["reducer"].components_)} components selected')
```

```bash
11 components selected
```

```python 
# Let PCA select 90% of the variance
pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=0.9))])

# Fit the pipe to the data
pipe.fit(ansur_df)

print(f'{len(pipe["reducer"].components_)} components selected')
```

```bash 
23 components selected
```

####  4.4.2. <a name='Choosingthenumberofcomponents'></a>Choosing the number of components

```python
# Pipeline a scaler and pca selecting 10 components
pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=10))])

# Fit the pipe to the data
pipe.fit(ansur_df)

# Plot the explained variance ratio
plt.plot(pipe['reducer'].explained_variance_ratio_)

plt.xlabel('Principal component index')
plt.ylabel('Explained variance ratio')
plt.show()
```

![]({{site.baseurl}}/images/pca3.svg)

####  4.4.3. <a name='PCAforimagecompression'></a>PCA for image compression

```python
# Plot the MNIST sample data
plot_digits(X_test)
```

![]({{site.baseurl}}/images/pca4.svg)

```python 
# Transform the input data to principal components
pc = pipe.transform(X_test)

# Inverse transform the components to original feature space
X_rebuilt = pipe.inverse_transform(pc)

# Plot the reconstructed data
plot_digits(X_rebuilt)
```

![]({{site.baseurl}}/images/pca5.svg)