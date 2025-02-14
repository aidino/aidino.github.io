---
layout: post
title: "Natural Language Processing with spaCy"
date: 2025-01-20 15:00:00 +0700
categories: machine learning in python
---



Learn spaCy, the fast-growing industry-standard NLP library, for tasks like tokenization, parsing, and named entity recognition. Master core operations, use classes like Doc and Token, and train models. Extract terms with pattern matching, create custom pipeline components, and handle real-world examples for your NLP projects.

### Table of contents

1. [Introduction to NLP and spaCy](#IntroductiontoNLPandspaCy)
	* 1.1. [Natural Language Processing (NLP) basics](#NaturalLanguageProcessingNLPbasics)
		* 1.1.1. [Doc container in spaCy](#DoccontainerinspaCy)
	* 1.2. [spaCy basics](#spaCybasics)
		* 1.2.1. [Running a spaCy pipeline](#RunningaspaCypipeline)
		* 1.2.2. [Lemmatization with spaCy](#LemmatizationwithspaCy)
		* 1.2.3. [Sentence segmentation with spaCy](#SentencesegmentationwithspaCy)
	* 1.3. [Linguistic features in spaCy](#LinguisticfeaturesinspaCy)
		* 1.3.1. [POS tagging with spaCy](#POStaggingwithspaCy)
		* 1.3.2. [NER with spaCy](#NERwithspaCy)
		* 1.3.3. [Text processing with spaCy](#TextprocessingwithspaCy)
2. [spaCy Linguistic Annotations and Word Vectors](#spaCyLinguisticAnnotationsandWordVectors)
	* 2.1. [Linguistic features](#Linguisticfeatures)
		* 2.1.1. [Word-sense disambiguation with spaCy](#Word-sensedisambiguationwithspaCy)
		* 2.1.2. [Dependency parsing with spaCy](#DependencyparsingwithspaCy)
	* 2.2. [Introduction to word vectors](#Introductiontowordvectors)
		* 2.2.1. [spaCy vocabulary](#spaCyvocabulary)
		* 2.2.2. [Word vectors in spaCy vocabulary](#WordvectorsinspaCyvocabulary)
	* 2.3. [Word vectors and spaCy](#WordvectorsandspaCy)
		* 2.3.1. [Word vectors projection](#Wordvectorsprojection)
		* 2.3.2. [Similar words in a vocabulary](#Similarwordsinavocabulary)
	* 2.4. [Measuring semantic similarity with spaCy](#MeasuringsemanticsimilaritywithspaCy)
		* 2.4.1. [Doc similarity with spaCy](#DocsimilaritywithspaCy)
		* 2.4.2. [Span similarity with spaCy](#SpansimilaritywithspaCy)
		* 2.4.3. [Semantic similarity for categorizing text](#Semanticsimilarityforcategorizingtext)
3. [Data Analysis with spaCy](#DataAnalysiswithspaCy)
	* 3.1. [spaCy pipelines](#spaCypipelines)
		* 3.1.1. [Analyzing pipelines in spaCy](#AnalyzingpipelinesinspaCy)
	* 3.2. [spaCy EntityRuler](#spaCyEntityRuler)
		* 3.2.1. [EntityRuler with blank spaCy model](#EntityRulerwithblankspaCymodel)
		* 3.2.2. [EntityRuler for NER](#EntityRulerforNER)
		* 3.2.3. [EntityRuler with multi-patterns in spaCy](#EntityRulerwithmulti-patternsinspaCy)
	* 3.3. [RegEx with spaCy](#RegExwithspaCy)
		* 3.3.1. [RegEx in Python](#RegExinPython)
		* 3.3.2. [RegEx with EntityRuler in spaCy](#RegExwithEntityRulerinspaCy)
	* 3.4. [spaCy Matcher and PhraseMatcher](#spaCyMatcherandPhraseMatcher)
		* 3.4.1. [Matching a single term in spaCy](#MatchingasingleterminspaCy)
		* 3.4.2. [PhraseMatcher in spaCy](#PhraseMatcherinspaCy)
		* 3.4.3. [Matching with extended syntax in spaCy](#MatchingwithextendedsyntaxinspaCy)
4. [Customizing spaCy Models](#CustomizingspaCyModels)
	* 4.1. [Customizing spaCy models](#CustomizingspaCymodels)
		* 4.1.1. [Model performance on your data](#Modelperformanceonyourdata)
	* 4.2. [spaCy training data format](#spaCytrainingdataformat)
		* 4.2.1. [Annotation and preparing training data](#Annotationandpreparingtrainingdata)
		* 4.2.2. [Compatible training data](#Compatibletrainingdata)
	* 4.3. [Training with spaCy](#TrainingwithspaCy)
		* 4.3.1. [Training preparation steps](#Trainingpreparationsteps)
		* 4.3.2. [Train an existing NER model](#TrainanexistingNERmodel)
		* 4.3.3. [Training a spaCy model from scratch](#TrainingaspaCymodelfromscratch)

---
##  1. <a name='IntroductiontoNLPandspaCy'></a>Introduction to NLP and spaCy

[Slide]({{site.baseurl}}/files/Natural_Language_Processing_with_spaCy_C1.pdf)

###  1.1. <a name='NaturalLanguageProcessingNLPbasics'></a>Natural Language Processing (NLP) basics

####  1.1.1. <a name='DoccontainerinspaCy'></a>Doc container in spaCy

```python
import spacy

text = 'NLP is becoming increasingly popular for providing business solutions.'

# Load en_core_web_sm and create an nlp object
nlp = spacy.load('en_core_web_sm')

# Create a Doc container for the text object
doc = nlp(text)

# Create a list containing the text of each token in the Doc container
print([token.text for token in doc])
```

```bash
<script.py> output:
    ['NLP', 'is', 'becoming', 'increasingly', 'popular', 'for', 'providing', 'business', 'solutions', '.']
```

###  1.2. <a name='spaCybasics'></a>spaCy basics

####  1.2.1. <a name='RunningaspaCypipeline'></a>Running a spaCy pipeline

```python
# Load en_core_web_sm model as nlp
nlp = spacy.load('en_core_web_sm')

# Run an nlp model on each item of texts and append the Doc container to documents
documents = []
for text in texts:
  documents.append(nlp(text))
  
# Print the token texts for each Doc container
for doc in documents:
  print([token.text for token in doc])
```

```bash
<script.py> output:
    ['A', 'loaded', 'spaCy', 'model', 'can', 'be', 'used', 'to', 'compile', 'documents', 'list', '!']
    ['Tokenization', 'is', 'the', 'first', 'step', 'in', 'any', 'spacy', 'pipeline', '.']
```

####  1.2.2. <a name='LemmatizationwithspaCy'></a>Lemmatization with spaCy

```python
document = nlp(text)
tokens = [token.text for token in document]

# Append the lemma for all tokens in the document
lemmas = [token.lemma_ for token in document]
print("Lemmas:\n", lemmas, "\n")

# Print tokens and compare with lemmas list
print("Tokens:\n", tokens)
```

```bash
<script.py> output:
    Lemmas:
     ['I', 'have', 'buy', 'several', 'of', 'the', 'vitality', 'can', 'dog', 'food', 'product', 'and', 'have', 'find', 'they', 'all', 'to', 'be', 'of', 'good', 'quality', '.', 'the', 'product', 'look', 'more', 'like', 'a', 'stew', 'than', 'a', 'process', 'meat', 'and', 'it', 'smell', 'well', '.', 'my', 'Labrador', 'be', 'finicky', 'and', 'she', 'appreciate', 'this', 'product', 'well', 'than', ' ', 'most', '.'] 
    
    Tokens:
     ['I', 'have', 'bought', 'several', 'of', 'the', 'Vitality', 'canned', 'dog', 'food', 'products', 'and', 'have', 'found', 'them', 'all', 'to', 'be', 'of', 'good', 'quality', '.', 'The', 'product', 'looks', 'more', 'like', 'a', 'stew', 'than', 'a', 'processed', 'meat', 'and', 'it', 'smells', 'better', '.', 'My', 'Labrador', 'is', 'finicky', 'and', 'she', 'appreciates', 'this', 'product', 'better', 'than', ' ', 'most', '.']
```

####  1.2.3. <a name='SentencesegmentationwithspaCy'></a>Sentence segmentation with spaCy

```python
# Generating a documents list of all Doc containers
documents = [nlp(text) for text in texts]

# Iterate through documents and append sentences in each doc to the sentences list
sentences = []
for doc in documents:
  sentences.append([s for s in doc.sents])
  
# Find number of sentences per each doc container
print([len(s) for s in sentences])
```

```bash
<script.py> output:
    [3, 3, 8, 3, 4, 5, 5, 5, 3, 4]
```

###  1.3. <a name='LinguisticfeaturesinspaCy'></a>Linguistic features in spaCy

####  1.3.1. <a name='POStaggingwithspaCy'></a>POS tagging with spaCy

```python
# Compile a list of all Doc containers of texts
documents = [nlp(text) for text in texts]

# Print token texts and POS tags for each Doc container
for doc in documents:
    for token in doc:
        print("Text: ", token.text, "| POS tag: ", token.pos_)
    print("\n")
```

```bash
<script.py> output:
    Text:  What | POS tag:  PRON
    Text:  is | POS tag:  AUX
    Text:  the | POS tag:  DET
    Text:  arrival | POS tag:  NOUN
    Text:  time | POS tag:  NOUN
    Text:  in | POS tag:  ADP
    Text:  San | POS tag:  PROPN
    Text:  francisco | POS tag:  PROPN
    Text:  for | POS tag:  ADP
    Text:  the | POS tag:  DET
    Text:  7:55 | POS tag:  NUM
    Text:  AM | POS tag:  NOUN
    Text:  flight | POS tag:  NOUN
    Text:  leaving | POS tag:  VERB
    Text:  Washington | POS tag:  PROPN
    Text:  ? | POS tag:  PUNCT
    
    
    Text:  Cheapest | POS tag:  PROPN
    Text:  airfare | POS tag:  ADJ
    Text:  from | POS tag:  ADP
    Text:  Tacoma | POS tag:  PROPN
    Text:  to | POS tag:  ADP
    Text:  Orlando | POS tag:  PROPN
    Text:  is | POS tag:  AUX
    Text:  650 | POS tag:  NUM
    Text:  dollars | POS tag:  NOUN
    Text:  . | POS tag:  PUNCT
    
    
    Text:  Round | POS tag:  ADJ
    Text:  trip | POS tag:  NOUN
    Text:  fares | POS tag:  NOUN
    Text:  from | POS tag:  ADP
    Text:  Pittsburgh | POS tag:  PROPN
    Text:  to | POS tag:  ADP
    Text:  Philadelphia | POS tag:  PROPN
    Text:  are | POS tag:  AUX
    Text:  under | POS tag:  ADP
    Text:  1000 | POS tag:  NUM
    Text:  dollars | POS tag:  NOUN
    Text:  ! | POS tag:  PUNCT
```

####  1.3.2. <a name='NERwithspaCy'></a>NER with spaCy

```python
# Compile a list of all Doc containers of texts
documents = [nlp(text) for text in texts]

# Print the entity text and label for the entities in each document
for doc in documents:
    print([(ent.text, ent.label_) for ent in doc.ents])
    
# Print the 6th token's text and entity type of the second document
print("\nText:", documents[1][5].text, "| Entity type: ", documents[1][5].ent_type_)
```

```bash
<script.py> output:
    [('Boston', 'GPE'), ('8:38 am', 'TIME'), ('Denver', 'GPE'), ('11:10 in the morning', 'TIME')]
    [('Pittsburgh', 'GPE'), ('Baltimore', 'GPE'), ('Thursday', 'DATE'), ('morning', 'TIME')]
    [('San francisco', 'GPE'), ('Washington', 'GPE')]
    
    Text: Pittsburgh | Entity type:  GPE
```

####  1.3.3. <a name='TextprocessingwithspaCy'></a>Text processing with spaCy

![]({{site.baseurl}}/images/spacy_convention.jpeg)

```python
# Create a list to store sentences of each Doc container in documents
sentences = [[sent for sent in doc.sents] for doc in documents]

# Create a list to track number of sentences per Doc container in documents
num_sentences = [len([sent for sent in doc.sents]) for doc in documents]
print("Number of sentences in documents:\n", num_sentences, "\n")

# Record entities text and corresponding label of the third Doc container
third_text_entities = [(ent.text, ent.label_) for ent in documents[2].ents]
print("Third text entities:\n", third_text_entities, "\n")

# Record first ten tokens and corresponding POS tag for the third Doc container
third_text_10_pos = [(token.text, token.pos_) for token in documents[2]][:10]
print("First ten tokens of third text:\n", third_text_10_pos)
```

```bash
<script.py> output:
    Number of sentences in documents:
     [3, 3, 8, 3, 4] 
    
    Third text entities:
     [('around a few centuries', 'DATE'), ('gelatin', 'ORG'), ("C.S. Lewis'", 'ORG'), ('The Lion, The Witch', 'WORK_OF_ART'), ('Edmund', 'WORK_OF_ART'), ('Witch', 'ORG')] 
    
    First ten tokens of third text:
     [('This', 'DET'), ('is', 'AUX'), ('a', 'DET'), ('confection', 'NOUN'), ('that', 'DET'), ('has', 'AUX'), ('been', 'VERB'), ('around', 'ADV'), ('a', 'DET'), ('few', 'ADJ')]
```

---
##  2. <a name='spaCyLinguisticAnnotationsandWordVectors'></a>spaCy Linguistic Annotations and Word Vectors

[Slide]({{site.baseurl}}/files/Natural_Language_Processing_with_spaCy_C2.pdf)


###  2.1. <a name='Linguisticfeatures'></a>Linguistic features

####  2.1.1. <a name='Word-sensedisambiguationwithspaCy'></a>Word-sense disambiguation with spaCy

```python
texts = ["This device is used to jam the signal.",
         "I am stuck in a traffic jam"]

# Create a list of Doc containers in the texts list
documents = [nlp(t) for t in texts]

# Print a token's text and POS tag if the word jam is in the token's text
for i, doc in enumerate(documents):
    print(f"Sentence {i+1}: ", [(token.text, token.pos_) for token in doc if "jam" in token.text], "\n")
```

```bash
Sentence 1:  [('jam', 'VERB')] 

Sentence 2:  [('jam', 'NOUN')] 
```

####  2.1.2. <a name='DependencyparsingwithspaCy'></a>Dependency parsing with spaCy

```python
# Create a list of Doc containts of texts list
documents = [nlp(t) for t in texts]

# Print each token's text, dependency label and its explanation
for doc in documents:
    print([(token.text, token.dep_, spacy.explain(token.dep_)) for token in doc], "\n")
```

```bash
<script.py> output:
    [('I', 'nsubj', 'nominal subject'), ('want', 'ROOT', None), ('to', 'aux', 'auxiliary'), ('fly', 'xcomp', 'open clausal complement'), ('from', 'prep', 'prepositional modifier'), ('Boston', 'pobj', 'object of preposition'), ('at', 'prep', 'prepositional modifier'), ('8:38', 'nummod', 'numeric modifier'), ('am', 'pobj', 'object of preposition'), ('and', 'cc', 'coordinating conjunction'), ('arrive', 'conj', 'conjunct'), ('in', 'prep', 'prepositional modifier'), ('Denver', 'pobj', 'object of preposition'), ('at', 'prep', 'prepositional modifier'), ('11:10', 'pobj', 'object of preposition'), ('in', 'prep', 'prepositional modifier'), ('the', 'det', 'determiner'), ('morning', 'pobj', 'object of preposition')] 
    
    [('What', 'det', 'determiner'), ('flights', 'nsubj', 'nominal subject'), ('are', 'ROOT', None), ('available', 'acomp', 'adjectival complement'), ('from', 'prep', 'prepositional modifier'), ('Pittsburgh', 'pobj', 'object of preposition'), ('to', 'prep', 'prepositional modifier'), ('Baltimore', 'pobj', 'object of preposition'), ('on', 'prep', 'prepositional modifier'), ('Thursday', 'compound', 'compound'), ('morning', 'pobj', 'object of preposition'), ('?', 'punct', 'punctuation')] 
    
    [('What', 'attr', 'attribute'), ('is', 'ROOT', None), ('the', 'det', 'determiner'), ('arrival', 'compound', 'compound'), ('time', 'nsubj', 'nominal subject'), ('in', 'prep', 'prepositional modifier'), ('San', 'compound', 'compound'), ('francisco', 'pobj', 'object of preposition'), ('for', 'prep', 'prepositional modifier'), ('the', 'det', 'determiner'), ('7:55', 'nummod', 'numeric modifier'), ('AM', 'compound', 'compound'), ('flight', 'pobj', 'object of preposition'), ('leaving', 'acl', 'clausal modifier of noun (adjectival clause)'), ('Washington', 'dobj', 'direct object'), ('?', 'punct', 'punctuation')] 
    
```

###  2.2. <a name='Introductiontowordvectors'></a>Introduction to word vectors

####  2.2.1. <a name='spaCyvocabulary'></a>spaCy vocabulary

```python
# Load the en_core_web_md model
md_nlp = spacy.load('en_core_web_md')

# Print the number of words in the model's vocabulary
print("Number of words: ", md_nlp.meta["vectors"]["vectors"], "\n")

# Print the dimensions of word vectors in en_core_web_md model
print("Dimension of word vectors: ", md_nlp.meta["vectors"]["width"])
```

```bash
<script.py> output:
    Number of words:  20000 
    
    Dimension of word vectors:  300
```

####  2.2.2. <a name='WordvectorsinspaCyvocabulary'></a>Word vectors in spaCy vocabulary

```python
words = ["like", "love"]

# IDs of all the given words
ids = [nlp.vocab.strings[w] for w in words]

# Store the first ten elements of the word vectors for each word
word_vectors = [nlp.vocab.vectors[i][:10] for i in ids]

# Print the first ten elements of the first word vector
print(word_vectors[0])
```

```bash
<script.py> output:
    [-0.18417   0.055115 -0.36953  -0.20895   0.25672   0.30142   0.16299
     -0.16437  -0.070268  2.1638  ]
```

###  2.3. <a name='WordvectorsandspaCy'></a>Word vectors and spaCy

####  2.3.1. <a name='Wordvectorsprojection'></a>Word vectors projection

```python
words = ["tiger", "bird"]

# Extract word IDs of given words
word_ids = [nlp.vocab.strings[w] for w in words]

# Extract word vectors and stack the first five elements vertically
word_vectors = np.vstack([nlp.vocab.vectors[i][:5] for i in word_ids])

# Calculate the transformed word vectors using the pca object
pca = PCA(n_components=2)
word_vectors_transformed = pca.fit_transform(word_vectors)

# Print the first component of the transformed word vectors
print(word_vectors_transformed[:, 0])
```

```bash
<script.py> output:
    [ 0.5182773 -0.5182773]
```

####  2.3.2. <a name='Similarwordsinavocabulary'></a>Similar words in a vocabulary

```python
# Find the most similar word to the word computer
most_similar_words = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings["computer"]]]), n = 1)

# Find the list of similar words given the word IDs
words = [nlp.vocab.strings[w] for w in most_similar_words[0][0]]
print(words)
```

```bash
<script.py> output:
    ['computer-related']
```

###  2.4. <a name='MeasuringsemanticsimilaritywithspaCy'></a>Measuring semantic similarity with spaCy

####  2.4.1. <a name='DocsimilaritywithspaCy'></a>Doc similarity with spaCy

```bash
In [1]:
texts 
Out[1]:

['I like the Vitality canned dog food products.',
 'The peanuts were actually small sized unsalted. Not sure if this was an error.',
 'It is a light, pillowy citrus gelatin with nuts - in this case Filberts.',
 'the Root Beer Extract I ordered is very medicinal.',
 'Great taffy at a great price.']
```

```python
# Create a documents list containing Doc containers
documents = [nlp(t) for t in texts]

# Create a Doc container of the category
category = "canned dog food"
category_document = nlp(category)

# Print similarity scores of each Doc container and the category_document
for i, doc in enumerate(documents):
  print(f"Semantic similarity with document {i+1}:", round(doc.similarity(category_document), 3))
```

```bash
<script.py> output:
    Semantic similarity with document 1: 0.84
    Semantic similarity with document 2: 0.561
    Semantic similarity with document 3: 0.577
    Semantic similarity with document 4: 0.583
    Semantic similarity with document 5: 0.526
```

####  2.4.2. <a name='SpansimilaritywithspaCy'></a>Span similarity with spaCy

```python
# Create a Doc container for the category
category = "canned dog food"
category_document = nlp(category)

# Print similarity score of a given Span and category_document
document_span = document[0:3]
print(f"Semantic similarity with", document_span.text, ":", round(document_span.similarity(category_document), 3))
```

```bash
<script.py> output:
    Semantic similarity with canned food products : 0.866
```

####  2.4.3. <a name='Semanticsimilarityforcategorizingtext'></a>Semantic similarity for categorizing text

```bash
In [1]:
texts
Out[1]:
'This hot sauce is amazing! We picked up a bottle on a trip! '
```

```python
# Populate Doc containers for the word "sauce" and for "texts" string
key = nlp('sauce')
sentences = nlp(texts)

# Calculate similarity score of each sentence and a Doc container for the word sauce
semantic_scores = []
for sent in sentences.sents:
	semantic_scores.append({"score": round(sent.similarity(key), 2)})
print(semantic_scores)
```

```bash
<script.py> output:
    [{'score': 0.65}, {'score': 0.35}]
```

---
##  3. <a name='DataAnalysiswithspaCy'></a>Data Analysis with spaCy

[Slide]({{site.baseurl}}/files/Natural_Language_Processing_with_spaCy_C3.pdf)

###  3.1. <a name='spaCypipelines'></a>spaCy pipelines

```python
# Load a blank spaCy English model and add a sentencizer component
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

# Create Doc containers, store sentences and print its number of sentences
doc = nlp(texts)
sentences = [s for s in doc.sents]
print("Number of sentences: ", len(sentences), "\n")

# Print the list of tokens in the second sentence
print("Second sentence tokens: ", [token for token in sentences[1]])
```

```bash
<script.py> output:
    Number of sentences:  19 
    
    Second sentence tokens:  [The, product, looks, more, like, a, stew, than, a, processed, meat, and, it, smells, better, .]
```

####  3.1.1. <a name='AnalyzingpipelinesinspaCy'></a>Analyzing pipelines in spaCy

```python
# Load a blank spaCy English model
nlp = spacy.blank("en")

# Add tagger and entity_linker pipeline components
nlp.add_pipe("tagger")
nlp.add_pipe("entity_linker")

# Analyze the pipeline
analysis = nlp.analyze_pipes(pretty=True)
```

```bash
<script.py> output:
    [1m
    ============================= Pipeline Overview =============================[0m
    
    #   Component       Assigns           Requires         Scores        Retokenizes
    -   -------------   ---------------   --------------   -----------   -----------
    0   tagger          token.tag                          tag_acc       False      
                                                                                    
    1   entity_linker   token.ent_kb_id   doc.ents         nel_micro_f   False      
                                          doc.sents        nel_micro_r              
                                          token.ent_iob    nel_micro_p              
                                          token.ent_type                            
    
    [1m
    ================================ Problems (4) ================================[0m
    [38;5;3m⚠ 'entity_linker' requirements not met: doc.ents, doc.sents,
    token.ent_iob, token.ent_type[0m
``` 

###  3.2. <a name='spaCyEntityRuler'></a>spaCy EntityRuler

Trong lĩnh vực Xử lý Ngôn ngữ Tự nhiên (Natural Language Processing - NLP) và đặc biệt là Nhận dạng Thực thể Có tên (Named Entity Recognition - NER), việc xác định và phân loại các thực thể như tên người, tổ chức, địa điểm, ngày tháng, v.v. là một nhiệm vụ quan trọng.  `spaCy EntityRuler` là một thành phần mạnh mẽ của thư viện spaCy, cho phép chúng ta tạo các quy tắc (rules) để nhận diện các thực thể tùy chỉnh (custom entities) một cách linh hoạt và chính xác.

**Tại sao cần EntityRuler?**

Đôi khi, các mô hình NER được huấn luyện sẵn (pretrained models) không thể nhận diện được tất cả các thực thể mà chúng ta quan tâm trong một ngữ cảnh cụ thể. Ví dụ, trong một dự án về y tế, có thể có những thuật ngữ chuyên ngành hoặc tên thuốc mà mô hình chung không nhận ra.  `EntityRuler` cho phép chúng ta "dạy" cho spaCy cách nhận diện những thực thể này bằng cách định nghĩa các quy tắc dựa trên mẫu (patterns).

**Cách hoạt động của EntityRuler:**

`EntityRuler` hoạt động dựa trên việc so khớp mẫu (pattern matching). Chúng ta cung cấp cho nó một tập hợp các mẫu, mỗi mẫu bao gồm một hoặc nhiều token (từ/cụm từ) và nhãn (label) tương ứng với loại thực thể. Khi spaCy xử lý một đoạn văn bản, `EntityRuler` sẽ quét văn bản đó để tìm kiếm các mẫu đã được định nghĩa. Nếu tìm thấy một mẫu khớp, nó sẽ gán nhãn cho các token tương ứng là thực thể với nhãn đã được chỉ định.

**Ưu điểm của EntityRuler:**

* **Chính xác:**  Vì dựa trên quy tắc, `EntityRuler` có thể đạt độ chính xác cao trong việc nhận diện các thực thể được định nghĩa.
* **Linh hoạt:**  Có thể định nghĩa các quy tắc phức tạp, bao gồm cả các mẫu dựa trên từ điển, biểu thức chính quy (regular expressions), v.v.
* **Dễ dàng tùy chỉnh:**  Có thể dễ dàng thêm, sửa đổi hoặc xóa các quy tắc để phù hợp với nhu cầu cụ thể.

**Kết luận:**

`spaCy EntityRuler` là một công cụ mạnh mẽ và hữu ích cho việc nhận diện các thực thể tùy chỉnh trong NLP. Nó bổ sung cho các mô hình NER được huấn luyện sẵn bằng cách cho phép chúng ta định nghĩa các quy tắc riêng biệt, giúp tăng cường độ chính xác và linh hoạt trong quá trình xử lý ngôn ngữ.  Hy vọng giải thích này giúp bạn hiểu rõ hơn về `spaCy EntityRuler` trong ngữ cảnh Machine Learning.

####  3.2.1. <a name='EntityRulerwithblankspaCymodel'></a>EntityRuler with blank spaCy model

```python
nlp = spacy.blank("en")
patterns = [{"label": "ORG", "pattern": [{"LOWER": "openai"}]},
            {"label": "ORG", "pattern": [{"LOWER": "microsoft"}]}]
text = "OpenAI has joined forces with Microsoft."

# Add EntityRuler component to the model
entity_ruler = nlp.add_pipe("entity_ruler")

# Add given patterns to the EntityRuler component
entity_ruler.add_patterns(patterns)

# Run the model on a given text
doc = nlp(text)

# Print entities text and type for all entities in the Doc container
print([(ent.text, ent.label_) for ent in doc.ents])
```

```bash
<script.py> output:
    [('OpenAI', 'ORG'), ('Microsoft', 'ORG')]
```

####  3.2.2. <a name='EntityRulerforNER'></a>EntityRuler for NER

```python
nlp = spacy.load("en_core_web_sm")
text = "New York Group was built in 1987."

# Add an EntityRuler to the nlp before NER component
ruler = nlp.add_pipe("entity_ruler", before="ner")

# Define a pattern to classify lower cased new york group as ORG
patterns = [{"label": "ORG", "pattern": [{"lower": "new york group"}]}]

# Add the patterns to the EntityRuler component
ruler.add_patterns(patterns)

# Run the model and print entities text and type for all the entities
doc = nlp(text)
print([(ent.text, ent.label_) for ent in doc.ents])
```

```bash
<script.py> output:
    [('New York Group', 'ORG'), ('1987', 'DATE')]
```

####  3.2.3. <a name='EntityRulerwithmulti-patternsinspaCy'></a>EntityRuler with multi-patterns in spaCy

```python
nlp = spacy.load("en_core_web_md")

# Print a list of tuples of entities text and types in the example_text
print("Before EntityRuler: ", [(ent.text, ent.label_) for ent in nlp(example_text).ents], "\n")

# Define pattern to add a label PERSON for lower cased sisters and brother entities
patterns = [{"label": "PERSON", "pattern": [{"lower": "brother"}]},
            {"label": "PERSON", "pattern": [{"lower": "sisters"}]}]

# Add an EntityRuler component and add the patterns to the ruler
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(patterns)

# Print a list of tuples of entities text and types
print("After EntityRuler: ", [(ent.text, ent.label_) for ent in nlp(example_text).ents])
```

```bash
<script.py> output:
    Before EntityRuler:  [('Filberts', 'ORG'), ('Edmund', 'PERSON')] 
    
    After EntityRuler:  [('Filberts', 'ORG'), ('Edmund', 'PERSON'), ('Brother', 'PERSON'), ('Sisters', 'PERSON')]
```

###  3.3. <a name='RegExwithspaCy'></a>RegEx with spaCy

####  3.3.1. <a name='RegExinPython'></a>RegEx in Python

```python
text = "Our phone number is (425)-123-4567."

# Define a pattern to match phone numbers
pattern = r"\((\d){3}\)-(\d){3}-(\d){4}"

# Find all the matching patterns in the text
phones = re.finditer(pattern, text)

# Print start and end characters and matching section of the text
for match in phones:
    start_char = match.start()
    end_char = match.end()
    print("Start character: ", start_char, "| End character: ", end_char, "| Matching text: ", text[start_char:end_char])
```

```bash
<script.py> output:
    Start character:  20 | End character:  34 | Matching text:  (425)-123-4567
```

####  3.3.2. <a name='RegExwithEntityRulerinspaCy'></a>RegEx with EntityRuler in spaCy

```python
text = "Our phone number is 4251234567."

# Define a pattern to match phone numbers
patterns = [{"label": "PHONE_NUMBERS", "pattern": [{"TEXT": {"REGEX": "(\d){10}"}}]}]

# Load a blank model and add an EntityRuler
nlp = spacy.blank("en")
ruler = nlp.add_pipe("entity_ruler")

# Add the compiled patterns to the EntityRuler
ruler.add_patterns(patterns)

# Print the tuple of entities texts and types for the given text
doc = nlp(text)
print([(ent.text, ent.label_) for ent in doc.ents])
```

```bash
<script.py> output:
    [('4251234567', 'PHONE_NUMBERS')]
```

###  3.4. <a name='spaCyMatcherandPhraseMatcher'></a>spaCy Matcher and PhraseMatcher

####  3.4.1. <a name='MatchingasingleterminspaCy'></a>Matching a single term in spaCy

```python
nlp = spacy.load("en_core_web_sm")
doc = nlp(example_text)

# Initialize a Matcher object
matcher = Matcher(nlp.vocab)

# Define a pattern to match lower cased word witch
pattern = [{"lower" : "witch"}]

# Add the pattern to matcher object and find matches
matcher.add("CustomMatcher", [pattern])
matches = matcher(doc)

# Print start and end token indices and span of the matched text
for match_id, start, end in matches:
    print("Start token: ", start, " | End token: ", end, "| Matched text: ", doc[start:end].text)
```

```bash
<script.py> output:
    Start token:  24  | End token:  25 | Matched text:  Witch
    Start token:  47  | End token:  48 | Matched text:  Witch
```

####  3.4.2. <a name='PhraseMatcherinspaCy'></a>PhraseMatcher in spaCy

- "LOWER": So sánh chữ thường của token.
- "LEMMA": So sánh từ gốc của token.
- "TEXT": So sánh văn bản của token (mặc định).
- "SHAPE": So sánh hình dạng của token (ví dụ: "Xx" cho từ viết hoa, "dd" cho số).


```python
text = "There are only a few acceptable IP addresse: (1) 127.100.0.1, (2) 123.4.1.0."
terms = ["110.0.0.0", "101.243.0.0"]

# Initialize a PhraseMatcher class to match to shapes of given terms
matcher = PhraseMatcher(nlp.vocab, attr = "SHAPE")

# Create patterns to add to the PhraseMatcher object
patterns = [nlp.make_doc(term) for term in terms]
matcher.add("IPAddresses", patterns)

# Find matches to the given patterns and print start and end characters and matches texts
doc = nlp(text)
matches = matcher(doc)
for match_id, start, end in matches:
    print("Start token: ", start, " | End token: ", end, "| Matched text: ", doc[start:end].text)
```

```bash
<script.py> output:
    Start token:  12  | End token:  13 | Matched text:  127.100.0.1
    Start token:  17  | End token:  18 | Matched text:  123.4.1.0
```

####  3.4.3. <a name='MatchingwithextendedsyntaxinspaCy'></a>Matching with extended syntax in spaCy

```python
nlp = spacy.load("en_core_web_sm")
doc = nlp(example_text)

# Define a matcher object
matcher = Matcher(nlp.vocab)
# Define a pattern to match tiny squares and tiny mouthful
pattern = [{"lower": "tiny"}, {"lower": {"IN": ["squares", "mouthful"]}}]

# Add the pattern to matcher object and find matches
matcher.add("CustomMatcher", [pattern])
matches = matcher(doc)

# Print out start and end token indices and the matched text span per match
for match_id, start, end in matches:
    print("Start token: ", start, " | End token: ", end, "| Matched text: ", doc[start:end].text)
```

```bash
<script.py> output:
    Start token:  4  | End token:  6 | Matched text:  tiny squares
    Start token:  19  | End token:  21 | Matched text:  tiny mouthful
```

---
##  4. <a name='CustomizingspaCyModels'></a>Customizing spaCy Models

[Slide]({{site.baseurl}}/files/Natural_Language_Processing_with_spaCy_C4.pdf)

###  4.1. <a name='CustomizingspaCymodels'></a>Customizing spaCy models

####  4.1.1. <a name='Modelperformanceonyourdata'></a>Model performance on your data

```python
# Append a tuple of (entities text, entities label) if Jumbo is in the entity
target_entities = []
for doc in documents:
  target_entities.extend([(ent.text, ent.label_) for ent in doc.ents if "Jumbo" in ent.text])
print(target_entities)

# Append True to the correct_labels list if the entity label is `PRODUCT`
correct_labels = []
for ent in target_entities:
  if ent[1] == "PRODUCT":
    correct_labels.append(True)
  else:
    correct_labels.append(False)
print(correct_labels)
```

```bash
<script.py> output:
    [('Jumbo', 'PERSON'), ('Jumbo', 'PERSON')]
    [False, False]
```

###  4.2. <a name='spaCytrainingdataformat'></a>spaCy training data format

####  4.2.1. <a name='Annotationandpreparingtrainingdata'></a>Annotation and preparing training data

```python
text = "A patient with chest pain had hyperthyroidism."
entity_1 = "chest pain"
entity_2 = "hyperthyroidism"

# Store annotated data information in the correct format
annotated_data = {"sentence": text, "entities": [{"label": "SYMPTOM", "value": entity_1}, {"label": "DISEASE", "value": entity_2}]}

# Extract start and end characters of each entity
entity_1_start_char = text.find(entity_1)
entity_1_end_char = entity_1_start_char + len(entity_1)
entity_2_start_char = text.find(entity_2)
entity_2_end_char = entity_2_start_char + len(entity_2)

# Store the same input information in the proper format for training
training_data = [(text, {"entities": [(entity_1_start_char,entity_1_end_char,"SYMPTOM"), 
                                      (entity_2_start_char,entity_2_end_char,"DISEASE")]})]
print(training_data)
```

```bash
<script.py> output:
    [('A patient with chest pain had hyperthyroidism.', {'entities': [(15, 25, 'SYMPTOM'), (30, 45, 'DISEASE')]})]
```

####  4.2.2. <a name='Compatibletrainingdata'></a>Compatible training data

```python
example_text = 'A patient with chest pain had hyperthyroidism.'
training_data = [(example_text, {'entities': [(15, 25, 'SYMPTOM'), (30, 45, 'DISEASE')]})]

all_examples = []
# Iterate through text and annotations and convert text to a Doc container
for text, annotations in training_data:
  doc = nlp(text)
  
  # Create an Example object from the doc contianer and annotations
  example_sentence = Example.from_dict(doc, annotations)
  print(example_sentence.to_dict(), "\n")
  
  # Append the Example object to the list of all examples
  all_examples.append(example_sentence)
  
print("Number of formatted training data: ", len(all_examples))
```

```bash
<script.py> output:
    {'doc_annotation': {'cats': {}, 'entities': ['O', 'O', 'O', 'B-SYMPTOM', 'L-SYMPTOM', 'O', 'U-DISEASE', 'O'], 'links': {}}, 'token_annotation': {'ORTH': ['A', 'patient', 'with', 'chest', 'pain', 'had', 'hyperthyroidism', '.'], 'SPACY': [True, True, True, True, True, True, False, False], 'TAG': ['', '', '', '', '', '', '', ''], 'LEMMA': ['', '', '', '', '', '', '', ''], 'POS': ['', '', '', '', '', '', '', ''], 'MORPH': ['', '', '', '', '', '', '', ''], 'HEAD': [0, 1, 2, 3, 4, 5, 6, 7], 'DEP': ['', '', '', '', '', '', '', ''], 'SENT_START': [1, 0, 0, 0, 0, 0, 0, 0]}} 
    
    Number of formatted training data:  1
```

###  4.3. <a name='TrainingwithspaCy'></a>Training with spaCy

####  4.3.1. <a name='Trainingpreparationsteps'></a>Training preparation steps

```python
nlp = spacy.load("en_core_web_sm")

# Disable all pipeline components of  except `ner`
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
nlp.disable_pipes(*other_pipes)

# Convert a text and its annotations to the correct format usable for training
doc = nlp.make_doc(text)
example = Example.from_dict(doc, annotations)
print("Example object for training: \n", example.to_dict())
```

```bash
<script.py> output:
    Example object for training: 
     {'doc_annotation': {'cats': {}, 'entities': ['O', 'O', 'O', 'O', 'O', 'U-GPE', 'O'], 'links': {}}, 'token_annotation': {'ORTH': ['I', 'will', 'visit', 'you', 'in', 'Austin', '.'], 'SPACY': [True, True, True, True, True, False, False], 'TAG': ['', '', '', '', '', '', ''], 'LEMMA': ['', '', '', '', '', '', ''], 'POS': ['', '', '', '', '', '', ''], 'MORPH': ['', '', '', '', '', '', ''], 'HEAD': [0, 1, 2, 3, 4, 5, 6], 'DEP': ['', '', '', '', '', '', ''], 'SENT_START': [1, 0, 0, 0, 0, 0, 0]}}
```

####  4.3.2. <a name='TrainanexistingNERmodel'></a>Train an existing NER model

```python
nlp = spacy.load("en_core_web_sm")
print("Before training: ", [(ent.text, ent.label_) for ent in nlp(test).ents])
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
nlp.disable_pipes(*other_pipes)
optimizer = nlp.create_optimizer()

# Shuffle training data and the dataset using random package per epoch
for i in range(epochs):
    random.shuffle(training_data)
    for text, annotations in training_data:
      doc = nlp.make_doc(text)
      # Update nlp model after setting sgd argument to optimizer
      example = Example.from_dict(doc, annotations)
      nlp.update([example], sgd = optimizer)
print("After training: ", [(ent.text, ent.label_) for ent in nlp(test).ents])
```

```bash
<script.py> output:
    Before training:  [('Sam', 'PERSON')]
    After training:  [('Sam', 'PERSON'), ('house', 'GPE')]
```

####  4.3.3. <a name='TrainingaspaCymodelfromscratch'></a>Training a spaCy model from scratch

```python
# Load a blank English model, add NER component, add given labels to the ner pipeline
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")
for ent in labels:
    ner.add_label(ent)

# Disable other pipeline components, complete training loop and run training loop
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
nlp.disable_pipes(*other_pipes)
losses = {}
optimizer = nlp.begin_training()
for text, annotation in training_data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotation)
    nlp.update([example], sgd=optimizer, losses=losses)
    print(losses)
```

```bash
<script.py> output:
    {'ner': 98.42856240272522}
    {'ner': 189.34197914600372}
    {'ner': 310.98384952545166}
    {'ner': 377.18853384256363}
    {'ner': 578.3004557490349}
    {'ner': 608.2531691193581}
    {'ner': 673.164011657238}
    {'ner': 723.6257713735104}
    {'ner': 746.0405215527862}
    {'ner': 756.4262755732052}
    {'ner': 790.0200939634815}
    {'ner': 795.990012896822}
    {'ner': 796.0241677922168}
    {'ner': 798.0212131336592}
    {'ner': 813.9837758949773}
    {'ner': 817.9703837852048}
    {'ner': 829.9056551901582}
    {'ner': 845.8729668580933}
    {'ner': 853.8427640225843}
    {'ner': 863.77342558173}
```