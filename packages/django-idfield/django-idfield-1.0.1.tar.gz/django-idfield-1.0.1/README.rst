# django-idfield

Char ID filed for Django

Installation
============

Install it with pip (or easy_install):

```
pip install django-idfield
```

Usage
=====

```
from idfield import IDField

class MyModel(models.Model):
	id = IDField(max_length=10, readable=False, primary_key=True, editable=False)
	code = IDField(max_length=4, readable=True)
```

Notes
=====

* IDField is not a completely unique ID. The larger value of **max_length** makes less collisions possible.
* IDField always generate a value, if value is not set.
* If **readable=True**, value will be generated from caps letters and numbers, which do not look alike.
