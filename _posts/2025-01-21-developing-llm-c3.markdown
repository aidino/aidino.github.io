---
layout: post
title: "Deep Learning for Text with PyTorch"
date: 2025-01-21 02:00:00 +0700
categories: developing large language models
---

Discover the exciting world of Deep Learning for Text with PyTorch and unlock new possibilities in natural language processing and text generation.

### Table of contents
- [Table of contents](#table-of-contents)
- [1. Introduction to Deep Learning for Text with PyTorch](#1-introduction-to-deep-learning-for-text-with-pytorch)
  - [1.1. Introduction to preprocessing for text](#11-introduction-to-preprocessing-for-text)
  - [1.2. Encoding text data](#12-encoding-text-data)
  - [1.3. Introduction to building a text processing pipeline](#13-introduction-to-building-a-text-processing-pipeline)
- [2. Text Classification with PyTorch](#2-text-classification-with-pytorch)
  - [2.1. Overview of Text Classification](#21-overview-of-text-classification)
  - [2.2. Convolutional neural networks for text classification](#22-convolutional-neural-networks-for-text-classification)
  - [2.3. Recurrent neural networks for text classification](#23-recurrent-neural-networks-for-text-classification)
  - [2.4. Evaluation metrics for text classification](#24-evaluation-metrics-for-text-classification)
- [3. Text Generation with PyTorch](#3-text-generation-with-pytorch)
  - [3.1. Introduction to text generation](#31-introduction-to-text-generation)
  - [3.2. Generative adversarial networks for text generation](#32-generative-adversarial-networks-for-text-generation)
  - [3.3. Pre-trained models for text generation](#33-pre-trained-models-for-text-generation)
  - [3.4. Evaluation metrics for text generation](#34-evaluation-metrics-for-text-generation)
- [4. Advanced Topics in Deep Learning for Text with PyTorch](#4-advanced-topics-in-deep-learning-for-text-with-pytorch)
  - [4.1. Transfer learning for text classification](#41-transfer-learning-for-text-classification)
  - [4.2. Transformers for text processing](#42-transformers-for-text-processing)
  - [4.3. Attention mechanisms for text generation](#43-attention-mechanisms-for-text-generation)
  - [4.4. Adversarial attacks on text classification models](#44-adversarial-attacks-on-text-classification-models)
* 3. [Text Generation with PyTorch](#TextGenerationwithPyTorch)
    * 3.1. [Introduction to text generation](#Introductiontotextgeneration)
    * 3.2. [Generative adversarial networks for text generation](#Generativeadversarialnetworksfortextgeneration)
    * 3.3. [Pre-trained models for text generation](#Pre-trainedmodelsfortextgeneration)
    * 3.4. [Evaluation metrics for text generation](#Evaluationmetricsfortextgeneration)
* 4. [Advanced Topics in Deep Learning for Text with PyTorch](#AdvancedTopicsinDeepLearningforTextwithPyTorch)
    * 4.1. [Transfer learning for text classification](#Transferlearningfortextclassification)
    * 4.2. [Transformers for text processing](#Transformersfortextprocessing)
    * 4.3. [Attention mechanisms for text generation](#Attentionmechanismsfortextgeneration)
    * 4.4. [Adversarial attacks on text classification models](#Adversarialattacksontextclassificationmodels)

---
###  1. <a name='IntroductiontoDeepLearningforTextwithPyTorch'></a>Introduction to Deep Learning for Text with PyTorch

[Slide]({{site.baseurl}}/files/DeepLearningforTextwithPyTorch-C1.pdf)

####  1.1. <a name='Introductiontopreprocessingfortext'></a>Introduction to preprocessing for text

Tiền xử lý dữ liệu là bước quan trọng trước khi huấn luyện mô hình học máy, đặc biệt là trong xử lý ngôn ngữ tự nhiên (NLP). Mục đích của tiền xử lý là làm sạch và chuẩn hóa dữ liệu, giúp mô hình học hiệu quả hơn. Dưới đây là giải thích và ví dụ minh họa cho các kỹ thuật tiền xử lý phổ biến:

**1. Tokenization (Phân tách từ)**

**Giải thích:** Tokenization là quá trình chia văn bản thành các đơn vị nhỏ hơn, gọi là token. Token có thể là từ, cụm từ hoặc ký tự, tùy thuộc vào mục đích và phương pháp.

**Ví dụ:**

```python
import nltk

nltk.download('punkt')

text = "Đây là một ví dụ về tokenization."
tokens = nltk.word_tokenize(text)
print(tokens)
```

**Output:**

```
['Đây', 'là', 'một', 'ví', 'dụ', 'về', 'tokenization', '.']
```

Trong ví dụ này, ta sử dụng thư viện `nltk` (Natural Language Toolkit) để phân tách câu văn bản thành các từ riêng lẻ.

**2. Stop word removal (Loại bỏ từ dừng)**

**Giải thích:** Từ dừng là những từ phổ biến như "và", "hoặc", "là",... thường không mang nhiều ý nghĩa trong phân tích văn bản. Loại bỏ từ dừng giúp giảm kích thước dữ liệu và tập trung vào những từ quan trọng hơn.

**Ví dụ:**

```python
import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords

stop_words = set(stopwords.words('vietnamese'))
text = "Đây là một ví dụ về loại bỏ từ dừng."
tokens = nltk.word_tokenize(text)
filtered_tokens = [w for w in tokens if not w.lower() in stop_words]
print(filtered_tokens)
```

**Output:**

```
['ví', 'dụ', 'loại', 'bỏ', 'từ', 'dừng', '.']
```

Trong ví dụ này, ta sử dụng danh sách từ dừng tiếng Việt có sẵn trong `nltk.corpus` để loại bỏ các từ dừng khỏi danh sách token.

**3. Stemming (Rút gọn từ)**

**Giải thích:** Stemming là quá trình rút gọn từ về dạng gốc của nó. Ví dụ, "chạy", "chạy bộ", "chạy nhảy" đều được rút gọn về "chạy". Stemming giúp giảm số lượng từ vựng và nhóm các từ có cùng ý nghĩa.

**Ví dụ:** (Thư viện `vncorenlp` cho tiếng Việt)

```python
from vncorenlp import VnCoreNLP

rdrsegmenter = VnCoreNLP("./VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m') 

text = "Những người đang chạy bộ ngoài công viên"
segmented_text = rdrsegmenter.tokenize(text)
print(segmented_text)
```

**Output:**

```
[['Những', 'người', 'đang', 'chạy_bộ', 'ngoài', 'công_viên']]
```

Lưu ý: Stemming cho tiếng Việt phức tạp hơn tiếng Anh. Thư viện `vncorenlp` có thể giúp tách từ ghép ("chạy_bộ"), tuy nhiên việc rút gọn về từ gốc "chạy" cần các phương pháp phức tạp hơn.

**4. Rare word removal (Loại bỏ từ hiếm)**

**Giải thích:** Từ hiếm là những từ xuất hiện rất ít trong dữ liệu. Loại bỏ từ hiếm giúp giảm kích thước từ vựng, loại bỏ nhiễu và tập trung vào những từ phổ biến, mang nhiều thông tin.

**Ví dụ:**

```python
from collections import Counter

text = "Đây là một ví dụ về loại bỏ từ hiếm. Từ hiếm xuất hiện rất ít."
tokens = nltk.word_tokenize(text)
word_counts = Counter(tokens)
filtered_tokens = [w for w in tokens if word_counts[w] > 1]
print(filtered_tokens)
```

**Output:**

```
['là', 'một', 'ví', 'dụ', 'về', 'từ', 'hiếm', '.', 'từ', 'hiếm', '.']
```

Trong ví dụ này, ta sử dụng `Counter` để đếm số lần xuất hiện của mỗi từ, sau đó loại bỏ những từ chỉ xuất hiện một lần.

**Example**

- **Word frequency analysis**

```python
# Import the necessary functions
from torchtext.data.utils import get_tokenizer
from nltk.probability import FreqDist

text = "In the city of Dataville, a data analyst named Alex explores hidden insights within vast data. With determination, Alex uncovers patterns, cleanses the data, and unlocks innovation. Join this adventure to unleash the power of data-driven decisions."

# Initialize the tokenizer and tokenize the text
tokenizer = get_tokenizer("basic_english")
tokens = tokenizer(text)

threshold = 1
# Remove rare words and print common tokens
freq_dist = FreqDist(tokens)
common_tokens = [token for token in tokens if freq_dist[token] > threshold]
print(common_tokens)
```

- **Preprocessing text**

```python
from torchtext.data.utils import get_tokenizer
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')

# Initialize and tokenize the text
tokenizer = get_tokenizer("basic_english")
tokens = tokenizer(text)

# Remove any stopwords
stop_words = set(stopwords.words("english"))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

# Perform stemming on the filtered tokens
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
print(stemmed_tokens)
```
####  1.2. <a name='Encodingtextdata'></a>Encoding text data

Mã hóa văn bản là quá trình chuyển đổi văn bản thành dạng số để máy tính có thể hiểu và xử lý. Dưới đây là giải thích về các kỹ thuật mã hóa phổ biến:

**1. One-hot encoding**

**Thuật toán:** Mỗi từ trong từ vựng được gán một vector riêng biệt, với tất cả các phần tử bằng 0 ngoại trừ một phần tử bằng 1 tại vị trí tương ứng với từ đó.

**Ví dụ:**

Từ vựng: ["tôi", "yêu", "Việt", "Nam"]

* "tôi": [1, 0, 0, 0]
* "yêu": [0, 1, 0, 0]
* "Việt": [0, 0, 1, 0]
* "Nam": [0, 0, 0, 1]

**Ưu điểm:**

* Đơn giản, dễ hiểu.
* Phù hợp với các mô hình đơn giản.

**Nhược điểm:**

* Vector có kích thước lớn, tốn bộ nhớ.
* Không thể hiện mối quan hệ ngữ nghĩa giữa các từ.
* Không xử lý được từ mới (out-of-vocabulary).

**2. Bag-of-Words (BoW)**

**Thuật toán:** Đếm số lần xuất hiện của mỗi từ trong văn bản, tạo thành một vector biểu diễn.

**Ví dụ:**

Văn bản: "Tôi yêu Việt Nam. Việt Nam đẹp quá."

Từ vựng: ["tôi", "yêu", "Việt", "Nam", "đẹp", "quá"]

Vector BoW: [1, 1, 2, 2, 1, 1]

**Ưu điểm:**

* Đơn giản, dễ thực hiện.
* Hiệu quả với một số bài toán phân loại văn bản.

**Nhược điểm:**

* Mất thông tin về thứ tự từ.
* Không thể hiện mối quan hệ ngữ nghĩa giữa các từ.
* Vector có thể rất thưa (sparse) với văn bản dài.

**3. TF-IDF (Term Frequency-Inverse Document Frequency)**

**Thuật toán:** Gán trọng số cho mỗi từ dựa trên tần suất xuất hiện trong văn bản (TF) và độ hiếm của từ trong toàn bộ tập dữ liệu (IDF).

* **TF:** Tần suất xuất hiện của từ trong văn bản.
* **IDF:** Logarit của tỷ lệ số lượng văn bản trong tập dữ liệu chia cho số lượng văn bản chứa từ đó.

**Ưu điểm:**

* Cân nhắc cả tần suất xuất hiện và độ quan trọng của từ.
* Hiệu quả trong việc tìm kiếm thông tin và phân loại văn bản.

**Nhược điểm:**

* Vẫn không thể hiện mối quan hệ ngữ nghĩa giữa các từ.
* Vector có thể rất thưa.

**4. Embedding (Nhúng từ)**

**Thuật toán:** Biểu diễn mỗi từ bằng một vector dày đặc (dense vector) trong không gian vector liên tục. Các từ có ngữ nghĩa tương đồng sẽ có vector gần nhau trong không gian này.

**Ví dụ:**

Word2Vec, GloVe, FastText là các mô hình nhúng từ phổ biến.

**Ưu điểm:**

* Biểu diễn được mối quan hệ ngữ nghĩa giữa các từ.
* Vector có kích thước nhỏ gọn hơn one-hot encoding.
* Xử lý được từ mới thông qua các từ tương đồng.

**Nhược điểm:**

* Huấn luyện mô hình nhúng từ cần nhiều dữ liệu.
* Chất lượng vector phụ thuộc vào chất lượng dữ liệu huấn luyện.


**Example**

- **One-hot encoded book titles**

```python
genres = ['Fiction','Non-fiction','Biography', 'Children','Mystery']

# Define the size of the vocabulary
vocab_size = len(genres)

# Create one-hot vectors
one_hot_vectors = torch.eye(vocab_size)

# Create a dictionary mapping genres to their one-hot vectors
one_hot_dict = {genre: one_hot_vectors[i] for i, genre in enumerate(genres)}

for genre, vector in one_hot_dict.items():
    print(f'{genre}: {vector.numpy()}')
```

- **Bag-of-words for book titles**

```python
# Import from sklearn
from sklearn.feature_extraction.text import CountVectorizer

titles = ['The Great Gatsby','To Kill a Mockingbird','1984','The Catcher in the Rye','The Hobbit', 'Great Expectations']

# Initialize Bag-of-words with the list of book titles
vectorizer = CountVectorizer()
bow_encoded_titles = vectorizer.fit_transform(titles)

# Extract and print the first five features
print(vectorizer.get_feature_names_out()[:5])
print(bow_encoded_titles.toarray()[0, :5])
```

- **Applying TF-IDF to book descriptions**

```python
# Importing TF-IDF from sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TF-IDF encoding vectorizer
vectorizer = TfidfVectorizer()
tfidf_encoded_descriptions = vectorizer.fit_transform(descriptions)

# Extract and print the first five features
print(vectorizer.get_feature_names_out()[:5])
print(tfidf_encoded_descriptions.toarray()[0, :5])
```

####  1.3. <a name='Introductiontobuildingatextprocessingpipeline'></a>Introduction to building a text processing pipeline

- **Shakespearean language preprocessing pipeline**

```python
# Create a list of stopwords
stop_words = set(stopwords.words("english"))

# Initialize the tokenizer and stemmer
tokenizer = get_tokenizer("basic_english")
stemmer = PorterStemmer() 

# Complete the function to preprocess sentences
def preprocess_sentences(sentences):
    processed_sentences = []
    for sentence in sentences:
        sentence = sentence.lower()
		# Tokenize the sentence
        tokens = tokenizer(sentence)
		# Remove stop words
        tokens = [token for token in tokens if token not in stop_words]
		# Stem the tokens
        tokens = [stemmer.stem(token) for token in tokens]
        processed_sentences.append(' '.join(tokens))
    return processed_sentences

processed_shakespeare = preprocess_sentences(shakespeare)
print(processed_shakespeare[:5]) 
```

- **Shakespearean language encoder**

```python
# Define your Dataset class
class ShakespeareDataset(Dataset):
    def __init__(self, data):
        self.data = data
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        return self.data[idx]

# Complete the encoding function
def encode_sentences(sentences):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(sentences)
    return X.toarray(), vectorizer
    
# Complete the text processing pipeline
def text_processing_pipeline(sentences):
    processed_sentences = preprocess_sentences(sentences)
    encoded_sentences, vectorizer = encode_sentences(processed_sentences)
    dataset = ShakespeareDataset(encoded_sentences)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    return dataloader, vectorizer

dataloader, vectorizer = text_processing_pipeline(processed_shakespeare)

# Print the vectorizer's feature names and the first 10 components of the first item
print(vectorizer.get_feature_names_out()[:10]) 
print(next(iter(dataloader))[0, :10])
```

---
###  2. <a name='TextClassificationwithPyTorch'></a>Text Classification with PyTorch

[Slide]({{site.baseurl}}/files/DeepLearningforTextwithPyTorch-C2.pdf)

####  2.1. <a name='OverviewofTextClassification'></a>Overview of Text Classification

- Embedding in PyTorch

```python
# Map a unique index to each word
words = ["This", "book", "was", "fantastic", "I", "really", "love", "science", "fiction", "but", "the", "protagonist", "was", "rude", "sometimes"]
word_to_idx = {word: i for i, word in enumerate(words)}

# Convert word_to_idx to a tensor
inputs = torch.LongTensor([word_to_idx[w] for w in words])

# Initialize embedding layer with ten dimensions
embedding = nn.Embedding(num_embeddings=len(words), embedding_dim=10)

# Pass the tensor to the embedding layer
output = embedding(inputs)
print(output)
```
####  2.2. <a name='Convolutionalneuralnetworksfortextclassification'></a>Convolutional neural networks for text classification

- **Build a CNN model for text**

```python
class TextClassificationCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super(TextClassificationCNN, self).__init__()
        # Initialize the embedding layer 
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.conv = nn.Conv1d(embed_dim, embed_dim, kernel_size=3, stride=1, padding=1)
        self.fc = nn.Linear(embed_dim, 2)
    def forward(self, text):
        embedded = self.embedding(text).permute(0, 2, 1)
        # Pass the embedded text through the convolutional layer and apply a ReLU
        conved = F.relu(self.conv(embedded))
        conved = conved.mean(dim=2) 
        return self.fc(conved)
```

- **Train a CNN model for text**

```python
# Define the loss function
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

for epoch in range(10):
    for sentence, label in data:     
        # Clear the gradients
        model.zero_grad()
        sentence = torch.LongTensor([word_to_ix.get(w, 0) for w in sentence]).unsqueeze(0) 
        label = torch.LongTensor([int(label)])
        outputs = model(sentence)
        loss = criterion(outputs, label)
        loss.backward()
        # Update the parameters
        optimizer.step()
print('Training complete!')
```

- **Testing the Sentiment Analysis CNN Model**

```python
book_reviews = [
    "I love this book".split(),
    "I do not like this book".split()
]
for review in book_reviews:
    # Convert the review words into tensor form
    input_tensor = torch.tensor([word_to_ix[w] for w in review], dtype=torch.long).unsqueeze(0) 
    # Get the model's output
    outputs = model(input_tensor)
    # Find the index of the most likely sentiment category
    _, predicted_label = torch.max(outputs.data, 1)
    # Convert the predicted label into a sentiment string
    sentiment = "Positive" if predicted_label.item()==1 else "Negative"
    print(f"Book Review: {' '.join(review)}")
    print(f"Sentiment: {sentiment}\n")
```

####  2.3. <a name='Recurrentneuralnetworksfortextclassification'></a>Recurrent neural networks for text classification

- **Building an RNN model for text**

```python
# Complete the RNN class
class RNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNNModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.rnn(x, h0)
        out = out[:, -1, :] 
        out = self.fc(out)
        return out

# Initialize the model
rnn_model = RNNModel(input_size, hidden_size, num_layers, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(rnn_model.parameters(), lr=0.01)

# Train the model for ten epochs and zero the gradients
for epoch in range(10): 
    optimizer.zero_grad()
    outputs = rnn_model(X_train_seq)
    loss = criterion(outputs, y_train_seq)
    loss.backward()
    optimizer.step()
    print(f'Epoch: {epoch+1}, Loss: {loss.item()}')
```

- **Building an LSTM model for text**

```python
# Initialize the LSTM and the output layer with parameters
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = out[:, -1, :] 
        out = self.fc(out)
        return out

# Initialize model with required parameters
lstm_model = LSTMModel(input_size, hidden_size, num_layers, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(lstm_model.parameters(), lr=0.01)

# Train the model by passing the correct parameters and zeroing the gradient
for epoch in range(10): 
    optimizer.zero_grad()
    outputs = lstm_model(X_train_seq)
    loss = criterion(outputs, y_train_seq)
    loss.backward()
    optimizer.step()
    print(f'Epoch: {epoch+1}, Loss: {loss.item()}')
```

- **Building a GRU model for text**

```python
# Complete the GRU model
class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(GRUModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)       
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size) 
        out, _ = self.gru(x, h0)
        out = out[:, -1, :] 
        out = self.fc(out)
        return out

# Initialize the model
gru_model = GRUModel(input_size, hidden_size, num_layers, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(gru_model.parameters(), lr=0.01)

# Train the model and backpropagate the loss after initialization
for epoch in range(15): 
    optimizer.zero_grad()
    outputs = gru_model(X_train_seq)
    loss = criterion(outputs, y_train_seq)
    loss.backward()
    optimizer.step()
    print(f'Epoch: {epoch+1}, Loss: {loss.item()}')
```

####  2.4. <a name='Evaluationmetricsfortextclassification'></a>Evaluation metrics for text classification

- **Evaluating RNN classification models**

```python
# Create an instance of the metrics
accuracy = Accuracy(task="multiclass", num_classes=num_classes)
precision = Precision("multiclass", num_classes=num_classes)
recall = Recall(task="multiclass", num_classes=num_classes)
f1 = F1Score(task="multiclass", num_classes=num_classes)

# Generate the predictions
outputs = rnn_model(X_test_seq)
_, predicted = torch.max(outputs, 1)

# Calculate the metrics
accuracy_score = accuracy(predicted, y_test_seq)
precision_score = precision(predicted, y_test_seq)
recall_score = recall(predicted, y_test_seq)
f1_score = f1(predicted, y_test_seq)
print("RNN Model - Accuracy: {}, Precision: {}, Recall: {}, F1 Score: {}".format(accuracy_score, precision_score, recall_score, f1_score))
```

- **Evaluating the model's performance**

```python
# Create an instance of the metrics
accuracy = Accuracy(task="multiclass", num_classes=3)
precision = Precision(task="multiclass", num_classes=3)
recall = Recall(task="multiclass", num_classes=3)
f1 = F1Score(task="multiclass", num_classes=3)

# Calculate metrics for the LSTM model
accuracy_1 = accuracy(y_pred_lstm, y_test)
precision_1 = precision(y_pred_lstm, y_test)
recall_1 = recall(y_pred_lstm, y_test)
f1_1 = f1(y_pred_lstm, y_test)
print("LSTM Model - Accuracy: {}, Precision: {}, Recall: {}, F1 Score: {}".format(accuracy_1, precision_1, recall_1, f1_1))

# Calculate metrics for the GRU model
accuracy_2 = accuracy(y_pred_gru, y_test)
precision_2 = precision(y_pred_gru, y_test)
recall_2 = recall(y_pred_gru, y_test)
f1_2 = f1(y_pred_gru, y_test)
print("GRU Model - Accuracy: {}, Precision: {}, Recall: {}, F1 Score: {}".format(accuracy_2, precision_2, recall_2, f1_2))
```

---
###  3. <a name='TextGenerationwithPyTorch'></a>Text Generation with PyTorch

[Slide]({{site.baseurl}}/files/DeepLearningforTextwithPyTorch-C3.pdf)

####  3.1. <a name='Introductiontotextgeneration'></a>Introduction to text generation

- **Creating a RNN model for text generation**

```python
# Include an RNN layer and linear layer in RNNmodel class
class RNNmodel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNNmodel, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
      h0 = torch.zeros(1, x.size(0), self.hidden_size)
      out, _ = self.rnn(x, h0)  
      out = self.fc(out[:, -1, :])  
      return out

# Instantiate the RNN model
model = RNNmodel(len(chars), 16, len(chars))
```

- **Text generation using RNN - Training and Generation**

```python
# Instantiate the loss function
criterion = nn.CrossEntropyLoss()
# Instantiate the optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Train the model
for epoch in range(100):
    model.train()
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch+1) % 10 == 0:
        print(f'Epoch {epoch+1}/100, Loss: {loss.item()}')

# Test the model
model.eval()
test_input = char_to_ix['r']
test_input = nn.functional.one_hot(torch.tensor(test_input).view(-1, 1), num_classes=len(chars)).float()
predicted_output = model(test_input)
predicted_char_ix = torch.argmax(predicted_output, 1).item()
print(f"Test Input: 'r', Predicted Output: '{ix_to_char[predicted_char_ix]}'")
```

####  3.2. <a name='Generativeadversarialnetworksfortextgeneration'></a>Generative adversarial networks for text generation

- **Building a generator and discriminator**

```python
# Define the generator class
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(nn.Linear(seq_length, seq_length), nn.Sigmoid())
    def forward(self, x):
        return self.model(x)

# Define the discriminator networks
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(nn.Linear(seq_length, 1), nn.Sigmoid())
    def forward(self, x):
        return self.model(x)
```

- **Training a GAN model**

```python
# Define the loss function and optimizer
criterion = nn.BCELoss()
optimizer_gen = torch.optim.Adam(generator.parameters(), lr=0.001)
optimizer_disc = torch.optim.Adam(discriminator.parameters(), lr=0.001)

for epoch in range(num_epochs):
    for real_data in data:
        # Unsqueezing real_data and prevent gradient recalculations
        real_data = real_data.unsqueeze(0)
        noise = torch.rand((1, seq_length))
        fake_data = generator(noise)
        disc_real = discriminator(real_data)
        disc_fake = discriminator(fake_data.detach())
        loss_disc = criterion(disc_real, torch.ones_like(disc_real)) + criterion(disc_fake, torch.zeros_like(disc_fake))
        optimizer_disc.zero_grad()
        loss_disc.backward()
        optimizer_disc.step()

        # Train the generator
        disc_fake = discriminator(fake_data)
        loss_gen = criterion(disc_fake, torch.ones_like(disc_fake))
        optimizer_gen.zero_grad()
        loss_gen.backward()
        optimizer_gen.step()

    if (epoch+1) % print_every == 0:
        print(f"Epoch {epoch+1}/{num_epochs}:\t Generator loss: {loss_gen.item()}\t Discriminator loss: {loss_disc.item()}")

print("\nReal data: ")
print(data[:5])

print("\nGenerated data: ")
for _ in range(5):
    noise = torch.rand((1, seq_length))
    generated_data = generator(noise)
    # Detach the tensor and print data
    print(torch.round(generated_data).detach())
```

####  3.3. <a name='Pre-trainedmodelsfortextgeneration'></a>Pre-trained models for text generation

- **Text completion with pre-trained GPT-2 models**

```python
# Initialize the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Initialize the pre-trained model
model = GPT2LMHeadModel.from_pretrained('gpt2')

seed_text = "Once upon a time"

# Encode the seed text to get input tensors
input_ids = tokenizer.encode(seed_text, return_tensors='pt')

# Generate text from the model
output = model.generate(input_ids, max_length=100, temperature=0.7, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id) 

generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

print(generated_text)
```

- **Language translation with pretrained PyTorch model**

```python
# Initalize tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

input_prompt = "translate English to French: 'Hello, how are you?'"

# Encode the input prompt using the tokenizer
input_ids = tokenizer.encode(input_prompt, return_tensors="pt")

# Generate the translated ouput
output = model.generate(input_ids, max_length=50)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated text:",generated_text)
```

####  3.4. <a name='Evaluationmetricsfortextgeneration'></a>Evaluation metrics for text generation

**BLEU score là gì?**

BLEU (Bilingual Evaluation Understudy) là một chỉ số được sử dụng để đánh giá chất lượng của văn bản được tạo ra bởi máy (machine-generated text) bằng cách so sánh nó với một hoặc nhiều văn bản tham chiếu do con người tạo ra. 

Nói một cách đơn giản, BLEU score đo lường mức độ tương đồng giữa văn bản do máy tạo ra và văn bản do con người viết. Điểm số càng cao (tiến gần đến 1) thì văn bản máy tạo ra càng giống với văn bản tham chiếu, tức là chất lượng càng tốt.

BLEU thường được sử dụng trong các nhiệm vụ sau:

* **Dịch máy:** Đánh giá chất lượng của bản dịch máy so với bản dịch của con người.
* **Tóm tắt văn bản:** Đo lường mức độ bao quát và chính xác của bản tóm tắt do máy tạo ra so với bản tóm tắt do con người viết.
* **Sinh caption ảnh:** Đánh giá mức độ phù hợp của caption do máy tạo ra với nội dung của ảnh.
* **Nhận dạng giọng nói:** Đo lường độ chính xác của văn bản được chuyển đổi từ giọng nói.

**Thuật toán tính BLEU score**

BLEU score được tính toán dựa trên **n-gram**. N-gram là tập hợp các từ liền kề nhau trong văn bản. Ví dụ:

* **Unigram (1-gram):**  "tôi", "yêu", "Việt", "Nam"
* **Bigram (2-gram):** "tôi yêu", "yêu Việt", "Việt Nam"
* **Trigram (3-gram):** "tôi yêu Việt", "yêu Việt Nam"

BLEU score tính toán độ chính xác (precision) bằng cách đếm số lượng n-gram trùng khớp giữa văn bản máy tạo ra và văn bản tham chiếu, sau đó chia cho tổng số n-gram trong văn bản máy tạo ra. 

Tuy nhiên, chỉ sử dụng precision có thể dẫn đến kết quả sai lệch. Ví dụ, một văn bản máy tạo ra chỉ lặp đi lặp lại một từ có trong văn bản tham chiếu sẽ có precision cao, mặc dù chất lượng kém. Để khắc phục điều này, BLEU score sử dụng thêm **hình phạt độ ngắn (brevity penalty)**. Hình phạt này sẽ giảm điểm số nếu văn bản máy tạo ra ngắn hơn nhiều so với văn bản tham chiếu.

**Công thức tính BLEU score:**

```
BLEU = brevity penalty * exp( sum( w_n * log( p_n ) ) )
```

Trong đó:

* **brevity penalty:** Hình phạt độ ngắn.
* **w_n:** Trọng số của n-gram thứ n (thường là 1/N với N là số lượng n-gram).
* **p_n:** Độ chính xác của n-gram thứ n.



**ROUGE score là gì?**

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) là một tập hợp các chỉ số được sử dụng để đánh giá chất lượng của văn bản tóm tắt do máy tạo ra bằng cách so sánh nó với một hoặc nhiều văn bản tóm tắt tham chiếu do con người tạo ra. 

Tóm lại, ROUGE score đo lường mức độ tương đồng giữa bản tóm tắt do máy tạo ra và bản tóm tắt do con người viết. Điểm số càng cao thì bản tóm tắt của máy càng giống với bản tóm tắt tham chiếu, tức là chất lượng càng tốt.

ROUGE thường được sử dụng trong các nhiệm vụ sau:

* **Tóm tắt văn bản:** Đo lường mức độ bao quát và chính xác của bản tóm tắt do máy tạo ra so với bản tóm tắt do con người viết.
* **Dịch máy:** Đánh giá chất lượng của bản dịch máy so với bản dịch của con người (trong trường hợp dịch rút gọn).

**Thuật toán tính ROUGE score**

ROUGE score được tính toán dựa trên sự **chồng chéo** giữa các đơn vị (unit) trong văn bản tóm tắt do máy tạo ra và văn bản tóm tắt tham chiếu. Các đơn vị này có thể là **n-gram** (tập hợp các từ liền kề nhau), **chuỗi con chung dài nhất (LCS)** hoặc **chuỗi từ khớp**.

Có nhiều biến thể của ROUGE score, mỗi biến thể sử dụng một đơn vị khác nhau để tính toán sự chồng chéo:

* **ROUGE-N:** Sử dụng n-gram để tính toán sự chồng chéo. Ví dụ, ROUGE-1 sử dụng unigram (từ đơn), ROUGE-2 sử dụng bigram (cặp từ liền kề).
* **ROUGE-L:** Sử dụng LCS để tính toán sự chồng chéo. LCS là chuỗi các từ dài nhất (không nhất thiết phải liên tiếp) xuất hiện trong cả hai văn bản.
* **ROUGE-S:** Sử dụng chuỗi từ khớp (skip-bigram) để tính toán sự chồng chéo. Skip-bigram là cặp từ có thể xuất hiện cách nhau bởi các từ khác trong văn bản.

**Các chỉ số ROUGE metrics**

Đối với mỗi biến thể của ROUGE, ta có thể tính toán ba chỉ số sau:

* **Recall:** Tỷ lệ các đơn vị trong văn bản tham chiếu xuất hiện trong văn bản máy tạo ra. Recall đo lường mức độ bao quát của bản tóm tắt máy.
* **Precision:** Tỷ lệ các đơn vị trong văn bản máy tạo ra xuất hiện trong văn bản tham chiếu. Precision đo lường mức độ chính xác của bản tóm tắt máy.
* **F-measure:** Trung bình điều hòa của Recall và Precision. F-measure cân bằng giữa Recall và Precision.


```python
reference_text = "Once upon a time, there was a little girl who lived in a village near the forest."
generated_text = "Once upon a time, the world was a place of great beauty and great danger. The world of the gods was the place where the great gods were born, and where they were to live."

# Initialize BLEU and ROUGE scorers
bleu = BLEUScore()
rouge = ROUGEScore()

# Calculate the BLEU and ROUGE scores
bleu_score = bleu([generated_text], [[reference_text]])
rouge_score = rouge([generated_text], [[reference_text]])

# Print the BLEU and ROUGE scores
print("BLEU Score:", bleu_score.item())
print("ROUGE Score:", rouge_score)
```

---
###  4. <a name='AdvancedTopicsinDeepLearningforTextwithPyTorch'></a>Advanced Topics in Deep Learning for Text with PyTorch

[Slide]({{site.baseurl}}/files/DeepLearningforTextwithPyTorch-C4.pdf)

####  4.1. <a name='Transferlearningfortextclassification'></a>Transfer learning for text classification

- **Transfer learning using BERT**

```python
# Load the BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Tokenize your data and return PyTorch tensors
inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=32)
inputs["labels"] = torch.tensor(labels)

# Setup the optimizer using model parameters
optimizer = torch.optim.AdamW(model.parameters(), lr=0.00001)
model.train()
for epoch in range(2):
    outputs = model(**inputs)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    print(f"Epoch: {epoch+1}, Loss: {loss.item()}")
```

- **Evaluating the BERT model**

```python
text = "I had an awesome day!"

# Tokenize the text and return PyTorch tensors
input_eval = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=32)
outputs_eval = model(**input_eval)

# Convert the output logits to probabilities
predictions = torch.nn.functional.softmax(outputs_eval.logits, dim=-1)

# Display the sentiments
predicted_label = "positive" if torch.argmax(predictions) > 0 else "negative"
print(f"Text: {text}\nSentiment: {predicted_label}")
```

####  4.2. <a name='Transformersfortextprocessing'></a>Transformers for text processing

- **Creating a transformer model**

```python
class TransformerEncoder(nn.Module):
    def __init__(self, embed_size, heads, num_layers, dropout):
        super(TransformerEncoder, self).__init__()
        # Initialize the encoder 
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=embed_size, nhead=heads),
            num_layers=num_layers)
        # Define the fully connected layer
        self.fc = nn.Linear(embed_size, 2)

    def forward(self, x):
        # Pass the input through the transformer encoder 
        x = self.encoder(x)
        x = x.mean(dim=1) 
        return self.fc(x)

model = TransformerEncoder(embed_size=512, heads=8, num_layers=3, dropout=0.5)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()
```

- **Training and testing the Transformer model**

```python
for epoch in range(5):  
    for sentence, label in zip(train_sentences, train_labels):
        # Split the sentences into tokens and stack the embeddings
        tokens = sentence.split()
        data = torch.stack([token_embeddings[token] for token in tokens], dim=1)
        output = model(data)
        loss = criterion(output, torch.tensor([label]))
        # Zero the gradients and perform a backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch}, Loss: {loss.item()}")

def predict(sentence):
    model.eval()
    # Deactivate the gradient computations and get the sentiment prediction.
    with torch.no_grad():
        tokens = sentence.split()
        data = torch.stack([token_embeddings.get(token, torch.rand((1, 512))) for token in tokens], dim=1)
        output = model(data)
        predicted = torch.argmax(output, dim=1)
        return "Positive" if predicted.item() == 1 else "Negative"

sample_sentence = "This product can be better"
print(f"'{sample_sentence}' is {predict(sample_sentence)}")
```

####  4.3. <a name='Attentionmechanismsfortextgeneration'></a>Attention mechanisms for text generation

- **Creating a RNN model with attention**

```python
class RNNWithAttentionModel(nn.Module):
    def __init__(self):
        super(RNNWithAttentionModel, self).__init__()
        # Create an embedding layer for the vocabulary
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim, batch_first=True)
        # Apply a linear transformation to get the attention scores
        self.attention = nn.Linear(hidden_dim, 1)
        self.fc = nn.Linear(hidden_dim, vocab_size)
    def forward(self, x):
        x = self.embeddings(x)
        out, _ = self.rnn(x)
        #  Get the attention weights
        attn_weights = torch.nn.functional.softmax(self.attention(out).squeeze(2), dim=1)
        # Compute the context vector 
        context = torch.sum(attn_weights.unsqueeze(2) * out, dim=1)
        out = self.fc(context)
        return out
      
attention_model = RNNWithAttentionModel()
optimizer = torch.optim.Adam(attention_model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()
print("Model Instantiated")
```

- **Training and testing the RNN model with attention**

```python
for epoch in range(epochs):
    attention_model.train()
    optimizer.zero_grad()
    padded_inputs = pad_sequences(inputs)
    outputs = attention_model(padded_inputs)
    loss = criterion(outputs, targets)
    loss.backward()
    optimizer.step()

for input_seq, target in zip(input_data, target_data):
    input_test = torch.tensor(input_seq, dtype=torch.long).unsqueeze(0)
   	
    #  Set the RNN model to evaluation mode
    rnn_model.eval()
    # Get the RNN output by passing the appropriate input 
    rnn_output = rnn_model(input_test)
    # Extract the word with the highest prediction score 
    rnn_prediction = ix_to_word[torch.argmax(rnn_output).item()]

    attention_model.eval()
    attention_output = attention_model(input_test)
    # Extract the word with the highest prediction score
    attention_prediction = ix_to_word[torch.argmax(attention_output).item()]

    print(f"\nInput: {' '.join([ix_to_word[ix] for ix in input_seq])}")
    print(f"Target: {ix_to_word[target]}")
    print(f"RNN prediction: {rnn_prediction}")
    print(f"RNN with Attention prediction: {attention_prediction}")
```

####  4.4. <a name='Adversarialattacksontextclassificationmodels'></a>Adversarial attacks on text classification models

Tưởng tượng bạn có một chú chó biết phân loại đồ chơi. Bạn đưa cho nó một quả bóng, nó sủa "bóng!". Bạn đưa cho nó một cái xe, nó sủa "xe!". Chú chó này chính là mô hình phân loại văn bản của chúng ta. 

Bây giờ, một người bạn tinh nghịch muốn đánh lừa chú chó. Họ lấy quả bóng, dán thêm vài miếng sticker lên đó. Chú chó nhìn thấy, bối rối và sủa "xe!". 

Đó chính là **Adversarial attack**! 

**Giải thích chi tiết hơn:**

* **Mô hình phân loại văn bản:**  Giống như chú chó, nó được huấn luyện để đọc văn bản và phân loại chúng vào các nhóm khác nhau (ví dụ: tin tức, thư rác, bình luận tích cực/tiêu cực).
* **Adversarial attack:** Là những thay đổi nhỏ, tinh vi đối với văn bản đầu vào, nhằm đánh lừa mô hình đưa ra kết quả sai. Giống như việc dán sticker lên quả bóng. Những thay đổi này có thể là:
    * Thay đổi một vài từ đồng nghĩa.
    * Thêm các ký tự đặc biệt hoặc khoảng trắng.
    * Thay đổi thứ tự từ.
* **Mục tiêu:**  
    * **Gây lỗi cho mô hình:** Khiến mô hình phân loại sai.
    * **Tìm hiểu điểm yếu:**  Hiểu rõ hơn cách thức hoạt động của mô hình để cải thiện nó.

**Ví dụ:**

Một mô hình phân loại bình luận phim được huấn luyện để nhận biết bình luận tích cực ("Phim này thật tuyệt vời!") và tiêu cực ("Tôi ghét bộ phim này").  

Kẻ tấn công có thể thay đổi bình luận tích cực thành "Phim này thật tuyệt vời... **không!**"  

Mô hình có thể bị đánh lừa bởi sự thay đổi nhỏ này và phân loại bình luận là tiêu cực.

**Tại sao Adversarial attacks lại quan trọng?**

* **An ninh:**  Tấn công này có thể được sử dụng để đánh lừa các hệ thống lọc thư rác, phát hiện tin giả, hoặc đánh giá rủi ro tín dụng.
* **Độ tin cậy:**  Nó cho thấy các mô hình AI vẫn còn nhiều hạn chế và dễ bị tổn thương.

Hiểu rõ về Adversarial attacks giúp chúng ta phát triển các mô hình AI mạnh mẽ và đáng tin cậy hơn.


**Fast Gradient Sign Method (FGSM)**

Fast Gradient Sign Method (FGSM) là một phương pháp đơn giản nhưng hiệu quả để tạo ra các adversarial examples (ví dụ đối kháng) nhằm tấn công các mô hình học máy, đặc biệt là trong lĩnh vực thị giác máy tính. 

Hãy tưởng tượng bạn có một bức ảnh con mèo. Mô hình học máy của bạn có thể nhận ra nó là một con mèo. Bây giờ, bạn muốn đánh lừa mô hình này bằng cách thêm vào bức ảnh một lượng nhiễu nhỏ, không thể nhận ra bằng mắt thường. Nhiễu này được tính toán bởi FGSM sao cho nó làm tăng tối đa lỗi của mô hình. Kết quả là, mô hình có thể sẽ nhận nhầm bức ảnh con mèo thành một thứ khác, ví dụ như con chó.

**Cách thức hoạt động của FGSM:**

1. **Tính toán gradient của loss function:**  FGSM bắt đầu bằng cách tính toán gradient của hàm mất mát (loss function) của mô hình đối với ảnh đầu vào. Gradient này cho biết hướng cần thay đổi các pixel của ảnh để làm tăng lỗi của mô hình.

2. **Lấy dấu của gradient:**  Tiếp theo, FGSM lấy dấu của gradient. Điều này có nghĩa là mỗi thành phần của gradient sẽ được thay thế bằng +1 nếu nó dương và -1 nếu nó âm. 

3. **Tạo nhiễu đối kháng:** Cuối cùng, FGSM nhân dấu của gradient với một hằng số nhỏ (epsilon). Kết quả là một nhiễu đối kháng được thêm vào ảnh gốc để tạo ra adversarial example.

**Công thức:**

`adversarial_image = original_image + epsilon * sign(gradient(loss_function(original_image, true_label)))`

**Ưu điểm của FGSM:**

* **Đơn giản và hiệu quả:** FGSM dễ dàng thực hiện và có thể tạo ra các adversarial examples hiệu quả.
* **Tính toán nhanh:**  Do chỉ cần tính toán gradient một lần, FGSM rất nhanh.

**Nhược điểm của FGSM:**

* **Tấn công white-box:** FGSM yêu cầu truy cập vào gradient của mô hình, nghĩa là kẻ tấn công cần biết kiến trúc và trọng số của mô hình (white-box attack).
* **Dễ bị phòng thủ:** Các phương pháp phòng thủ đơn giản có thể làm giảm hiệu quả của FGSM.

**Ứng dụng:**

* **Nghiên cứu về tính robustness của mô hình:** FGSM được sử dụng để đánh giá khả năng chống chịu của các mô hình học máy trước các tấn công đối kháng.
* **Phát triển các phương pháp phòng thủ:** Hiểu rõ FGSM giúp phát triển các kỹ thuật phòng thủ hiệu quả hơn.

**Projected Gradient Descent (PGD)**

Projected Gradient Descent (PGD) là một phương pháp lặp được sử dụng để tìm giá trị tối thiểu của một hàm số, đặc biệt khi có ràng buộc đối với các biến. Nó thường được ứng dụng trong học máy để tạo ra các adversarial examples mạnh mẽ hơn so với FGSM.

**Tưởng tượng:**

Hãy hình dung bạn đang đứng trên một ngọn đồi và muốn tìm đường xuống chân đồi nhanh nhất. Bạn có thể sử dụng gradient descent, tức là di chuyển theo hướng dốc nhất xuống dưới. Tuy nhiên, nếu có một hàng rào chắn ngang đường đi, bạn sẽ phải đi dọc theo hàng rào cho đến khi tìm được lối đi xuống tiếp. PGD hoạt động tương tự như vậy, nó kết hợp gradient descent với việc "chiếu" (project) các bước di chuyển vào vùng ràng buộc cho phép.

**Cách thức hoạt động:**

1. **Khởi tạo:** Bắt đầu từ một điểm bất kỳ trong vùng ràng buộc.

2. **Tính toán gradient:**  Tính toán gradient của hàm mục tiêu tại điểm hiện tại. Gradient chỉ hướng làm tăng giá trị hàm số, vì vậy ta sẽ di chuyển theo hướng ngược lại.

3. **Thực hiện bước di chuyển:** Di chuyển một bước nhỏ theo hướng ngược với gradient.

4. **Chiếu:** Nếu bước di chuyển đưa ra khỏi vùng ràng buộc, "chiếu" điểm đó trở lại vùng ràng buộc. Có nhiều cách chiếu khác nhau, ví dụ như chiếu vuông góc đến biên của vùng ràng buộc.

5. **Lặp lại:** Lặp lại các bước 2-4 cho đến khi đạt được điều kiện dừng (ví dụ: số lần lặp tối đa hoặc giá trị hàm mục tiêu không giảm đáng kể).

**So sánh với FGSM:**

* **FGSM:** Thực hiện một bước tấn công duy nhất theo hướng ngược với gradient.
* **PGD:** Thực hiện nhiều bước tấn công, mỗi bước đều được chiếu vào vùng ràng buộc. Điều này cho phép PGD khám phá không gian tấn công rộng hơn và tạo ra các adversarial examples mạnh mẽ hơn, khó phòng thủ hơn.

**Ưu điểm của PGD:**

* **Tạo ra adversarial examples mạnh mẽ:** PGD thường được coi là phương pháp tấn công mạnh nhất trong số các phương pháp dựa trên gradient.
* **Linh hoạt:** Có thể điều chỉnh các tham số như kích thước bước di chuyển và số lần lặp để kiểm soát cường độ tấn công.

**Nhược điểm của PGD:**

* **Tốn kém về mặt tính toán:** Do thực hiện nhiều lần lặp, PGD tốn nhiều thời gian tính toán hơn FGSM.
* **Vẫn là tấn công white-box:**  Tương tự FGSM, PGD yêu cầu truy cập vào gradient của mô hình.

**Ứng dụng:**

* **Đánh giá tính robustness của mô hình:** PGD được sử dụng để đánh giá khả năng chống chịu của các mô hình học máy trước các tấn công mạnh mẽ.
* **Phát triển các phương pháp phòng thủ:** Nghiên cứu về PGD giúp phát triển các kỹ thuật phòng thủ tiên tiến hơn.

Tóm lại, PGD là một phương pháp tấn công mạnh mẽ và phổ biến trong lĩnh vực adversarial machine learning. Nó đóng vai trò quan trọng trong việc đánh giá và cải thiện tính an toàn của các mô hình học máy.


**The Carlini & Wagner (C&W) attack**

Tấn công Carlini & Wagner (C&W) là một phương pháp tạo ra các adversarial examples (ví dụ đối kháng) rất hiệu quả, được đánh giá là một trong những phương pháp tấn công mạnh mẽ nhất hiện nay. Không giống như FGSM và PGD dựa trên gradient descent, C&W sử dụng một phương pháp tối ưu hóa phức tạp hơn để tìm ra nhiễu tối thiểu cần thiết để đánh lừa mô hình.

**Mục tiêu:**

Mục tiêu của C&W là tìm ra nhiễu đối kháng nhỏ nhất (theo một số metric khoảng cách, ví dụ L2 norm) có thể khiến mô hình phân loại sai. Nói cách khác, C&W cố gắng tìm ra sự thay đổi nhỏ nhất đối với đầu vào khiến mô hình đưa ra dự đoán hoàn toàn khác.

**Cách thức hoạt động:**

1. **Định nghĩa hàm mục tiêu:**  C&W định nghĩa một hàm mục tiêu kết hợp hai yếu tố:
    * **Sự tự tin của mô hình đối với lớp sai:**  Hàm mục tiêu muốn tối đa hóa sự tự tin của mô hình đối với lớp sai (tức là lớp mà kẻ tấn công muốn mô hình dự đoán).
    * **Khoảng cách giữa ảnh gốc và ảnh đối kháng:**  Đồng thời, hàm mục tiêu muốn tối thiểu hóa khoảng cách giữa ảnh gốc và ảnh đối kháng để nhiễu không bị phát hiện.

2. **Tối ưu hóa hàm mục tiêu:** C&W sử dụng các kỹ thuật tối ưu hóa phức tạp để tìm ra nhiễu tối ưu thỏa mãn hàm mục tiêu. Quá trình này liên quan đến việc giải một bài toán tối ưu hóa ràng buộc.

**Ưu điểm của C&W:**

* **Hiệu quả cao:** C&W tạo ra các adversarial examples rất hiệu quả, có thể đánh lừa nhiều loại mô hình.
* **Tìm ra nhiễu tối thiểu:** C&W tập trung vào việc tìm ra nhiễu nhỏ nhất có thể, khiến các adversarial examples khó bị phát hiện hơn.

**Nhược điểm của C&W:**

* **Tốn kém về mặt tính toán:** Quá trình tối ưu hóa của C&W phức tạp và tốn nhiều thời gian hơn so với FGSM và PGD.
* **Vẫn là tấn công white-box:** C&W cũng yêu cầu truy cập vào kiến trúc và trọng số của mô hình.


**So sánh với FGSM và PGD:**

| Phương pháp | Cách thức hoạt động | Ưu điểm | Nhược điểm |
|---|---|---|---|
| FGSM |  Một bước tấn công theo hướng gradient | Đơn giản, nhanh |  Yếu, dễ phòng thủ |
| PGD | Nhiều bước tấn công, chiếu vào vùng ràng buộc |  Mạnh mẽ hơn FGSM | Tốn kém hơn FGSM |
| C&W | Tối ưu hóa hàm mục tiêu phức tạp | Hiệu quả cao, nhiễu tối thiểu | Rất tốn kém |


**Ứng dụng:**

* **Nghiên cứu về tính robustness:** C&W là một công cụ mạnh mẽ để đánh giá khả năng chống chịu của các mô hình học máy trước các tấn công tinh vi.
* **Phát triển các phương pháp phòng thủ:**  Nghiên cứu về C&W thúc đẩy việc phát triển các kỹ thuật phòng thủ tiên tiến hơn để chống lại các adversarial examples.

Tóm lại, C&W là một phương pháp tấn công tiên tiến và hiệu quả, đóng vai trò quan trọng trong việc nghiên cứu và cải thiện tính an toàn của các mô hình học máy.

---

**Giải thích đơn giản**

Hãy tưởng tượng bạn có một chú chó robot được huấn luyện để nhận diện các loại trái cây. Khi bạn đưa cho nó xem một quả táo, nó sẽ nói "Táo!". 

Bây giờ, bạn muốn thử đánh lừa chú chó này bằng cách "chỉnh sửa" quả táo một chút, khiến nó nhận nhầm thành quả cam. Có ba cách để làm điều này:

**1. FGSM (Fast Gradient Sign Method):**

* **Thay đổi nhanh:** Giống như việc bạn **vẽ nhanh một nét bút** lên quả táo. Sự thay đổi này rất nhỏ, mắt thường khó nhận ra, nhưng đủ để đánh lừa chú chó robot.
* **Ví dụ:** Bạn chấm một chấm nhỏ màu cam lên quả táo. Chú chó có thể sẽ bị nhầm lẫn và nói "Cam!".

**2. PGD (Projected Gradient Descent):**

* **Thay đổi từ từ:** Giống như việc bạn **dùng bút chì tô màu cam lên quả táo từng chút một**, sau mỗi lần tô lại kiểm tra xem chú chó đã nhận nhầm chưa. Bạn sẽ tiếp tục tô cho đến khi chú chó nói "Cam!".
* **Ví dụ:** Bạn tô một chút màu cam lên quả táo. Chú chó vẫn nói "Táo!". Bạn tô thêm một chút nữa. Cứ như vậy cho đến khi chú chó robot bị đánh lừa.

**3. C&W (Carlini & Wagner attack):**

* **Thay đổi tinh vi:** Giống như việc bạn **dùng công nghệ cao để thay đổi màu sắc của quả táo một cách tinh vi**, sao cho vừa giống cam nhất có thể, vừa khó bị phát hiện nhất.
* **Ví dụ:** Bạn sử dụng một loại sơn đặc biệt để phủ lên quả táo một lớp màu cam rất mỏng, gần như không thể nhìn thấy bằng mắt thường. Chú chó robot chắc chắn sẽ bị đánh lừa!

**Tóm lại:**

* **FGSM:** Thay đổi nhanh, đơn giản.
* **PGD:** Thay đổi từ từ, kiên trì hơn, hiệu quả hơn FGSM.
* **C&W:** Thay đổi tinh vi, hiệu quả nhất, nhưng cũng phức tạp nhất.

Cả ba phương pháp này đều là những "chiêu trò" để đánh lừa mô hình học máy, giúp chúng ta hiểu rõ hơn về điểm yếu của mô hình và từ đó cải thiện chúng.
