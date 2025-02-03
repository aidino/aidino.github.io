---
layout: post
title: "Project: Service Desk Ticket Classification with Deep Learning"
date: 2025-01-21 03:00:00 +0700
categories: developing large language models
---


CleverSupport is a company at the forefront of AI innovation, specializing in the development of AI-driven solutions to enhance customer support services. Their latest endeavor is to engineer a text classification system that can automatically categorize customer complaints. 

Your role as a data scientist involves the creation of a sophisticated machine learning model that can accurately assign complaints to specific categories, such as mortgage, credit card, money transfers, debt collection, etc.

---

**CleverSupport là một công ty tiên phong trong lĩnh vực đổi mới AI, chuyên phát triển các giải pháp dựa trên AI để nâng cao dịch vụ hỗ trợ khách hàng. Đề án mới nhất của họ là xây dựng một hệ thống phân loại văn bản có thể tự động phân loại khiếu nại của khách hàng.**

**Vai trò của bạn với tư cách là một nhà khoa học dữ liệu bao gồm việc tạo ra một mô hình học máy tinh vi có thể chính xác gán các khiếu nại vào các danh mục cụ thể, chẳng hạn như thế chấp, thẻ tín dụng, chuyển tiền, thu hồi nợ, v.v.**



```python
!pip install torchmetrics -q
```


```python
from collections import Counter
import nltk, json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from torchmetrics import Accuracy, Precision, Recall
```


```python
nltk.download('punkt')
```

    [nltk_data] Downloading package punkt to
    [nltk_data]     /Users/ngohongthai/nltk_data...
    [nltk_data]   Package punkt is already up-to-date!





    True




```python
# Import data and labels
with open("words.json", 'r') as f1:
    words = json.load(f1)
with open("text.json", 'r') as f2:
    text = json.load(f2)
labels = np.load('labels.npy')
```


```python
set(labels)
```




    {np.int8(0), np.int8(1), np.int8(2), np.int8(3), np.int8(4)}




```python
# Dictionaries to store the word to index mappings and vice versa
word2idx = {o:i for i,o in enumerate(words)}
idx2word = {i:o for i,o in enumerate(words)}

# Looking up the mapping dictionary and assigning the index to the respective words
for i, sentence in enumerate(text):
    text[i] = [word2idx[word] if word in word2idx else 0 for word in sentence]
    
# Defining a function that either shortens sentences or pads sentences with 0 to a fixed length
def pad_input(sentences, seq_len):
    features = np.zeros((len(sentences), seq_len),dtype=int)
    for ii, review in enumerate(sentences):
        if len(review) != 0:
            features[ii, -len(review):] = np.array(review)[:seq_len]
    return features

text = pad_input(text, 50)
```


```python
# Splitting dataset
train_text, test_text, train_label, test_label = train_test_split(text, labels, test_size=0.2, random_state=42)
train_data = TensorDataset(torch.from_numpy(train_text), torch.from_numpy(train_label).long())
test_data = TensorDataset(torch.from_numpy(test_text), torch.from_numpy(test_label).long())
```


```python
batch_size=400
train_loader=DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_loader=DataLoader(test_data, batch_size=batch_size, shuffle=True)
```

### 1. Defining the classifier model



```python
# Define the classifier class
class TicketClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, target_size):
        super(TicketClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.conv = nn.Conv1d(embed_dim, embed_dim, kernel_size=3, stride=1, padding=1)
        self.fc = nn.Linear(embed_dim, target_size)

    def forward(self, text):
        embedded = self.embedding(text).permute(0, 2, 1)
        conved = F.relu(self.conv(embedded))
        conved = conved.mean(dim=2) 
        return self.fc(conved)
```


```python
vocab_size = len(word2idx) + 1
target_size = len(np.unique(labels))
embedding_dim = 64

# Create an instance of the TicketClassifier class
model = TicketClassifier(vocab_size, embedding_dim, target_size)

```

### 2. Train the model


```python
lr = 0.05
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

epochs = 3

# Train the model
model.train()
for i in range(epochs):
    running_loss, num_processed = 0,0
    for inputs, labels in train_loader:
        model.zero_grad()
        output = model(inputs)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        num_processed += len(inputs)
    print(f"Epoch: {i+1}, Loss: {running_loss/num_processed}")


accuracy_metric = Accuracy(task='multiclass', num_classes=5)
precision_metric = Precision(task='multiclass', num_classes=5, average=None)
recall_metric = Recall(task='multiclass', num_classes=5, average=None)

```

    Epoch: 1, Loss: 0.0038048693239688875
    Epoch: 2, Loss: 0.0016321743056178094
    Epoch: 3, Loss: 0.0007453516572713852


### 3. Evaluate the model


```python
# Evaluate model on test set
model.eval()
predicted = []

for i, (inputs, labels) in enumerate(test_loader):
    output = model(inputs)
    cat = torch.argmax(output, dim=-1)
    predicted.extend(cat.tolist())
    accuracy_metric(cat, labels)
    precision_metric(cat, labels)
    recall_metric(cat, labels)

accuracy = accuracy_metric.compute().item()
precision = precision_metric.compute().tolist()
recall = recall_metric.compute().tolist()
print('Accuracy:', accuracy)
print('Precision (per class):', precision)
print('Recall (per class):', recall)
```

    Accuracy: 0.7900000214576721
    Precision (per class): [0.6934673190116882, 0.6995305418968201, 0.8737373948097229, 0.7908163070678711, 0.9020618796348572]
    Recall (per class): [0.71875, 0.7842105031013489, 0.8009259104728699, 0.8072916865348816, 0.8333333134651184]



```python

```
