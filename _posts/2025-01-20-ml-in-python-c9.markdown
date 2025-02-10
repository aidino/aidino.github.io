---
layout: post
title: "Cluster Analysis in Python"
date: 2025-01-20 08:00:00 +0700
categories: machine learning in python
---

In this course, you will be introduced to unsupervised learning through clustering using the SciPy library in Python. This course covers pre-processing of data and application of hierarchical and k-means clustering. Through the course, you will explore player statistics from a popular football video game, FIFA 18. After completing the course, you will be able to quickly apply various clustering algorithms on data, visualize the clusters formed and analyze results.


## Introduction to Clustering

[Slide]({{site.baseurl}}/files/Cluster_Analysis_in_Python_C1.pdf)

### Basics of cluster analysis

#### Example - Pokémon sightings: hierarchical clustering

```python
# Import linkage and fcluster functions
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib import pyplot as plt
import seaborn as sns, pandas as pd

# Use the linkage() function to compute distance
Z = linkage(df, 'ward')

# Generate cluster labels
df['cluster_labels'] = fcluster(Z, 2, criterion='maxclust')

# Plot the points with seaborn
sns.scatterplot(x='x', y='y', hue='cluster_labels', data=df)
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster1.svg)

#### Example - Pokémon sightings: k-means clustering

```python
# Import kmeans and vq functions
from scipy.cluster.vq import kmeans, vq
from matplotlib import pyplot as plt
import seaborn as sns, pandas as pd

# Compute cluster centers
centroids,_ = kmeans(df, 2)

# Assign cluster labels
df['cluster_labels'], _ = vq(df, centroids)

# Plot the points with seaborn
sns.scatterplot(x='x', y='y', hue='cluster_labels', data=df)
plt.show()
```

Output

![]({{site.baseurl}}/images/cluster2.svg)


### Data preparation for cluster analysis 

#### Example - Normalize basic list data (scipy)

```python
# Import the whiten function
from scipy.cluster.vq import whiten

goals_for = [4,3,2,3,1,1,2,0,1,4]

# Use the whiten() function to standardize the data
scaled_data = whiten(goals_for)
print(scaled_data)
```

#### Example - Visualize normalized data

```python
# Plot original data
plt.plot(goals_for, label='original')

# Plot scaled data
plt.plot(scaled_data, label='scaled')

# Show the legend in the plot
plt.legend()

# Display the plot
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster3.svg)

#### Example - Normalization of small numbers

In earlier examples, you have normalization of whole numbers. In this exercise, you will look at the treatment of fractional numbers - the change of interest rates in the country of Bangalla over the years. 

```python
# Prepare data
rate_cuts = [0.0025, 0.001, -0.0005, -0.001, -0.0005, 0.0025, -0.001, -0.0015, -0.001, 0.0005]

# Use the whiten() function to standardize the data
scaled_data = whiten(rate_cuts)

# Plot original data
plt.plot(rate_cuts, label='original')

# Plot scaled data
plt.plot(scaled_data, label='scaled')

plt.legend()
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster4.svg)

#### Example - FIFA 18: Normalize data

```python
# Scale wage and value
fifa['scaled_wage'] = whiten(fifa['eur_wage'])
fifa['scaled_value'] = whiten(fifa['eur_value'])

# Plot the two columns in a scatter plot
fifa.plot(x='scaled_wage', y='scaled_value', kind = 'scatter')
plt.show()

# Check mean and standard deviation of scaled values
print(fifa[['scaled_wage', 'scaled_value']].describe())
```

Output

![]({{site.baseurl}}/images/cluster5.svg)

---
## Hierarchical Clustering

[Slide]({{site.baseurl}}/files/Cluster_Analysis_in_Python_C2.pdf)

### Basics of hierarchical clustering

#### Example: Hierarchical clustering: ward method

**1. Hierarchical Clustering (Phân cụm phân cấp)**

Phân cụm phân cấp (Hierarchical Clustering) là một thuật toán học máy không giám sát (unsupervised learning) được sử dụng để nhóm các điểm dữ liệu lại với nhau dựa trên sự tương đồng của chúng.  Nó tạo ra một cấu trúc dạng cây phân cấp (hay còn gọi là dendrogram) thể hiện mối quan hệ giữa các cụm.  Có hai loại chính của phân cụm phân cấp:

*   **Agglomerative (Bottom-up):** Bắt đầu với mỗi điểm dữ liệu là một cụm riêng biệt, sau đó liên tục hợp nhất các cụm gần nhau nhất cho đến khi chỉ còn lại một cụm duy nhất.
*   **Divisive (Top-down):** Bắt đầu với tất cả các điểm dữ liệu trong một cụm duy nhất, sau đó liên tục chia nhỏ cụm thành các cụm nhỏ hơn.

**2. Ward Method (Phương pháp Ward)**

Phương pháp Ward (Ward's method) là một thuật toán *agglomerative hierarchical clustering* cụ thể.  Nó được sử dụng để xác định cụm nào nên được hợp nhất dựa trên việc *tối thiểu hóa phương sai* (variance) của các cụm sau khi hợp nhất.  Cụ thể hơn, phương pháp Ward tìm cách hợp nhất hai cụm sao cho tổng *tổng bình phương khoảng cách* (sum of squared distances - SSD) từ tất cả các điểm trong một cụm đến tâm của cụm đó là nhỏ nhất.

Nói một cách dễ hiểu, phương pháp Ward ưu tiên hợp nhất các cụm "gần" nhau theo nghĩa là việc hợp nhất chúng sẽ làm cho các điểm dữ liệu trong các cụm mới *ít phân tán* hơn xung quanh tâm của chúng.  Nó cố gắng tạo ra các cụm *compact* (gọn gàng) và *spherical* (hình cầu).

**Ví dụ:**

Hãy tưởng tượng bạn có một tập dữ liệu các khách hàng, và bạn muốn nhóm họ lại dựa trên hành vi mua hàng của họ.  Bạn có thể sử dụng *hierarchical clustering* với *Ward's method* để tạo ra các nhóm khách hàng khác nhau.  Phương pháp Ward sẽ giúp bạn tìm ra cách nhóm các khách hàng sao cho sự khác biệt trong hành vi mua hàng *bên trong* mỗi nhóm là nhỏ nhất, và sự khác biệt *giữa* các nhóm là lớn nhất.

```python
# Import the fcluster and linkage functions
from scipy.cluster.hierarchy import fcluster, linkage

# Use the linkage() function
distance_matrix = linkage(comic_con[['x_scaled', 'y_scaled']], method = 'ward', metric = 'euclidean')

# Assign cluster labels
comic_con['cluster_labels'] = fcluster(distance_matrix, 2, criterion='maxclust')

# Plot clusters
sns.scatterplot(x='x_scaled', y='y_scaled', 
                hue='cluster_labels', data = comic_con)
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster6.svg)

#### Hierarchical clustering: single method

Như đã đề cập trước đó, *Hierarchical Clustering* (phân cụm phân cấp) là một thuật toán học máy không giám sát (unsupervised learning) để nhóm các điểm dữ liệu dựa trên sự tương đồng.  Nó tạo ra một cấu trúc dạng cây phân cấp (dendrogram).  *Single Method* (hay còn gọi là *single-linkage clustering*) là một trong những phương pháp liên kết (linkage criteria) được sử dụng trong *agglomerative hierarchical clustering*.

**Cách thức hoạt động của Single Method:**

*Single Method* tính toán khoảng cách giữa hai cụm bằng cách tìm *khoảng cách ngắn nhất* giữa bất kỳ hai điểm dữ liệu nào trong hai cụm đó.  Nói cách khác, nó xem xét hai điểm "gần nhau nhất" giữa hai cụm.

**Ví dụ:**

Hãy tưởng tượng bạn có ba cụm: A, B, và C.

*   Cụm A chứa các điểm {a1, a2}.
*   Cụm B chứa các điểm {b1, b2, b3}.
*   Cụm C chứa các điểm {c1, c2}.

Để xác định cụm nào gần nhau nhất bằng *Single Method*, ta sẽ tính khoảng cách giữa *tất cả* các cặp điểm sau:

*   a1 - b1, a1 - b2, a1 - b3
*   a2 - b1, a2 - b2, a2 - b3
*   a1 - c1, a1 - c2
*   a2 - c1, a2 - c2
*   b1 - c1, b1 - c2
*   b2 - c1, b2 - c2
*   b3 - c1, b3 - c2

Sau đó, ta chọn cặp điểm có khoảng cách *nhỏ nhất*.  Giả sử khoảng cách nhỏ nhất là giữa a1 và b2.  Khi đó, *Single Method* sẽ coi cụm A và cụm B là "gần nhau nhất" và sẽ hợp nhất chúng trước.

**Ưu điểm của Single Method:**

*   Có thể phát hiện các cụm có hình dạng bất kỳ, không nhất thiết phải là hình cầu.  Vì nó chỉ dựa vào khoảng cách gần nhất, nó có thể "kết nối" các cụm thông qua một vài điểm "cầu nối".

**Nhược điểm của Single Method:**

*   Dễ bị ảnh hưởng bởi *outliers* (điểm ngoại lai).  Một điểm ngoại lai có thể làm sai lệch kết quả phân cụm, vì nó có thể tạo ra một "liên kết" không mong muốn giữa các cụm.
*   Có xu hướng tạo ra các cụm "dài" và "mỏng" (chain-like clusters).

**So sánh với các phương pháp liên kết khác:**

Các phương pháp liên kết khác như *Complete Method* (khoảng cách lớn nhất), *Average Method* (khoảng cách trung bình), và *Ward's Method* (tối thiểu hóa phương sai) sử dụng các tiêu chí khác nhau để xác định khoảng cách giữa các cụm.  Do đó, chúng có thể tạo ra các kết quả phân cụm khác nhau.

**Tóm lại:**

*   *Single Method* là một phương pháp liên kết trong *agglomerative hierarchical clustering*.
*   Nó tính khoảng cách giữa hai cụm dựa trên khoảng cách *nhỏ nhất* giữa hai điểm bất kỳ trong hai cụm đó.
*   Ưu điểm: Phát hiện cụm hình dạng bất kỳ.
*   Nhược điểm: Dễ bị ảnh hưởng bởi *outliers*, tạo cụm dài và mỏng.

```python
# Import the fcluster and linkage functions
from scipy.cluster.hierarchy import fcluster, linkage

# Use the linkage() function
distance_matrix = linkage(comic_con[['x_scaled', 'y_scaled']], method = 'single', metric = 'euclidean')

# Assign cluster labels
comic_con['cluster_labels'] = fcluster(distance_matrix, 2, criterion='maxclust')

# Plot clusters
sns.scatterplot(x='x_scaled', y='y_scaled', 
                hue='cluster_labels', data = comic_con)
plt.show()
```

Output

![]({{site.baseurl}}/images/cluster7.svg)


#### Hierarchical clustering: complete method

Như đã đề cập, *Hierarchical Clustering* (phân cụm phân cấp) là một thuật toán học máy không giám sát (unsupervised learning) để nhóm dữ liệu dựa trên sự tương đồng, tạo ra cấu trúc cây phân cấp (dendrogram). *Complete Method* (hay còn gọi là *complete-linkage clustering* hoặc *maximum linkage clustering*) là một trong các phương pháp liên kết (linkage criteria) được dùng trong *agglomerative hierarchical clustering*.

**Cách thức hoạt động của Complete Method:**

Khác với *Single Method* chỉ quan tâm đến khoảng cách *nhỏ nhất* giữa hai điểm dữ liệu thuộc hai cụm, *Complete Method* lại xem xét khoảng cách *lớn nhất* giữa chúng.  Cụ thể, khoảng cách giữa hai cụm được định nghĩa là khoảng cách *lớn nhất* giữa *tất cả* các cặp điểm có thể được tạo thành, mỗi điểm thuộc một cụm.

**Ví dụ:**

Giả sử ta có ba cụm: A, B, và C.

*   Cụm A chứa các điểm {a1, a2}.
*   Cụm B chứa các điểm {b1, b2, b3}.
*   Cụm C chứa các điểm {c1, c2}.

Để xác định cụm nào gần nhau nhất bằng *Complete Method*, ta sẽ tính khoảng cách giữa *tất cả* các cặp điểm (như ví dụ với Single Method), nhưng thay vì chọn khoảng cách nhỏ nhất, ta sẽ chọn khoảng cách *lớn nhất* trong số đó. Giả sử khoảng cách lớn nhất là giữa a2 và b1. Khi đó, *Complete Method* sẽ coi khoảng cách giữa cụm A và B là khoảng cách giữa a2 và b1.

**Ưu điểm của Complete Method:**

*   Ít nhạy cảm hơn với *outliers* (điểm ngoại lai) so với *Single Method*. Vì nó xem xét khoảng cách lớn nhất, một điểm ngoại lai sẽ ít ảnh hưởng đến việc hợp nhất cụm.
*   Có xu hướng tạo ra các cụm *compact* (gọn gàng) và *spherical* (hình cầu) hơn.

**Nhược điểm của Complete Method:**

*   Có thể gặp khó khăn trong việc phân tách các cụm có hình dạng phức tạp hoặc không lồi (non-convex).  Vì nó dựa trên khoảng cách lớn nhất, nó có thể bỏ lỡ các liên kết "gần gũi" bên trong cụm nếu có một vài điểm "xa xôi" trong cụm đó.

**So sánh với các phương pháp liên kết khác:**

*   *Single Method*: Khoảng cách nhỏ nhất.
*   *Average Method*: Khoảng cách trung bình giữa tất cả các cặp điểm.
*   *Ward's Method*: Tối thiểu hóa phương sai.

Mỗi phương pháp có ưu và nhược điểm riêng, và việc lựa chọn phương pháp nào phụ thuộc vào đặc điểm của dữ liệu và mục tiêu phân cụm.

**Tóm lại:**

*   *Complete Method* là một phương pháp liên kết trong *agglomerative hierarchical clustering*.
*   Nó tính khoảng cách giữa hai cụm dựa trên khoảng cách *lớn nhất* giữa hai điểm bất kỳ trong hai cụm đó.
*   Ưu điểm: Ít nhạy cảm với *outliers*, tạo cụm gọn gàng.
*   Nhược điểm: Khó phân tách cụm phức tạp, có thể bỏ lỡ liên kết gần gũi.

```python
# Import the fcluster and linkage functions
from scipy.cluster.hierarchy import fcluster, linkage

# Use the linkage() function
distance_matrix = linkage(comic_con[['x_scaled', 'y_scaled']], method='complete')

# Assign cluster labels
comic_con['cluster_labels'] = fcluster(distance_matrix, 2, criterion='maxclust')

# Plot clusters
sns.scatterplot(x='x_scaled', y='y_scaled', 
                hue='cluster_labels', data = comic_con)
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster8.svg)

### Visualize clusters

#### Example - Visualize clusters with matplotlib

```python
# Import the pyplot class
from matplotlib import pyplot as plt

# Define a colors dictionary for clusters
colors = {1:'red', 2:'blue'}

# Plot a scatter plot
comic_con.plot.scatter(x='x_scaled', 
                	   y='y_scaled',
                	   c=comic_con['cluster_labels'].apply(lambda x: colors[x]))
plt.show()
```
Output:

![]({{site.baseurl}}/images/cluster9.svg)

#### Visualize clusters with seaborn

```python
# Import the seaborn module
import seaborn as sns

# Plot a scatter plot using seaborn
sns.scatterplot(x='x_scaled', 
                y='y_scaled', 
                hue='cluster_labels', 
                data = comic_con)
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster10.svg)

### How many clusters?

#### Example - Create a dendrogram

```python
# Import the dendrogram function
from scipy.cluster.hierarchy import dendrogram

# Create a dendrogram
dn = dendrogram(distance_matrix)

# Display the dendogram
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster11.svg)

### Limitations of hierarchical clustering

#### Example - FIFA 18: exploring defenders

```python
# Fit the data into a hierarchical clustering algorithm
distance_matrix = linkage(fifa[['scaled_sliding_tackle', 'scaled_aggression']], 'ward')

# Assign cluster labels to each row of data
fifa['cluster_labels'] = fcluster(distance_matrix, 3, criterion='maxclust')

# Display cluster centers of each cluster
print(fifa[['scaled_sliding_tackle', 'scaled_aggression', 'cluster_labels']].groupby('cluster_labels').mean())

# Create a scatter plot through seaborn
sns.scatterplot(x='scaled_sliding_tackle', y='scaled_aggression', hue='cluster_labels', data=fifa)
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster12.svg)

---
## K-Means Clustering

[Slide]({{site.baseurl}}/files/Cluster_Analysis_in_Python_C3.pdf)

### Basics of k-means clustering

#### Example

```python
# Import the kmeans and vq functions
from scipy.cluster.vq import kmeans, vq

# Generate cluster centers
cluster_centers, distortion = kmeans(comic_con[['x_scaled', 'y_scaled']], 2)

# Assign cluster labels
comic_con['cluster_labels'], distortion_list = vq(comic_con[['x_scaled', 'y_scaled']], cluster_centers)

# Plot clusters
sns.scatterplot(x='x_scaled', y='y_scaled', 
                hue='cluster_labels', data = comic_con)
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster13.svg)

### How many clusters?

#### Example - Elbow method on distinct clusters

```python
distortions = []
num_clusters = range(1, 7)

# Create a list of distortions from the kmeans function
for i in num_clusters:
    cluster_centers, distortion = kmeans(comic_con[['x_scaled', 'y_scaled']], i)
    distortions.append(distortion)

# Create a DataFrame with two lists - num_clusters, distortions
elbow_plot = pd.DataFrame({'num_clusters': num_clusters, 'distortions': distortions})

# Creat a line plot of num_clusters and distortions
sns.lineplot(x='num_clusters', y='distortions', data = elbow_plot)
plt.xticks(num_clusters)
plt.show()
```

Output

![]({{site.baseurl}}/images/cluster14.svg)


### Limitations of k-means clustering

K-means là một thuật toán phân cụm phổ biến, nhưng nó cũng có một số hạn chế cần lưu ý:

1.  **Assumption of spherical clusters (Giả định về cụm hình cầu):** K-means hoạt động tốt nhất khi các cụm có hình dạng *lồi* (convex) và gần giống hình cầu (spherical).  Nó gặp khó khăn với các cụm có hình dạng phức tạp, không lồi, hoặc có độ đậm đặc khác nhau. Ví dụ, nếu các cụm có hình dạng vòng cung hoặc xoắn ốc, k-means có thể không phân cụm chính xác.

2.  **Sensitivity to initial centroids (Nhạy cảm với tâm cụm ban đầu):** Kết quả của k-means có thể thay đổi đáng kể tùy thuộc vào việc lựa chọn *centroids* (tâm cụm) ban đầu.  Nếu các *centroids* ban đầu được chọn không tốt, thuật toán có thể hội tụ đến một kết quả *local optimum* (cực trị địa phương) không phải là kết quả tốt nhất.  Để giảm thiểu vấn đề này, người ta thường chạy k-means nhiều lần với các *centroids* ban đầu khác nhau và chọn kết quả tốt nhất.

3.  **Need to specify the number of clusters k (Cần xác định số lượng cụm k):**  Bạn phải xác định trước số lượng cụm *k* trước khi chạy thuật toán.  Việc lựa chọn *k* không đúng có thể dẫn đến kết quả phân cụm kém.  Có nhiều phương pháp để ước lượng *k*, chẳng hạn như *elbow method* (phương pháp khuỷu tay) hoặc *silhouette analysis* (phân tích silhouette), nhưng chúng không phải lúc nào cũng hiệu quả.

4.  **Sensitive to outliers (Nhạy cảm với điểm ngoại lai):** K-means rất nhạy cảm với *outliers* (điểm ngoại lai).  *Outliers* có thể kéo các *centroids* ra xa khỏi vị trí "thực sự" của cụm, làm sai lệch kết quả phân cụm.  Việc xử lý *outliers* trước khi áp dụng k-means là rất quan trọng.

5.  **Equal variance assumption (Giả định phương sai bằng nhau):** K-means giả định rằng các cụm có phương sai (variance) gần bằng nhau.  Nếu các cụm có phương sai khác nhau đáng kể, k-means có thể ưu tiên các cụm có phương sai lớn hơn.

6.  **All features are equally important (Tất cả các đặc trưng đều quan trọng như nhau):** K-means coi tất cả các đặc trưng (features) là quan trọng như nhau trong việc tính toán khoảng cách.  Nếu một số đặc trưng không liên quan hoặc ít quan trọng hơn, chúng vẫn có thể ảnh hưởng đến kết quả phân cụm.  Việc lựa chọn đặc trưng (feature selection) hoặc giảm chiều dữ liệu (dimensionality reduction) có thể giúp cải thiện kết quả.

**Tóm lại:**

K-means là một thuật toán phân cụm hữu ích, nhưng cần lưu ý các hạn chế của nó.  Việc hiểu rõ những hạn chế này giúp bạn lựa chọn thuật toán phù hợp và xử lý dữ liệu một cách hiệu quả hơn.  Nếu dữ liệu của bạn không thỏa mãn các giả định của k-means, bạn có thể xem xét các thuật toán phân cụm khác như *hierarchical clustering*, *DBSCAN*, hoặc *Gaussian Mixture Models (GMMs)*.

#### Impact of seeds on distinct clusters

```python
# Import random class
from numpy import random

# Initialize seed
random.seed(0)

# Run kmeans clustering
cluster_centers, distortion = kmeans(comic_con[['x_scaled', 'y_scaled']], 2)
comic_con['cluster_labels'], distortion_list = vq(comic_con[['x_scaled', 'y_scaled']], cluster_centers)

# Plot the scatterplot
sns.scatterplot(x='x_scaled', y='y_scaled', 
                hue='cluster_labels', data = comic_con)
plt.show()
```


Output

![]({{site.baseurl}}/images/cluster16.svg)

```python
# Import random class
from numpy import random

# Initialize seed
random.seed([1, 2, 1000])

# Run kmeans clustering
cluster_centers, distortion = kmeans(comic_con[['x_scaled', 'y_scaled']], 2)
comic_con['cluster_labels'], distortion_list = vq(comic_con[['x_scaled', 'y_scaled']], cluster_centers)

# Plot the scatterplot
sns.scatterplot(x='x_scaled', y='y_scaled', 
                hue='cluster_labels', data = comic_con)
plt.show()
```

Output

![]({{site.baseurl}}/images/cluster17.svg)

#### Example: FIFA 18: defenders revisited

```python
# Set up a random seed in numpy
random.seed([1000,2000])

# Fit the data into a k-means algorithm
cluster_centers,_ = kmeans(fifa[['scaled_def', 'scaled_phy']], 3)

# Assign cluster labels
fifa['cluster_labels'], _ = vq(fifa[['scaled_def', 'scaled_phy']], cluster_centers)

# Display cluster centers 
print(fifa[['scaled_def', 'scaled_phy', 'cluster_labels']].groupby('cluster_labels').mean())

# Create a scatter plot through seaborn
sns.scatterplot(x='scaled_def', y='scaled_phy', hue='cluster_labels', data=fifa)
plt.show()
```

Output

![]({{site.baseurl}}/images/cluster18.svg)

---
## Clustering in Real World

[Slide]({{site.baseurl}}/files/Cluster_Analysis_in_Python_C4.pdf)

### Sử dụng Clustering để tìm màu chủ đạo trong ảnh

Bài toán "Tìm màu chủ đạo trong ảnh" là xác định một tập hợp các màu đại diện cho một hình ảnh, thường là những màu xuất hiện nhiều nhất hoặc quan trọng nhất.  Clustering là một kỹ thuật học máy không giám sát (unsupervised learning) rất phù hợp để giải quyết vấn đề này.

**Ý tưởng chính:**

Mỗi pixel trong ảnh có thể được biểu diễn bằng một vector màu, ví dụ trong không gian màu RGB (Red, Green, Blue).  Chúng ta có thể coi mỗi pixel là một điểm dữ liệu.  Sau đó, chúng ta sử dụng thuật toán clustering để nhóm các pixel có màu sắc tương tự lại với nhau thành các cụm.  Mỗi cụm sẽ đại diện cho một màu "chủ đạo" trong ảnh.  Màu trung tâm (centroid) của mỗi cụm thường được chọn làm màu đại diện cho cụm đó.

**Các bước cụ thể:**

1.  **Dữ liệu:**  Dữ liệu đầu vào là một hình ảnh.  Mỗi pixel của ảnh được chuyển đổi thành một vector màu (ví dụ: RGB, HSV, Lab).  Tập hợp tất cả các vector màu của pixel tạo thành tập dữ liệu của chúng ta.

2.  **Chọn thuật toán Clustering:**  Một số thuật toán clustering phổ biến có thể được sử dụng cho bài toán này, bao gồm:
    *   **K-means:**  Đây là lựa chọn phổ biến vì tính đơn giản và hiệu quả của nó.  Chúng ta cần xác định số lượng cụm *k* trước, tương ứng với số lượng màu chủ đạo mà chúng ta muốn tìm.
    *   **Hierarchical Clustering:**  Có thể hữu ích nếu chúng ta không biết trước số lượng màu chủ đạo.  Chúng ta có thể cắt dendrogram ở một mức độ phù hợp để có được số lượng cụm mong muốn.
    *   **DBSCAN:**  Có thể phát hiện các cụm có hình dạng bất kỳ và ít bị ảnh hưởng bởi *outliers* (điểm ngoại lai) hơn so với k-means.

3.  **Áp dụng thuật toán Clustering:**  Áp dụng thuật toán đã chọn lên tập dữ liệu màu của pixel.  Kết quả là mỗi pixel sẽ được gán cho một cụm.

4.  **Xác định màu chủ đạo:**  Màu trung tâm (centroid) của mỗi cụm được coi là một màu chủ đạo.  Ví dụ, trong thuật toán k-means, *centroid* là trung bình của tất cả các vector màu của các pixel thuộc cụm đó.

5.  **Biểu diễn kết quả:**  Các màu chủ đạo có thể được biểu diễn dưới dạng một bảng màu, hoặc có thể được sử dụng để tạo ra một phiên bản "giảm màu" của ảnh gốc.

**Ví dụ với K-means:**

Giả sử bạn muốn tìm 5 màu chủ đạo trong một bức ảnh.

1.  Chuyển đổi ảnh sang không gian màu RGB.
2.  Áp dụng thuật toán k-means với *k* = 5 cho tập dữ liệu màu của pixel.
3.  Kết quả, bạn sẽ có 5 cụm, mỗi cụm đại diện cho một màu chủ đạo.
4.  Tính *centroid* của mỗi cụm.  Đây chính là 5 màu chủ đạo của bức ảnh.

**Ưu điểm của phương pháp này:**

*   Tự động xác định màu chủ đạo mà không cần phải thiết lập ngưỡng (threshold) thủ công.
*   Có thể xử lý ảnh có nhiều màu sắc phức tạp.

**Nhược điểm:**

*   Kết quả phụ thuộc vào thuật toán clustering được sử dụng và các tham số của nó (ví dụ: *k* trong k-means).
*   Có thể bỏ sót các màu ít xuất hiện nhưng vẫn quan trọng về mặt cảm quan.

#### Example: Extract RGB values from image

```python
# Import image class of matplotlib
import matplotlib.image as img

# Read batman image and print dimensions
batman_image = img.imread('batman.jpg')
print(batman_image.shape)

# Store RGB values of all pixels in lists r, g and b
for row in batman_image:
    for temp_r, temp_g, temp_b in row:
        r.append(temp_r)
        g.append(temp_g)
        b.append(temp_b)
```

make `bathman_df` like:

```bash
In [1]:
batman_df.head()
Out[1]:

   red  blue  green  scaled_red  scaled_blue  scaled_green
0    6     7      1       0.084        0.124         0.016
1   22    46     34       0.309        0.813         0.556
2   75  -123    111       1.054       -2.173         1.815
3   49  -121    106       0.688       -2.138         1.733
4   38  -121    103       0.534       -2.138         1.684

```

The RGB values have been standardized used the `whiten()`

#### Example: How many dominant colors? (elbow_plot)

```python
distortions = []
num_clusters = range(1, 7)

# Create a list of distortions from the kmeans function
for i in num_clusters:
    cluster_centers, distortion = kmeans(batman_df[['scaled_red', 'scaled_blue', 'scaled_green']], i)
    distortions.append(distortion)

# Create a DataFrame with two lists, num_clusters and distortions
elbow_plot = pd.DataFrame({
    'num_clusters': num_clusters,
    'distortions': distortions
})

# Create a line plot of num_clusters and distortions
sns.lineplot(x='num_clusters', y='distortions', data = elbow_plot)
plt.xticks(num_clusters)
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster19.svg)

#### Display dominant colors

```python
# Get standard deviations of each color
r_std, g_std, b_std = batman_df[['red', 'green', 'blue']].std()

for cluster_center in cluster_centers:
    scaled_r, scaled_g, scaled_b = cluster_center
    # Convert each standardized value to scaled value
    colors.append((
        scaled_r * r_std / 255,
        scaled_g * g_std / 255,
        scaled_b * b_std / 255
    ))

# Display colors of cluster centers
plt.imshow([colors])
plt.show()
```

Output:

![]({{site.baseurl}}/images/cluster20.svg)


### Sử dụng Clustering để giải quyết bài toán Phân cụm Văn bản (Document Clustering)

Bài toán *Document Clustering* là việc nhóm các văn bản lại với nhau dựa trên sự tương đồng về nội dung.  Clustering là một kỹ thuật học máy không giám sát (unsupervised learning) rất phù hợp để giải quyết vấn đề này.

**Ý tưởng chính:**

Mỗi văn bản được biểu diễn bằng một vector đặc trưng (feature vector), thường sử dụng các phương pháp như *TF-IDF* (Term Frequency-Inverse Document Frequency), *Word2Vec*, hoặc *Doc2Vec*.  Vector này thể hiện nội dung của văn bản.  Sau đó, chúng ta sử dụng thuật toán clustering để nhóm các văn bản có vector đặc trưng tương tự lại với nhau thành các cụm.  Các văn bản trong cùng một cụm được coi là có nội dung liên quan.

**Các bước cụ thể:**

1.  **Tiền xử lý văn bản (Text Preprocessing):**
    *   Loại bỏ các ký tự đặc biệt, dấu câu, và chuyển đổi tất cả các ký tự về chữ thường.
    *   *Tokenization*: Chia văn bản thành các từ hoặc cụm từ (tokens).
    *   *Stop Word Removal*: Loại bỏ các từ không mang nhiều ý nghĩa (ví dụ: "the", "a", "is").
    *   *Stemming/Lemmatization*: Đưa các từ về dạng gốc của chúng (ví dụ: "running" -> "run").

2.  **Biểu diễn văn bản bằng vector đặc trưng (Feature Vector Representation):**
    *   *TF-IDF*: Tính tần suất xuất hiện của từ trong văn bản, đồng thời xem xét mức độ quan trọng của từ đó trong toàn bộ tập văn bản.
    *   *Word2Vec/Doc2Vec*: Sử dụng mạng nơ-ron để học biểu diễn vector của từ hoặc toàn bộ văn bản, dựa trên ngữ cảnh xuất hiện của chúng.

3.  **Chọn thuật toán Clustering:**  Một số thuật toán clustering phổ biến có thể được sử dụng cho bài toán này:
    *   *K-means*:  Đây là lựa chọn phổ biến vì tính đơn giản và hiệu quả.  Cần xác định số lượng cụm *k* trước.
    *   *Hierarchical Clustering*:  Có thể hữu ích nếu không biết trước số lượng cụm.
    *   *DBSCAN*:  Có thể phát hiện các cụm có hình dạng bất kỳ.

4.  **Áp dụng thuật toán Clustering:** Áp dụng thuật toán đã chọn lên tập dữ liệu vector đặc trưng của văn bản. Kết quả là mỗi văn bản sẽ được gán cho một cụm.

5.  **Đánh giá kết quả (Evaluation):**  Sử dụng các độ đo như *Silhouette Score*, *Davies-Bouldin Index*, hoặc *Normalized Mutual Information (NMI)* để đánh giá chất lượng của các cụm.  Ngoài ra, có thể kiểm tra thủ công để đảm bảo các văn bản trong cùng một cụm thực sự liên quan đến nhau.

**Ví dụ với K-means và TF-IDF:**

Giả sử bạn có một tập hợp các bài báo về các chủ đề khác nhau.

1.  Tiền xử lý các bài báo.
2.  Sử dụng TF-IDF để tạo vector đặc trưng cho mỗi bài báo.
3.  Áp dụng thuật toán k-means với *k* = 5 (giả sử bạn muốn 5 nhóm chủ đề).
4.  Kết quả, bạn sẽ có 5 cụm, mỗi cụm chứa các bài báo liên quan đến một chủ đề.

**Ưu điểm của phương pháp này:**

*   Tự động nhóm các văn bản dựa trên nội dung.
*   Có thể xử lý một lượng lớn văn bản.

**Nhược điểm:**

*   Kết quả phụ thuộc vào thuật toán clustering, phương pháp biểu diễn vector đặc trưng, và các tham số của chúng.
*   Việc lựa chọn *k* trong k-means có thể khó khăn.

#### Example - TF-IDF of movie plots

```python

### Remove noise
from nltk.tokenize import word_tokenize
import re

def remove_noise(text, stop_words = []):
    tokens = word_tokenize(text)
    cleaned_tokens = []
    for token in tokens:
        token = re.sub('[^A-Za-z0-9]+', '', token)
        if len(token) > 1 and token.lower() not in stop_words:
            # Get lowercase
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

### TF-IDF of movie plots

# Import TfidfVectorizer class from sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(max_df=0.75, max_features=50, min_df=0.1, tokenizer=remove_noise)
# Use the .fit_transform() method on the list plots
tfidf_matrix = tfidf_vectorizer.fit_transform(plots)
```

#### Top terms in movie clusters

```python
num_clusters = 2

# Generate cluster centers through the kmeans function
cluster_centers, distortion = kmeans(tfidf_matrix.todense(), num_clusters)

# Generate terms from the tfidf_vectorizer object
terms = tfidf_vectorizer.get_feature_names_out()

for i in range(num_clusters):
    # Sort the terms and print top 3 terms
    center_terms = dict(zip(terms, list(cluster_centers[i])))
    sorted_terms = sorted(center_terms, key=center_terms.get, reverse=True)
    print(sorted_terms[:3])
```

Output

```bash
<script.py> output:
    ['father', 'back', 'one']
    ['police', 'man', 'killed']
```


### Clustering with multiple features

Bài toán "Phân cụm với nhiều đặc trưng" đề cập đến việc phân cụm dữ liệu khi mỗi điểm dữ liệu được mô tả bởi nhiều đặc trưng (features).  Các đặc trưng này có thể thuộc các kiểu dữ liệu khác nhau (ví dụ: số, văn bản, hoặc categorical).  Clustering là một kỹ thuật học máy không giám sát (unsupervised learning) rất phù hợp để giải quyết vấn đề này.

**Ý tưởng chính:**

Mục tiêu là nhóm các điểm dữ liệu lại với nhau dựa trên sự tương đồng của chúng, xem xét *tất cả* các đặc trưng.  Việc xử lý nhiều đặc trưng đòi hỏi một số kỹ thuật và cân nhắc đặc biệt.

**Các bước cụ thể:**

1.  **Tiền xử lý dữ liệu (Data Preprocessing):**

    *   **Xử lý dữ liệu bị thiếu (Missing Data Handling):**  Quyết định cách xử lý các giá trị bị thiếu (ví dụ: loại bỏ, điền giá trị trung bình/trung vị, hoặc sử dụng các phương pháp phức tạp hơn).
    *   **Xử lý dữ liệu không đồng nhất (Handling Heterogeneous Data):** Nếu có các đặc trưng thuộc các kiểu dữ liệu khác nhau (ví dụ: số và categorical), cần chuyển đổi chúng sang một dạng phù hợp để tính toán khoảng cách.  Ví dụ:
        *   Số: Chuẩn hóa (scaling) hoặc chuẩn hóa (standardization).
        *   Categorical: One-hot encoding.
    *   **Chuẩn hóa/Chuẩn hóa đặc trưng (Feature Scaling/Standardization):**  Đảm bảo rằng các đặc trưng có cùng một thang đo để tránh các đặc trưng có giá trị lớn hơn chi phối kết quả phân cụm.  Các phương pháp phổ biến bao gồm *Min-Max Scaling* và *Standardization (Z-score normalization)*.

2.  **Chọn độ đo khoảng cách (Distance Metric):**  Lựa chọn độ đo khoảng cách phù hợp để tính toán sự tương đồng giữa các điểm dữ liệu.  Một số độ đo phổ biến bao gồm:
    *   *Euclidean Distance*: Phù hợp cho dữ liệu số liên tục.
    *   *Manhattan Distance*: Ít nhạy cảm hơn với *outliers* so với Euclidean.
    *   *Cosine Similarity*:  Phù hợp cho dữ liệu văn bản hoặc dữ liệu có chiều cao.
    *   *Hamming Distance*: Phù hợp cho dữ liệu categorical.
    *   *Gower Distance*: Phù hợp cho dữ liệu hỗn hợp (cả số và categorical).

3.  **Chọn thuật toán Clustering:**  Lựa chọn thuật toán clustering phù hợp với đặc điểm của dữ liệu và mục tiêu phân cụm.  Một số thuật toán phổ biến:
    *   *K-means*:  Hiệu quả cho dữ liệu số, nhưng nhạy cảm với *outliers* và giả định các cụm có hình dạng hình cầu.
    *   *Hierarchical Clustering*:  Có thể tạo ra cấu trúc phân cấp, nhưng tốn kém tính toán hơn.
    *   *DBSCAN*:  Có thể phát hiện các cụm có hình dạng bất kỳ và ít nhạy cảm với *outliers*.
    *   *GMM (Gaussian Mixture Models)*:  Giả định dữ liệu được tạo ra từ hỗn hợp các phân phối Gaussian.

4.  **Áp dụng thuật toán Clustering:**  Áp dụng thuật toán đã chọn lên dữ liệu đã được tiền xử lý.

5.  **Đánh giá kết quả (Evaluation):**  Sử dụng các độ đo phù hợp để đánh giá chất lượng của các cụm, ví dụ: *Silhouette Score*, *Davies-Bouldin Index*, *Calinski-Harabasz Index*.

**Ví dụ:**

Giả sử bạn muốn phân cụm khách hàng dựa trên nhiều đặc trưng như: tuổi (số), thu nhập (số), giới tính (categorical), và lịch sử mua hàng (văn bản).

1.  Tiền xử lý dữ liệu: Xử lý dữ liệu thiếu, chuyển đổi giới tính sang one-hot encoding, chuẩn hóa tuổi và thu nhập, sử dụng TF-IDF hoặc Word2Vec cho lịch sử mua hàng.
2.  Chọn độ đo khoảng cách:  Có thể sử dụng Gower Distance do dữ liệu hỗn hợp.
3.  Chọn thuật toán: K-means hoặc DBSCAN.
4.  Áp dụng thuật toán và đánh giá kết quả.

**Khó khăn và cân nhắc:**

*   **Lời nguyền chiều cao (Curse of Dimensionality):**  Khi số lượng đặc trưng quá lớn, dữ liệu trở nên thưa thớt, gây khó khăn cho việc phân cụm.  Cần xem xét giảm chiều dữ liệu (dimensionality reduction) bằng PCA hoặc các phương pháp khác.
*   **Lựa chọn tham số:**  Nhiều thuật toán clustering có các tham số cần được điều chỉnh (ví dụ: *k* trong k-means).  Cần sử dụng các phương pháp như *cross-validation* hoặc *grid search* để tìm tham số tốt nhất.

#### Example - FIFA 18: what makes a complete player?

```python
# Create centroids with kmeans for 2 clusters
cluster_centers,_ = kmeans(fifa[scaled_features], 2)

# Assign cluster labels and print cluster centers
fifa['cluster_labels'], _ = vq(fifa[scaled_features], cluster_centers)
print(fifa.groupby('cluster_labels')[scaled_features].mean())

# Plot cluster centers to visualize clusters
fifa.groupby('cluster_labels')[scaled_features].mean().plot(legend=True, kind='bar')
plt.show()

# Get the name column of first 5 players in each cluster
for cluster in fifa['cluster_labels'].unique():
    print(cluster, fifa[fifa['cluster_labels'] == cluster]['name'].values[:5])
```

Output

```bash
<script.py> output:
                    scaled_pac  scaled_sho  scaled_pas  scaled_dri  scaled_def  scaled_phy
    cluster_labels                                                                        
    0                     6.68        5.43        8.46        8.51        2.50        8.34
    1                     5.44        3.66        7.17        6.76        3.97        9.21
    0 ['Cristiano Ronaldo' 'L. Messi' 'Neymar' 'L. Suárez' 'M. Neuer']
    1 ['Sergio Ramos' 'G. Chiellini' 'D. Godín' 'Thiago Silva' 'M. Hummels']
```

![]({{site.baseurl}}/images/cluster21.svg)