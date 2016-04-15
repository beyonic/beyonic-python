# Beyonic Python Library

##### Installing dependencies
Please run following command to install dependencies:
```
pip install -r requirements/test.txt
```

##### Adding new api model
To create new api model you should perform below mentioned steps:
- Create a file under beyonic/apis folder containing a class for newly added model. See other file there for your reference.
- add import statement in ```beyonic/__init__.py``` file. E.g. ```from beyonic.apis.collection import CollectionRequest```


#### Testing:

##### Test execution


```sh
$ nosetests --with-coverage  --cover-html --cover-package=beyonic
...............................................................................
```

You can get detailed coverage report at cover/index.html, after tests has been ran.

##### API Mocking
For mocks [vcrpy](https://github.com/kevin1024/vcrpy) is used.
All recorded API interactions cassettes located on vcr_cassettes/ folder.
They can be deleted, in this case on next tests run specs will access to real API and cassettes will be recorded again.

### Releasing
To release a new version:
- Increment the version number in setup.py
- Push all code
- Run "python setup.py sdist upload -r pypi" to upload to pypi (You may need to follow the steps at http://peterdowns.com/posts/first-time-with-pypi.html)
