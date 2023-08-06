rpn\_calculator
===============

|LICENSE| |Maintainability|

RPN Calculator for CLI

Environment
-----------

-  Python 2.7
-  Python 3.2 or later

Supported operations
--------------------

+-------------+------------------+
| Operation   | Distraction      |
+=============+==================+
| ``+``       | Addition         |
+-------------+------------------+
| ``-``       | Subtraction      |
+-------------+------------------+
| ``*``       | Multiplication   |
+-------------+------------------+
| ``/``       | Division         |
+-------------+------------------+
| ``%``       | Residue          |
+-------------+------------------+
| ``^``       | Power            |
+-------------+------------------+

Example
-------

Case: ``10 * 5 + 2``

Pattern 1
::

    $ rpn
    > 10  
    10
    > 5*
    50
    > 2+
    52
    >


Pattern 2
::

    $ rpn
    > 10 5 * 2 +
    52
    >

Pattern 3
::

    $ rpn -e "10 5 * 2 +"
    52

.. |LICENSE| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/massongit/rpn-calculator/blob/master/LICENSE
   :alt: MIT License
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/ee4f5ab617bf49620731/maintainability
   :target: https://codeclimate.com/github/massongit/rpn-calculator/maintainability
   :alt: Maintainability
