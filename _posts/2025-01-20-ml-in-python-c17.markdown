---
layout: post
title: "Introduction to Natural Language Processing in Python"
date: 2025-01-20 14:00:00 +0700
categories: machine learning in python
---

In this course, you'll learn natural language processing (NLP) basics, such as how to identify and separate words, how to extract topics in a text, and how to build your own fake news classifier. You'll also learn how to use basic libraries such as NLTK, alongside libraries which utilize deep learning to solve common NLP problems. This course will give you the foundation to process and parse text as you move forward in your Python learning.



---
## Regular expressions & word tokenization

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C1.pdf)

### Introduction to regular expressions

**Common regex patterns**

**1. Khớp với ký tự đơn (Matching single characters):**

*   `.` (dấu chấm): Khớp với bất kỳ ký tự nào ngoại trừ ký tự xuống dòng (`\n`).

    ```python
    import re

    text = "xin chào"
    pattern = "x.n"  # Khớp với "xin"
    match = re.search(pattern, text)
    if match:
        print(match.group())  # In ra: xin
    ```

*   `\d`: Khớp với bất kỳ chữ số nào (0-9).

    ```python
    text = "123abc456"
    pattern = "\d+"  # Khớp với một hoặc nhiều chữ số liên tiếp
    matches = re.findall(pattern, text)
    print(matches)  # In ra: ['123', '456']
    ```

*   `\w`: Khớp với bất kỳ ký tự chữ cái, chữ số hoặc dấu gạch dưới (\_).  Tương đương với `[a-zA-Z0-9_]`.

    ```python
    text = "hello_world123"
    pattern = "\w+"
    match = re.search(pattern, text)
    print(match.group())  # In ra: hello_world123
    ```

*   `\s`: Khớp với bất kỳ ký tự khoảng trắng nào (dấu cách, tab, xuống dòng, ...).

    ```python
    text = "hello world"
    pattern = "\s"
    matches = re.split(pattern, text)  # Tách chuỗi dựa trên khoảng trắng
    print(matches)  # In ra: ['hello', 'world']
    ```

**2. Lớp ký tự (Character classes):**

*   `[ ]`: Định nghĩa một tập hợp các ký tự. Ví dụ: `[aeiou]` khớp với bất kỳ nguyên âm nào.

    ```python
    text = "xin chao"
    pattern = "[aeiou]"
    matches = re.findall(pattern, text)
    print(matches)  # In ra: ['i', 'a', 'o']
    ```

*   `[^ ]`: Định nghĩa một tập hợp các ký tự *không* khớp. Ví dụ: `[^aeiou]` khớp với bất kỳ ký tự nào không phải nguyên âm.

    ```python
    text = "xin chao"
    pattern = "[^aeiou]"
    matches = re.findall(pattern, text)
    print(matches)  # In ra: ['x', 'n', ' ', 'c', 'h']
    ```

**3. Lặp lại (Repetition):**

*   `*`: Khớp với 0 hoặc nhiều lần xuất hiện của ký tự đứng trước.

    ```python
    text = "baaa"
    pattern = "ba*"
    match = re.search(pattern, text)
    print(match.group())  # In ra: baaa
    ```

*   `+`: Khớp với 1 hoặc nhiều lần xuất hiện của ký tự đứng trước.

    ```python
    text = "baaa"
    pattern = "ba+"
    match = re.search(pattern, text)
    print(match.group())  # In ra: baaa
    ```

*   `?`: Khớp với 0 hoặc 1 lần xuất hiện của ký tự đứng trước.

    ```python
    text = "ba"
    pattern = "ba?"
    match = re.search(pattern, text)
    print(match.group())  # In ra: ba

    text = "b"
    pattern = "ba?"
    match = re.search(pattern, text)
    if match:
        print(match.group())  # In ra: b
    ```

*   `{n}`: Khớp với đúng *n* lần xuất hiện.
*   `{n,}`: Khớp với *n* hoặc nhiều lần xuất hiện.
*   `{n,m}`: Khớp với ít nhất *n* và tối đa *m* lần xuất hiện.

    ```python
    text = "1234567890"
    pattern = "\d{3}"  # Khớp với 3 chữ số liên tiếp
    matches = re.findall(pattern, text)
    print(matches) # In ra: ['123', '456', '789']

    text = "1234567890"
    pattern = "\d{3,5}"  # Khớp với 3 đến 5 chữ số liên tiếp
    matches = re.findall(pattern, text)
    print(matches) # In ra: ['12345', '67890']
    ```

**4. Neo (Anchors):**

*   `^`: Khớp với đầu chuỗi.
*   `$`: Khớp với cuối chuỗi.

    ```python
    text = "hello world"
    pattern = "^hello"  # Khớp với "hello" ở đầu chuỗi
    match = re.search(pattern, text)
    print(match.group())  # In ra: hello

    pattern = "world$"  # Khớp với "world" ở cuối chuỗi
    match = re.search(pattern, text)
    print(match.group())  # In ra: world
    ```

**5. Nhóm (Grouping):**

*   `()`: Nhóm các ký tự lại với nhau.  Có thể dùng để lấy các phần khớp khác nhau.

    ```python
    text = "John Doe"
    pattern = "(\w+) (\w+)"  # Nhóm tên và họ
    match = re.search(pattern, text)
    print(match.group(1))  # In ra: John
    print(match.group(2))  # In ra: Doe
    ```

#### Practicing regular expressions: `re.split()` and `re.findall()`

```python
my_string = "Let's write RegEx!  Won't that be fun?  I sure think so.  Can you find 4 sentences?  Or perhaps, all 19 words?"

# Write a pattern to match sentence endings: sentence_endings
sentence_endings = r"[.?!]"

# Split my_string on sentence endings and print the result
print(re.split(sentence_endings, my_string))

# Find all capitalized words in my_string and print the result
capitalized_words = r"[A-Z]\w+"
print(re.findall(capitalized_words, my_string))

# Split my_string on spaces and print the result
spaces = r"\s+"
print(re.split(spaces, my_string))

# Find all digits in my_string and print the result
digits = r"\d+"
print(re.findall(digits, my_string))

```

```bash
["Let's write RegEx", "  Won't that be fun", '  I sure think so', '  Can you find 4 sentences', '  Or perhaps, all 19 words', '']
['Let', 'RegEx', 'Won', 'Can', 'Or']
["Let's", 'write', 'RegEx!', "Won't", 'that', 'be', 'fun?', 'I', 'sure', 'think', 'so.', 'Can', 'you', 'find', '4', 'sentences?', 'Or', 'perhaps,', 'all', '19', 'words?']
['4', '19']
```

### Introduction to tokenization

Sự khác biệt chính giữa `re.search()` và `re.match()` trong Python là vị trí chúng tìm kiếm mẫu trong chuỗi:

*   **`re.match()`:** Kiểm tra xem mẫu có khớp với **phần đầu** của chuỗi hay không. Nếu mẫu không khớp ngay từ đầu chuỗi, `re.match()` sẽ trả về `None`.

*   **`re.search()`:** Tìm kiếm mẫu **ở bất kỳ vị trí nào** trong chuỗi. Nếu tìm thấy mẫu, `re.search()` sẽ trả về một đối tượng khớp (match object), chứa thông tin về vị trí và nội dung của phần khớp.

**Ví dụ:**

```python
import re

text = "xin chào mọi người"
pattern = "chào"

# re.match()
match_match = re.match(pattern, text)
if match_match:
    print("re.match():", match_match.group())
else:
    print("re.match(): Không khớp")

# re.search()
match_search = re.search(pattern, text)
if match_search:
    print("re.search():", match_search.group())
else:
    print("re.search(): Không khớp")
```

**Kết quả:**

```
re.match(): Không khớp
re.search(): chào
```

**Giải thích:**

*   `re.match()` không tìm thấy "chào" ở đầu chuỗi "xin chào mọi người", nên trả về `None`.
*   `re.search()` tìm thấy "chào" trong chuỗi, nên trả về một đối tượng khớp.

**Tóm lại:**

*   Dùng `re.match()` khi bạn muốn kiểm tra xem chuỗi có bắt đầu bằng một mẫu cụ thể hay không.
*   Dùng `re.search()` khi bạn muốn tìm mẫu ở bất kỳ đâu trong chuỗi.

#### Word tokenization with NLTK

```python
# Import necessary modules
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# Split scene_one into sentences: sentences
sentences = sent_tokenize(scene_one)

# Use word_tokenize to tokenize the fourth sentence: tokenized_sent
tokenized_sent = word_tokenize(sentences[3])

# Make a set of unique tokens in the entire scene: unique_tokens
unique_tokens = set(word_tokenize(scene_one))

# Print the unique tokens result
print(unique_tokens)

```

```bash
<script.py> output:
    {'[', 'fly', 'beat', 'its', 'non-migratory', 'anyway', 'search', 'he', 'ridden', 'Well', 'Court', 'matter', 'sovereign', 'wings', 'It', 'Not', 'needs', 'servant', 'by', 'two', 'knights', "n't", 'lord', 'But', 'one', 'migrate', 'be', 'the', '?', 'covered', 'grips', 'master', 'European', 'snows', 'Am', 'five', 'house', 'Wait', 'at', 'trusty', 'bangin', 'kingdom', 'Are', 'I', 'if', 'maintain', 'ask', 'weight', "'re", 'King', 'these', 'held', 'yet', 'No', 'and', 'Please', "'em", 'point', 'castle', 'will', 'with', 'does', 'The', 'ounce', 'they', 'African', 'speak', 'swallows', 'Halt', 'then', 'sun', 'south', 'right', 'get', 'ARTHUR', 'strand', ',', 'Pendragon', 'Where', 'minute', "'ve", 'through', 'grip', 'second', 'KING', 'You', 'wind', 'from', 'Patsy', 'goes', 'Found', 'temperate', '!', 'found', 'strangers', 'martin', 'Listen', 'them', 'other', 'velocity', 'agree', 'land', 'swallow', '--', 'me', 'not', 'That', 'who', 'warmer', "'d", 'where', 'forty-three', '...', 'bring', 'in', 'length', 'Oh', 'coconuts', 'wants', 'yeah', 'simple', 'here', ':', 'interested', 'air-speed', 'got', 'Uther', 'that', 'using', 'coconut', 'Britons', 'zone', 'my', 'but', 'all', 'They', 'have', 'Will', 'an', 'climes', 'am', 'Saxons', "'", 'carrying', 'tell', "'s", 'plover', 'order', 'SOLDIER', 'creeper', 'SCENE', 'Whoa', 'carried', 'winter', 'Supposing', 'together', 'question', 'to', 'maybe', 'course', 'you', 'under', 'clop', 'could', 'mean', 'are', 'bird', 'every', 'times', 'So', 'join', 'seek', 'A', 'go', 'tropical', 'Who', 'line', '.', 'there', 'husk', 'guiding', 'Yes', 'England', 'Pull', 'empty', 'What', 'just', '1', 'of', 'this', 'use', '#', 'court', 'it', 'on', 'ratios', '2', 'since', 'back', 'Ridden', 'Arthur', 'your', 'our', 'We', 'Mercea', 'is', 'why', 'must', "'m", 'do', 'son', 'feathers', 'breadth', 'Camelot', ']', 'may', 'or', 'In', 'carry', 'pound', 'horse', 'suggesting', 'defeator', 'halves', 'dorsal', 'a'}
```

#### More regex with re.search()

```python
# Search for the first occurrence of "coconuts" in scene_one: match
match = re.search(r"coconuts", scene_one)

# Print the start and end indexes of match
print(match.start(), match.end())
```

```bash
580 588
```

```python
# Write a regular expression to search for anything in square brackets: pattern1
pattern1 = r"\[.*\]"

# Use re.search to find the first text in square brackets
print(re.search(pattern1, scene_one))
```

```bash
<re.Match object; span=(9, 32), match='[wind] [clop clop clop]'>
```

```python
# Find the script notation at the beginning of the fourth sentence and print it
pattern2 = r"[\w\s]+:"
print(re.match(pattern2, sentences[3]))
```

### Advanced tokenization with NLTK and regex

#### Regex with NLTK tokenization

```bash
In [1]:
tweets
Out[1]:

['This is the best #nlp exercise ive found online! #python',
 '#NLP is super fun! <3 #learning',
 'Thanks @datacamp :) #nlp #python']
```

```python
# Import the necessary modules
from nltk.tokenize import regexp_tokenize
from nltk.tokenize import TweetTokenizer
# Define a regex pattern to find hashtags: pattern1
pattern1 = r"#\w+"
# Use the pattern on the first tweet in the tweets list
hashtags = regexp_tokenize(tweets[0], pattern1)
print(hashtags)
```

```bash
['#nlp', '#python']
```

```python
# Import the necessary modules
from nltk.tokenize import regexp_tokenize
from nltk.tokenize import TweetTokenizer
# Write a pattern that matches both mentions (@) and hashtags
pattern2 = r"([#|@]\w+)"
# Use the pattern on the last tweet in the tweets list
mentions_hashtags = regexp_tokenize(tweets[-1], pattern2)
print(mentions_hashtags)
```

```bash
['@datacamp', '#nlp', '#python']
```

```python
# Import the necessary modules
from nltk.tokenize import regexp_tokenize
from nltk.tokenize import TweetTokenizer
# Use the TweetTokenizer to tokenize all tweets into one list
tknzr = TweetTokenizer()
all_tokens = [tknzr.tokenize(t) for t in tweets]
print(all_tokens)
```

```bash
<script.py> output:
    [['This', 'is', 'the', 'best', '#nlp', 'exercise', 'ive', 'found', 'online', '!', '#python'], ['#NLP', 'is', 'super', 'fun', '!', '<3', '#learning'], ['Thanks', '@datacamp', ':)', '#nlp', '#python']]
```

#### Non-ascii tokenization

```python
# Tokenize and print all words in german_text
all_words = word_tokenize(german_text)
print(all_words)

# Tokenize and print only capital words
capital_words = r"[A-Z|Ü]\w+"
print(regexp_tokenize(german_text, capital_words))

# Tokenize and print only emoji
emoji = "['\U0001F300-\U0001F5FF'|'\U0001F600-\U0001F64F'|'\U0001F680-\U0001F6FF'|'\u2600-\u26FF\u2700-\u27BF']"
print(regexp_tokenize(german_text, emoji))
```

```bash
<script.py> output:
    ['Wann', 'gehen', 'wir', 'Pizza', 'essen', '?', '🍕', 'Und', 'fährst', 'du', 'mit', 'Über', '?', '🚕']
    ['Wann', 'Pizza', 'Und', 'Über']
    ['🍕', '🚕']
```

### Charting word length with NLTK

#### Charting practice

```python
# Split the script into lines: lines
lines = holy_grail.split('\n')

# Replace all script lines for speaker
pattern = "[A-Z]{2,}(\s)?(#\d)?([A-Z]{2,})?:"
lines = [re.sub(pattern, '', l) for l in lines]

# Tokenize each line: tokenized_lines
tokenized_lines = [regexp_tokenize(s, r"\w+") for s in lines]

# Make a frequency list of lengths: line_num_words
line_num_words = [len(t_line) for t_line in tokenized_lines]

# Plot a histogram of the line lengths
plt.hist(line_num_words)

# Show the plot
plt.show()
```

![]({{site.baseurl}}/images/nlp1.svg)

---
## Simple topic identification

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C2.pdf)

### Word counts with bag-of-words

#### Building a Counter with bag-of-words

```python
# Import Counter
from collections import Counter

# Tokenize the article: tokens
tokens = word_tokenize(article)

# Convert the tokens into lowercase: lower_tokens
lower_tokens = [t.lower() for t in tokens]

# Create a Counter with the lowercase tokens: bow_simple
bow_simple = Counter(lower_tokens)

# Print the 10 most common tokens
print(bow_simple.most_common(10))

```

```bash
<script.py> output:
    [(',', 151), ('the', 150), ('.', 89), ('of', 81), ("''", 66), ('to', 63), ('a', 60), ('``', 47), ('in', 44), ('and', 41)]
```

### Simple text preprocessing

#### Text preprocessing practice

```python
# Import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer

# Retain alphabetic words: alpha_only
alpha_only = [t for t in lower_tokens if t.isalpha()]

# Remove all stop words: no_stops
no_stops = [t for t in alpha_only if t not in english_stops]

# Instantiate the WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

# Lemmatize all tokens into a new list: lemmatized
lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]

# Create the bag-of-words: bow
bow = Counter(lemmatized)

# Print the 10 most common tokens
print(bow.most_common(10))

```

```bash
<script.py> output:
    [('debugging', 40), ('system', 25), ('bug', 17), ('software', 16), ('problem', 15), ('tool', 15), ('computer', 14), ('process', 13), ('term', 13), ('debugger', 13)]
```


### Introduction to gensim
### Tf-idf with gensim


---
## Named-entity recognition

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C3.pdf)

### Named Entity Recognition
### Introduction to SpaCy
### Multilingual NER with polyglot


---
## Building a "fake news" classifier

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C4.pdf)

### Classifying fake news using supervised learning with NLP
### Building word count vectors with scikit-learn
### Training and testing a classification model with scikit-learn
### Simple NLP, complex problems


