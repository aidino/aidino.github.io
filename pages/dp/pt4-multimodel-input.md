---
layout: libdoc/page
title: DB4 - Multimodel Input
permalink: /multimodel-input
category: Design Pattern
description: "Multimodel input design pattern giải quyết vấn đề biểu diễn các loại dữ liệu hoặc dữ liệu khác nhau có thể được biểu thị theo những cách phức tạp bằng cách ghép nối tất cả các biểu diễn dữ liệu có sẵn. "
order: 4
---
{:toc}

#### Problem

Thông thường, đầu vào của một mô hình có thể được biểu diễn dưới dạng số hoặc dưới dạng danh mục, hình ảnh hoặc văn bản dạng tự do. Nhiều mô hình có sẵn chỉ được xác định cho các loại đầu vào cụ thể—ví dụ: mô hình phân loại hình ảnh tiêu chuẩn như
Resnet-50 không có khả năng xử lý các đầu vào khác ngoài hình ảnh  

Để hiểu nhu cầu về multimodel input, giả sử chúng ta có một camera ghi lại cảnh quay tại giao lộ để xác định vi phạm giao thông.
Chúng tôi muốn mô hình của mình xử lý cả dữ liệu hình ảnh (cảnh quay của camera) và một số siêu dữ liệu về thời điểm hình ảnh được chụp (thời gian trong ngày, ngày trong tuần, thời tiết, v.v.),  

Không giống như dữ liệu số, hình ảnh và văn bản không thể được đưa trực tiếp vào mô hình. Do đó, chúng ta sẽ cần thể hiện các đầu vào hình ảnh và
văn bản theo cách mà mô hình của chúng ta có thể hiểu được (thường sử dụng Embedding), sau đó kết hợp các đầu vào này với các tính năng dạng bảng khác. 

Ví dụ: chúng tôi có thể muốn dự đoán xếp hạng của khách hàng quen nhà hàng dựa trên văn bản đánh giá của họ và các thuộc tính khác như số tiền họ đã thanh toán và đó là bữa trưa hay bữa tối   

![](/pages/resources/multimodel-input-1.png)





#### Solution

Để bắt đầu, hãy lấy ví dụ ở trên với văn bản từ bài đánh giá nhà hàng kết hợp với siêu dữ liệu dạng bảng về bữa ăn được tham chiếu bởi bài đánh giá.

```python
embedding_input = Input(shape=(30,))
embedding_layer = Embedding(batch_size, 64)(embedding_input)
embedding_layer = Flatten()(embedding_layer)
embedding_layer = Dense(3, activation='relu')(embedding_layer)

tabular_input = Input(shape=(4,))
tabular_layer = Dense(32, activation='relu')(tabular_input)

merged_input = keras.layers.concatenate([embedding_layer, tabular_layer])
merged_dense = Dense(16)(merged_input)
output = Dense(1)(merged_dense)
model = Model(inputs=[embedding_input, tabular_input],
outputs=output)
merged_dense = Dense(16, activation='relu')(merged_input)
output = Dense(1)(merged_dense)
model = Model(inputs=[embedding_input, tabular_input],
outputs=output)
```



Code Example: https://github.com/aidino/ml-design-patterns/blob/master/02_data_representation/mixed_representation.ipynb