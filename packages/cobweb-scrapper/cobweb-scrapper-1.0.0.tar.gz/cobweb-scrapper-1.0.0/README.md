# CobWeb #

This small application (possibly framework in future) is designed to automate scrapping process

## Table of contents ##

1. [Getting started](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-getting-started)
    1. [Prerequisites](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-prerequisites)
    2. [Installing](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-installing)
    3. [Example](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-example)
    4. [Response](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-response)
2. [Advanced](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-advanced)
    1. [Cobweb class](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-cobweb-class)
    2. [Spider](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-spider)
    3. [Link extractor](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-link-extractor)
    4. [Custom Adapter](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-custom-adapter)
    5. [Block Bypass System](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-block-bypass-system)
3. [Running the tests](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-running-the-tests)
4. [Authors](https://bitbucket.org/pollux_cast0r/cobweb/overview#markdown-header-authors)

## Getting started ##
### Prerequisites ###

This projects if build around following requirements:

+ requests
+ bs4
+ pygtrie
+ PyYAML

### Installing ###

To install this projects type
```shell
$ pip install cobweb_scrapper
```
in your virtual environment

### Example ###

To start your first scrapper project execute following command
```bash
$ cobweb init project_name
```

This will auto-generate some folders and main scrapper file that will look like this

```python
from cobweb import Cobweb

START_URL = "https://www.wikipedia.org/"

def process_callback(response):
    pass

if __name__ == "__main__":
    cobweb = Cobweb()
    cobweb.start_from(START_URL)
    cobweb.default_process_function = process_callback
    cobweb.populate_spiders()
    cobweb.start()

```

The above function **process_callback** can be any python callable that accepts *response* as it's first argument

### Response ###

The **Cobweb** comes with out-of-box *Response* object that represent some proxies functionality over **requests** response object

This object comes with some of a usefull properties

 property | type | description 
 :--- | :--- | :---
 status_code | int | status code of a returned response
 headers | CaseInsensitiveDict | headers-to-value mapping of a response
 cookies | CookieJar | cookies returned by server
 content | bytes/str | raw response content
 data | BeautifulSoup/BytesIO/Image | preprocessed response content (type depends on the chosen Adapter)
 apparent_encoding | str | response encoding 

To get a hands-on experience of this object usage you can type in your terminal
```bash
$ cobweb shell url
```
to open python console with pre-defined response object
```python
>>> response.status_code
200
```

## Advanced ##
### Cobweb class ###

Every scrapper starts from creating **Cobweb** object to cover all of a scrapper's logic. All configuration methods can be called directly on the instances of this class
```python
from cobweb import Cobweb

c = Cobweb()
c.follow_rules(["https://**", "http://**"])
c.exclude_rules("*.com")
c.domain_only = True
```
Above code configures scrapper to follow links that match anything given in `follow_rules` method and skip pages that match `exclude_rules`.
**Cobweb** class is a singleton object so it can be used to reference current scrapper anywhere in the project.

### Spider ###

The `populate_spiders` method that's available on Cobweb class creates given amount of spiders with default configuration. Usually it's enough but sometimes we want to configure spider ourselves.
```python
from cobweb import Cobweb
from cobweb.spiders import Spider

def do_nothing(*args, **kwargs):
    pass

if __name__ == "__main__":
    c = Cobweb()
    s = Spider()
    
    s.process_response = do_nothing
    s.on_failure_callback = do_nothing
    s.on_queue_timeout = do_nothing
    s.validator = lambda: True
    
    c.add_spider(s)
```
Default spider comes with 4 properties that can accept any function type:

Method              | Arguments | Description
------------------- |:---------:| --- 
process\_response    | response  | Obligatory callback. Spider won't start unless you set a function callback to process a response
on\_failure\_callback | response  | Optional callback. Called when server responded with bad status code
on\_queue\_timeout    |           | Optional callback. Called when scrapping queue is empty. Default behavior is to wait a little longer till new tasks appear
validator           | response  | Optional callback. Called when page is successfully retrieved. Can be used for additional filtering since return value indicated whether or not page should be processed

### Link extractor ###

The default class for retrieving links from and html page.
```python
from cobweb.link_extractor import LinkExtractor

l = LinkExtractor(
    follow="^.+\.com$",
    exclude=["^.+\.ru$", "^.+\.gb$"],
    regex_type=LinkExtractor.REGEX_REGULAR,
    mode=LinkExtractor.TRIE
)
```
**LinkExtractor** class can accept 2 types of regular expressions that can be set via class constants.

+ LinkExtractor.REGEX_REGULAR
```regexp
    ^/.+/$
```   
+ LinkExtractor.REGEX_UNIX
```regexp
    p?s*
```
### Custom Adapter ###

**Cobweb** comes with some Adapters that can help you establish a connection with the server. For example:

+ HttpAdapter 
+ FileAdapter
+ ImageAdapter

To create your own adapter you can inherit from and abstract class from `cobweb.adapters`
```python
from cobweb.adapters import AbstractAdapter

class CustomAdapter(AbstractAdapter):
    def invoke(self, url: str):
        """Called when spider wants adapter to return response"""

    def send(self, url: str):
        """Called to make an actual request for the server"""

    def prepare_request(self, url: str):
        """Method is pretty self-explanatory. Used by adapter to make a request"""
        
    def process_response(self, response):
        """Some additional postprocessing"""
```
All of these method should be overridden. Remember that when inheriting from an Abstract class you should implement all request/response logic by yourself.
To avoid unnecessary work you can inherit from **SessionAbstractAdapter** from `cobweb.adapters.session`

```python
from cobweb.adapters.session import SessionAbstractAdapter

class CustomSessionAdapter(SessionAbstractAdapter):
    def process_response(self, response):
        response = super().process_response(response)
```
In that case **SessionAbstractAdapter** will take care of establishing calls to the server. All you need is to override *process_response* method to apply your changes to *response* object.
Remember to call `super().process_response(response)` in the beginning of your custom method to call the base class **Response** constructor.

### Block Bypass System ###

The **Cobweb** has new innovational *BlockBypassSystem* (*bbs* for short) class that is not fully implemented yet.
All of it's logic is incapsulated in **BlockBypassSystem** class from `cobweb.bbs` and usually you have no need to interact with it. To disable bbs just set *use_bbs* flag in your settings class to **False**. Because all of the *Cobweb* adapters use it by default.
To enable bss in your custom adapter do the following
```python
from cobweb.adapters.session import SessionAbstractAdapter
from cobweb.bbs import BlockBypassSystem

class CustomAdapter(SessionAbstractAdapter):

    bbs = BlockBypassSystem()
    
    @bbs.monitor_requests
    def prepare_request(self, url: str):
        pass
        
    @bbs.monitor_responses
    def process_response(self, response):
        pass
```
Then you can mannualy call `self.bbs.stop()` and `self.bbs.start()` in your adapter's code.

## Running the tests ##

All tests are located inside `tests` directory. 
```bash
$ python -m unittest tests
```
 
## Authors ##

1. [Alexander Svito](https://bitbucket.org/pollux_cast0r/)