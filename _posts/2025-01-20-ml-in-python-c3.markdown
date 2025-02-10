---
layout: post
title: "UnSuppervised Learning in Python"
date: 2025-01-20 03:00:00 +0700
categories: machine learning in python
---

Hãy tưởng tượng bạn có một hộp đầy các loại kẹo với nhiều màu sắc và hình dạng khác nhau. Bạn muốn phân loại chúng mà không biết trước loại kẹo nào là gì. Học máy không giám sát giống như việc bạn tự phân loại kẹo dựa trên những đặc điểm quan sát được như màu sắc, hình dạng, kích thước... mà không cần ai cho biết trước đó là kẹo gì.

Ví dụ: Phân loại các bài báo tin tức thành các chủ đề khác nhau (thể thao, chính trị, kinh tế...) dựa trên nội dung của chúng mà không cần biết trước chủ đề của từng bài.

### Clustering for Dataset Exploration

[Slide]({{site.baseurl}}/files/UnsupervisedLearninginPython_C1.pdf)

- **Example scatter plot**

```python
import matplotlib.pyplot as plt

# Sample data
weight = [180, 120, 150, 160, 130]  # Trọng lượng của trái cây
color = [1, 2, 1, 1, 3]  # Màu sắc được mã hóa bằng số (ví dụ: 1: đỏ, 2: vàng, 3: xanh)
clusters = [0, 1, 0, 0, 1]  # Nhãn cụm (0 hoặc 1)

# Tạo scatter plot
plt.scatter(weight, color, c=clusters)  # 'c' chỉ định màu sắc dựa trên nhãn cụm

# Đặt tên cho các trục
plt.xlabel('Trọng lượng (gram)')
plt.ylabel('Màu sắc')

# Hiển thị plot
plt.show()
```

**Giải thích:**

* `matplotlib.pyplot` là thư viện Python dùng để vẽ đồ thị.
* `weight` và `color` là hai danh sách chứa dữ liệu về trọng lượng và màu sắc của trái cây.
* `clusters` là danh sách chứa nhãn cụm tương ứng với mỗi trái cây.
* `plt.scatter(weight, color, c=clusters)` tạo scatter plot với `weight` là trục hoành, `color` là trục tung, và màu sắc của các điểm được xác định bởi `clusters`.
* `plt.xlabel()` và `plt.ylabel()` đặt tên cho các trục.
* `plt.show()` hiển thị biểu đồ.

- **Clustering 2D points**

```python
# Import KMeans
from sklearn.cluster import KMeans

# Create a KMeans instance with 3 clusters: model
model = KMeans(n_clusters=3)

# Fit model to points
model.fit(points)

# Determine the cluster labels of new_points: labels
labels = model.predict(new_points)

# Print cluster labels of new_points
print(labels)
# Import pyplot
import matplotlib.pyplot as plt

# Assign the columns of new_points: xs and ys
xs = new_points[:, 0]
ys = new_points[:, 1]

# Make a scatter plot of xs and ys, using labels to define the colors
plt.scatter(xs, ys, c=labels, alpha=0.5)

# Assign the cluster centers: centroids
centroids = model.cluster_centers_

# Assign the columns of centroids: centroids_x, centroids_y
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]

# Make a scatter plot of centroids_x and centroids_y
plt.scatter(centroids_x, centroids_y, marker="D", s=50)
plt.show()

```

#### Evaluating the clustering

```python
# Import pyplot
import matplotlib.pyplot as plt

# Assign the columns of new_points: xs and ys
xs = new_points[:, 0]
ys = new_points[:, 1]

# Make a scatter plot of xs and ys, using labels to define the colors
plt.scatter(xs, ys, c=labels, alpha=0.5)

# Assign the cluster centers: centroids
centroids = model.cluster_centers_

# Assign the columns of centroids: centroids_x, centroids_y
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]

# Make a scatter plot of centroids_x and centroids_y
plt.scatter(centroids_x, centroids_y, marker="D", s=50)
plt.show()

```

```python
# Create a KMeans model with 3 clusters: model
model = KMeans(n_clusters=3)

# Use fit_predict to fit model and obtain cluster labels: labels
labels = model.fit_predict(samples)

# Create a DataFrame with labels and varieties as columns: df
df = pd.DataFrame({'labels': labels, 'varieties': varieties})

# Create crosstab: ct
ct = pd.crosstab(df['labels'], df['varieties'])

# Display ct
print(ct)

```

#### Transforming feature for better clusterings

```python
# Perform the necessary imports
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
import pandas as pd

# Create scaler: scaler
scaler = StandardScaler()

# Create KMeans instance: kmeans
kmeans = KMeans(n_clusters=4)

# Create pipeline: pipeline
pipeline = make_pipeline(scaler, kmeans)

# Fit the pipeline to samples
pipeline.fit(samples)

# Calculate the cluster labels: labels
labels = pipeline.predict(samples)

# Create a DataFrame with labels and species as columns: df
df = pd.DataFrame({"labels": labels, "species":species})

# Create crosstab: ct
ct = pd.crosstab(df['labels'], df['species'])

# Display ct
print(ct)

```

---
### Visualization with Hierarchical Clustering and t-SNE

[Slide]({{site.baseurl}}/files/UnsupervisedLearninginPython_C2.pdf)

#### Visualizing hierarchies

- **Hierarchical clustering of the grain data**

```python
# Perform the necessary imports
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# Calculate the linkage: mergings
mergings = linkage(samples, method='complete')

# Plot the dendrogram, using varieties as labels
dendrogram(mergings,
           labels=varieties,
           leaf_rotation=90,
           leaf_font_size=6,
)
plt.show()
```

**output**

![]({{site.baseurl}}/images/sample.svg)

- **Hierarchies of stocks**

```python
# Import normalize
from sklearn.preprocessing import normalize

# Normalize the movements: normalized_movements
normalized_movements = normalize(movements)

# Calculate the linkage: mergings
mergings = linkage(normalized_movements, method="complete")

# Plot the dendrogram
dendrogram(
    mergings,
    labels=companies,
    leaf_rotation=90,
    leaf_font_size=6
)

plt.show()

```

**Output**

![]({{site.baseurl}}/images/sample2.svg)

#### Cluster labels in hierarchical clustering

#### t-SNE for 2-dimensional maps

---
### Decorrelating Your Data and Dimension Reduction

---
### Discovering Interpretable Features