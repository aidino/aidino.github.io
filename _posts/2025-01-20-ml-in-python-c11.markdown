---
layout: post
title: "Preprocessing for Machine Learning in Python"
date: 2025-01-20 10:00:00 +0700
categories: machine learning in python
---

This course covers the basics of how and when to perform data preprocessing. This essential step in any machine learning project is when you get your data ready for modeling. Between importing and cleaning your data and fitting your machine learning model is when preprocessing comes into play. You'll learn how to standardize your data so that it's in the right form for your model, create new features to best leverage the information in your dataset, and select the best features to improve your model fit. Finally, you'll have some practice preprocessing by getting a dataset on UFO sightings ready for modeling.

### Table of contents

- [1. Introduction to Data Preprocessing](#1-introduction-to-data-preprocessing)
  - [1.1. Working with data types](#11-working-with-data-types)
    - [1.1.1. Converting a column type](#111-converting-a-column-type)
  - [1.2. Training and test sets](#12-training-and-test-sets)
    - [1.2.1. Stratified sampling](#121-stratified-sampling)
- [2. Standardizing Data](#2-standardizing-data)
  - [2.1. Standardization](#21-standardization)
    - [2.1.1. Modeling without normalizing](#211-modeling-without-normalizing)
  - [2.2. Log normalization](#22-log-normalization)
    - [2.2.1. Log normalization in Python](#221-log-normalization-in-python)
  - [2.3. Scaling data for feature comparison](#23-scaling-data-for-feature-comparison)
    - [2.3.1. Scaling data - standardizing columns](#231-scaling-data---standardizing-columns)
  - [2.4. Standardized data and modeling](#24-standardized-data-and-modeling)
    - [2.4.1. KNN on non-scaled data](#241-knn-on-non-scaled-data)
    - [2.4.2. KNN on scaled data](#242-knn-on-scaled-data)
- [3. Feature Engineering](#3-feature-engineering)
  - [3.1. Encoding categorical variables](#31-encoding-categorical-variables)
    - [3.1.1. Encoding categorical variables - binary](#311-encoding-categorical-variables---binary)
    - [3.1.2. Encoding categorical variables - one-hot](#312-encoding-categorical-variables---one-hot)
  - [3.2. Engineering numerical features](#32-engineering-numerical-features)
    - [3.2.1. Aggregating numerical features](#321-aggregating-numerical-features)
    - [3.2.2. Extracting datetime components](#322-extracting-datetime-components)
  - [3.3. Engineering text features](#33-engineering-text-features)
    - [3.3.1. Extracting string patterns](#331-extracting-string-patterns)
    - [3.3.2. Vectorizing text](#332-vectorizing-text)
    - [3.3.3. Text classification using tf/idf vectors](#333-text-classification-using-tfidf-vectors)
- [4. Selecting Features for Modeling](#4-selecting-features-for-modeling)
  - [4.1. Removing redundant features](#41-removing-redundant-features)
    - [4.1.1. Checking for correlated features](#411-checking-for-correlated-features)
  - [4.2. Selecting features using text vectors](#42-selecting-features-using-text-vectors)
    - [4.2.1. Exploring text vectors, part 1](#421-exploring-text-vectors-part-1)
    - [4.2.2. Exploring text vectors, part 2](#422-exploring-text-vectors-part-2)
    - [4.2.3. Training Naive Bayes with feature selection](#423-training-naive-bayes-with-feature-selection)
  - [4.3. Dimensionality reduction](#43-dimensionality-reduction)
    - [4.3.1. Using PCA](#431-using-pca)
    - [4.3.2. Training a model with PCA](#432-training-a-model-with-pca)
- [5. Putting It All Together](#5-putting-it-all-together)
  - [5.1. UFOs and preprocessing](#51-ufos-and-preprocessing)
    - [5.1.1. Checking column types](#511-checking-column-types)
    - [5.1.2. Dropping missing data](#512-dropping-missing-data)
  - [5.2. Categorical variables and standardization](#52-categorical-variables-and-standardization)
    - [5.2.1. Extracting numbers from strings](#521-extracting-numbers-from-strings)
    - [5.2.2. Identifying features for standardization](#522-identifying-features-for-standardization)
  - [5.3. Engineering new features](#53-engineering-new-features)
    - [5.3.1. Encoding categorical variables](#531-encoding-categorical-variables)
    - [5.3.2. Features from dates](#532-features-from-dates)
    - [5.3.3. Text vectorization](#533-text-vectorization)
  - [5.4. Feature selection and modeling](#54-feature-selection-and-modeling)
    - [5.4.1. Selecting the ideal dataset](#541-selecting-the-ideal-dataset)
    - [5.4.2. Modeling the UFO dataset, part 1](#542-modeling-the-ufo-dataset-part-1)
    - [5.4.3. Modeling the UFO dataset, part 2](#543-modeling-the-ufo-dataset-part-2)


##  1. <a name='IntroductiontoDataPreprocessing'></a>Introduction to Data Preprocessing

[Slide]({{site.baseurl}}/files/Preprocessing_for_Machine_Learning_in_Python_C1.pdf)

###  1.1. <a name='Workingwithdatatypes'></a>Working with data types

####  1.1.1. <a name='Convertingacolumntype'></a>Converting a column type

```python
# Print the head of the hits column
print(volunteer["hits"].head())

# Convert the hits column to type int
volunteer["hits"] = volunteer["hits"].astype("int")

# Look at the dtypes of the dataset
print(volunteer.dtypes)
```

```bash
<script.py> output:
    0    737
    1     22
    2     62
    3     14
    4     31
    Name: hits, dtype: object

opportunity_id          int64
    content_id              int64
    vol_requests            int64
    event_time              int64
    title                  object
    hits                    int64
    summary                object
    is_priority            object
    category_id           float64
    category_desc          object
    amsl                  float64
    amsl_unit             float64
    org_title              object
    org_content_id          int64
    addresses_count         int64
    locality               object
    region                 object
    postalcode            float64
    primary_loc           float64
    display_url            object
    recurrence_type        object
    hours                   int64
    created_date           object
    last_modified_date     object
    start_date_date        object
    end_date_date          object
    status                 object
    Latitude              float64
    Longitude             float64
    Community Board       float64
    Community Council     float64
    Census Tract          float64
    BIN                   float64
    BBL                   float64
    NTA                   float64
    dtype: object
```

###  1.2. <a name='Trainingandtestsets'></a>Training and test sets

####  1.2.1. <a name='Stratifiedsampling'></a>Stratified sampling

```python
# Create a DataFrame with all columns except category_desc
X = volunteer.drop('category_desc', axis=1)

# Create a category_desc labels dataset
y = volunteer[['category_desc']]

# Use stratified sampling to split up the dataset according to the y dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# Print the category_desc counts from y_train
print(y_train['category_desc'].value_counts())
```

```bash
<script.py> output:
    Strengthening Communities    230
    Helping Neighbors in Need     89
    Education                     69
    Health                        39
    Environment                   24
    Emergency Preparedness        11
    Name: category_desc, dtype: int64
```

##  2. <a name='StandardizingData'></a>Standardizing Data

[Slide]({{site.baseurl}}/files/Preprocessing_for_Machine_Learning_in_Python_C2.pdf)

###  2.1. <a name='Standardization'></a>Standardization

####  2.1.1. <a name='Modelingwithoutnormalizing'></a>Modeling without normalizing

```python
# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

knn = KNeighborsClassifier()

# Fit the knn model to the training data
knn.fit(X_train, y_train)

# Score the model on the test data
print(knn.score(X_test, y_test))
```

```bash
<script.py> output:
    0.6888888888888889
```

###  2.2. <a name='Lognormalization'></a>Log normalization

####  2.2.1. <a name='LognormalizationinPython'></a>Log normalization in Python

```python
# Print out the variance of the Proline column
print(wine['Proline'].var())

# Apply the log normalization function to the Proline column
wine['Proline_log'] = np.log(wine['Proline'])

# Check the variance of the normalized Proline column
print(wine['Proline_log'].var())
```

```bash
<script.py> output:
    99166.71735542436
    0.17231366191842012
```

###  2.3. <a name='Scalingdataforfeaturecomparison'></a>Scaling data for feature comparison

####  2.3.1. <a name='Scalingdata-standardizingcolumns'></a>Scaling data - standardizing columns

```python
# Import StandardScaler
from sklearn.preprocessing import StandardScaler

# Create the scaler
scaler = StandardScaler()

# Subset the DataFrame you want to scale 
wine_subset = wine[['Ash', 'Alcalinity of ash', 'Magnesium']]

# Apply the scaler to wine_subset
wine_subset_scaled = scaler.fit_transform(wine_subset)# Import StandardScaler
from sklearn.preprocessing import StandardScaler

# Create the scaler
scaler = StandardScaler()

# Subset the DataFrame you want to scale 
wine_subset = wine[['Ash', 'Alcalinity of ash', 'Magnesium']]

# Apply the scaler to wine_subset
wine_subset_scaled = scaler.fit_transform(wine_subset)
```

###  2.4. <a name='Standardizeddataandmodeling'></a>Standardized data and modeling

####  2.4.1. <a name='KNNonnon-scaleddata'></a>KNN on non-scaled data

```python
# Split the dataset and labels into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# Fit the k-nearest neighbors model to the training data
knn.fit(X_train, y_train)

# Score the model on the test data
print(knn.score(X_test, y_test))
```

```bash
<script.py> output:
    0.7777777777777778
```

####  2.4.2. <a name='KNNonscaleddata'></a>KNN on scaled data

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# Instantiate a StandardScaler
scaler = StandardScaler()

# Scale the training and test features
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Fit the k-nearest neighbors model to the training data
knn.fit(X_train_scaled, y_train)

# Score the model on the test data
print(knn.score(X_test_scaled, y_test))
```

```bash
<script.py> output:
    0.9333333333333333
```

##  3. <a name='FeatureEngineering'></a>Feature Engineering

[Slide]({{site.baseurl}}/files/Preprocessing_for_Machine_Learning_in_Python_C3.pdf)

###  3.1. <a name='Encodingcategoricalvariables'></a>Encoding categorical variables

####  3.1.1. <a name='Encodingcategoricalvariables-binary'></a>Encoding categorical variables - binary

```python
from sklearn.preprocessing import LabelEncoder

# Set up the LabelEncoder object
enc = LabelEncoder()

# Apply the encoding to the "Accessible" column
hiking['Accessible_enc'] = enc.fit_transform(hiking['Accessible'])

# Compare the two columns
print(hiking[['Accessible_enc', 'Accessible']].head())
```

```bash
<script.py> output:
       Accessible_enc Accessible
    0               1          Y
    1               0          N
    2               0          N
    3               0          N
    4               0          N
```

####  3.1.2. <a name='Encodingcategoricalvariables-one-hot'></a>Encoding categorical variables - one-hot

```python
# Transform the category_desc column
category_enc = pd.get_dummies(volunteer['category_desc'])

# Take a look at the encoded columns
print(category_enc.head())
```

```bash
<script.py> output:
       Education  Emergency Preparedness  Environment  Health  Helping Neighbors in Need  Strengthening Communities
    0          0                       0            0       0                          0                          0
    1          0                       0            0       0                          0                          1
    2          0                       0            0       0                          0                          1
    3          0                       0            0       0                          0                          1
    4          0                       0            1       0                          0                          0
```

###  3.2. <a name='Engineeringnumericalfeatures'></a>Engineering numerical features

####  3.2.1. <a name='Aggregatingnumericalfeatures'></a>Aggregating numerical features

```python
# Use .loc to create a mean column
running_times_5k["mean"] = running_times_5k.loc[:, "run1":"run5"].mean(axis=1)

# Take a look at the results
print(running_times_5k.head())
```

```bash
<script.py> output:
        name  run1  run2  run3  run4  run5   mean
    0    Sue  20.1  18.5  19.6  20.3  18.3  19.36
    1   Mark  16.5  17.1  16.9  17.6  17.3  17.08
    2   Sean  23.5  25.1  25.2  24.6  23.9  24.46
    3   Erin  21.7  21.1  20.9  22.1  22.2  21.60
    4  Jenny  25.8  27.1  26.1  26.7  26.9  26.52
``` 

####  3.2.2. <a name='Extractingdatetimecomponents'></a>Extracting datetime components

```python
# First, convert string column to date column
volunteer["start_date_converted"] = pd.to_datetime(volunteer['start_date_date'])

# Extract just the month from the converted column
volunteer["start_date_month"] = volunteer['start_date_converted'].dt.month

# Take a look at the converted and new month columns
print(volunteer[['start_date_converted', 'start_date_month']].head())
```

```bash
<script.py> output:
      start_date_converted  start_date_month
    0           2011-07-30                 7
    1           2011-02-01                 2
    2           2011-01-29                 1
    3           2011-02-14                 2
    4           2011-02-05                 2
```


###  3.3. <a name='Engineeringtextfeatures'></a>Engineering text features

####  3.3.1. <a name='Extractingstringpatterns'></a>Extracting string patterns

```python
import re

# Write a pattern to extract numbers and decimals
def return_mileage(length):
    
    # Search the text for matches
    mile = re.search("\d+\.\d+", length)
    
    # If a value is returned, use group(0) to return the found value
    if mile is not None:
        return float(mile.group(0))
        
# Apply the function to the Length column and take a look at both columns
hiking["Length_num"] = hiking['Length'].apply(return_mileage)
print(hiking[["Length", "Length_num"]].head())
```

```bash
<script.py> output:
           Length  Length_num
    0   0.8 miles        0.80
    1    1.0 mile        1.00
    2  0.75 miles        0.75
    3   0.5 miles        0.50
    4   0.5 miles        0.50
```

####  3.3.2. <a name='Vectorizingtext'></a>Vectorizing text

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Take the title text
title_text = volunteer["title"]

# Create the vectorizer method
tfidf_vec = TfidfVectorizer()

# Transform the text into tf-idf vectors
text_tfidf = tfidf_vec.fit_transform(title_text)
```

####  3.3.3. <a name='Textclassificationusingtfidfvectors'></a>Text classification using tf/idf vectors

```python
# Split the dataset according to the class distribution of category_desc
y = volunteer["category_desc"]
X_train, X_test, y_train, y_test = train_test_split(text_tfidf.toarray(), y, stratify=y, random_state=42)

# Fit the model to the training data
nb.fit(X_train, y_train)

# Print out the model's accuracy
print(nb.score(X_test, y_test))
```

```bash
<script.py> output:
    0.5161290322580645
```

##  4. <a name='SelectingFeaturesforModeling'></a>Selecting Features for Modeling

[Slide]({{site.baseurl}}/files/Preprocessing_for_Machine_Learning_in_Python_C4.pdf)

###  4.1. <a name='Removingredundantfeatures'></a>Removing redundant features

####  4.1.1. <a name='Checkingforcorrelatedfeatures'></a>Checking for correlated features

```python
# Print out the column correlations of the wine dataset
print(wine.corr())

# Drop that column from the DataFrame
wine = wine.drop(['Flavanoids'], axis=1)

print(wine.head())
```

```bash
<script.py> output:
                                  Flavanoids  Total phenols  Malic acid  OD280/OD315 of diluted wines    Hue
    Flavanoids                         1.000          0.865      -0.411                         0.787  0.543
    Total phenols                      0.865          1.000      -0.335                         0.700  0.434
    Malic acid                        -0.411         -0.335       1.000                        -0.369 -0.561
    OD280/OD315 of diluted wines       0.787          0.700      -0.369                         1.000  0.565
    Hue                                0.543          0.434      -0.561                         0.565  1.000
       Total phenols  Malic acid  OD280/OD315 of diluted wines   Hue
    0           2.80        1.71                          3.92  1.04
    1           2.65        1.78                          3.40  1.05
    2           2.80        2.36                          3.17  1.03
    3           3.85        1.95                          3.45  0.86
    4           2.80        2.59                          2.93  1.04
```

###  4.2. <a name='Selectingfeaturesusingtextvectors'></a>Selecting features using text vectors

####  4.2.1. <a name='Exploringtextvectorspart1'></a>Exploring text vectors, part 1

```python
def return_weights(vocab, original_vocab, vector, vector_index, top_n):
    zipped = dict(zip(vector[vector_index].indices, vector[vector_index].data))
    
    # Transform that zipped dict into a series
    zipped_series = pd.Series({vocab[i]:zipped[i] for i in vector[vector_index].indices})
    
    # Sort the series to pull out the top n weighted words
    zipped_index = zipped_series.sort_values(ascending=False)[:top_n].index
    return [original_vocab[i] for i in zipped_index]

# Print out the weighted words
print(return_weights(vocab, tfidf_vec.vocabulary_, text_tfidf, 8, 3))
```

```bash
<script.py> output:
    [189, 942, 466]
```

####  4.2.2. <a name='Exploringtextvectorspart2'></a>Exploring text vectors, part 2

```python
def words_to_filter(vocab, original_vocab, vector, top_n):
    filter_list = []
    for i in range(0, vector.shape[0]):
    
        # Call the return_weights function and extend filter_list
        filtered = return_weights(vocab, original_vocab, vector, i, top_n)
        filter_list.extend(filtered)
        
    # Return the list in a set, so we don't get duplicate word indices
    return set(filter_list)

# Call the function to get the list of word indices
filtered_words = words_to_filter(vocab, tfidf_vec.vocabulary_, text_tfidf, 3)

# Filter the columns in text_tfidf to only those in filtered_words
filtered_text = text_tfidf[:, list(filtered_words)]
```

####  4.2.3. <a name='TrainingNaiveBayeswithfeatureselection'></a>Training Naive Bayes with feature selection

```python
# Split the dataset according to the class distribution of category_desc
X_train, X_test, y_train, y_test = train_test_split(filtered_text.toarray(), y, stratify=y, random_state=42)

# Fit the model to the training data
nb.fit(X_train, y_train)

# Print out the model's accuracy
print(nb.score(X_test, y_test))
```

```bash
<script.py> output:
    0.5161290322580645
```

###  4.3. <a name='Dimensionalityreduction'></a>Dimensionality reduction

####  4.3.1. <a name='UsingPCA'></a>Using PCA

```python
from sklearn.decomposition import PCA

# Instantiate a PCA object
pca = PCA()

# Define the features and labels from the wine dataset
X = wine.drop(['Type'], axis=1)
y = wine["Type"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# Apply PCA to the wine dataset X vector
pca_X_train = pca.fit_transform(X_train)
pca_X_test = pca.transform(X_test)

# Look at the percentage of variance explained by the different components
print(pca.explained_variance_ratio_)
```

####  4.3.2. <a name='TrainingamodelwithPCA'></a>Training a model with PCA

```python
# Fit knn to the training data
knn.fit(pca_X_train, y_train)

# Score knn on the test data and print it out
print(knn.score(pca_X_test, y_test))
```

```bash
<script.py> output:
    0.7777777777777778
```

##  5. <a name='PuttingItAllTogether'></a>Putting It All Together

[Slide]({{site.baseurl}}/files/Preprocessing_for_Machine_Learning_in_Python_C5.pdf)

###  5.1. <a name='UFOsandpreprocessing'></a>UFOs and preprocessing

####  5.1.1. <a name='Checkingcolumntypes'></a>Checking column types

```python
# Print the DataFrame info
print(ufo.info())

# Change the type of seconds to float
ufo["seconds"] = ufo["seconds"].astype(float)

# Change the date column to type datetime
ufo["date"] = pd.to_datetime(ufo['date'])

# Check the column types
print(ufo.info())
```

```bash
<script.py> output:
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4935 entries, 0 to 4934
    Data columns (total 11 columns):
     #   Column          Non-Null Count  Dtype  
    ---  ------          --------------  -----  
     0   date            4935 non-null   object 
     1   city            4926 non-null   object 
     2   state           4516 non-null   object 
     3   country         4255 non-null   object 
     4   type            4776 non-null   object 
     5   seconds         4935 non-null   object 
     6   length_of_time  4792 non-null   object 
     7   desc            4932 non-null   object 
     8   recorded        4935 non-null   object 
     9   lat             4935 non-null   object 
     10  long            4935 non-null   float64
    dtypes: float64(1), object(10)
    memory usage: 424.2+ KB
    None
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4935 entries, 0 to 4934
    Data columns (total 11 columns):
     #   Column          Non-Null Count  Dtype         
    ---  ------          --------------  -----         
     0   date            4935 non-null   datetime64[ns]
     1   city            4926 non-null   object        
     2   state           4516 non-null   object        
     3   country         4255 non-null   object        
     4   type            4776 non-null   object        
     5   seconds         4935 non-null   float64       
     6   length_of_time  4792 non-null   object        
     7   desc            4932 non-null   object        
     8   recorded        4935 non-null   object        
     9   lat             4935 non-null   object        
     10  long            4935 non-null   float64       
    dtypes: datetime64[ns](1), float64(2), object(8)
    memory usage: 424.2+ KB
    None
```

####  5.1.2. <a name='Droppingmissingdata'></a>Dropping missing data

```python
# Count the missing values in the length_of_time, state, and type columns, in that order
print(ufo[['length_of_time', 'state', 'type']].isna().sum())

# Drop rows where length_of_time, state, or type are missing
ufo_no_missing = ufo.dropna(subset=['length_of_time', 'state', 'type'])

# Print out the shape of the new dataset
print(ufo_no_missing.shape)
```

```bash
<script.py> output:
    length_of_time    143
    state             419
    type              159
    dtype: int64
    (4283, 4)
```

###  5.2. <a name='Categoricalvariablesandstandardization'></a>Categorical variables and standardization

####  5.2.1. <a name='Extractingnumbersfromstrings'></a>Extracting numbers from strings

```python
def return_minutes(time_string):

    # Search for numbers in time_string
    num = re.search("\d+", time_string)
    if num is not None:
        return int(num.group(0))
        
# Apply the extraction to the length_of_time column
ufo["minutes"] = ufo["length_of_time"].apply(return_minutes)

# Take a look at the head of both of the columns
print(ufo[['length_of_time', 'minutes']].head())
```

```bash
<script.py> output:
        length_of_time  minutes
    2  about 5 minutes      5.0
    4       10 minutes     10.0
    7        2 minutes      2.0
    8        2 minutes      2.0
    9        5 minutes      5.0
```

####  5.2.2. <a name='Identifyingfeaturesforstandardization'></a>Identifying features for standardization

```python
# Check the variance of the seconds and minutes columns
print(ufo[['seconds', 'minutes']].var())

# Log normalize the seconds column
ufo["seconds_log"] = np.log(ufo['seconds'])

# Print out the variance of just the seconds_log column
print(ufo["seconds_log"].var())
```

```bash
<script.py> output:
    seconds    424087.417
    minutes       117.546
    dtype: float64
    1.1223923881183004
```

###  5.3. <a name='Engineeringnewfeatures'></a>Engineering new features

####  5.3.1. <a name='Encodingcategoricalvariables-1'></a>Encoding categorical variables

```python
# Use pandas to encode us values as 1 and others as 0
ufo["country_enc"] = ufo["country"].apply(lambda val: 1 if val == "us" else 0)

# Print the number of unique type values
print(len(ufo['type'].unique()))

# Create a one-hot encoded set of the type values
type_set = pd.get_dummies(ufo['type'])

# Concatenate this set back to the ufo DataFrame
ufo = pd.concat([ufo, type_set], axis=1)
```

```bash
<script.py> output:
    21
```

####  5.3.2. <a name='Featuresfromdates'></a>Features from dates

```python
# Look at the first 5 rows of the date column
print(ufo['date'].head())

# Extract the month from the date column
ufo["month"] = ufo["date"].dt.month

# Extract the year from the date column
ufo["year"] = ufo["date"].dt.year

# Take a look at the head of all three columns
print(ufo[['date', 'month', 'year']].head())
```

```bash
<script.py> output:
    0   2002-11-21 05:45:00
    1   2012-06-16 23:00:00
    2   2013-06-09 00:00:00
    3   2013-04-26 23:27:00
    4   2013-09-13 20:30:00
    Name: date, dtype: datetime64[ns]
                     date  month  year
    0 2002-11-21 05:45:00     11  2002
    1 2012-06-16 23:00:00      6  2012
    2 2013-06-09 00:00:00      6  2013
    3 2013-04-26 23:27:00      4  2013
    4 2013-09-13 20:30:00      9  2013
```

####  5.3.3. <a name='Textvectorization'></a>Text vectorization

```python
# Take a look at the head of the desc field
print(ufo['desc'].head())

# Instantiate the tfidf vectorizer object
vec = TfidfVectorizer()

# Fit and transform desc using vec
desc_tfidf = vec.fit_transform(ufo['desc'])

# Look at the number of columns and rows
print(desc_tfidf.shape)
```

```bash
<script.py> output:
    0    It was a large&#44 triangular shaped flying ob...
    1    Dancing lights that would fly around and then ...
    2    Brilliant orange light or chinese lantern at o...
    3    Bright red light moving north to north west fr...
    4    North-east moving south-west. First 7 or so li...
    Name: desc, dtype: object
    (1866, 3422)
```

###  5.4. <a name='Featureselectionandmodeling'></a>Feature selection and modeling

####  5.4.1. <a name='Selectingtheidealdataset'></a>Selecting the ideal dataset

```python
# Make a list of features to drop
to_drop = ['country', 'city', 'lat', 'long', 'state', 'date', 'recorded', 'seconds', 'minutes', 'desc', 'length_of_time']

# Drop those features
ufo_dropped = ufo.drop(to_drop, axis=1)

# Let's also filter some words out of the text vector we created
filtered_words = words_to_filter(vocab, vec.vocabulary_, desc_tfidf, 4)
```

####  5.4.2. <a name='ModelingtheUFOdatasetpart1'></a>Modeling the UFO dataset, part 1

```python
# Take a look at the features in the X set of data
print(X.columns)

# Split the X and y sets
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# Fit knn to the training sets
knn.fit(X_train, y_train)

# Print the score of knn on the test sets
print(knn.score(X_test, y_test))
```

```bash
<script.py> output:
    Index(['seconds_log', 'changing', 'chevron', 'cigar', 'circle', 'cone', 'cross', 'cylinder', 'diamond', 'disk', 'egg', 'fireball', 'flash', 'formation', 'light', 'other', 'oval', 'rectangle',
           'sphere', 'teardrop', 'triangle', 'unknown', 'month', 'year'],
          dtype='object')
    0.8650963597430407
```

####  5.4.3. <a name='ModelingtheUFOdatasetpart2'></a>Modeling the UFO dataset, part 2

```python
# Use the list of filtered words we created to filter the text vector
filtered_text = desc_tfidf[:, list(filtered_words)]

# Split the X and y sets using train_test_split, setting stratify=y 
X_train, X_test, y_train, y_test = train_test_split(filtered_text.toarray(), y, stratify=y, random_state=42)

# Fit nb to the training sets
nb.fit(X_train, y_train)

# Print the score of nb on the test sets
nb.score(X_test, y_test)
```

```bash
0.17987152034261242
```