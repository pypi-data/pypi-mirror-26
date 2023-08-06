# 3db - three DB

[![Build Status](https://travis-ci.org/EvgenyAK/3db.svg?branch=master)](https://travis-ci.org/EvgenyAK/3db.svg?branch=master)

Небольшая БД для хранения и работы с данными используемыми при проведении [DDT](https://en.wikipedia.org/wiki/Data-driven_testing).

## Возможности хранения

### Плоский список файлов

```
числовой индекс

data_1.txt
etalon_1.txt
data_2.txt
etalon_2.txt

или в начале

0001_data.txt
0001_etalon.txt
0002_data.txt
0002_etalon.txt

или буквенный

data_A.txt
etalon_A.txt
data_B.txt
etalon_B.txt
```

### Плоская структура папок

```
0001_Single_Data/
    data_1.txt
    etalon_1.txt

0002_Few_Data/
    data_1.txt
    etalon_1.txt
    data_2.txt
    etalon_2.txt
```

### Дерево папок

```
ServiceA/
    0001_Single_Data/
        data_1.txt
        etalon_1.txt
    ....
ServiceB/
    0001_Single_Data/
        data_1.txt
        etalon_1.txt
    ....
IntegrationServiceAServiceB/
    10001_ServiceAUp_ServiceBDown/
        data_1.txt
        etalon_1.txt
    10002_ServiceADown_ServiceBUp/
        data_1.txt
        etalon_1.txt
    10003_ServiceAUp_ServiceBUp/
        data_A_1.txt
        etalon_A_1.txt
        data_B_1.txt
        data_B_1.txt
    ....
Some/
    BugFix44/
        ServiceA/
            data_1.txt
            etalon_2.txt
        ServiceB/
            data_2.txt
            etalon_2.txt
    ServiceD
        001_A/
            data_1.txt
            etalon_1.txt
```

## Тегирование данных

Часто удобно тегировать данные и производить выборки по произвольным тагам.
Теги прописываюися в фале *metadata.yaml*.
```
$ cat metadata.yaml

# навесить на все тесты таг serviceA
tags:
    - serviceA
0001:
   # теги навесить только на serviceA, serviceB
   tags:
       - serviceA
       - serviceB
0002:
   # Исключить таг serviceC
   tags:
       - serviceC:false
```

### Древовидная структура metadata.yaml
Поддержка нескольких вложенных файлов metadata.yaml для удобства разнесения тегов данных.

```
Some/
    metadata.yaml # tags: notci
    BugFix44/
        metadata.yaml # tags: bugfix
        ServiceA/
            data_1.txt
            etalon_2.txt
        ServiceB/
            data_2.txt
            etalon_2.txt
    ServiceD
        001_A/
            data_1.txt
            etalon_1.txt
```

## Примеры использования

### Поиск данных

```python
import threedb
from threedb import simple_storage

db = threedb.connect('.', type='simple')
rows = db.search()
print(rows)
>>> [('data_1.txt', 'etalon_1.txt'), ('data_2.txt', 'etalon_2.txt')]

# позвращает итератор
for part in db.isearch(".", storage=simple_storage):
    print(part)

>>> ('data_1.txt', 'etalon_1.txt')
>>> ('data_2.txt', 'etalon_2.txt')

# поиск по дереву
for part in db.search("Some"):
    print(part)

>>> ('Some/BugFix44/ServiceA/data_1.txt', 'Some/BugFix44/ServiceA/etalon_1.txt')
>>> etc.

# поиск по индексу
db.search('.', '0001' | '0002') 
db.search('.', '0001' & '0002')

# поиск по тагу
db.search('.', 'ci')
```

### Чтение данных

Чтение данных. По умолчанию все текстовые файлы читаются в память.

```python
import threedb

db = threedb.connect('.', type=simple_storage)
rows = db.load('.')
print(rows)

>>> [{"data_1_txt": "1", "etalon_1_txt": "1"}, {"data_2_txt": "2", "etalon_2_txt": "2"}]
```
