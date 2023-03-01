<!-- ---
layout: libdoc/page
title: DB3 - Feature Cross
permalink: /feature-cross
category: Design Pattern
description: "Feature Cross design pattern giúp các mô hình tìm hiểu mối quan hệ giữa các yếu tố đầu vào nhanh hơn bằng cách làm cho mỗi kết hợp giá trị đầu vào trở thành một tính năng riêng biệt một cách rõ ràng.  "
order: 4
---
{:toc} -->

#### Problem

Xem xét tập dữ liệu trong Hình 2-14 và nhiệm vụ tạo bộ phân loại nhị phân phân tách các nhãn `+` và ` -  `

<img src="\pages\resources/feature-cross-1.png" alt="feature-cross-1" style="zoom:100%;" />

Điều này có nghĩa là để giải quyết vấn đề này, chúng ta phải làm cho mô hình phức tạp hơn, có thể bằng cách thêm nhiều lớp hơn vào mô hình. 

Tuy nhiên, một giải pháp đơn giản hơn tồn tại.  

#### Solution

Trong học máy, Feature engine là quá trình sử dụng kiến thức miền để tạo ra các tính năng mới hỗ trợ quá trình học máy và tăng khả năng dự đoán cho mô hình của chúng ta. 

Một kỹ thuật kỹ thuật tính năng thường được sử dụng là tạo một Feature cross.  

 Feature cross là một tính năng tổng hợp được hình thành bằng cách ghép hai hoặc nhiều tính năng phân loại để nắm bắt sự tương tác giữa chúng. 

Bằng cách kết hợp hai tính năng theo cách này, có thể mã hóa tính phi tuyến tính vào môhình, điều này có thể cho phép các khả năng dự đoán vượt quá khả năng mà mỗi tính năng có thể cung cấp riêng lẻ. 

Các tính năng chéo cung cấp một cách để mô hình ML tìm hiểu mối quan hệ giữa các tính năng nhanh hơn. Mặc dù các mô hình
phức tạp hơn như Neural Network và Tree có thể tự học các đặc điểm chéo, nhưng việc sử dụng các đặc điểm chéo một cách rõ ràng có thể cho phép chúng ta thoát khỏi việc đào tạo chỉ một mô hình tuyến tính. 

Do đó, các tính năng chéo có thể tăng tốc độ đào tạo mô hình (ít tốn kém hơn) và giảm độ phức tạp của mô hình (cần ít dữ liệu đào tạo hơn).  



Trong Tensorflow:

```python
# is_male can take 3 value (true, false, unknown)
# the plurality input can take  6 values (Single(1), Twins(2), Triplets(3), Quadruplets(4),Quintuplets(5), Multiple(2+))
# => there are 18 possible (is_male, plurality) pairs. If we set hash_bucket_size to 1,000, we can be 85% sure there are no collisions.

gender_x_plurality = fc.crossed_column(["is_male", "plurality"], hash_bucket_size=1000)
crossed_feature = fc.embedding_column(gender_x_plurality, dimension=2)
# or
gender_x_plurality = fc.crossed_column(["is_male", "plurality"], hash_bucket_size=1000)
crossed_feature = fc.indicator_column(gender_x_plurality)
```

#### Why It Works

Feature cross cung cấp một phương tiện có giá trị của Feature enginering. Chúng mang lại sự phức tạp hơn, biểu cảm hơn và nhiều khả năng hơn cho các mô hình đơn giản. 

Hãy suy nghĩ lại về Feature cross của `is_male` và đa số trong bộ dữ liệu sinh sản. Mẫu Feature Cross này cho phép mô hình xử lý các cặp song sinh nam riêng biệt với cặp song sinh nữ và tách biệt với nam giới sinh ba và tách biệt với nữ giới độc thân, v.v. Khi chúng ta sử dụng một indicator_column, mô hình có thể xử lý từng kết quả chéo như một biến độc lập, về cơ bản thêm 18  các tính năng phân loại nhị phân bổ sung cho mô hình  .





Code Example: https://github.com/aidino/ml-design-patterns/blob/master/02_data_representation/feature_cross.ipynb