## Embedding

Embedding là một biểu diễn dữ liệu học được. Nó ánh xạ dữ liệu high-cardinality sang không gian với số chiều thấp hơn mà không làm mất đi thông tin

#### Problem

Xử lý dữ liệu để đưa vào mô hình học máy là một bước vô cùng quan trọng, nó ảnh hưởng rất lớn đến kết quả dự đoán của mô hình. Sử lý dữ liệu Categorical, biến nó thành dữ liệu dạng số để đưa vào mô hình là một bước quan trọng trong data processing.

Embedding cung cấp một cách để xử lý loại dữ liệu này, giúp duy trì sự tương đồng giữa các mục, cải thiện khả năng tìm hiểu mẫu của mô hình.

Với One-hot encoding, khi các mục trong một biến categorical lớn sẽ dẫn đến số chiều sau khi One-hot là rất lớn.

#### Solution

Embedding design pattern giải quyết vấn đề biểu diễn dữ liệu số chiều lớn sang dữ liệu có số chiều thấp hơn bằng cách chuyển dữ liệu qua một lớp nhúng có trọng số và có thể huấn luyện. Điều này sẽ ánh xạ biến đầu vào phân loại, có chiều cao thành một vectơ có giá trị thực trong một số không gian có chiều thấp.  Các trọng số để tạo biểu diễn dày đặc được học như một phần của quá trình tối ưu hóa mô hình.

Trong thực tế, các phần nhúng này cuối cùng nắm bắt được các mối quan hệ gần gũi trong dữ liệu đầu vào .

> Note: Vì các lớp nhúng nắm bắt các mối quan hệ gần gũi trong dữ liệu đầu vào ở dạng biểu diễn ít chiều hơn nên chúng ta có thể sử dụng lớp nhúng để thay thế cho các kỹ thuật phân cụm (ví dụ: phân khúc khách hàng) và các phương pháp giảm kích thước như phân tích thành phần chính (PCA).
> Các trọng số nhúng được xác định trong vòng đào tạo mô hình chính, do đó tiết kiệm được nhu cầu phân cụm hoặc thực hiện PCA trước.  



Trong Tensorflow:

```python
# Tạo dữ liệ
plurality = tf.feature_column.categorical_column_with_vocabulary_list('plurality', ['Single(1)', 'Multiple(2+)',
'Twins(2)', 'Triplets(3)', 'Quadruplets(4)', 'Quintuplets(5)'])

# Đưa dữ liệu qua Embedding
plurality_embed = tf.feature_column.embedding_column(plurality, dimension=2)
```

Kết quả:

<img src="resources\embedding-1.png" alt="embedding-1" style="zoom:100%;" align="left" />

Một ví dụ khác của Embeding là trong NLP, chúng ta cần mã hóa văn bản, các từ vựng trong văn bản.



#### Why It Works

Lớp nhúng chỉ là một lớp ẩn khác của Neural Network.  Sau đó, các trọng số được liên kết với từng high-cadinality dimensions và đầu ra được chuyển qua phần còn lại của mạng.  Do đó, các trọng số để tạo nhúng được học thông qua gradient descent  giống như bất kỳ trọng số nào khác trong Neural Network . Điều này có nghĩa là kết quả nhúng véc-tơ biểu thị biểu diễn chiều thấp hiệu quả nhất của các giá trị đặc trưng đó đối với nhiệm vụ học tập.  

#### Trade-Off and Alternatives

Có sự mất mát thông tin khi chuyển đổi từ dữ liệu chiều cao sang chiều thấp hơn.

- **Chọn dimention**

  + Chọn kích thước nhúng bằng ` căn bậc 4 của số lượng biến categorical duy nhất` 
  + Một con số thứ 2 có thể chọn là `1,6 x căn bậc 2 của số lượng biến categorical duy nhất`

  Ví dụ để mã hóa một feature có 625 giá trị duy nhất, khi ấy có thể chọn dimention = ` căn bậc 4 của 625` = `5`, hoặc `1.6 x căn bậc 2 của 625` = `40`.

  Nếu chúng tôi đang thực hiện điều chỉnh siêu tham số, có thể đáng để tìm kiếm trong phạm vi này  