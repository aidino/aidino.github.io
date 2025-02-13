---
layout: post
title: "Introduction to Natural Language Processing in Python"
date: 2025-01-20 14:00:00 +0700
categories: machine learning in python
---

In this course, you'll learn natural language processing (NLP) basics, such as how to identify and separate words, how to extract topics in a text, and how to build your own fake news classifier. You'll also learn how to use basic libraries such as NLTK, alongside libraries which utilize deep learning to solve common NLP problems. This course will give you the foundation to process and parse text as you move forward in your Python learning.

### Table of contents

1. [Regular expressions & word tokenization](#Regularexpressionswordtokenization)
	* 1.1. [Introduction to regular expressions](#Introductiontoregularexpressions)
		* 1.1.1. [Practicing regular expressions: `re.split()` and `re.findall()`](#Practicingregularexpressions:re.splitandre.findall)
	* 1.2. [Introduction to tokenization](#Introductiontotokenization)
		* 1.2.1. [Word tokenization with NLTK](#WordtokenizationwithNLTK)
		* 1.2.2. [More regex with re.search()](#Moreregexwithre.search)
	* 1.3. [Advanced tokenization with NLTK and regex](#AdvancedtokenizationwithNLTKandregex)
		* 1.3.1. [Regex with NLTK tokenization](#RegexwithNLTKtokenization)
		* 1.3.2. [Non-ascii tokenization](#Non-asciitokenization)
	* 1.4. [Charting word length with NLTK](#ChartingwordlengthwithNLTK)
		* 1.4.1. [Charting practice](#Chartingpractice)
2. [Simple topic identification](#Simpletopicidentification)
	* 2.1. [Word counts with bag-of-words](#Wordcountswithbag-of-words)
		* 2.1.1. [Building a Counter with bag-of-words](#BuildingaCounterwithbag-of-words)
	* 2.2. [Simple text preprocessing](#Simpletextpreprocessing)
		* 2.2.1. [Text preprocessing practice](#Textpreprocessingpractice)
	* 2.3. [Introduction to gensim](#Introductiontogensim)
		* 2.3.1. [Creating and querying a corpus with gensim](#Creatingandqueryingacorpuswithgensim)
		* 2.3.2. [Gensim bag-of-words](#Gensimbag-of-words)
	* 2.4. [Tf-idf with gensim](#Tf-idfwithgensim)
		* 2.4.1. [Tf-idf with Wikipedia](#Tf-idfwithWikipedia)
3. [Named-entity recognition](#Named-entityrecognition)
	* 3.1. [Named Entity Recognition](#NamedEntityRecognition)
		* 3.1.1. [NER with NLTK](#NERwithNLTK)
		* 3.1.2. [Charting practice](#Chartingpractice-1)
	* 3.2. [Introduction to SpaCy](#IntroductiontoSpaCy)
		* 3.2.1. [Comparing NLTK with spaCy NER](#ComparingNLTKwithspaCyNER)
	* 3.3. [Multilingual NER with polyglot](#MultilingualNERwithpolyglot)
		* 3.3.1. [French NER with polyglot I](#FrenchNERwithpolyglotI)
		* 3.3.2. [French NER with polyglot II](#FrenchNERwithpolyglotII)
4. [Building a "fake news" classifier](#Buildingafakenewsclassifier)
	* 4.1. [Building word count vectors with scikit-learn](#Buildingwordcountvectorswithscikit-learn)
		* 4.1.1. [CountVectorizer for text classification](#CountVectorizerfortextclassification)
		* 4.1.2. [TfidfVectorizer for text classification](#TfidfVectorizerfortextclassification)
		* 4.1.3. [Inspecting the vectors](#Inspectingthevectors)
	* 4.2. [Training and testing a classification model with scikit-learn](#Trainingandtestingaclassificationmodelwithscikit-learn)
		* 4.2.1. [Training and testing the "fake news" model with CountVectorizer](#TrainingandtestingthefakenewsmodelwithCountVectorizer)
		* 4.2.2. [Training and testing the "fake news" model with TfidfVectorizer](#TrainingandtestingthefakenewsmodelwithTfidfVectorizer)
	* 4.3. [Simple NLP, complex problems](#SimpleNLPcomplexproblems)
		* 4.3.1. [Improving your model](#Improvingyourmodel)
		* 4.3.2. [Inspecting your model](#Inspectingyourmodel)


---
##  1. <a name='Regularexpressionswordtokenization'></a>Regular expressions & word tokenization

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C1.pdf)

###  1.1. <a name='Introductiontoregularexpressions'></a>Introduction to regular expressions

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

####  1.1.1. <a name='Practicingregularexpressions:re.splitandre.findall'></a>Practicing regular expressions: `re.split()` and `re.findall()`

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

###  1.2. <a name='Introductiontotokenization'></a>Introduction to tokenization

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

####  1.2.1. <a name='WordtokenizationwithNLTK'></a>Word tokenization with NLTK

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

####  1.2.2. <a name='Moreregexwithre.search'></a>More regex with re.search()

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

###  1.3. <a name='AdvancedtokenizationwithNLTKandregex'></a>Advanced tokenization with NLTK and regex

####  1.3.1. <a name='RegexwithNLTKtokenization'></a>Regex with NLTK tokenization

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

####  1.3.2. <a name='Non-asciitokenization'></a>Non-ascii tokenization

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

###  1.4. <a name='ChartingwordlengthwithNLTK'></a>Charting word length with NLTK

####  1.4.1. <a name='Chartingpractice'></a>Charting practice

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
##  2. <a name='Simpletopicidentification'></a>Simple topic identification

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C2.pdf)

###  2.1. <a name='Wordcountswithbag-of-words'></a>Word counts with bag-of-words

####  2.1.1. <a name='BuildingaCounterwithbag-of-words'></a>Building a Counter with bag-of-words

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

###  2.2. <a name='Simpletextpreprocessing'></a>Simple text preprocessing

####  2.2.1. <a name='Textpreprocessingpractice'></a>Text preprocessing practice

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

###  2.3. <a name='Introductiontogensim'></a>Introduction to gensim

####  2.3.1. <a name='Creatingandqueryingacorpuswithgensim'></a>Creating and querying a corpus with gensim

```python
# Import Dictionary
from gensim.corpora.dictionary import Dictionary 

# Create a Dictionary from the articles: dictionary
dictionary = Dictionary(articles)

# Select the id for "computer": computer_id
computer_id = dictionary.token2id.get("computer")

# Use computer_id with the dictionary to print the word
print(dictionary.get(computer_id))

# Create a MmCorpus: corpus
corpus = [dictionary.doc2bow(article) for article in articles]

# Print the first 10 word ids with their frequency counts from the fifth document
print(corpus[4][:10])

```

```bash
<script.py> output:
    computer
    [(0, 85), (8, 11), (10, 2), (25, 1), (27, 2), (41, 33), (42, 1), (43, 1), (44, 1), (45, 3)]
```

####  2.3.2. <a name='Gensimbag-of-words'></a>Gensim bag-of-words

```python
# Save the fifth document: doc
doc = corpus[4]

# Sort the doc for frequency: bow_doc
bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)

# Print the top 5 words of the document alongside the count
for word_id, word_count in bow_doc[:5]:
    print(dictionary.get(word_id), word_count)
    
# Create the defaultdict: total_word_count
total_word_count = defaultdict(int)
for word_id, word_count in itertools.chain.from_iterable(corpus):
    total_word_count[word_id] += word_count

# print(total_word_count)

# Create a sorted list from the defaultdict: sorted_word_count
sorted_word_count = sorted(total_word_count.items(), key=lambda w: w[1], reverse=True) 

# Print the top 5 words across all documents alongside the count
for word_id, word_count in sorted_word_count[:5]:
    print(dictionary.get(word_id), word_count)
```

```bash
<script.py> output:
    engineering 91
    '' 85
    reverse 73
    software 51
    `` 33
    '' 1006
    computer 598
    `` 555
    software 450
    cite 322
```


###  2.4. <a name='Tf-idfwithgensim'></a>Tf-idf with gensim

####  2.4.1. <a name='Tf-idfwithWikipedia'></a>Tf-idf with Wikipedia

```python
from gensim.models.tfidfmodel import TfidfModel

# Create a new TfidfModel using the corpus: tfidf
tfidf = TfidfModel(corpus)

# Calculate the tfidf weights of doc: tfidf_weights
tfidf_weights = tfidf[doc]

# Print the first five weights
print(tfidf_weights[:5])

# Sort the weights from highest to lowest: sorted_tfidf_weights
sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)

# Print the top 5 weighted words
for term_id, weight in sorted_tfidf_weights[:5]:
    print(dictionary.get(term_id), weight)
```

```bash
[(10, 0.0022676967632877364), (25, 0.004310646654948723), (27, 0.008621293309897447), (42, 0.0054444950365925915), (43, 0.004310646654948723)]
reverse 0.4987515710425556
infringement 0.1854420793422032
engineering 0.16280628072296138
interoperability 0.12362805289480211
reverse-engineered 0.12362805289480211
```

---
##  3. <a name='Named-entityrecognition'></a>Named-entity recognition

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C3.pdf)

###  3.1. <a name='NamedEntityRecognition'></a>Named Entity Recognition

####  3.1.1. <a name='NERwithNLTK'></a>NER with NLTK

```python
# Tokenize the article into sentences: sentences
sentences = sent_tokenize(article)

# Tokenize each sentence into words: token_sentences
token_sentences = [word_tokenize(sent) for sent in sentences]

# Tag each tokenized sentence into parts of speech: pos_sentences
pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences] 

# Create the named entity chunks: chunked_sentences
chunked_sentences = nltk.ne_chunk_sents(pos_sentences, binary=True)

# Test for stems of the tree with 'NE' tags
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, "label") and chunk.label() == "NE":
            print(chunk)

```

```bash
<script.py> output:
    (NE Uber/NNP)
    (NE Beyond/NN)
    (NE Apple/NNP)
    (NE Uber/NNP)
    (NE Uber/NNP)
    (NE Travis/NNP Kalanick/NNP)
    (NE Tim/NNP Cook/NNP)
    (NE Apple/NNP)
    (NE Silicon/NNP Valley/NNP)
    (NE CEO/NNP)
    (NE Yahoo/NNP)
    (NE Marissa/NNP Mayer/NNP)
```

####  3.1.2. <a name='Chartingpractice-1'></a>Charting practice

```python
# Create the defaultdict: ner_categories
ner_categories = defaultdict(int)

# Create the nested for loop
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, 'label'):
            ner_categories[chunk.label()] += 1
            
# Create a list from the dictionary keys for the chart labels: labels
labels = list(ner_categories.keys())

# Create a list of the values: values
values = [ner_categories.get(v) for v in labels]

# Create the pie chart
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

# Display the chart
plt.show()
```

![]({{site.baseurl}}/images/nlp2.svg)

###  3.2. <a name='IntroductiontoSpaCy'></a>Introduction to SpaCy

####  3.2.1. <a name='ComparingNLTKwithspaCyNER'></a>Comparing NLTK with spaCy NER

```python
# Import spacy
import spacy

# Instantiate the English model: nlp
nlp = spacy.load('en_core_web_sm', disable=['tagger', 'parser', 'matcher'])

# Create a new document: doc
doc = nlp(article)

# Print all of the found entities and their labels
for ent in doc.ents:
    print(ent.label_, ent.text)

```

```bash
ORG Apple
PERSON Travis Kalanick of Uber
PERSON Tim Cook
ORG Apple
CARDINAL Millions
LOC Silicon Valley
ORG Yahoo
PERSON Marissa Mayer
MONEY 186
```

###  3.3. <a name='MultilingualNERwithpolyglot'></a>Multilingual NER with polyglot

####  3.3.1. <a name='FrenchNERwithpolyglotI'></a>French NER with polyglot I

```python
from polyglot.text import Text

# Create a new text object using Polyglot's Text class: txt
txt = Text(article)

# Print each of the entities found
for ent in txt.entities:
    print(ent)
# Print the type of ent
print(type(ent))

```

```bash
<script.py> output:
    ['Charles', 'Cuvelliez']
    ['Charles', 'Cuvelliez']
    ['Bruxelles']
    ['l’IA']
    ['Julien', 'Maldonato']
    ['Deloitte']
    ['Ethiquement']
    ['l’IA']
    ['.']
    <class 'polyglot.text.Chunk'>
```

####  3.3.2. <a name='FrenchNERwithpolyglotII'></a>French NER with polyglot II

```python
# Create the list of tuples: entities
entities = [(ent.tag, ' '.join(ent)) for ent in txt.entities]

# Print entities
print(entities)

```

```bash
<script.py> output:
    [('I-PER', 'Charles Cuvelliez'), ('I-PER', 'Charles Cuvelliez'), ('I-ORG', 'Bruxelles'), ('I-PER', 'l’IA'), ('I-PER', 'Julien Maldonato'), ('I-ORG', 'Deloitte'), ('I-PER', 'Ethiquement'), ('I-LOC', 'l’IA'), ('I-PER', '.')]
```

---
##  4. <a name='Buildingafakenewsclassifier'></a>Building a "fake news" classifier

[Slide]({{site.baseurl}}/files/Introduction_to_Natural_Language_Processing_in_Python_C4.pdf)

###  4.1. <a name='Buildingwordcountvectorswithscikit-learn'></a>Building word count vectors with scikit-learn

####  4.1.1. <a name='CountVectorizerfortextclassification'></a>CountVectorizer for text classification

```python
# Import the necessary modules
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# Print the head of df
print(df.head())

# Create a series to store the labels: y
y = df['label']

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)

# Initialize a CountVectorizer object: count_vectorizer
count_vectorizer = CountVectorizer(stop_words="english")

# Transform the training data using only the 'text' column values: count_train 
count_train = count_vectorizer.fit_transform(X_train)

# Transform the test data using only the 'text' column values: count_test 
count_test = count_vectorizer.transform(X_test)

# Print the first 10 features of the count_vectorizer
print(count_vectorizer.get_feature_names()[:10])
```

```bash
['00', '000', '0000', '00000031', '000035', '00006', '0001', '0001pt', '000ft', '000km']
```

####  4.1.2. <a name='TfidfVectorizerfortextclassification'></a>TfidfVectorizer for text classification

```python
# Import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize a TfidfVectorizer object: tfidf_vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)

# Transform the training data: tfidf_train 
tfidf_train = tfidf_vectorizer.fit_transform(X_train)

# Transform the test data: tfidf_test 
tfidf_test = tfidf_vectorizer.transform(X_test)

# Print the first 10 features
print(tfidf_vectorizer.get_feature_names()[:10])

# Print the first 5 vectors of the tfidf training data
print(tfidf_train.A[:5])

```

```bash
<script.py> output:
    ['00', '000', '001', '008s', '00am', '00pm', '01', '01am', '02', '024']
    [[0.         0.01928563 0.         ... 0.         0.         0.        ]
     [0.         0.         0.         ... 0.         0.         0.        ]
     [0.         0.02895055 0.         ... 0.         0.         0.        ]
     [0.         0.03056734 0.         ... 0.         0.         0.        ]
     [0.         0.         0.         ... 0.         0.         0.        ]]
```

####  4.1.3. <a name='Inspectingthevectors'></a>Inspecting the vectors

```python
# Create the CountVectorizer DataFrame: count_df
count_df = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())

# Create the TfidfVectorizer DataFrame: tfidf_df
tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vectorizer.get_feature_names())

# Print the head of count_df
print(count_df.head())

# Print the head of tfidf_df
print(tfidf_df.head())

# Calculate the difference in columns: difference
difference = set(count_df.columns) - set(tfidf_df.columns)
print(difference)

# Check whether the DataFrames are equal
print(count_df.equals(tfidf_df))

```

```bash
<script.py> output:
       000  00am  0600  10  100  ...  yuan  zawahiri  zeitung  zero  zerohedge
    0    0     0     0   0    0  ...     0         0        0     1          0
    1    0     0     0   3    0  ...     0         0        0     0          0
    2    0     0     0   0    0  ...     0         0        0     0          0
    3    0     0     0   0    0  ...     0         0        0     0          0
    4    0     0     0   0    0  ...     0         0        0     0          0
    
    [5 rows x 5111 columns]
       000  00am  0600     10  100  ...  yuan  zawahiri  zeitung   zero  zerohedge
    0  0.0   0.0   0.0  0.000  0.0  ...   0.0       0.0      0.0  0.034        0.0
    1  0.0   0.0   0.0  0.106  0.0  ...   0.0       0.0      0.0  0.000        0.0
    2  0.0   0.0   0.0  0.000  0.0  ...   0.0       0.0      0.0  0.000        0.0
    3  0.0   0.0   0.0  0.000  0.0  ...   0.0       0.0      0.0  0.000        0.0
    4  0.0   0.0   0.0  0.000  0.0  ...   0.0       0.0      0.0  0.000        0.0
    
    [5 rows x 5111 columns]
    set()
    False

```

###  4.2. <a name='Trainingandtestingaclassificationmodelwithscikit-learn'></a>Training and testing a classification model with scikit-learn

####  4.2.1. <a name='TrainingandtestingthefakenewsmodelwithCountVectorizer'></a>Training and testing the "fake news" model with CountVectorizer

```python
# Import the necessary modules
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB

# Instantiate a Multinomial Naive Bayes classifier: nb_classifier
nb_classifier = MultinomialNB()

# Fit the classifier to the training data
nb_classifier.fit(count_train, y_train)

# Create the predicted tags: pred
pred = nb_classifier.predict(count_test)

# Calculate the accuracy score: score
score = metrics.accuracy_score(y_test, pred)
print(score)

# Calculate the confusion matrix: cm
cm = metrics.confusion_matrix(y_test, pred, labels=['FAKE', 'REAL'])
print(cm)

```

```bash
<script.py> output:
    0.893352462936394
    [[ 865  143]
     [  80 1003]]
```

####  4.2.2. <a name='TrainingandtestingthefakenewsmodelwithTfidfVectorizer'></a>Training and testing the "fake news" model with TfidfVectorizer

```python 
# Create a Multinomial Naive Bayes classifier: nb_classifier
nb_classifier = MultinomialNB()

# Fit the classifier to the training data
nb_classifier.fit(tfidf_train, y_train)

# Create the predicted tags: pred
pred = nb_classifier.predict(tfidf_test)

# Calculate the accuracy score: score
score = metrics.accuracy_score(y_test, pred)
print(score)

# Calculate the confusion matrix: cm
cm = metrics.confusion_matrix(y_test, pred, labels=["FAKE", "REAL"])
print(cm)

```

```bash
<script.py> output:
    0.8565279770444764
    [[ 739  269]
     [  31 1052]]
```
 
###  4.3. <a name='SimpleNLPcomplexproblems'></a>Simple NLP, complex problems

####  4.3.1. <a name='Improvingyourmodel'></a>Improving your model

```python
# Create the list of alphas: alphas
alphas = np.arange(0, 1, 0.1)

# Define train_and_predict()
def train_and_predict(alpha):
    # Instantiate the classifier: nb_classifier
    nb_classifier = MultinomialNB(alpha=alpha)
    # Fit to the training data
    nb_classifier.fit(tfidf_train, y_train)
    # Predict the labels: pred
    pred = nb_classifier.predict(tfidf_test)
    # Compute accuracy: score
    score = metrics.accuracy_score(y_test, pred)
    return score

# Iterate over the alphas and print the corresponding score
for alpha in alphas:
    print('Alpha: ', alpha)
    print('Score: ', train_and_predict(alpha))
    print()

```


```bash
<script.py> output:
    Alpha:  0.0
    Score:  0.8813964610234337
    
    Alpha:  0.1
    Score:  0.8976566236250598
    
    Alpha:  0.2
    Score:  0.8938307030129125
    
    Alpha:  0.30000000000000004
    Score:  0.8900047824007652
    
    Alpha:  0.4
    Score:  0.8857006217120995
    
    Alpha:  0.5
    Score:  0.8842659014825442
    
    Alpha:  0.6000000000000001
    Score:  0.874701099952176
    
    Alpha:  0.7000000000000001
    Score:  0.8703969392635102
    
    Alpha:  0.8
    Score:  0.8660927785748446
    
    Alpha:  0.9
    Score:  0.8589191774270684
```

####  4.3.2. <a name='Inspectingyourmodel'></a>Inspecting your model

```python
# Get the class labels: class_labels
class_labels = nb_classifier.classes_

# Extract the features: feature_names
feature_names = tfidf_vectorizer.get_feature_names()

# Zip the feature names together with the coefficient array and sort by weights: feat_with_weights
feat_with_weights = sorted(zip(nb_classifier.coef_[0], feature_names))

# Print the first class label and the top 20 feat_with_weights entries
print(class_labels[0], feat_with_weights[:20])

# Print the second class label and the bottom 20 feat_with_weights entries
print(class_labels[1], feat_with_weights[-20:])

```

```bash
<script.py> output:
    FAKE [(-12.641778440826338, '0000'), (-12.641778440826338, '000035'), (-12.641778440826338, '0001'), (-12.641778440826338, '0001pt'), (-12.641778440826338, '000km'), (-12.641778440826338, '0011'), (-12.641778440826338, '006s'), (-12.641778440826338, '007'), (-12.641778440826338, '007s'), (-12.641778440826338, '008s'), (-12.641778440826338, '0099'), (-12.641778440826338, '00am'), (-12.641778440826338, '00p'), (-12.641778440826338, '00pm'), (-12.641778440826338, '014'), (-12.641778440826338, '015'), (-12.641778440826338, '018'), (-12.641778440826338, '01am'), (-12.641778440826338, '020'), (-12.641778440826338, '023')]
    REAL [(-6.790929954967984, 'states'), (-6.765360557845787, 'rubio'), (-6.751044290367751, 'voters'), (-6.701050756752027, 'house'), (-6.695547793099875, 'republicans'), (-6.670191249042969, 'bush'), (-6.661945235816139, 'percent'), (-6.589623788689861, 'people'), (-6.559670340096453, 'new'), (-6.489892292073902, 'party'), (-6.452319082422527, 'cruz'), (-6.452076515575875, 'state'), (-6.397696648238072, 'republican'), (-6.376343060363355, 'campaign'), (-6.324397735392007, 'president'), (-6.2546017970213645, 'sanders'), (-6.144621899738043, 'obama'), (-5.756817248152807, 'clinton'), (-5.596085785733112, 'said'), (-5.357523914504495, 'trump')]
```