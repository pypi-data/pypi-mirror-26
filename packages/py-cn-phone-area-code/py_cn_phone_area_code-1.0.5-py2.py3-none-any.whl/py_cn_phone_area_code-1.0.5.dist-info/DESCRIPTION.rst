# py-cn-phone-area-code


Python lib , convert phone to area code , or find area phone code


https://github.com/netroby/py-cn-phone-area-code

## Install

>From pip

https://pypi.python.org/pypi/py-cn-phone-area-code

```
pip install -U py-cn-phone-area-code
```

## Usage


to use it, see tests

```

from py_cn_phone_area_code import *

def main():
     print(find_area_by_phone("0595")) # == "泉州"
     print(find_phone_by_area("泉州")) #== "0595"

```



