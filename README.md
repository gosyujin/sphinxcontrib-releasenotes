sphinxcontrib-releasenotes
==========================

Sphinx 拡張 + Sphinxを導入するためのあれこれ

setting
-------

append `conf.py`

..

try:
    import sphinxcontrib.releasenotes
    sys.path.append(os.path.abspath('exts/sphinxcontrib-releasenotes/'))
    extensions += ['sphinxcontrib.releasenotes']
except:
    pass

example
-------

..

.. releasenotes::
   :sur: 山田
   :app: 鈴木
