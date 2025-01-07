---
layout: post
title: "[Fluent python] Chapter 3. Dictionaries and Sets"
date: 2025-01-07 09:00:00 +0700
categories: fluent python
---

Chúng ta sử dụng **dictionaries** trong tất cả các chương trình Python. Nếu không trực tiếp trong code, thì gián tiếp bởi vì kiểu **dict** là một phần cơ bản trong cách triển khai của Python. Các thuộc tính của Class và instance, **namespaces** của module, và các **keyword arguments** của hàm là một số cấu trúc cốt lõi của Python được biểu diễn bằng **dictionaries** trong bộ nhớ. `__builtins__.__dict__` lưu trữ tất cả các kiểu, đối tượng và hàm tích hợp sẵn.

Do vai trò quan trọng của chúng, các **dicts** trong Python được tối ưu hóa cao — và tiếp tục được cải thiện. **Hash tables** là động cơ đằng sau hiệu suất cao của **dicts** trong Python. Các kiểu dữ liệu tích hợp sẵn khác dựa trên **hash tables** là **set** và **frozenset**. Chúng cung cấp các **API** và toán tử phong phú hơn so với các **sets** mà bạn có thể đã gặp trong các ngôn ngữ phổ biến khác. Đặc biệt, các **sets** trong Python triển khai tất cả các phép toán cơ bản từ lý thuyết tập hợp, như hợp, giao, kiểm tra tập con, v.v. Với chúng, chúng ta có thể thể hiện các thuật toán theo cách khai báo hơn, tránh nhiều vòng lặp lồng nhau và câu lệnh điều kiện.

### Modern dict Syntax

#### dict Comprehensions

Kể từ Python 2.7, cú pháp của **listcomps** và **genexps** đã được điều chỉnh cho **dict comprehensions** (và cả **set comprehensions**, mà chúng ta sẽ sớm tìm hiểu). Một **dictcomp** (**dict comprehension**) xây dựng một instance **dict** bằng cách lấy các cặp `key:value` từ bất kỳ **iterable** nào.

Ví dụ 3-1 cho thấy cách sử dụng **dict comprehensions** để xây dựng hai **dictionaries** từ cùng một danh sách các **tuples**.

Ví dụ 3-1. Ví dụ về **dict comprehensions**

```python
>>> dial_codes = [
...(880, 'Bangladesh'),
...(55, 'Brazil'),
...(86, 'China'),
...(91, 'India'),
...(62, 'Indonesia'),
...(81, 'Japan'),
...(234, 'Nigeria'),
...(92, 'Pakistan'),
...(7,'Russia'),
...(1,'United States'),]
>>> country_dial = {country: code for code, country in dial_codes}
>>> country_dial
{'Bangladesh': 880, 'Brazil': 55, 'China': 86, 'India': 91, 'Indonesia': 62,
'Japan': 81, 'Nigeria': 234, 'Pakistan': 92, 'Russia': 7, 'United States': 1}
>>> {code: country.upper()
...
for country, code in sorted(country_dial.items())
...
if code < 70}
{55: 'BRAZIL', 62: 'INDONESIA', 7: 'RUSSIA', 1: 'UNITED STATES'}
```

Một **iterable** gồm các cặp `key-value` như `dial_codes` có thể được truyền trực tiếp đến **constructor** của **dict**, nhưng…

…ở đây chúng ta hoán đổi các cặp: `country` là **key**, và `code` là **value**.

Sắp xếp `country_dial` theo tên, đảo ngược các cặp một lần nữa, viết hoa các **values**, và lọc các mục có `code < 70`.

Nếu bạn đã quen với **listcomps**, **dictcomps** là một bước tiếp theo tự nhiên. Nếu bạn chưa quen, thì việc mở rộng cú pháp **comprehension** có nghĩa là bây giờ việc thành thạo nó sẽ có lợi hơn bao giờ hết.

#### Unpacking Mappings

PEP 448—Additional Unpacking Generalizations đã tăng cường hỗ trợ cho việc **unpacking mappings** theo hai cách, kể từ Python 3.5.

Đầu tiên, chúng ta có thể áp dụng `**` cho nhiều hơn một đối số trong một lệnh gọi hàm. Điều này hoạt động khi tất cả các **keys** đều là chuỗi và duy nhất trên tất cả các đối số (vì các **keyword arguments** trùng lặp bị cấm):

```python
>>> def dump(**kwargs):
...
return kwargs
...
>>> dump(**{'x': 1}, y=2, **{'z': 3})
{'x': 1, 'y': 2, 'z': 3}
```

Thứ hai, `**` có thể được sử dụng bên trong một **dict literal** — cũng nhiều lần:

```python
>>> {'a': 0, **{'x': 1}, 'y': 2, **{'z': 3, 'x': 4}}
{'a': 0, 'x': 4, 'y': 2, 'z': 3}
```

Trong trường hợp này, các **keys** trùng lặp được phép. Các lần xuất hiện sau sẽ ghi đè lên các lần xuất hiện trước đó — hãy xem giá trị được ánh xạ tới `x` trong ví dụ.

Cú pháp này cũng có thể được sử dụng để hợp nhất các **mappings**, nhưng có những cách khác. Vui lòng đọc tiếp.

#### Merging Mappings with |

Python 3.9 hỗ trợ sử dụng `|` và `|=` để hợp nhất các **mappings**. Điều này hợp lý, vì đây cũng là các toán tử hợp của **set**.

Toán tử `|` tạo ra một **mapping** mới:

```python
>>> d1 = {'a': 1, 'b': 3}
>>> d2 = {'a': 2, 'b': 4, 'c': 6}
>>> d1 | d2
{'a': 2, 'b': 4, 'c': 6}
```

Thông thường, kiểu của **mapping** mới sẽ giống với kiểu của toán hạng bên trái —`d1` trong ví dụ — nhưng nó có thể là kiểu của toán hạng thứ hai nếu các kiểu do người dùng định nghĩa có liên quan, theo các quy tắc quá tải toán tử mà chúng ta sẽ khám phá trong Chương 16.

Để cập nhật một **mapping** hiện có tại chỗ, hãy sử dụng `|=`. Tiếp tục từ ví dụ trước, `d1` đã không bị thay đổi, nhưng bây giờ nó sẽ là:

```python
>>> d1
{'a': 1, 'b': 3}
>>> d1 |= d2
>>> d1
{'a': 2, 'b': 4, 'c': 6}
```

### Pattern Matching with Mappings

Câu lệnh `match/case` hỗ trợ các đối tượng là mapping. Các mẫu cho mapping trông giống như khai báo `dict`, nhưng chúng có thể khớp với các instance của bất kỳ lớp con thực tế hoặc ảo nào của `collections.abc.Mapping`.

Trong Chương 2, chúng ta chỉ tập trung vào các mẫu chuỗi, nhưng các loại mẫu khác nhau có thể được kết hợp và lồng vào nhau. Nhờ vào việc giải cấu trúc, so khớp mẫu là một công cụ mạnh mẽ để xử lý các bản ghi được cấu trúc giống như các mapping và chuỗi lồng nhau, mà chúng ta thường cần đọc từ các API JSON và cơ sở dữ liệu với lược đồ bán cấu trúc, như MongoDB, EdgeDB hoặc PostgreSQL. Ví dụ 3-2 minh họa điều đó. Các gợi ý kiểu đơn giản trong `get_creators` cho thấy rõ ràng rằng nó nhận một `dict` và trả về một `list`.

**Ví dụ 3-2.** `creator.py`: `get_creators()` trích xuất tên của người tạo từ các bản ghi phương tiện

```python
def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            return names
        case {'type': 'book', 'api': 1, 'author': name}:
            return [name]
        case {'type': 'book'}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:
            return [name]
        case _:
            raise ValueError(f'Invalid record: {record!r}')

# Khớp với bất kỳ mapping nào có 'type': 'book', 'api': 2 và key 'authors' 
# được ánh xạ tới một chuỗi. Trả về các mục trong chuỗi, dưới dạng một list mới.
# Khớp với bất kỳ mapping nào có 'type': 'book', 'api': 1 và key 'author' 
# được ánh xạ tới bất kỳ đối tượng nào. Trả về đối tượng bên trong một list.
# Bất kỳ mapping nào khác có 'type': 'book' là không hợp lệ, raise ValueError.
# Khớp với bất kỳ mapping nào có 'type': 'movie' và key 'director' được ánh xạ tới 
# một đối tượng duy nhất. Trả về đối tượng bên trong một list.
# Bất kỳ đối tượng nào khác là không hợp lệ, raise ValueError.
```

Ví dụ 3-2 cho thấy một số cách thực hành hữu ích để xử lý dữ liệu bán cấu trúc như các bản ghi JSON:

* Bao gồm một trường mô tả loại bản ghi (ví dụ: `'type': 'movie'`)
* Bao gồm một trường xác định phiên bản lược đồ (ví dụ: `'api': 2`) để cho phép sự phát triển trong tương lai của các API công khai
* Có các mệnh đề `case` để xử lý các bản ghi không hợp lệ của một loại cụ thể (ví dụ: `'book'`), cũng như một mệnh đề bắt tất cả

Bây giờ, hãy xem cách `get_creators` xử lý một số doctest cụ thể:

```python
>>> b1 = dict(api=1, author='Douglas Hofstadter', 
... type='book', title='Gödel, Escher, Bach')
>>> get_creators(b1)
['Douglas Hofstadter']
>>> from collections import OrderedDict
>>> b2 = OrderedDict(api=2, type='book', 
... title='Python in a Nutshell', 
... authors='Martelli Ravenscroft Holden'.split())
>>> get_creators(b2)
['Martelli', 'Ravenscroft', 'Holden']
>>> get_creators({'type': 'book', 'pages': 770})
Traceback (most recent call last):
...
ValueError: Invalid 'book' record: {'type': 'book', 'pages': 770}
>>> get_creators('Spam, spam, spam')
Traceback (most recent call last):
...
ValueError: Invalid record: 'Spam, spam, spam'
```

Lưu ý rằng thứ tự của các key trong các mẫu là không liên quan, ngay cả khi đối tượng là một `OrderedDict` như `b2`.

Trái ngược với các mẫu chuỗi, các mẫu mapping thành công trên các kết quả khớp một phần. Trong các doctest, các đối tượng `b1` và `b2` bao gồm key `'title'` không xuất hiện trong bất kỳ mẫu `'book'` nào, nhưng chúng vẫn khớp.

Không cần sử dụng `**extra` để khớp với các cặp key-value bổ sung, nhưng nếu bạn muốn nắm bắt chúng dưới dạng `dict`, bạn có thể thêm tiền tố `**` vào một biến. Nó phải là biến cuối cùng trong mẫu và `**_` bị cấm vì nó sẽ là dư thừa. Một ví dụ đơn giản:

```python
>>> food = dict(category='ice cream', flavor='vanilla', cost=199)
>>> match food:
...     case {'category': 'ice cream', **details}:
...         print(f'Ice cream details: {details}')
...
Ice cream details: {'flavor': 'vanilla', 'cost': 199}
```

Trong phần "Xử lý tự động các key bị thiếu" trên trang 90, chúng ta sẽ nghiên cứu `defaultdict` và các mapping khác trong đó tra cứu key thông qua `__getitem__` (tức là `d[key]`) thành công vì các mục bị thiếu được tạo ra một cách nhanh chóng. Trong ngữ cảnh so khớp mẫu, một kết quả khớp chỉ thành công nếu đối tượng đã có các key bắt buộc ở đầu câu lệnh `match`.
