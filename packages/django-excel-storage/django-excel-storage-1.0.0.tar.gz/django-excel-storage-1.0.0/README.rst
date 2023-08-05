====================
django-excel-storage
====================

Installation
============

::

    pip install django-excel-storage


Usage
=====

::

    from excel_storage import ExcelStorage

    def excelfunc():
        objs = SomeModel.objects.all()
        fpath = ExcelStorage(data).save()


or::

    from excel_storage import ExcelStorage

    def excelfunc():
        data = [
            ['Column 1', 'Column 2'],
            [1, 2],
            [3, 4]
        ]
        fpath = ExcelStorage(data, 'my_data', font='name SimSum')


Params
======

* font='name SimSum'
    * Set Font as SimSum(宋体)
* force_csv=True
    * CSV Format? True for Yes, False for No, Default is False


CSV
===

+-----------------+----------------+----------------+----------------+-------------+
|                 | Win Excel 2013 | Mac Excel 2011 | Mac Excel 2016 | Mac Numbers |
+=================+================+================+================+=============+
| UTF8            | Messy          | Messy          |                | Normal      |
+-----------------+----------------+----------------+----------------+-------------+
| GB18030         | Normal         | Normal         |                | Messy       |
+-----------------+----------------+----------------+----------------+-------------+
| UTF8 + BOM_UTF8 | Normal         | Messy          |                | Normal      |
+-----------------+----------------+----------------+----------------+-------------+
