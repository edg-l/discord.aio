pydiscord
=========
.. image:: https://readthedocs.org/projects/pydiscord/badge/?version=latest
  :target: http://pydiscord.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

Currently under early development

.. role:: bash(code)
   :language: bash

Local development
-----------------
- :bash:`cd pydiscord && pip3 install -e .` (Will create a symlink to this module)

Building the documentation
--------------------------
- :bash:`sudo apt install python3-sphinx`
- :bash:`pip3 install sphinx_rtd_theme recommonmark`
- :bash:`cd docs/ && make html`