---
layout: libdoc/page
title: DP1 - Hashed Feature
permalink: /hashed-feature
unlisted: true
description: "Thay vì sử dụng One-hot encoder cho các biến categorical có high-cardinality, ta hash chúng để đưa vào các nhóm nhỏ"
category: Design Pattern
order: 4
---
{:toc}

#### Problem

- Khi dùng one-hot encoding để xử lý các biến phân loại, chúng ta cần phải biết số lượng các biến phân loại ngay từ đầu. Điều gì sẽ sảy ra khi có một số biến phân loại mà chúng ra không thể xác định hết ngay từ quá trình training?
- Khi số lượng các biến phân loại lớn (hàng ngàn loại khác nhau cho 1 feature), One-hot encoding sẽ làm cho kích thước của tập training trở lên rất lớn => kích thước model cũng lớn theo
- Một vấn đề nữa là khi model đã được đưa vào production, mà lúc này phát sinh thêm các loại mới, như khi có các bệnh viện mới (thêm `hospital_id`) hay thêm các bác sĩ mới... vấn đề này gọi là `cold-start` problem

#### Solution

Đi vào một ví dụ cụ thể là bài toán dự đoán thời gian hạ cánh trễ của một chuyến bay. Một trong những dữ liệu đầu vào là sân bay khởi hành. Giả sử, tại thời điểm dữ liệu được thu thâp, có 347 sân bay. Nếu dùng One-hot encoding thì cả 3 vấn đề kể trên sẽ sảy ra.

Giải quyết vấn đề này, **Hashed Feature** design pattern được sinh ra, nó thực hiện các công việc:

2.  Chuyển đổi biến categorical đầu vào thành string duy nhất.
2. Gọi một thuật toán băm trên chuỗi
2. Sau đó chia cho số nhóm mà ta mong muốn, trong trường hợp số âm thì lấy giá trị tuyệt đối.



Trong Tensorflow, các bước này sẽ được triển khai trong: 

```python
tf.feature_column.categorical_column_with_hash_bucket(
    key,
    hash_bucket_size,
    dtype=tf.dtypes.string
)
```

<img src="/pages/resources/hash-features-1.png" alt="hash-features-1" style="zoom:35%;" align="left"/>


Bảng này là một ví dụ sau khi thực hiện Hashed Feature trên biến `departure_airport` , và được băm thành 3, 10, 1000 nhóm.

#### Why It Works

Giả sử chúng tôi đã chọn băm mã sân bay thành 10 nhóm (hash10 trong bảng 2.1). Làm thế nào để điều này giải quyết được các vấn đề kể trên?

- **Out-of-vocabulary input**:

  Ngay cả với một số ít sân bay khi không có trong tập training, thì giá trị sau khi hash của nó vẫn nằm trong khoảng giá trị `[0-9]`. Do đó mô hình sẽ không bị lỗi.

  Nếu chúng tôi có 347 sân bay, thì trung bình 35 sân bay sẽ nhận được cùng một mã nhóm băm nếu chúng tôi băm nó thành 10 nhóm. Một sân bay bị thiếu trong tập dữ liệu huấn luyện sẽ “*mượn*” các đặc điểm của nó từ ~35 sân bay tương tự khác trong nhóm băm. Tất nhiên, dự đoán về một sân bay bị mất tích sẽ không chính xác (không hợp lý khi mong đợi dự đoán chính xác cho các thông tin đầu vào không xác định), nhưng nó sẽ nằm trong phạm vi phù hợp.  

  Chọn số lượng nhóm băm bằng cách cân bằng giữa nhu cầu xử lý đầu vào *out-of-vocabulary* một cách hợp lý và nhu cầu để mô hình phản ánh chính xác đầu vào phân loại. Với 10 nhóm băm, ~35 sân bay trở nên lộn xộn. 

  Một nguyên tắc nhỏ là chọn số lượng nhóm băm sao cho mỗi nhóm có khoảng năm entries . Trong trường hợp này, điều đó có nghĩa
  là `347/5 = 70` nhóm băm là một sự thỏa hiệp tốt

- **High cardinality**

  Dễ dàng nhận thấy rằng vấn đề về số lượng thẻ cao được giải quyết miễn là chúng ta chọn một số lượng nhóm băm đủ nhỏ. Ngay cả khi chúng tôi có hàng triệu sân bay hoặc bệnh viện hoặc bác sĩ, chúng tôi có thể băm chúng thành vài trăm nhóm, do đó giữ cho các yêu cầu về kích thước mô hình và bộ nhớ của hệ thống là thực tế.  

- **Cold start**

  Trong tình huống này, khi một sân bay mới được thêm vào hệ thống, ban đầu nó sẽ nhận được các dự đoán tương ứng các sân bay khác trong nhóm băm. Khi một sân bay trở lên nổi tiếng, sẽ có nhiều chuyến bay hơn, lúc đó chúng ra sẽ lại đào tạo lại mô hình theo chu kỳ.  

  Bằng cách chọn số lượng nhóm băm sao cho mỗi nhóm có khoảng năm entries, chúng tôi có thể đảm bảo rằng bất kỳ nhóm nào cũng sẽ có kết quả ban đầu hợp lý  (Cho đến khi Model được training lại)

  

#### Trade-Offs and Alternatives (Đánh đổi và lựa chọn thay thế)

Sự đánh đổi chính ở đây là chúng ta mất đi độ chính xác của mô hình.  

Việc mất độ chính xác đặc biệt nghiêm trọng khi phân phối đầu vào phân loại bị sai lệch cao. Ví dụ, trong số các sân bay có ORD (Chicago), một sân bay bận rộn bậc nhất thế giới. Khi dùng Hashed Feature, rất có khả năng một sân bay ít bận rộn nào đó sẽ cùng nhóm với ORD, do đó kết quả dự đoán với sân bay đó sẽ bị sai lệch đi rất nhiều.

Do đó, một lời khuyên là nên đưa số lượng nhóm băm vào làm một Hyperparameter để điều chỉnh  



Code Example: https://github.com/aidino/ml-design-patterns/blob/master/02_data_representation/hashed_feature.ipynb
