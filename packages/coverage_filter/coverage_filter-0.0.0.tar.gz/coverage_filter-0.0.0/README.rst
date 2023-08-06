Coverage filter
===============

Allows developers to indicate which code they are trying to test when using
coverage tools.

**Warning** This is just a proof of concept. The API will likely change as I 
receive feedback. There are also no unit tests, or other code quality control
methods in place.  If you wish to use this code, please make a copy for 
yourself, so my changes won't break your build.


Example
=======

Example code to be tested: (in ``target.py``)

.. code-block::

    def target(self):
        return target_inner()
    
    def target_inner(self):
        return 42


Example unit test: (in ``test_target.py``)

.. code-block::

    from coverage_filter import CoverageFilter
    from target import target
    
    @CoverageFilter('target.py:target')
    def test_target(self):   
        assert target() == 42


For more information, check out my blog on the topic.



    