sphinxcontrib-releasenotes
==========================

Sphinx 拡張 + Sphinxを導入するためのあれこれ

## setting

- clone

```
$ cd SPHINX_PROJECT/source
$ mkdir exts
$ cd exts
$ git clone https://github.com/gosyujin/sphinxcontrib-releasenotes.git
```

- append `conf.py`

```python
try:
    sys.path.append(os.path.abspath('exts/sphinxcontrib-releasenotes/sphinxcontrib'))
    import releasenotes
    extensions += ['releasenotes']
except:
    pass
```

## example

```
.. releasenotes::
   :sur: 山田
   :app: 鈴木
```
