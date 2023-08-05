WebParser
=========


Description
-----------
Tiny framework for parsing web.

**Crawler.py** module provides base class for webparser, it can

- open webpages with selenium webdriver;
- run a set of parsers;
- handle selenium exceptions;
- log success and log fail.


Usage
-----

Important
'''''''''

To use a remote webdriver don't forget to start selenium server.

.. code-block:: bash

    $ java -jar selenium-server-standalone.jar


Example
'''''''

Create module contains parsers:

.. code-block:: python

    #-------[ amazon.py ]---------------------------------------------------
        from webparser.crawler import Crawler

        class AmazonBook(Crawler):
            def __init__(self, url=None):
                self.parsers = {self.parse_title, self.parse_cover_url}
                super().__init__(url)

            def parse_title(self):
                title = self.webdriver.find_element_by_xpath(
                    "//span[@id='productTitle'][1]"
                ).get_attribute('innerHTML')
                self.data['title'] = title
                if title:
                    return None
                return 'Title not found.'

            def parse_cover_url(self):
                cover_url = self.webdriver.find_element_by_xpath(
                    "//img[@id='imgBlkFront'][1]"
                ).get_attribute('src')
                self.data['cover_url'] = cover_url
                if cover_url:
                    return None
                return 'Cover url not found.'
    #-----------------------------------------------------------------------


Create parsers:

.. code-block:: python

    # Example script 01:
    #-------[ parser.py ]---------------------------------------------------
        from webparser.amazon import AmazonBook

        amazon_book = AmazonBook('http://...')  # Load webpage and parse it
        print(amazon_book.data['title'])        # Print parsed book title
        print(amazon_book.data['cover_url'])    # Print parsed url title
    #-----------------------------------------------------------------------

    # Example script 02:
    #-------[ parser.py ]---------------------------------------------------
        from webparser.amazon import AmazonBook

        amazon_book = AmazonBook()        # Create object
        amazon_book.get('http://...')     # Load webpage
        amazon book.parse_title()         # Parse book title
        print(amazon_book.data['title'])  # Print parsed book title
    #-----------------------------------------------------------------------


Guideline
---------

Webdriver
'''''''''

Change default webdriver for new objects

.. code-block:: python

    Crawler.webdriver = None
    Crawler.webdriver_default = lambda : Crawler.init_webdriver_chrome_remote(ip, port)

Change default webdriver for new objects of selected class

.. code-block:: python

    AmazonBook.webdriver = None
    AmazonBook.webdriver_default = lambda : Crawler.init_webdriver_chrome_remote(ip, port)

Change webdriver for selected object

.. code-block:: python

    myobject.webdriver = Crawler.init_webdriver_chrome_remote(ip, port)


Child classes
'''''''''''''

Realization of parsers should be placed in child classes. See the example of child class in the Example section.

Child class should have constructor

.. code-block:: python

    def __init__(self, url=None):
        self.parsers = {self.parse_title}  # Set of routine parsers
        super().__init__(url)              # Parent class constructor

Child class should have parsers

.. code-block:: python

    def parse_title(self):          # Recommend to begin name with 'parser_'
        '''Parses book title.'''    # Docstring is important for logs
        title = self.webdriver.find_element_by_xpath(
            "//span[@id='productTitle'][1]"
        ).get_attribute('src')      # Recommend to retrieve data with xpath
        self.data['title'] = title  # Data should be stored in data[]
        if title:
            return None             # If success, return None
        return 'Title not found.'   # If failed, return error message

Recommend to make separate class for each webpage type,
and separate module (with several classes) for each website.
Example: module "amazon.py" with classes "AmazonBook", "AmazonCoupons".


Logging
'''''''

Level WARNINGS

* logs fail messages.

Level INFO

* logs exception messages about fails;
* logs success messages.

Set log level in your script:

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.INFO)


Copyright
---------
Copyright (c) 2017 Mikhail Ananyevskiy


License
-------

This programm is free software; you can redistribute it and/or modify
it under the terms of

**MIT License**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
