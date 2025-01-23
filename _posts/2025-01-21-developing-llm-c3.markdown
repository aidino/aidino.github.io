---
layout: post
title: "Deep Learning for Text with PyTorch"
date: 2025-01-21 02:00:00 +0700
categories: developing large language models
---

Discover the exciting world of Deep Learning for Text with PyTorch and unlock new possibilities in natural language processing and text generation.

---
### Introduction to Deep Learning for Text with PyTorch

[Slide]({{site.baseurl}}/files/DeepLearningforTextwithPyTorch-C1.pdf)

#### Introduction to preprocessing for text

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
#### Encoding text data

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

#### Introduction to building a text processing pipeline

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
### Text Classification with PyTorch

#### Overview of Text Classification

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
#### Convolutional neural networks for text classification

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

#### Recurrent neural networks for text classification
#### Evaluation metrics for text classification

---
### Text Generation with PyTorch

---
### Advanced Topics in Deep Learning for Text with PyTorch