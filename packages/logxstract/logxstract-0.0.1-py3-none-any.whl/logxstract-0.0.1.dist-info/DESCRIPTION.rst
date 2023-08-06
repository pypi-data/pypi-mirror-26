logxstract
==========

Library for extracting xml from logs. Finds xml matching criteria and
saves results to file.

Install
-------

.. code:: shell

    $ pip install logxstract

Usage as library
----------------

.. code:: python


            from logxstract import extract_xml_from_file

            extract_xml_from_file(
                path='/item',
                body='/item',
                input_file='sample.log',
                output_file='result.txt'
            )
            #extracted xml is now in result.txt file

Usage in shell
--------------

.. code:: shell

    $ logxtract -p /item -b /item -f sample.log -o result.txt


=======
History
=======

0.0.1 (2017-11-04)
------------------

* First release on PyPI.


