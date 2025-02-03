---
layout: post
title: "[Project] Clustering Antarctic Penguin Species"
date: 2025-01-20 03:00:00 +0700
categories: machine learning in python
---

You have been asked to support a team of researchers who have been collecting data about penguins in Antartica! The data is available in csv-Format as `penguins.csv`

**Origin of this data** : Data were collected and made available by Dr. Kristen Gorman and the Palmer Station, Antarctica LTER, a member of the Long Term Ecological Research Network.

**The dataset consists of 5 columns.**

Column | Description
--- | ---
culmen_length_mm | culmen length (mm)
culmen_depth_mm | culmen depth (mm)
flipper_length_mm | flipper length (mm)
body_mass_g | body mass (g)
sex | penguin sex

Unfortunately, they have not been able to record the species of penguin, but they know that there are **at least three** species that are native to the region: **Adelie**, **Chinstrap**, and **Gentoo**.  Your task is to apply your data science skills to help them identify groups in the dataset!

---

Bạn đã được yêu cầu hỗ trợ một nhóm các nhà nghiên cứu, những người đã thu thập dữ liệu về chim cánh cụt ở Nam Cực! Dữ liệu có sẵn ở định dạng CSV là `penguins.csv`

**Nguồn gốc của dữ liệu này**: Dữ liệu được thu thập và cung cấp bởi Tiến sĩ Kristen Gorman và Trạm Palmer, Nam Cực LTER, một thành viên của Mạng lưới Nghiên cứu Sinh thái Dài hạn.

**Tập dữ liệu bao gồm 5 cột.**

Cột | Mô tả
--- | ---
culmen_length_mm | chiều dài mỏ (mm)
culmen_depth_mm | độ sâu mỏ (mm)
flipper_length_mm | chiều dài vây (mm)
body_mass_g | khối lượng cơ thể (g)
sex | giới tính chim cánh cụt

Thật không may, họ đã không thể ghi lại loài chim cánh cụt, nhưng họ biết rằng có **ít nhất ba** loài bản địa của khu vực: **Adelie**, **Chinstrap** và **Gentoo**. Nhiệm vụ của bạn là áp dụng các kỹ năng khoa học dữ liệu của mình để giúp họ xác định các nhóm trong tập dữ liệu!


### Step 1- Import Required Packages and Loading and examining the dataset


```python

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Loading and examining the dataset
penguins_df = pd.read_csv("penguins.csv")
penguins_df.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>culmen_length_mm</th>
      <th>culmen_depth_mm</th>
      <th>flipper_length_mm</th>
      <th>body_mass_g</th>
      <th>sex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>39.1</td>
      <td>18.7</td>
      <td>181.0</td>
      <td>3750.0</td>
      <td>MALE</td>
    </tr>
    <tr>
      <th>1</th>
      <td>39.5</td>
      <td>17.4</td>
      <td>186.0</td>
      <td>3800.0</td>
      <td>FEMALE</td>
    </tr>
    <tr>
      <th>2</th>
      <td>40.3</td>
      <td>18.0</td>
      <td>195.0</td>
      <td>3250.0</td>
      <td>FEMALE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>36.7</td>
      <td>19.3</td>
      <td>193.0</td>
      <td>3450.0</td>
      <td>FEMALE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>39.3</td>
      <td>20.6</td>
      <td>190.0</td>
      <td>3650.0</td>
      <td>MALE</td>
    </tr>
  </tbody>
</table>
</div>




```python
penguins_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 332 entries, 0 to 331
    Data columns (total 5 columns):
     #   Column             Non-Null Count  Dtype  
    ---  ------             --------------  -----  
     0   culmen_length_mm   332 non-null    float64
     1   culmen_depth_mm    332 non-null    float64
     2   flipper_length_mm  332 non-null    float64
     3   body_mass_g        332 non-null    float64
     4   sex                332 non-null    object 
    dtypes: float64(4), object(1)
    memory usage: 13.1+ KB



```python
penguins_df.isna().sum()
```




    culmen_length_mm     0
    culmen_depth_mm      0
    flipper_length_mm    0
    body_mass_g          0
    sex                  0
    dtype: int64



### Step 2 - Perform preprocessing steps on the dataset to create dummy variables

Convert categorical variables into dummy/indicator variables


```python
penguins_df = pd.get_dummies(penguins_df, dtype='int') # dtype='int' ensure the output will be 0/1 instead of True/False
penguins_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>culmen_length_mm</th>
      <th>culmen_depth_mm</th>
      <th>flipper_length_mm</th>
      <th>body_mass_g</th>
      <th>sex_FEMALE</th>
      <th>sex_MALE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>39.1</td>
      <td>18.7</td>
      <td>181.0</td>
      <td>3750.0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>39.5</td>
      <td>17.4</td>
      <td>186.0</td>
      <td>3800.0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>40.3</td>
      <td>18.0</td>
      <td>195.0</td>
      <td>3250.0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>36.7</td>
      <td>19.3</td>
      <td>193.0</td>
      <td>3450.0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>39.3</td>
      <td>20.6</td>
      <td>190.0</td>
      <td>3650.0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>327</th>
      <td>47.2</td>
      <td>13.7</td>
      <td>214.0</td>
      <td>4925.0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>328</th>
      <td>46.8</td>
      <td>14.3</td>
      <td>215.0</td>
      <td>4850.0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>329</th>
      <td>50.4</td>
      <td>15.7</td>
      <td>222.0</td>
      <td>5750.0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>330</th>
      <td>45.2</td>
      <td>14.8</td>
      <td>212.0</td>
      <td>5200.0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>331</th>
      <td>49.9</td>
      <td>16.1</td>
      <td>213.0</td>
      <td>5400.0</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>332 rows × 6 columns</p>
</div>



### Step 3 - Perform preprocessing steps on the dataset - standarizing/scaling

Scaling variables (also called standardizing) is recommended before performing a clustering algorithm since this can increase the performance greatly (see https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html)



```python
scaler = StandardScaler()
X = scaler.fit_transform(penguins_df)
penguins_preprocessed = pd.DataFrame(data=X,columns=penguins_df.columns)
penguins_preprocessed.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>culmen_length_mm</th>
      <th>culmen_depth_mm</th>
      <th>flipper_length_mm</th>
      <th>body_mass_g</th>
      <th>sex_FEMALE</th>
      <th>sex_MALE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-0.903906</td>
      <td>0.790360</td>
      <td>-1.425342</td>
      <td>-0.566948</td>
      <td>-0.993994</td>
      <td>0.993994</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.830434</td>
      <td>0.126187</td>
      <td>-1.068577</td>
      <td>-0.504847</td>
      <td>1.006042</td>
      <td>-1.006042</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-0.683490</td>
      <td>0.432728</td>
      <td>-0.426399</td>
      <td>-1.187953</td>
      <td>1.006042</td>
      <td>-1.006042</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1.344738</td>
      <td>1.096901</td>
      <td>-0.569105</td>
      <td>-0.939551</td>
      <td>1.006042</td>
      <td>-1.006042</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-0.867170</td>
      <td>1.761074</td>
      <td>-0.783164</td>
      <td>-0.691149</td>
      <td>-0.993994</td>
      <td>0.993994</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-0.940642</td>
      <td>0.330548</td>
      <td>-1.425342</td>
      <td>-0.722199</td>
      <td>1.006042</td>
      <td>-1.006042</td>
    </tr>
    <tr>
      <th>6</th>
      <td>-0.885538</td>
      <td>1.250172</td>
      <td>-0.426399</td>
      <td>0.581912</td>
      <td>-0.993994</td>
      <td>0.993994</td>
    </tr>
    <tr>
      <th>7</th>
      <td>-0.536545</td>
      <td>0.228367</td>
      <td>-1.353989</td>
      <td>-1.250054</td>
      <td>1.006042</td>
      <td>-1.006042</td>
    </tr>
    <tr>
      <th>8</th>
      <td>-0.995746</td>
      <td>2.067616</td>
      <td>-0.711811</td>
      <td>-0.504847</td>
      <td>-0.993994</td>
      <td>0.993994</td>
    </tr>
    <tr>
      <th>9</th>
      <td>-1.363106</td>
      <td>0.330548</td>
      <td>-1.139930</td>
      <td>-0.629049</td>
      <td>1.006042</td>
      <td>-1.006042</td>
    </tr>
  </tbody>
</table>
</div>



### Step 4 - Detect the optimal number of clusters for k-means clustering

Phân tích Elbow (Elbow Method) là một kỹ thuật được sử dụng trong machine learning, đặc biệt trong bài toán phân cụm (clustering), để xác định số lượng cụm tối ưu (k) cho thuật toán k-means.  Nó dựa trên việc quan sát sự thay đổi của tổng bình phương khoảng cách từ các điểm dữ liệu đến tâm cụm của chúng (Within-Cluster Sum of Squares - WCSS) khi số lượng cụm thay đổi.

**Ý tưởng cốt lõi:**

Khi bạn tăng số lượng cụm (k), WCSS thường giảm.  Ban đầu, sự giảm này có thể khá lớn, nhưng đến một điểm nào đó, việc tăng k sẽ không làm WCSS giảm đáng kể nữa.  Điểm "khuỷu tay" (elbow) trên đồ thị biểu diễn WCSS theo k chính là vị trí mà sự giảm WCSS bắt đầu chậm lại.  Điểm này được coi là số lượng cụm tối ưu.

**Cách thức hoạt động:**

1.  **Tính toán WCSS cho các giá trị k khác nhau:**  Bạn chạy thuật toán k-means với các giá trị k khác nhau (ví dụ: từ 1 đến 10) và tính toán WCSS cho mỗi giá trị k.  WCSS được tính bằng tổng bình phương khoảng cách từ mỗi điểm dữ liệu đến tâm cụm gần nhất của nó. Công thức tính WCSS như sau:

    ```
    WCSS = Σ (khoảng cách từ điểm dữ liệu i đến tâm cụm của nó)^2
    ```

2.  **Vẽ đồ thị Elbow:** Vẽ đồ thị đường biểu diễn WCSS theo k.  Trục x là số lượng cụm (k), và trục y là WCSS.

3.  **Xác định "khuỷu tay":** Quan sát đồ thị và tìm điểm "khuỷu tay" - điểm mà đường cong bắt đầu "uốn cong" và trở nên ít dốc hơn.  Điểm này biểu diễn giá trị k tối ưu.  Đôi khi, "khuỷu tay" không rõ ràng, và bạn cần xem xét thêm các yếu tố khác.

**Tại sao gọi là "khuỷu tay"?**

Đồ thị WCSS theo k thường có hình dạng giống như cánh tay khuỷu tay.  Phần "khuỷu tay" chính là điểm mà sự giảm WCSS chậm lại, giống như khớp khuỷu tay.

**Ưu điểm của phân tích Elbow:**

*   Đơn giản và dễ hiểu.
*   Thường cho kết quả tốt trong nhiều trường hợp.

**Nhược điểm của phân tích Elbow:**

*   "Khuỷu tay" có thể không rõ ràng trong một số trường hợp.
*   Chỉ dựa trên WCSS, không xem xét các yếu tố khác.
*   Có thể nhạy cảm với việc khởi tạo tâm cụm ban đầu trong thuật toán k-means.

**Lưu ý:**

Phân tích Elbow là một phương pháp heuristic (dựa trên kinh nghiệm), không phải là một phương pháp chính xác tuyệt đối.  Đôi khi, bạn cần kết hợp nó với các phương pháp khác (ví dụ: phân tích Silhouette, Gap Statistic) để xác định số lượng cụm tối ưu.

**Ví dụ:**

Hãy tưởng tượng bạn có một tập dữ liệu về khách hàng và bạn muốn phân nhóm họ thành các nhóm dựa trên hành vi mua hàng.  Bạn có thể sử dụng phân tích Elbow để xác định số lượng nhóm khách hàng tối ưu.  Bạn sẽ tính toán WCSS cho các giá trị k khác nhau (ví dụ: từ 2 đến 10) và vẽ đồ thị Elbow.  Điểm "khuỷu tay" trên đồ thị sẽ cho bạn biết số lượng nhóm khách hàng tối ưu.



```python
inertia = []
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, random_state=42).fit(penguins_preprocessed)
    inertia.append(kmeans.inertia_)    
plt.plot(range(1, 10), inertia, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()

```


    
![png]({{site.baseurl}}/example_codes/clustering_antarctic_penguin_species/notebook_files/notebook_11_0.png)
    



```python
n_clusters = 4
```

### Step 5 - Run the k-means clustering algorithm


```python
kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(penguins_preprocessed)
penguins_df['label'] = kmeans.labels_
```

**and visualize the clusters (here for the 'culmen_length_mm' column)**

Trong bài toán phân cụm (clustering), phương sai của đặc trưng (feature variance) thể hiện mức độ phân tán của giá trị của một đặc trưng cụ thể trong một cụm. Nó cho biết liệu giá trị của đặc trưng đó có xu hướng tập trung gần giá trị trung bình của cụm hay phân tán rộng rãi.

**Vai trò của Feature variance:**

* **Đánh giá mức độ "chặt chẽ" của cụm:** Phương sai thấp cho thấy các điểm dữ liệu trong cụm có giá trị của đặc trưng đó gần nhau, cho thấy cụm chặt chẽ hơn theo đặc trưng đó. Ngược lại, phương sai cao cho thấy các điểm dữ liệu phân tán hơn, cụm có thể "lỏng lẻo" hơn theo đặc trưng đó.
* **Xác định đặc trưng quan trọng:** Các đặc trưng có phương sai lớn có thể đóng vai trò quan trọng trong việc phân biệt các cụm, vì chúng cho thấy sự khác biệt lớn giữa các cụm. Ngược lại, các đặc trưng có phương sai nhỏ có thể ít quan trọng hơn, vì chúng không thay đổi nhiều giữa các cụm.
* **Lựa chọn đặc trưng:** Dựa trên phương sai, ta có thể lựa chọn các đặc trưng phù hợp cho việc phân cụm. Ví dụ, ta có thể ưu tiên các đặc trưng có phương sai lớn để đảm bảo rằng các cụm được phân biệt rõ ràng dựa trên các đặc trưng này.
* **Phân tích độ nhạy cảm của thuật toán:** Một số thuật toán phân cụm có thể nhạy cảm với phương sai của đặc trưng. Ví dụ, thuật toán k-means có xu hướng tạo ra các cụm có kích thước và hình dạng tương tự nhau, và có thể gặp khó khăn với dữ liệu có phương sai đặc trưng khác nhau.

**Ví dụ:**

Giả sử ta có dữ liệu về chiều cao và cân nặng của một nhóm người. Ta muốn phân cụm họ thành các nhóm dựa trên hai đặc trưng này. Nếu phương sai của đặc trưng chiều cao trong một cụm là thấp, điều đó có nghĩa là chiều cao của các thành viên trong cụm đó khá đồng đều. Ngược lại, nếu phương sai của đặc trưng cân nặng là cao, điều đó có nghĩa là cân nặng của các thành viên trong cụm đó phân tán rộng rãi hơn.

**Lưu ý:**

* Phương sai của đặc trưng cần được xem xét trong ngữ cảnh của từng bài toán cụm.
* Phương sai chỉ là một trong nhiều yếu tố cần xem xét khi phân cụm dữ liệu. Các yếu tố khác bao gồm khoảng cách giữa các điểm dữ liệu, hình dạng của cụm, và mục tiêu của việc phân cụm.

Hy vọng giải thích này giúp bạn hiểu rõ hơn về vai trò của phương sai đặc trưng trong bài toán phân cụm.



```python
plt.scatter(penguins_df['label'], penguins_df['culmen_length_mm'], c=kmeans.labels_, cmap='viridis')
plt.xlabel('Cluster')
plt.ylabel('culmen_length_mm')
plt.xticks(range(int(penguins_df['label'].min()), int(penguins_df['label'].max()) + 1))
plt.title(f'K-means Clustering (K={n_clusters})')
plt.show()
```


    
![png]({{site.baseurl}}/example_codes/clustering_antarctic_penguin_species/notebook_files/notebook_16_0.png)
    


### Step 6 - create final `stat_penguins` DataFrame


```python

numeric_columns = ['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm','label']
stat_penguins = penguins_df[numeric_columns].groupby('label').mean()
stat_penguins
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>culmen_length_mm</th>
      <th>culmen_depth_mm</th>
      <th>flipper_length_mm</th>
    </tr>
    <tr>
      <th>label</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>43.878302</td>
      <td>19.111321</td>
      <td>194.764151</td>
    </tr>
    <tr>
      <th>1</th>
      <td>45.563793</td>
      <td>14.237931</td>
      <td>212.706897</td>
    </tr>
    <tr>
      <th>2</th>
      <td>40.217757</td>
      <td>17.611215</td>
      <td>189.046729</td>
    </tr>
    <tr>
      <th>3</th>
      <td>49.473770</td>
      <td>15.718033</td>
      <td>221.540984</td>
    </tr>
  </tbody>
</table>
</div>


