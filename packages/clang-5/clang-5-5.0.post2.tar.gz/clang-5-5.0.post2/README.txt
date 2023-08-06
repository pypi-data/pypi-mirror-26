# python-clang5
Python bindings for clang from clang release branches

This is the python bindings subdir of llvm clang repository.
https://github.com/llvm-mirror/clang/tree/master/bindings/python

Specifically, it's from the **release_50** branch.

This is a non-official fork. Mainly for Pypi packaging purposes.
The pypi package is not official either.

Test:
-----

You may need to alter `LD_LIBRARY_PATH` so that the Clang library can be
found. The unit tests are designed to be run with `nosetests`. For example:

```shell
$ env PYTHONPATH=$(echo ~/llvm/tools/clang/bindings/python/) \
      LD_LIBRARY_PATH=$(llvm-config --libdir) \
  nosetests -v
tests.cindex.test_index.test_create ... ok
...
```

Credit to [trolldbois/python-clang](https://github.com/trolldbois/python-clang)
for the original repository, which is no longer maintained. This isn't a fork
because I am not maintaining the older branches from that repository.
