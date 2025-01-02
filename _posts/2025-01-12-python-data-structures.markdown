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


Điều đầu tiên cần lưu ý là việc sử dụng `collections.namedtuple` để xây dựng một lớp đơn giản đại diện cho từng quân bài. Chúng ta sử dụng `namedtuple` để tạo ra các lớp đối tượng chỉ là tập hợp các thuộc tính mà không có phương thức tùy chỉnh nào, giống như một bản ghi cơ sở dữ liệu. 

Trong ví dụ này, chúng ta sử dụng nó để cung cấp một cách biểu diễn đẹp mắt cho các quân bài trong bộ bài, như được hiển thị trong phiên làm việc trên console:

```python
>>> beer_card = Card('7', 'diamonds')
>>> beer_card
Card(rank='7', suit='diamonds')
```

Công cụ này giúp tạo ra các kiểu dữ liệu đơn giản, giống như một cách để lưu trữ thông tin. Trong trường hợp này, nó được dùng để tạo ra một kiểu dữ liệu "quân bài" với hai thuộc tính là "rank" (hạng) và "suit" (chất). 


Tuy nhiên, điểm mấu chốt của ví dụ này nằm ở lớp `FrenchDeck`. Mặc dù ngắn gọn, nhưng nó chứa đựng nhiều sức mạnh.

Đầu tiên, giống như bất kỳ tập hợp Python tiêu chuẩn nào, một bộ bài (`deck`) phản hồi hàm `len()` bằng cách trả về số lượng quân bài trong đó:

```python
>>> deck = FrenchDeck()
>>> len(deck)
52
```

Việc đọc các quân bài cụ thể từ bộ bài - chẳng hạn như quân bài đầu tiên hoặc cuối cùng - rất dễ dàng, nhờ phương thức `__getitem__`:

```python
>>> deck[0]
Card(rank='2', suit='spades')
>>> deck[-1]
Card(rank='A', suit='hearts')
```

Chúng ta có nên tạo một phương thức để chọn một quân bài ngẫu nhiên không? Không cần thiết. Python đã có sẵn một hàm để lấy một phần tử ngẫu nhiên từ một chuỗi: `random.choice`. Chúng ta có thể sử dụng nó trên một instance của bộ bài:

```python
>>> from random import choice
>>> choice(deck)
Card(rank='3', suit='hearts')
>>> choice(deck)
Card(rank='K', suit='spades')
>>> choice(deck)
Card(rank='2', suit='clubs')
```

Chúng ta vừa thấy hai lợi ích của việc sử dụng các phương thức đặc biệt để tận dụng python data model:

*   Người dùng không phải ghi nhớ các tên phương thức tùy ý cho các thao tác tiêu chuẩn. ("Làm thế nào để lấy số lượng phần tử? Là `.size()`, `.length()`, hay cái gì khác?")
*   Dễ dàng hơn để hưởng lợi từ Python standard library và tránh việc "phát minh lại bánh xe", như hàm `random.choice`.

**But it gets better.**

Vì `__getitem__` delegates cho toán tử `[]` của `self._cards`, bộ bài của chúng ta tự động hỗ trợ slicing:

```python
>>> deck[:3]
[Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]
>>> deck[12::13] #deck[start:stop:step]
[Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'), Card(rank='A', 'suit='clubs'), Card(rank='A', suit='hearts')]
```

Chỉ bằng cách triển khai phương thức đặc biệt `__getitem__`, chúng ta cũng có thể chạy các vòng lặp:

```python
>>> for card in deck: # doctest: +ELLIPSIS
...     print(card)
Card(rank='2', suit='spades')
Card(rank='3', suit='spades')
Card(rank='4', suit='spades')
...
```

Theo thứ tự ngược lại:

```python
>>> for card in reversed(deck):
...     print(card)
Card(rank='A', suit='hearts')
Card(rank='K', suit='hearts')
Card(rank='Q', suit='hearts')
...
```
Việc lặp lại thường là ngầm định. Nếu một tập hợp không có phương thức `__contains__`, toán tử `in` sẽ thực hiện quét tuần tự. Trường hợp điển hình: `in` hoạt động với lớp `FrenchDeck` của chúng ta vì nó có thể lặp lại được. Hãy xem thử:

```python
>>> Card('Q', 'hearts') in deck
True
>>> Card('7', 'beasts') in deck
False
```

Còn việc sắp xếp thì sao? Một hệ thống xếp hạng quân bài phổ biến là theo hạng (với quân Át là cao nhất), sau đó theo chất theo thứ tự bích (cao nhất), cơ, rô và chuồn (thấp nhất). Dưới đây là một hàm xếp hạng quân bài theo quy tắc đó, trả về 0 cho quân 2 chuồn và 51 cho quân Át bích:

```python
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
```

Với hàm `spades_high`, giờ đây chúng ta có thể liệt kê bộ bài theo thứ tự tăng dần:

```python
>>> for card in sorted(deck, key=spades_high):
...     print(card)
Card(rank='2', suit='clubs')
Card(rank='2', suit='diamonds')
Card(rank='2', suit='hearts')
... (46 cards omitted)
Card(rank='A', suit='diamonds')
Card(rank='A', suit='hearts')
Card(rank='A', suit='spades')
# doctest: +ELLIPSIS
```

Mặc dù `FrenchDeck` kế thừa ngầm định từ lớp `object`, nhưng hầu hết chức năng của nó không phải được kế thừa mà đến từ việc tận dụng data model và kỹ thuật composition. Bằng cách triển khai các phương thức đặc biệt `__len__` và `__getitem__`, lớp `FrenchDeck` của chúng ta hoạt động giống như một standard Python sequence, cho phép nó hưởng lợi từ các tính năng cốt lõi của ngôn ngữ (ví dụ: iteration và slicing)) và từ standard library, như được hiển thị trong các ví dụ sử dụng `random.choice`, `reversed` và `sorted`. Nhờ kỹ thuật composition, việc triển khai `__len__` và `__getitem__` có thể delegate toàn bộ công việc cho một đối tượng list, `self._cards`.

### How Special Methods Are Used


## Chapter 2. An array of sequences

## Chapter 3. Dictionaries and Sets

## Chapter 4. Unicode Text versus bytes

## Chapter 5. Data class Builders

## Chapter 6. Object reference, Mutability and Recycling

