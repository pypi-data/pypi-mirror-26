
Condition Chain
===============

Process a series of conditional judgement with a chained call.

Example
-------

>>> from condition_chain import Condition
>>> condition = Condition(1).be(2).equal(2.0 - 2)\
        .differ('a').instance_of(str).expect(lambda x: x, 1)
>>> print(condition.result(), condition.success, condition.failures, sep='\n')
False
[('be', 2), ('equal', 0.0), ('differ', 'a'), ('instance_of', 'str'), ('expect', ('<lambda>', 1))]
[('be', 2), ('equal', 0.0), ('instance_of', 'str')]
>>> condition = Condition([1,2,3]).contain(1).have('append').hold(3)
True
[('contain', 1), ('have', 'append'), ('hold', 3)]
[]

Install
-------

.. code-block:: shell
pip install condition_chain

Author
------
Yixian Du (duyixian1234@outlook.com)

