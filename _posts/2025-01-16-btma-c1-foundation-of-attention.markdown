---
layout: post
title: "Foundations of Attention"
date: 2025-01-16 00:00:00 +0700
categories: transformer
---

Trong học máy (machine learning), "attention" đang trở nên ngày càng phổ biến. Nhưng điều gì khiến nó hấp dẫn đến vậy? Mối quan hệ giữa "attention" trong mạng nơ-ron nhân tạo (artificial neural networks) và cơ chế tương tự trong sinh học là gì? Một hệ thống "attention-based" trong học máy cần những thành phần nào?

### What Is Attention?
#### Attention

"Attention" là một khái niệm được nghiên cứu rộng rãi, thường được xem xét cùng với sự hưng phấn (arousal), sự tỉnh táo (alertness) và sự tương tác với môi trường xung quanh (engagement).

Nói một cách đơn giản, "attention" có thể được hiểu là mức độ tỉnh táo chung hoặc khả năng tương tác với môi trường.

**Sự chú ý thị giác (Visual attention)** là một trong những lĩnh vực được nghiên cứu nhiều nhất từ góc độ khoa học thần kinh và tâm lý học. Khi một người được cho xem các hình ảnh khác nhau, chuyển động mắt của họ có thể tiết lộ những phần nổi bật của hình ảnh mà họ **chú ý** đến nhất. Các phần nổi bật này thường có các đặc điểm thị giác như độ tương phản cường độ (intensity contrast), các cạnh định hướng (oriented edges), góc và điểm nối (corners and junctions), và chuyển động (motion).

Não bộ con người chú ý đến các đặc điểm thị giác nổi bật này ở các giai đoạn thần kinh khác nhau. Các nơ-ron ở giai đoạn đầu sẽ được điều chỉnh để nhận biết các thuộc tính thị giác đơn giản như độ tương phản, màu sắc đối lập, hướng, tốc độ chuyển động.  Các nơ-ron ở giai đoạn sau sẽ xử lý các thông tin phức tạp hơn như góc cạnh, hình dạng, hoặc thậm chí là các vật thể cụ thể trong thế giới thực.

Điều thú vị là, nghiên cứu cũng cho thấy những người khác nhau thường bị thu hút bởi cùng một **dấu hiệu thị giác nổi bật (salient visual cues)**.

**Ví dụ:**

Hãy tưởng tượng bạn đang xem một bức ảnh có rất nhiều người.  Mắt bạn sẽ tự động bị thu hút bởi những người có quần áo màu sắc sặc sỡ hoặc những người đang có hành động nổi bật. Đây chính là "visual attention" trong thực tế.

**Mối quan hệ giữa trí nhớ (memory) và sự chú ý (attention):**

Nghiên cứu cũng đã phát hiện ra mối quan hệ tương tác giữa trí nhớ và sự chú ý. Vì não bộ có dung lượng bộ nhớ hạn chế, nên việc lựa chọn thông tin nào để lưu trữ trở nên rất quan trọng. Não bộ thực hiện điều này bằng cách dựa vào sự chú ý, nghĩa là nó sẽ ưu tiên lưu trữ những thông tin mà chúng ta **chú ý** nhiều nhất.

**Ví dụ:**

Khi bạn đang học bài, nếu bạn tập trung cao độ vào một đoạn văn, bạn sẽ dễ dàng ghi nhớ nó hơn. Ngược lại, nếu bạn bị phân tâm bởi những thứ xung quanh, bạn sẽ khó lòng nhớ được nội dung bài học.

Tóm lại, "attention" là một cơ chế quan trọng giúp não bộ xử lý thông tin hiệu quả. Nó cho phép chúng ta tập trung vào những thông tin quan trọng, từ đó hiểu và ghi nhớ tốt hơn.

#### Attention in Machine Learning
Việc triển khai cơ chế "attention" trong mạng nơ-ron nhân tạo không nhất thiết phải theo sát cơ chế sinh học và tâm lý của não người. Thay vào đó, chính khả năng **làm nổi bật và sử dụng những phần thông tin quan trọng một cách linh hoạt** - tương tự như cách não bộ hoạt động - đã khiến "attention" trở thành một khái niệm hấp dẫn trong học máy.

Một hệ thống "attention-based" thường bao gồm ba thành phần:

1. **Bộ đọc (Reader):** Đọc dữ liệu thô (ví dụ như các từ trong câu) và chuyển đổi chúng thành các biểu diễn phân tán (distributed representations), với mỗi từ được gán một vector đặc trưng.
2. **Bộ nhớ (Memory):**  Lưu trữ danh sách các vector đặc trưng đầu ra của bộ đọc. Có thể hiểu đây là một "bộ nhớ" chứa chuỗi các thông tin, có thể được truy xuất sau này mà không cần phải duyệt qua tất cả.
3. **Bộ khai thác (Exploiter):** Sử dụng nội dung của bộ nhớ để thực hiện nhiệm vụ một cách tuần tự, tại mỗi bước thời gian có khả năng **tập trung** vào nội dung của một (hoặc một vài) phần tử trong bộ nhớ.

**Ví dụ với mô hình Encoder-Decoder:**

Giả sử chúng ta đang xử lý một chuỗi các từ đầu vào. Chuỗi này sẽ được đưa vào **bộ mã hóa (encoder)**, tạo ra một vector cho mỗi từ trong chuỗi. **Bộ giải mã (decoder)** sẽ sử dụng các vector này, cùng với trạng thái ẩn trước đó của nó, để tạo ra chuỗi đầu ra. **Cơ chế "attention"** sẽ giúp decoder **tập trung** vào những từ quan trọng trong chuỗi đầu vào để tạo ra kết quả chính xác hơn.

**Cụ thể:**

* Tại mỗi bước thời gian, "attention" sẽ tính toán mức độ liên quan giữa trạng thái ẩn của decoder và từng vector trong bộ nhớ.
* Các mức độ liên quan này được chuẩn hóa bằng hàm **softmax** để tạo thành các trọng số (weights), có giá trị từ 0 đến 1 và tổng bằng 1.
* Các vector trong bộ nhớ được nhân với trọng số tương ứng để tạo ra một **vector ngữ cảnh (context vector)**.
* Vector ngữ cảnh này được đưa vào decoder để tạo ra đầu ra.

**Lợi ích của "attention":**

* **Linh hoạt:** "Attention" cho phép mô hình tập trung vào những phần thông tin khác nhau tùy thuộc vào ngữ cảnh.
* **Hiệu quả:**  Decoder có thể truy cập thông tin quan trọng từ toàn bộ chuỗi đầu vào, thay vì chỉ một vector cố định.

**Ví dụ:**

Khi dịch câu "Tôi thích ăn phở", "attention" có thể giúp mô hình tập trung vào từ "phở" khi dịch sang tiếng Anh ("I like to eat pho"), vì đây là từ mang ý nghĩa quan trọng nhất trong câu.

**Ứng dụng:**

Ban đầu, "attention" được sử dụng trong dịch máy (machine translation) để xử lý chuỗi từ. Tuy nhiên, nó có thể được áp dụng cho nhiều loại dữ liệu khác, bao gồm cả hình ảnh.

Tóm lại, "attention" là một cơ chế mạnh mẽ giúp mô hình học máy xử lý thông tin hiệu quả hơn bằng cách tập trung vào những phần quan trọng nhất.


---
### A Bird’s Eye View of Research on Attention
#### The Concept of Attention

Nghiên cứu về "attention" bắt nguồn từ lĩnh vực tâm lý học. Các thí nghiệm hành vi trong tâm lý học đã giúp chứng minh một cách chính xác xu hướng và khả năng tập trung của con người trong các hoàn cảnh khác nhau. Từ đó, các nhà nghiên cứu có thể suy luận ra các quá trình tâm lý đằng sau những hành vi này.

Mặc dù tâm lý học, khoa học thần kinh, và gần đây là học máy, đều có những định nghĩa riêng về "attention", nhưng có một đặc điểm cốt lõi chung cho tất cả:

> **"Attention" là sự kiểm soát linh hoạt các nguồn lực tính toán hạn chế (flexible control of limited computational resources).**

**Ví dụ:**

Hãy tưởng tượng bạn đang làm bài kiểm tra với thời gian hạn chế. Bạn sẽ phải **tập trung** vào những câu hỏi quan trọng nhất để đạt điểm cao, thay vì lãng phí thời gian vào những câu hỏi khó mà bạn không chắc chắn. Đây chính là sự kiểm soát linh hoạt nguồn lực tính toán (thời gian và năng lượng) để đạt được mục tiêu.

Trong học máy, "attention" cũng hoạt động theo nguyên tắc tương tự. Mô hình sẽ học cách **tập trung** vào những phần dữ liệu quan trọng nhất, giúp xử lý thông tin hiệu quả hơn với nguồn lực tính toán hạn chế.

**Ví dụ:**

Khi dịch một đoạn văn dài, mô hình "attention" sẽ tập trung vào những từ khóa quan trọng, thay vì xử lý tất cả các từ một cách đều nhau. Điều này giúp mô hình tiết kiệm tài nguyên và dịch chính xác hơn.

**Tầm quan trọng của "attention" trong học máy:**

"Attention" đã cách mạng hóa lĩnh vực học máy bằng cách:

* **Nâng cao hiệu quả:** Giúp mô hình xử lý thông tin hiệu quả hơn với nguồn lực tính toán hạn chế.
* **Cải thiện độ chính xác:** Cho phép mô hình tập trung vào những phần dữ liệu quan trọng, từ đó đưa ra kết quả chính xác hơn.
* **Mở rộng khả năng ứng dụng:** "Attention" có thể được áp dụng cho nhiều loại dữ liệu và nhiệm vụ khác nhau, từ xử lý ngôn ngữ tự nhiên đến thị giác máy tính.

Các phần tiếp theo sẽ đi sâu vào vai trò của "attention" trong việc cách mạng hóa lĩnh vực học máy.

#### Attention in Machine Learning

Khái niệm "attention" trong học máy được lấy cảm hứng một cách **lỏng lẻo** từ cơ chế tâm lý của sự chú ý trong não người. 

Cũng giống như não bộ cần sự chú ý để hoạt động linh hoạt, "attention" trong mạng nơ-ron nhân tạo (artificial neural networks - ANNs) cũng ra đời với mục đích tương tự: **giúp hệ thống thần kinh nhân tạo trở nên linh hoạt hơn.**

Ý tưởng chính là tạo ra một mạng nơ-ron nhân tạo có thể hoạt động tốt với các dữ liệu đầu vào có độ dài, kích thước hoặc cấu trúc **thay đổi**, thậm chí là xử lý nhiều tác vụ khác nhau. Chính vì vậy, có thể nói "attention" trong học máy lấy cảm hứng từ tâm lý học, chứ không phải là sao chép hoàn toàn cơ chế sinh học của não người.

**Ví dụ:**

Trong dịch máy, encoder sẽ chuyển đổi câu tiếng Việt thành một biểu diễn vector, decoder sẽ sử dụng biểu diễn vector này và "attention" để tạo ra câu tiếng Anh tương ứng.

Có nhiều kiến trúc mạng nơ-ron khác nhau triển khai cơ chế "attention", và chúng thường gắn liền với các ứng dụng cụ thể. **Xử lý ngôn ngữ tự nhiên (Natural language processing - NLP)** và **thị giác máy tính (computer vision)** là hai trong số những ứng dụng phổ biến nhất của "attention".

**Ví dụ:**

* Trong NLP, "attention" được sử dụng để dịch máy, tóm tắt văn bản, phân tích cảm xúc,...
* Trong thị giác máy tính, "attention" được sử dụng để nhận dạng đối tượng, tạo chú thích cho ảnh,...

**Attention in Natural Language Processing**

Một ứng dụng ban đầu của "attention" trong NLP là **dịch máy (machine translation)**, với mục tiêu dịch một câu đầu vào từ ngôn ngữ nguồn sang ngôn ngữ đích.

Trong ngữ cảnh này, **encoder** sẽ tạo ra một tập hợp các **vector ngữ cảnh (context vectors)**, mỗi vector đại diện cho một từ trong câu nguồn. **Decoder** sẽ đọc các vector ngữ cảnh này để tạo ra câu đầu ra trong ngôn ngữ đích, từng từ một.

Trước đây, trong mô hình encoder-decoder truyền thống **không có attention**, encoder tạo ra một **vector có độ dài cố định** bất kể độ dài hay đặc điểm của câu đầu vào. Điều này gây ra vấn đề cho các câu dài hoặc phức tạp, vì chúng bị buộc phải có cùng kích thước biểu diễn với các câu ngắn hơn.

**Ví dụ:**

Khi dịch một câu tiếng Việt dài sang tiếng Anh, vector có độ dài cố định có thể không chứa đủ thông tin để decoder tạo ra câu dịch chính xác.

"Attention" giải quyết vấn đề này bằng cách cho phép decoder **tập trung vào những phần quan trọng nhất của câu đầu vào**.

**Ví dụ:**

Khi dịch câu "Hôm nay tôi đi học ở trường đại học", "attention" có thể giúp decoder tập trung vào các từ "học" và "trường đại học" để tạo ra câu dịch chính xác "Today I go to university".

**Một số nghiên cứu quan trọng về "attention" trong dịch máy:**

* **Bahdanau et al. (2015):** Sử dụng mạng nơ-ron hồi quy (Recurrent Neural Networks - RNNs) cho cả encoder và decoder. "Attention" được sử dụng để tính toán trọng số cho các từ trong câu nguồn, từ đó tạo ra vector ngữ cảnh cho decoder.
* **Sutskever et al. (2014):** Sử dụng mạng LSTM (Long Short-Term Memory) nhiều lớp cho encoder và decoder.
* **Luong et al. (2015):** Giới thiệu khái niệm "attention" toàn cục (global) và cục bộ (local). "Attention" toàn cục xem xét tất cả các trạng thái ẩn của encoder, trong khi "attention" cục bộ chỉ tập trung vào một tập hợp con các từ.
* **Vaswani et al. (2017):** Đề xuất kiến trúc **Transformer**, loại bỏ hoàn toàn các thành phần hồi quy và tích chập, thay vào đó sử dụng cơ chế **"self-attention"**. Transformer đã đạt được hiệu quả vượt trội trong dịch máy và nhanh hơn các kiến trúc trước đó.
* **Devlin et al. (2019):** Phát triển phương pháp **BERT** dựa trên Transformer, sử dụng kiến trúc hai chiều nhiều lớp.

**Kết quả:**

Kiến trúc Transformer đã nhanh chóng được áp dụng rộng rãi trong NLP và cả trong lĩnh vực thị giác máy tính.

Tóm lại, "attention" đã đóng góp đáng kể vào sự phát triển của NLP, đặc biệt là trong lĩnh vực dịch máy. Nó giúp cải thiện độ chính xác và hiệu quả của mô hình bằng cách cho phép mô hình tập trung vào những phần thông tin quan trọng nhất.

**Attention in Computer Vision**

Trong thị giác máy tính, "attention" đã được ứng dụng vào nhiều lĩnh vực, chẳng hạn như phân loại ảnh (image classification), phân đoạn ảnh (image segmentation) và tạo chú thích cho ảnh (image captioning).

**Ví dụ về tạo chú thích cho ảnh:**

Mô hình encoder-decoder có thể được điều chỉnh để thực hiện nhiệm vụ này. 

* **Encoder** có thể là một mạng nơ-ron tích chập (Convolutional Neural Network - CNN) để trích xuất các đặc trưng thị giác nổi bật trong ảnh và chuyển đổi thành biểu diễn vector.
* **Decoder** có thể là một mạng RNN hoặc LSTM để chuyển đổi biểu diễn vector này thành câu chú thích.

Trong thị giác máy tính, "attention" có thể được chia thành hai loại: **"attention" không gian (spatial attention)** và **"attention" đặc trưng (feature attention)**.

* **Spatial attention:** Gán trọng số khác nhau cho các vị trí không gian khác nhau trong ảnh.
    * **Ví dụ:** Khi tạo chú thích cho bức ảnh có một con mèo đang ngồi trên ghế sofa, "spatial attention" có thể giúp mô hình tập trung vào vùng ảnh chứa con mèo và ghế sofa, đồng thời giảm trọng số cho các vùng khác.
* **Feature attention:** Gán trọng số khác nhau cho các kênh đặc trưng khác nhau.
    * **Ví dụ:**  Mô hình có thể tập trung vào các kênh đặc trưng liên quan đến hình dạng và màu sắc của con mèo, đồng thời giảm trọng số cho các kênh đặc trưng khác như nền hoặc ánh sáng.

**Một số nghiên cứu quan trọng về "attention" trong thị giác máy tính:**

* **Xu et al. (2015):** Sử dụng "attention" để tạo chú thích cho ảnh. Mô hình kết hợp CNN làm encoder và LSTM làm decoder. Nghiên cứu này cũng so sánh hiệu quả của **"attention" mềm (soft attention)** và **"attention" cứng (hard attention)**.
* **Chen et al. (2017):** Sử dụng cả "spatial attention" và "feature attention" trong cùng một mô hình CNN để tạo chú thích cho ảnh.
* **Dosovitskiy et al. (2021):** Đề xuất kiến trúc **Vision Transformer (ViT)** cho nhiệm vụ phân loại ảnh. ViT thay thế CNN bằng Transformer, chứng minh rằng Transformer có thể đạt được hiệu quả tương đương hoặc tốt hơn trong xử lý ảnh.
* **Arnab et al. (2021):** Mở rộng ViT thành **ViViT** để xử lý video. ViViT khai thác thông tin không gian và thời gian trong video để thực hiện nhiệm vụ phân loại video.

**Kết quả:**

Kiến trúc Transformer đang ngày càng được ưa chuộng trong thị giác máy tính, được ứng dụng vào nhiều lĩnh vực như định vị hành động, ước lượng hướng nhìn và tạo ảnh.

Tóm lại, "attention" đã mang lại những tiến bộ đáng kể trong thị giác máy tính, giúp cải thiện hiệu quả và độ chính xác của mô hình trong nhiều ứng dụng khác nhau. Sự phát triển nhanh chóng của kiến trúc Transformer hứa hẹn một tương lai thú vị cho lĩnh vực này.

---
### A Tour of Attention-Based
#### The Encoder-Decoder Architecture
#### The Transformer
#### Graph Neural Networks
#### Memory-Augmented Neural Networks

---
### The Bahdanau Attention Mechanism
#### Introduction to the Bahdanau Attention
#### The Bahdanau Architecture

---
### The Luong Attention Mechanism
#### Introduction to the Luong Attention
#### The Luong Attention Algorithm
#### The Global Attentional Model
#### The Local Attentional Model
#### Comparison to the Bahdanau Attention