---
layout: post
title: "[Paper] Contrastive Preference Optimization: Pushing the Boundaries of LLM Performance in Machine Translation"
date: 2025-01-07 09:00:00 +0700
categories: nmt paper
Authors: Haoran Xu, Amr Sharaf, Yunmo Chen, Weiting Tan, Lingfeng Shen, Benjamin Van Durme, Kenton Murray, Young Jin Kim
---

Các mô hình ngôn ngữ lớn (LLM) cỡ vừa – với 7 tỷ hoặc 13 tỷ tham số – thể hiện hiệu suất dịch máy (MT) đầy hứa hẹn. Tuy nhiên, chúng không sánh được với hiệu suất của các mô hình dịch mã hóa-giải mã thông thường tiên tiến hoặc các LLM quy mô lớn hơn như GPT-4 (OpenAI, 2023). Trong nghiên cứu này, chúng tôi thu hẹp khoảng cách hiệu suất này. 

Trước tiên, chúng tôi đánh giá những thiếu sót của **supervised fine-tuning** đối với LLM trong nhiệm vụ MT, nhấn mạnh các vấn đề về chất lượng hiện diện trong dữ liệu tham chiếu, mặc dù được con người tạo ra. Sau đó, trái ngược với **supervised fine-tuning** vốn bắt chước các bản dịch tham chiếu, chúng tôi giới thiệu **Contrastive Preference Optimization (CPO)**, một phương pháp mới huấn luyện các mô hình để tránh tạo ra các bản dịch tạm được nhưng không hoàn hảo. 

Áp dụng CPO cho các mô hình ALMA (Xu et al., 2023) chỉ với 22 nghìn câu song ngữ và chỉ **fine-tuning** 0,1% tham số mang lại những cải thiện đáng kể. Mô hình thu được, được gọi là ALMA-R, có thể sánh ngang hoặc vượt qua hiệu suất của những người chiến thắng cuộc thi WMT và GPT-4 trên các bộ dữ liệu thử nghiệm WMT’21, WMT’22 và WMT’23.

Bài báo gốc: https://arxiv.org/abs/2401.08417 

### 1. Introduction

Dịch máy (MT) chủ yếu sử dụng kiến trúc mã hóa-giải mã transformer (Vaswani et al., 2017), điều này thể hiện rõ trong các mô hình nổi bật như NLLB-200 (NLLB TEAM et al., 2022), M2M100 (Fan et al., 2021), BiBERT (Xu et al., 2021) và MT5 (Xue et al., 2021). Tuy nhiên, sự xuất hiện của các mô hình ngôn ngữ lớn (LLM) chỉ giải mã như dòng GPT (Brown et al., 2020; OpenAI, 2023), Mistral (Jiang et al., 2023), dòng LLaMA (Touvron et al., 2023a;b), Falcon (Almazrouei et al., 2023), cùng nhiều mô hình khác, đã cho thấy hiệu quả đáng kể trong các nhiệm vụ NLP khác nhau, thu hút sự quan tâm đến việc phát triển dịch máy với các LLM chỉ giải mã này. 

Các nghiên cứu gần đây (Zhu et al., 2023a; Jiao et al., 2023b; Hendy et al., 2023; Kocmi et al., 2023; Freitag et al., 2023) chỉ ra rằng các LLM lớn hơn như GPT-3.5 (175B) và GPT-4 thể hiện khả năng dịch mạnh mẽ. Tuy nhiên, hiệu suất của các LLM kích thước nhỏ hơn (7B hoặc 13B) vẫn còn kém so với các mô hình dịch thông thường (Zhu et al., 2023a).

Do đó, có những nghiên cứu nhằm mục đích nâng cao hiệu suất dịch cho các LLM nhỏ hơn này (Yang et al., 2023; Zeng et al., 2023; Chen et al., 2023; Zhu et al., 2023b; Li et al., 2023; Jiao et al., 2023a; Zhang et al., 2023), nhưng những cải tiến của họ còn tương đối khiêm tốn, chủ yếu do việc **pre-training** LLM chủ yếu trên các tập dữ liệu tập trung vào tiếng Anh, dẫn đến sự đa dạng ngôn ngữ hạn chế (Xu et al., 2023). 

Để giải quyết hạn chế này, Xu et al. (2023) ban đầu **fine-tune** LLaMA-2 (Touvron et al., 2023b) với dữ liệu đơn ngữ không phải tiếng Anh mở rộng để nâng cao khả năng đa ngôn ngữ của chúng, và sau đó thực hiện **supervised fine-tune (SFT)** với dữ liệu song ngữ chất lượng cao để hướng dẫn mô hình tạo ra bản dịch. Mô hình của họ, được đặt tên là ALMA, vượt trội hơn tất cả các LLM cỡ vừa trước đó, và thậm chí cả các mô hình lớn hơn như GPT-3.5, trong nhiệm vụ dịch. Tuy nhiên, hiệu suất vẫn còn kém so với các mô hình dịch hàng đầu như GPT-4 và những người chiến thắng cuộc thi WMT. 

Nghiên cứu của chúng tôi thu hẹp khoảng cách này bằng cách **fine-tuning** thêm các mô hình ALMA với phương pháp huấn luyện mới của chúng tôi là **Contrastive Preference Optimization (CPO)** và chi phí tối thiểu, tức là chỉ 12 triệu tham số có thể học được (tương đương 0,1% kích thước mô hình ban đầu) và tập dữ liệu 22K cho 10 hướng dịch. Mô hình được **fine-tuned** được gọi là ALMA-R. So sánh hiệu suất chi tiết được minh họa trong Hình 1.

CPO nhằm mục đích giảm thiểu hai thiếu sót cơ bản của SFT. Đầu tiên, phương pháp của SFT là giảm thiểu sự khác biệt giữa đầu ra dự đoán và tham chiếu tiêu chuẩn vàng vốn đã giới hạn hiệu suất mô hình ở mức chất lượng của dữ liệu huấn luyện. Hạn chế này rất đáng kể, vì ngay cả dữ liệu do con người viết, theo truyền thống được coi là chất lượng cao, cũng không tránh khỏi các vấn đề về chất lượng (chi tiết hơn trong Phần 2).

Ví dụ, người ta có thể nhận thấy rằng một số mô hình dịch mạnh có khả năng tạo ra các bản dịch vượt trội so với tham chiếu vàng, như được minh họa trong Hình 1. Thứ hai, SFT thiếu cơ chế để ngăn mô hình từ chối các lỗi trong bản dịch. Mặc dù các mô hình dịch mạnh có thể tạo ra các bản dịch chất lượng cao, nhưng đôi khi chúng vẫn xuất hiện các lỗi nhỏ, chẳng hạn như bỏ sót các phần của bản dịch. Việc ngăn chặn việc tạo ra những bản dịch gần như hoàn hảo nhưng cuối cùng vẫn có sai sót này là điều cần thiết. Để khắc phục những vấn đề này, chúng tôi giới thiệu **Contrastive Preference Optimization (CPO)** để huấn luyện mô hình ALMA bằng cách sử dụng dữ liệu ưu tiên được tuyển chọn đặc biệt. Sau khi huấn luyện CPO, mô hình ALMA-R cho thấy những cải thiện rõ rệt, đạt được mức hiệu suất phù hợp hoặc thậm chí vượt qua GPT-4 và những người chiến thắng cuộc thi WMT.

Những đóng góp chính của chúng tôi được tóm tắt như sau:

**Tham chiếu là Vàng hay Mạ vàng?** Chúng tôi đã thực hiện một phân tích chuyên sâu về dữ liệu huấn luyện (dữ liệu FLORES-200) được sử dụng bởi mô hình ALMA. Chúng tôi đã so sánh tỉ mỉ chất lượng của các bản dịch tham chiếu với những bản dịch được tạo bởi các mô hình dịch mạnh. Kết quả của chúng tôi cho thấy, trong nhiều trường hợp, chất lượng của dữ liệu song ngữ do con người viết thậm chí còn kém hơn so với các bản dịch do hệ thống tạo ra. Quan sát này nhấn mạnh một nhận thức quan trọng: huấn luyện mô hình chỉ để sao chép các bản dịch tham chiếu có thể không phải là cách tiếp cận hiệu quả nhất và việc phụ thuộc vào đánh giá dựa trên tham chiếu có thể có sai sót.

**Đẩy Mạnh Ranh Giới Hiệu Suất của SFT** Chúng tôi giới thiệu **Contrastive Preference Optimization**, mang lại lợi thế về hiệu quả bộ nhớ, tốc độ và quan trọng là tăng cường hiệu quả trong việc cải thiện chất lượng dịch. CPO phá vỡ nút thắt cổ chai hiệu suất vốn có trong quá trình học bắt chước tham chiếu của SFT và đẩy mạnh ranh giới hiệu suất của các mô hình đã đạt đến độ bão hòa thông qua huấn luyện SFT.1

**Dữ liệu Ưu tiên** Chúng tôi xây dựng và phát hành một tập dữ liệu ưu tiên chất lượng cao cho lĩnh vực dịch máy.

### 2. Gold or Gilded? Scrutinizing Gold Reference Quality