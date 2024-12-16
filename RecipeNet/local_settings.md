# Secret_keyの生成方法

1. ```$ python manage.py shell```
2. ```>>> from django.core.management.utils import get_random_secret_key```
3. ```>>> get_random_secret_key()```
---
結果: ```'xxx-xxxx'```