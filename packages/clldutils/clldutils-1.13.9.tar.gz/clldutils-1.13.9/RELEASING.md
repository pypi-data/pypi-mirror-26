
Releasing clldutils
===================

Clone ``clld/clldutils`` and switch to the ``master`` branch. Then:

- Change version to the new version number in
  - ``setup.py``
  - ``clldutils/__init__.py``

- Do platform test via ``tox`` (making sure statement coverage is at 100%):
```shell
$ tox -r
```

- Make sure ``flake8`` passes (configuration in ``setup.cfg``):
```shell
$ flake8 clldutils
```
  
- Commit your change of the version number:
```shell
$ git commit -a -m"release <VERSION NUMBER>"
```

- Create a release tag:
```shell
$ git tag -a v<version> -m"<VERSION NUMBER> release"
```

- Make sure your Python has ``setuptools-git`` installed
```shell
$ pip install setuptools-git
```

- release to PyPI:
```shell
$ python setup.py sdist
$ twine upload dist/*
```

- Push to GitHub:
```shell
$ git push origin
$ git push --tags
```
