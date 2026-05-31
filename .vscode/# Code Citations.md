# Code Citations

## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```


## License: unknown
https://github.com/dmbryson/apto/blob/9184c91a3a82297c420540baaf355aac80213a29/include/apto/platform/Platform.h

```
---

## 根本原因

`Platform.h` の `LIB_EXPORT` 定義において、**`BUILDING_DLL` が未定義の場合、MSVC では `__declspec(dllexport)` のままになっているが、GNUC では `__declspec(dllimport)` に正しく変わっている** ためです。

Windows/MSVC でリンクする際の流れ：

1. **`aptoshared` (apto.dll) をビルド時**：`BUILDING_DLL` が定義される → `LIB_EXPORT = __declspec(dllexport)` → MAX_SEED/UPPER_BOUND が DLL にエクスポート
2. **`avida` をビルド時**：`BUILDING_DLL` が未定義 → **`LIB_EXPORT = __declspec(dllexport)` のまま**（間違い）
3. **リンカーから見ると**：「MAX_SEED/UPPER_BOUND は export すべき外部シンボル」と判断 → DLL から import するための情報がない → `LNK2001`

正しくは、`avida` ビルド時に `LIB_EXPORT = __declspec(dllimport)` であるべきです（GNUC と同じ）。

---

## 修正ファイルパス

`c:\avida\libs\apto\include\apto\platform\Platform.h`

---

## 修正前コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)   // ← 問題：ここで dllimport にすべき
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllimport))
#  else
#   define LIB_EXPORT
#  endif
# endif
```

---

## 修正後コード

```cpp
// Visibility
#if APTO_PLATFORM(WINDOWS)
# ifdef BUILDING_DLL
#  if APTO_PLATFORM(MSVC)
#   define LIB_EXPORT __declspec(dllexport)
#  elif APTO_PLATFORM(GNUC)
#   define LIB_EXPORT __attribute__((dllexport))
#  else
#   define LIB_EXPORT
#  endif
# else
#  if APTO_PLATFORM(MSVC)
#   define
```

