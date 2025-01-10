---
layout: post
title: "[Fluent python] Chapter 4. Unicode Text versus bytes"
date: 2025-01-10 09:00:00 +0700
categories: fluent python
---

Python 3 đã giới thiệu một sự phân biệt rõ ràng giữa chuỗi văn bản của con người (`Unicode text`) và chuỗi các byte thô (`raw bytes`). Việc chuyển đổi ngầm định (`implicit conversion`) các chuỗi byte thành văn bản Unicode đã là quá khứ. Chương này đề cập đến các chuỗi Unicode, chuỗi nhị phân (`binary sequences`) và các mã hóa (`encodings`) được sử dụng để chuyển đổi giữa chúng.

Tùy thuộc vào loại công việc bạn làm với Python, bạn có thể nghĩ rằng việc hiểu Unicode là không quan trọng. Điều đó khó xảy ra, nhưng dù sao thì cũng không thể thoát khỏi sự phân chia `str` so với `byte`. Thêm vào đó, bạn sẽ thấy rằng các kiểu chuỗi nhị phân chuyên biệt cung cấp các tính năng mà kiểu `str` "đa năng" của Python 2 không có.

### Character Issues

Khái niệm "chuỗi" (`string`) khá đơn giản: một chuỗi là một dãy các ký tự (`characters`). Vấn đề nằm ở định nghĩa của "ký tự".

Năm 2021, định nghĩa tốt nhất về "ký tự" mà chúng ta có là một ký tự Unicode. Theo đó, các mục chúng ta nhận được từ một `str` trong Python 3 là các ký tự Unicode, giống như các mục của một đối tượng `unicode` trong Python 2 — chứ không phải là các byte thô mà chúng ta nhận được từ một `str` trong Python 2.

Tiêu chuẩn Unicode tách biệt rõ ràng nhận dạng của các ký tự với các biểu diễn byte cụ thể:

*   Nhận dạng của một ký tự — điểm mã (`code point`) của nó — là một số từ 0 đến 1.114.111 (cơ số 10), được hiển thị trong tiêu chuẩn Unicode dưới dạng 4 đến 6 chữ số thập lục phân với tiền tố "U+", từ U+0000 đến U+10FFFF. Ví dụ: điểm mã cho chữ cái A là U+0041, ký hiệu Euro là U+20AC và ký hiệu âm nhạc G clef được gán cho điểm mã U+1D11E. Khoảng 13% điểm mã hợp lệ có các ký tự được gán cho chúng trong Unicode 13.0.0, tiêu chuẩn được sử dụng trong Python 3.10.0b4.
*   Các byte thực tế đại diện cho một ký tự phụ thuộc vào mã hóa (`encoding`) được sử dụng. Mã hóa là một thuật toán chuyển đổi các điểm mã thành chuỗi byte và ngược lại. Điểm mã cho chữ cái A (U+0041) được mã hóa thành một byte \x41 trong mã hóa UTF-8, hoặc là các byte \x41\x00 trong mã hóa UTF-16LE. Một ví dụ khác, UTF-8 yêu cầu ba byte — \xe2\x82\xac — để mã hóa ký hiệu Euro (U+20AC), nhưng trong UTF-16LE, cùng một điểm mã được mã hóa thành hai byte: \xac\x20.

Chuyển đổi từ điểm mã sang byte là mã hóa (`encoding`); chuyển đổi từ byte sang điểm mã là giải mã (`decoding`). Xem Ví dụ 4-1.

Ví dụ 4-1. Mã hóa và giải mã

```python
>>> s = 'café'
>>> len(s)
4
>>> b = s.encode('utf8')
>>> b
b'caf\xc3\xa9'
>>> len(b)
5
>>> b.decode('utf8')
'café'
```

`str` 'café' có bốn ký tự Unicode.

Mã hóa `str` thành `bytes` bằng cách sử dụng mã hóa UTF-8.

`bytes` literal có tiền tố b.

`bytes` b có năm byte (điểm mã cho "é" được mã hóa thành hai byte trong UTF-8).

Giải mã `bytes` thành `str` bằng cách sử dụng mã hóa UTF-8.

Mặc dù `str` trong Python 3 gần giống với kiểu `unicode` trong Python 2 với một tên mới, nhưng `bytes` trong Python 3 không chỉ đơn giản là `str` cũ được đổi tên và cũng có kiểu `bytearray` liên quan chặt chẽ. Vì vậy, điều đáng giá là xem xét các kiểu chuỗi nhị phân trước khi chuyển sang các vấn đề mã hóa/giải mã.
