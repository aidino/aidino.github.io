---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: page
title: ML Design patterns
permalink: /design-patterns/
---

- *Book: Machine Learning Design Patterns by Valliappa Lakshmanan, Sara Robinson, and Michael Munn (O’Reilly). Copyright 2021 Valliappa Lakshmanan, Sara Robinson, and Michael Munn, 978-1-098-11578-4.*
  
- *Code:* https://github.com/GoogleCloudPlatform/ml-design-patterns

<hr>
<br>

#### **1. Data Representation Design Patterns**
- [Design Pattern 1: Hashed Feature](https://aidino.github.io/contents/design-patterns/pt1-hashed-feature.html) <br>
    *Thay vì sử dụng One-hot encoder cho các biến categorical có high-cardinality, ta hash chúng để đưa vào các nhóm nhỏ*
- [Design Pattern 2: Embeddings](https://aidino.github.io/contents/design-patterns/pt2-embedding.html) <br>
    *Ánh xạ dữ liệu high-cardinality sang không gian với số chiều thấp hơn*
- [Design Pattern 3: Feature Cross](https://aidino.github.io/contents/design-patterns/pt3-feature-cross.html) <br>
    *Giúp các mô hình tìm hiểu mối quan hệ giữa các yếu tố đầu vào nhanh hơn bằng cách làm cho mỗi kết hợp giá trị đầu vào trở thành một tính năng riêng biệt*
- [Design Pattern 4: Multimodal Input](https://aidino.github.io/contents/design-patterns/pt4-multimodel-input.html) <br>
    *Giải quyết vấn đề biểu diễn các loại dữ liệu hoặc dữ liệu khác nhau có thể được biểu thị theo những cách phức tạp bằng cách ghép nối tất cả các biểu diễn dữ liệu có sẵn.*

#### **2. Problem Representation Design Patterns**
- Design Pattern 5: Reframing
- Design Pattern 6: Multilabel
- Design Pattern 7: Ensembles
- Design Pattern 8: Cascade
- Design Pattern 9: Neutral Class
- Design Pattern 10: Rebalancing

#### **3. Model Training Patterns**
- Design Pattern 11: Useful Overfitting
- Design Pattern 12: Checkpoints
- Design Pattern 13: Transfer Learning
- Design Pattern 14: Distribution Strategy
- Design Pattern 15: Hyperparameter Tuning

#### **4. Design Patterns for Resilient Serving**
- Design Pattern 16: Stateless Serving Function
- Design Pattern 17: Batch Serving
- Design Pattern 18: Continued Model Evaluation
- Design Pattern 19: Two-Phase Predictions
- Design Pattern 20: Keyed Predictions

#### **5. Reproducibility Design Patterns**
- Design Pattern 21: Transform
- Design Pattern 22: Repeatable Splitting
- Design Pattern 23: Bridged Schema
- Design Pattern 24: Windowed Inference
- Design Pattern 25: Workflow Pipeline
- Design Pattern 26: Feature Store
- Design Pattern 27: Model Versioning

#### **6. Responsible AI**
- Design Pattern 28: Heuristic Benchmark
- Design Pattern 29: Explainable Predictions
- Design Pattern 30: Fairness Lens