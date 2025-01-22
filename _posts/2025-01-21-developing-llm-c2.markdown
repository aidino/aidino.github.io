---
layout: post
title: "Intermediate Deep Learning with PyTorch"
date: 2025-01-21 01:00:00 +0700
categories: developing large language models
---

**Deep learning** là một lĩnh vực đang phát triển nhanh chóng của **trí tuệ nhân tạo (AI)** đã cách mạng hóa lĩnh vực **machine learning**, cho phép đạt được những đột phá trong các lĩnh vực như **computer vision**, **natural language processing** và **speech recognition**. Trong khóa học này, bạn sẽ phát triển các **deep learning models** mạnh mẽ với **PyTorch** cho một loạt các ứng dụng, bao gồm **image models** và **sequence models**. Bạn sẽ làm quen với các kiến trúc mạng cốt lõi, chẳng hạn như **convolutional neural networks (CNNs)** và **recurrent neural networks (RNNs)**, bao gồm **Long Short-Term Memory (LSTM) networks** và **Gated Recurrent Units (GRUs)**.

- [Slide - Training Robust Neural Networks]({{site.baseurl}}/files/IntermediateDeepLearningwithPyTorch-C1.pdf)
- [Slide - Images & Convolutional Neural Networks]({{site.baseurl}}/files/IntermediateDeepLearningwithPyTorch-C2.pdf)
- [Slide - Sequences & Recurrent Neural Networks]({{site.baseurl}}/files/IntermediateDeepLearningwithPyTorch-C3.pdf)

---
### Training Robust Neural Networks

#### PyTorch and object-oriented programming 

Lập trình hướng đối tượng (OOP) là một cách tổ chức mã chương trình bằng cách tạo ra các "đối tượng". Hãy tưởng tượng mỗi đối tượng như một chiếc hộp chứa đựng cả dữ liệu (thuộc tính) và các hành động (phương thức) mà nó có thể thực hiện.

Trong Pytorch, OOP được sử dụng rộng rãi để xây dựng các mô hình mạng nơ-ron.

**PyTorch Dataset**

```python
import pandas as pd
from torch.utils.data import Dataset

class WaterDataset(Dataset):
    def __init__(self, csv_path):
        super().__init__()
        # Load data to pandas DataFrame
        df = pd.read_csv(csv_path)
        # Convert data to a NumPy array and assign to self.data
        self.data = df.to_numpy()
        
    # Implement __len__ to return the number of data samples
    def __len__(self):
        return self.data.shape[0]
    
    def __getitem__(self, idx):
        features = self.data[idx, :-1]
        # Assign last data column to label
        label = self.data[idx, -1]
        return features, label
```


**PyTorch DataLoader**

```python
import pandas as pd
from torch.utils.data import DataLoader

# Create an instance of the WaterDataset
dataset_train = WaterDataset("water_train.csv")

# Create a DataLoader based on dataset_train
dataloader_train = DataLoader(
    dataset_train,
    batch_size=2,
    shuffle=True,
)

# Get a batch of features and labels
features, labels = next(iter(dataloader_train))
print(features, labels)
```

**PyTorch Model**

```python
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # Define the three linear layers
        self.fc1 = nn.Linear(9, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)
        
    def forward(self, x):
        # Pass x through linear layers adding activations
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.relu(self.fc2(x))
        x = nn.functional.sigmoid(self.fc3(x))
        return x
```

#### Optimizers, training, and evaluation

**Training Loop**

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 1. Định nghĩa mô hình
class SimpleModel(nn.Module):
  def __init__(self):
    super(SimpleModel, self).__init__()
    self.linear = nn.Linear(10, 1)

  def forward(self, x):
    return self.linear(x)

# 2. Khởi tạo mô hình, hàm loss, và optimizer
model = SimpleModel()
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 3. Tạo dataset và dataloader

# 4. Training loop
epochs = 100
for epoch in range(epochs):
  # a. Forward pass
  y_pred = model(X)
  loss = criterion(y_pred, y)

  # b. Backward pass và tối ưu hóa
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

  # c. In ra loss sau mỗi epoch
  if (epoch+1) % 10 == 0:
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
```

**Giải thích:**

1. **Định nghĩa mô hình:**
   - Chúng ta định nghĩa một mô hình đơn giản `SimpleModel` với một lớp linear.
   - Hàm `forward` thực hiện phép tính forward pass, nhận input `x` và trả về output.

2. **Khởi tạo mô hình, hàm loss, và optimizer:**
   - `model = SimpleModel()` khởi tạo một instance của mô hình.
   - `criterion = nn.MSELoss()` chọn hàm loss là Mean Squared Error.
   - `optimizer = optim.SGD(model.parameters(), lr=0.01)` sử dụng Stochastic Gradient Descent để tối ưu trọng số của mô hình với learning rate 0.01.

3. **Tạo dataset và dataloader**
  
4. **Training loop:**
   - Vòng lặp `for epoch in range(epochs):` lặp qua `epochs` lần (ở đây là 100).
     - **a. Forward pass:**
       - `y_pred = model(X)` tính output dự đoán của mô hình.
       - `loss = criterion(y_pred, y)` tính loss giữa output dự đoán và output thực tế.
     - **b. Backward pass và tối ưu hóa:**
       - `optimizer.zero_grad()` reset gradients của các tham số về 0.
       - `loss.backward()` tính gradients của loss theo các tham số.
       - `optimizer.step()` cập nhật các tham số dựa trên gradients đã tính.
     - **c. In ra loss sau mỗi epoch:**
       - Câu lệnh `if (epoch+1) % 10 == 0:` in ra loss sau mỗi 10 epoch.

**Tóm lại, training loop thực hiện các bước sau lặp đi lặp lại:**

1. **Forward pass:** Tính output dự đoán và loss.
2. **Backward pass:** Tính gradients của loss.
3. **Tối ưu hóa:** Cập nhật trọng số của mô hình.


**1. Stochastic Gradient Descent (SGD)**

* **Ý tưởng:**  SGD cập nhật tham số của mô hình dựa trên gradient của loss function tính trên một batch dữ liệu nhỏ (mini-batch) được lấy ngẫu nhiên từ tập dữ liệu huấn luyện. 
* **Ưu điểm:** Đơn giản, dễ cài đặt, hiệu quả với tập dữ liệu lớn.
* **Nhược điểm:** Có thể bị "kẹt" ở các điểm cực tiểu cục bộ (local minima) hoặc dao động quanh điểm tối ưu do gradient thay đổi liên tục.
* **Ví dụ:**

```python
import torch.optim as optim

# ... (Khởi tạo mô hình) ...

optimizer = optim.SGD(model.parameters(), lr=0.01)
```

**2. Adaptive Gradient (Adagrad)**

* **Ý tưởng:** Adagrad điều chỉnh learning rate cho từng tham số dựa trên lịch sử cập nhật của tham số đó. Các tham số được cập nhật thường xuyên sẽ có learning rate giảm dần, giúp hội tụ nhanh hơn.
* **Ưu điểm:** Hiệu quả với dữ liệu thưa (sparse data), tự động điều chỉnh learning rate.
* **Nhược điểm:** Learning rate giảm quá nhanh, có thể khiến việc học dừng lại sớm.
* **Ví dụ:**

```python
import torch.optim as optim

# ... (Khởi tạo mô hình) ...

optimizer = optim.Adagrad(model.parameters(), lr=0.01)
```

**3. Root Mean Square Propagation (RMSprop)**

* **Ý tưởng:** RMSprop giải quyết vấn đề learning rate giảm quá nhanh của Adagrad bằng cách sử dụng trung bình bình phương động (moving average) của gradient. Điều này giúp duy trì learning rate ở mức hợp lý và tránh việc học dừng lại sớm.
* **Ưu điểm:** Khắc phục nhược điểm của Adagrad, hiệu quả trong nhiều trường hợp.
* **Nhược điểm:** Vẫn cần phải điều chỉnh learning rate thủ công.
* **Ví dụ:**

```python
import torch.optim as optim

# ... (Khởi tạo mô hình) ...

optimizer = optim.RMSprop(model.parameters(), lr=0.01)
```

**4. Adaptive Moment Estimation (Adam)**

* **Ý tưởng:** Adam kết hợp ý tưởng của Momentum (tích lũy gradient trước đó) và RMSprop (trung bình bình phương động của gradient).  Nó duy trì learning rate riêng cho từng tham số và điều chỉnh learning rate dựa trên cả gradient hiện tại và gradient trước đó.
* **Ưu điểm:** Hiệu quả cao, thường được sử dụng mặc định, ít cần điều chỉnh hyperparameter.
* **Nhược điểm:**  Phức tạp hơn các thuật toán khác.
* **Ví dụ:**

```python
import torch.optim as optim

# ... (Khởi tạo mô hình) ...

optimizer = optim.Adam(model.parameters(), lr=0.001)
```

**Tóm lại:**

- **SGD:** Đơn giản, hiệu quả, nhưng có thể dao động và bị kẹt ở local minima.
- **Adagrad:** Tự động điều chỉnh learning rate, hiệu quả với dữ liệu thưa, nhưng learning rate có thể giảm quá nhanh.
- **RMSprop:** Khắc phục nhược điểm của Adagrad, duy trì learning rate hợp lý.
- **Adam:** Kết hợp ưu điểm của Momentum và RMSprop, hiệu quả cao, thường được sử dụng mặc định.

**Model evaluation** 

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchmetrics import Accuracy

# 1. Định nghĩa mô hình
class SimpleModel(nn.Module):
  ...

# 2. Khởi tạo mô hình, hàm loss, optimizer, và accuracy metric
model = SimpleModel()
criterion = nn.BCELoss()  # Sử dụng Binary Cross Entropy Loss cho bài toán binary
optimizer = optim.SGD(model.parameters(), lr=0.01)
acc = Accuracy(task="binary")

# 3. Khởi tạo Dataset + DataLoader

# 4. Training loop
epochs = 100
for epoch in range(epochs):
  # a. Forward pass
  y_pred = model(X_train)
  loss = criterion(y_pred, y_train)

  # b. Backward pass và tối ưu hóa
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

  # c. In ra loss sau mỗi epoch
  if (epoch+1) % 10 == 0:
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

# 5. Model evaluation
model.eval()
with torch.no_grad():
  y_pred = model(X_test)
  loss = criterion(y_pred, y_test)
  print(f'Test Loss: {loss.item():.4f}')

  # Tính accuracy sử dụng torchmetrics
  accuracy = acc(y_pred, y_test.int())
  print(f'Accuracy: {accuracy:.4f}')
```

#### Vanishing and exploding gradients

Trong quá trình huấn luyện mạng nơ-ron, đặc biệt là mạng nơ-ron sâu, chúng ta sử dụng thuật toán lan truyền ngược (backpropagation) để tính toán gradient của hàm loss theo các tham số của mô hình. Gradient này cho biết hướng và độ lớn cần điều chỉnh các tham số để giảm thiểu loss.

* **Vanishing Gradients:**  Xảy ra khi gradient trở nên rất nhỏ khi lan truyền ngược qua các lớp. Điều này khiến các lớp đầu tiên của mạng học rất chậm hoặc gần như không học được gì, làm giảm hiệu quả huấn luyện.
* **Exploding Gradients:**  Ngược lại với vanishing gradients, exploding gradients xảy ra khi gradient trở nên rất lớn khi lan truyền ngược.  Điều này dẫn đến việc cập nhật tham số quá lớn, gây ra sự mất ổn định trong quá trình huấn luyện.

**2. Ví dụ minh họa:**

Hãy tưởng tượng bạn đang leo núi và muốn tìm đường đến đỉnh núi (tối ưu mô hình). Gradient giống như la bàn chỉ hướng đi.

* **Vanishing Gradients:**  La bàn của bạn bị yếu dần khi đi xuống núi. Đến chân núi, kim la bàn gần như không xoay, bạn không biết đi hướng nào để lên đỉnh.
* **Exploding Gradients:** La bàn của bạn bị nhiễu loạn mạnh, kim la bàn xoay liên tục, khiến bạn đi lung tung và không thể tìm được đường lên đỉnh.

**3. Nguyên nhân:**

* **Hàm kích hoạt:**  Các hàm kích hoạt như sigmoid và tanh có đạo hàm nhỏ hơn 1. Khi nhân nhiều đạo hàm nhỏ hơn 1 với nhau (trong quá trình lan truyền ngược), gradient sẽ giảm dần theo cấp số nhân.
* **Độ sâu của mạng:**  Mạng càng sâu, gradient càng phải đi qua nhiều lớp, tăng khả năng xảy ra vanishing gradients.
* **Khởi tạo trọng số:**  Khởi tạo trọng số không phù hợp cũng có thể gây ra exploding gradients.

**4. Solution to unstable gradients:**

* **Sử dụng hàm kích hoạt khác:**  ReLU và các biến thể của nó (Leaky ReLU, Parametric ReLU) có đạo hàm lớn hơn hoặc bằng 1, giúp giảm thiểu vanishing gradients.
* **Khởi tạo trọng số phù hợp:**  Các phương pháp khởi tạo trọng số như Xavier/Glorot initialization và He initialization giúp khởi tạo trọng số phù hợp, tránh exploding gradients.
* **Batch Normalization:**  Batch Normalization chuẩn hóa đầu vào của mỗi lớp, giúp ổn định quá trình huấn luyện và giảm thiểu vanishing gradients.
* **Gradient Clipping:**  Giới hạn độ lớn của gradient trong một khoảng nhất định, ngăn chặn exploding gradients.
* **Residual Connections (ResNet):**  Cho phép gradient "bỏ qua" một số lớp, giúp gradient lan truyền dễ dàng hơn trong mạng sâu.
* **LSTM, GRU (cho mạng nơ-ron tuần hoàn):**  Các kiến trúc này được thiết kế để giải quyết vanishing gradients trong mạng nơ-ron tuần hoàn.


**Ví dụ trong PyTorch:**

```python
import torch.nn as nn

# Sử dụng ReLU
model = nn.Sequential(
    nn.Linear(10, 20),
    nn.ReLU(),
    nn.Linear(20, 1)
)

# Sử dụng Batch Normalization
model = nn.Sequential(
    nn.Linear(10, 20),
    nn.BatchNorm1d(20),
    nn.ReLU(),
    nn.Linear(20, 1)
)

# Gradient Clipping
optimizer = optim.SGD(model.parameters(), lr=0.01)
for epoch in range(epochs):
  # ...
  optimizer.zero_grad()
  loss.backward()
  torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)  # Giới hạn gradient
  optimizer.step()
```

**Các phương pháp khởi tạo trọng số phổ biến:**

**1. Zero initialization:**

* Khởi tạo tất cả trọng số bằng 0.
* **Vấn đề:**  Tất cả neuron sẽ giống nhau, không học được gì.
* **Ví dụ:** `torch.nn.init.zeros_(model.linear1.weight)`

**2. Random initialization:**

* Khởi tạo trọng số ngẫu nhiên từ một phân phối xác suất, thường là phân phối đều hoặc phân phối chuẩn.
* **Vấn đề:** Nếu giá trị khởi tạo quá lớn, có thể dẫn đến exploding gradients.
* **Ví dụ:**
    * `torch.nn.init.uniform_(model.linear1.weight, a=-0.1, b=0.1)` (phân phối đều)
    * `torch.nn.init.normal_(model.linear1.weight, mean=0, std=0.1)` (phân phối chuẩn)


**3. Xavier/Glorot initialization:**

* Khởi tạo trọng số ngẫu nhiên từ một phân phối đều hoặc phân phối chuẩn với phương sai được tính toán dựa trên số lượng input và output của lớp.
* **Ý tưởng:** Giữ cho phương sai của activations và gradients ổn định khi lan truyền qua các lớp.
* **Ví dụ:**
    * `torch.nn.init.xavier_uniform_(model.linear1.weight)` (phân phối đều)
    * `torch.nn.init.xavier_normal_(model.linear1.weight)` (phân phối chuẩn)


**4. He initialization:**

* Tương tự Xavier initialization, nhưng được thiết kế cho các hàm kích hoạt ReLU và các biến thể của nó.
* **Ý tưởng:**  Tính đến ảnh hưởng của ReLU đến phương sai của activations.
* **Ví dụ:**
    * `torch.nn.init.kaiming_uniform_(model.linear1.weight, nonlinearity='relu')` (phân phối đều)
    * `torch.nn.init.kaiming_normal_(model.linear1.weight, nonlinearity='relu')` (phân phối chuẩn)


**Lựa chọn phương pháp khởi tạo:**

* **Xavier/Glorot:** Phù hợp với các hàm kích hoạt sigmoid và tanh.
* **He initialization:**  Phù hợp với ReLU và các biến thể.
* **Thử nghiệm:**  Bạn có thể thử nghiệm với các phương pháp khởi tạo khác nhau để tìm ra lựa chọn tốt nhất cho mô hình của mình.

**Example**

- Initialization and activation

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)
        
        # Apply He initialization
        init.kaiming_uniform_(self.fc1.weight)
        init.kaiming_uniform_(self.fc2.weight)
        init.kaiming_uniform_(
            self.fc3.weight,
            nonlinearity="sigmoid"
        )

    def forward(self, x):
        # Update ReLU activation to ELU
        x = nn.functional.elu(self.fc1(x))
        x = nn.functional.elu(self.fc2(x))
        x = nn.functional.sigmoid(self.fc3(x))
        return x
```

- Batch Normalization

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9, 16)
        # Add two batch normalization layers
        self.bn1 = nn.BatchNorm1d(16)
        self.fc2 = nn.Linear(16, 8)
        self.bn2 = nn.BatchNorm1d(8)
        self.fc3 = nn.Linear(8, 1)
        
        init.kaiming_uniform_(self.fc1.weight)
        init.kaiming_uniform_(self.fc2.weight)
        init.kaiming_uniform_(self.fc3.weight, nonlinearity="sigmoid")
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = nn.functional.elu(x)

        # Pass x through the second set of layers
        x = self.fc2(x)
        x = self.bn2(x)
        x = nn.functional.elu(x)

        x = nn.functional.sigmoid(self.fc3(x))
        return x
```

---
### Images & Convolutional Neural Networks

#### Handling images with PyTorch

- Image dataset

```python
from torchvision.datasets import ImageFolder
from torchvision import transforms

# Compose transformations
train_transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((128, 128)),
])

# Create Dataset using ImageFolder
dataset_train = ImageFolder(
    "clouds_train",
    transform=train_transforms,
)
```

- Data augmentation in PyTorch

```python
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision import transforms
import matplotlib.pyplot as plt

train_transforms = transforms.Compose([
    # Add horizontal flip and rotation
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(45),
    transforms.ToTensor(),
    transforms.Resize((128, 128)),
])

dataset_train = ImageFolder(
  "clouds_train",
  transform=train_transforms,
)

dataloader_train = DataLoader(
  dataset_train, shuffle=True, batch_size=1
)

image, label = next(iter(dataloader_train))
# Reshape the image tensor
image = image.squeeze().permute(1, 2, 0) 
# Display the image
plt.imshow(image)
plt.show()
```

Dòng lệnh `image = image.squeeze().permute(1, 2, 0)` thực hiện hai thao tác trên tensor `image`:

**1. `image.squeeze()`:**

- Loại bỏ các chiều (dimensions) có kích thước bằng 1 trong tensor.
- Ví dụ: Nếu `image` có shape là `(1, 3, 224, 224)`, sau khi `squeeze()` shape sẽ trở thành `(3, 224, 224)`.
- Trong trường hợp xử lý ảnh, thao tác này thường được dùng để loại bỏ chiều batch size bằng 1 khi chỉ có một ảnh duy nhất.

**2. `permute(1, 2, 0)`:**

- Thay đổi thứ tự các chiều của tensor.
- `permute(1, 2, 0)` hoán đổi vị trí các chiều: chiều 1 (chiều cao - height) thành chiều 0, chiều 2 (chiều rộng - width) thành chiều 1, và chiều 0 (kênh màu - channels) thành chiều 2.
- Ví dụ: Nếu `image` có shape là `(3, 224, 224)`, sau khi `permute(1, 2, 0)` shape sẽ trở thành `(224, 224, 3)`.
- Thao tác này thường được sử dụng để chuyển đổi thứ tự channels từ dạng PyTorch `(channels, height, width)` sang dạng `(height, width, channels)` mà các thư viện hiển thị ảnh như `matplotlib` yêu cầu.

#### Convolutional Neural Networks

- Building convolutional networks

```python
class Net(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # Define feature extractor
        self.feature_extractor = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ELU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ELU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Flatten(),
        )
        # Define classifier
        self.classifier = nn.Linear(64*16*16, num_classes)
    
    def forward(self, x):  
        # Pass input through feature extractor and classifier
        x = self.feature_extractor(x)
        x = self.classifier(x)
        return x
```

#### Training image classifiers

- Dataset with augmentations

```python
# Define transforms
train_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(45),
    transforms.RandomAutocontrast(),
    transforms.ToTensor(),
    transforms.Resize((64,64)),
])

dataset_train = ImageFolder(
  "clouds_train",
  transform=train_transforms,
)
dataloader_train = DataLoader(
  dataset_train, shuffle=True, batch_size=16
)
```

- Image classifier training loop

```python
# Define the model
net = Net(num_classes=7)
# Define the loss function
criterion = nn.CrossEntropyLoss()
# Define the optimizer
optimizer = optim.Adam(net.parameters(), lr=0.001)

for epoch in range(3):
    running_loss = 0.0
    # Iterate over training batches
    for images, labels in dataloader_train:
        optimizer.zero_grad()
        outputs = net(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    epoch_loss = running_loss / len(dataloader_train)
    print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}")
```

#### Evaluating image classifiers

![]({{site.baseurl}}/images/precision-recall.png)

F1-score là một thước đo đánh giá hiệu suất của mô hình phân loại, đặc biệt hữu ích khi dữ liệu không cân bằng (imbalanced data). Nó kết hợp precision (độ chính xác) và recall (độ nhạy) để đưa ra một đánh giá tổng quan. 

Khi làm việc với bài toán phân loại đa lớp (multi-class classification), có nhiều cách để tính toán F1-score, bao gồm: micro average, macro average và weighted average. Dưới đây là giải thích chi tiết về từng loại:

**1. Micro average:**

- **Cách tính:** Tính toán tổng số True Positives (TP), False Positives (FP) và False Negatives (FN) trên tất cả các lớp, sau đó tính precision, recall và F1-score dựa trên tổng số này.
- **Đặc điểm:** 
    - Coi tất cả các mẫu dữ liệu như nhau, không phân biệt lớp.
    - Phù hợp khi bạn quan tâm đến hiệu suất tổng thể của mô hình trên toàn bộ dữ liệu.
    - Bị ảnh hưởng nhiều bởi các lớp có số lượng mẫu lớn.
- **Ví dụ:** Giả sử bạn có 3 lớp (A, B, C) với số lượng mẫu lần lượt là 100, 50 và 10. Micro average sẽ coi 160 mẫu này như nhau và tính toán F1-score dựa trên tổng số TP, FP, FN của cả 3 lớp.

**2. Macro average:**

- **Cách tính:** Tính toán precision, recall và F1-score cho từng lớp riêng biệt, sau đó lấy trung bình cộng của các giá trị này trên tất cả các lớp.
- **Đặc điểm:** 
    - Coi tất cả các lớp như nhau, không phân biệt số lượng mẫu.
    - Phù hợp khi bạn quan tâm đến hiệu suất trung bình của mô hình trên từng lớp, đặc biệt khi các lớp có độ quan trọng như nhau.
    - Không bị ảnh hưởng bởi sự mất cân bằng về số lượng mẫu giữa các lớp.
- **Ví dụ:**  Tiếp tục ví dụ trên, macro average sẽ tính F1-score cho từng lớp A, B, C, sau đó lấy trung bình cộng của 3 giá trị F1-score này.

**3. Weighted average:**

- **Cách tính:** Tương tự macro average, nhưng mỗi lớp được gán một trọng số dựa trên số lượng mẫu của lớp đó. Sau đó, tính trung bình có trọng số của các giá trị F1-score trên tất cả các lớp.
- **Đặc điểm:** 
    - Coi trọng số của mỗi lớp tỉ lệ với số lượng mẫu của lớp đó.
    - Phù hợp khi bạn muốn cân bằng giữa hiệu suất tổng thể và hiệu suất trên từng lớp, đồng thời  xem xét đến sự mất cân bằng về số lượng mẫu.
    - Các lớp có số lượng mẫu lớn sẽ ảnh hưởng nhiều hơn đến kết quả.
- **Ví dụ:**  Weighted average sẽ tính F1-score cho từng lớp A, B, C, sau đó tính trung bình có trọng số, với trọng số của mỗi lớp tỉ lệ với số lượng mẫu (100, 50, 10).

> Note:
> - Micro: Imbalanced datasets
> - Macro: Care about performance on small classes
> - Weighted: Consider errors in larger classes as more important

**Example**

- Multi-class model evaluation

```python
from torchmetrics import Precision, Recall

# Define metrics
metric_precision = Precision(task="multiclass", num_classes=7, average="micro")
metric_recall = Recall(task="multiclass", num_classes=7, average="micro")

net.eval()
with torch.no_grad():
    for images, labels in dataloader_test:
        outputs = net(images)
        _, preds = torch.max(outputs, 1)
        metric_precision(preds, labels)
        metric_recall(preds, labels)

precision = metric_precision.compute()
recall = metric_recall.compute()
print(f"Precision: {precision}")
print(f"Recall: {recall}")
```

- Analyzing metrics per class

```python
# Define precision metric
metric_precision = Precision(
    task="multiclass", num_classes=7, average=None
)

net.eval()
with torch.no_grad():
    for images, labels in dataloader_test:
        outputs = net(images)
        _, preds = torch.max(outputs, 1)
        metric_precision(preds, labels)
precision = metric_precision.compute()

# Get precision per class
precision_per_class = {
    k: precision[v].item()
    for k, v 
    in dataset_test.class_to_idx.items()
}
print(precision_per_class)
```

---
### Sequences & Recurrent Neural Networks

---
### Multi-Input & Multi-Output Architectures
