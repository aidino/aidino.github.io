---
layout: post
title:  "Data structures"
date:   2025-01-02 09:00:00 +0700
categories: fluent python
---

> Khám phá thế giới cấu trúc dữ liệu Python! Note này sẽ hướng dẫn bạn về List, Tuple, Dictionary, Set và các khái niệm quan trọng như khả năng thay đổi, tham chiếu đối tượng.  Cùng nhau nâng cao kỹ năng lập trình Python thông qua việc tổ chức và lưu trữ dữ liệu hiệu quả!

[Example notebook](https://aidino.github.io/example_codes/fluent-python-c1-data-structures.ipynb)

## Chapter 1. The python data model

### A Pythonic Card Deck

{% highlight python %}
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'Zô Cơ Bích Tép'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
{% endhighlight %}

`collections.namedtuple` trong Python là một hàm tạo ra một loại tuple đặc biệt, cho phép bạn truy cập các phần tử của nó bằng tên, bên cạnh việc truy cập bằng chỉ số như tuple thông thường. 

**Lợi ích:**

* **Dễ đọc hơn:** Thay vì nhớ chỉ số, bạn có thể dùng tên để truy cập, giúp code rõ ràng và dễ hiểu hơn. Ví dụ, `card.rank` dễ hiểu hơn `card[0]`.
* **Ít lỗi hơn:**  Việc dùng tên giúp giảm thiểu lỗi do nhầm lẫn chỉ số.
* **Tự ghi chép:** Code trở nên tự giải thích hơn, dễ bảo trì hơn.




## Chapter 2. An array of sequences

## Chapter 3. Dictionaries and Sets

## Chapter 4. Unicode Text versus bytes

## Chapter 5. Data class Builders

## Chapter 6. Object reference, Mutability and Recycling

