---
layout: post
title: "Dimensionality Reduction in Python"
date: 2025-01-20 09:00:00 +0700
categories: machine learning in python
---

High-dimensional datasets can be overwhelming and leave you not knowing where to start. Typically, you’d visually explore a new dataset first, but when you have too many dimensions the classical approaches will seem insufficient. Fortunately, there are visualization techniques designed specifically for high dimensional data and you’ll be introduced to these in this course. After exploring the data, you’ll often find that many features hold little information because they don’t show any variance or because they are duplicates of other features. 


## Exploring High Dimensional Data

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C1.pdf)

### Introduction
### Feature selection vs. feature extraction
### t-SNE visualization of high-dimensional data

---
## Feature Selection I - Selecting for Feature Information

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C2.pdf)

### The curse of dimensionality
### Features with missing values or little variance
### Pairwise correlation
### Removing highly correlated features

---
## Feature Selection II - Selecting for Model Accuracy

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C3.pdf)

### Selecting features for model performance
### Tree-based feature selection
### Regularized linear regression
### Combining feature selectors

---
## Feature Extraction

[Slide]({{site.baseurl}}/files/Dimensionality_Reduction_in_Python_C4.pdf)

### Feature extraction
### Principal component analysis
### PCA applications
### Principal Component selection
