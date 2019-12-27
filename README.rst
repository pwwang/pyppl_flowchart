
pyppl_flowchart
===============

`
.. image:: https://img.shields.io/pypi/v/pyppl_flowchart?style=flat-square
   :target: https://img.shields.io/pypi/v/pyppl_flowchart?style=flat-square
   :alt: Pypi
 <https://pypi.org/project/pyppl_flowchart/>`_ `
.. image:: https://img.shields.io/github/tag/pwwang/pyppl_flowchart?style=flat-square
   :target: https://img.shields.io/github/tag/pwwang/pyppl_flowchart?style=flat-square
   :alt: Github
 <https://github.com/pwwang/pyppl_flowchart>`_ `
.. image:: https://img.shields.io/github/tag/pwwang/pyppl?label=PyPPL&style=flat-square
   :target: https://img.shields.io/github/tag/pwwang/pyppl?label=PyPPL&style=flat-square
   :alt: PyPPL
 <https://github.com/pwwang/PyPPL>`_ `
.. image:: https://img.shields.io/pypi/pyversions/pyppl_flowchart?style=flat-square
   :target: https://img.shields.io/pypi/pyversions/pyppl_flowchart?style=flat-square
   :alt: PythonVers
 <https://pypi.org/project/pyppl_flowchart/>`_ `
.. image:: https://img.shields.io/travis/pwwang/pyppl_flowchart?style=flat-square
   :target: https://img.shields.io/travis/pwwang/pyppl_flowchart?style=flat-square
   :alt: Travis building
 <https://travis-ci.org/pwwang/pyppl_flowchart>`_ `
.. image:: https://img.shields.io/codeclimate/maintainability-percentage/pwwang/pyppl_flowchart?style=flat-square
   :target: https://img.shields.io/codeclimate/maintainability-percentage/pwwang/pyppl_flowchart?style=flat-square
   :alt: Codacy
 <https://app.codacy.com/project/pwwang/pyppl_flowchart/dashboard>`_ `
.. image:: https://img.shields.io/codeclimate/coverage/pwwang/pyppl_flowchart?style=flat-square
   :target: https://img.shields.io/codeclimate/coverage/pwwang/pyppl_flowchart?style=flat-square
   :alt: Codacy coverage
 <https://app.codacy.com/project/pwwang/pyppl_flowchart/dashboard>`_

Flowchart generator for `PyPPL <https://github.com/pwwang/PyPPL>`_.

Installation
------------

.. code-block:: shell

   pip install pyppl_flowchart

Usage
-----

Generating flowchart for your pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # process definition

   PyPPL().start(...).flowchart(fcfile = '/path/to/your/flowchart.svg').run()

Hiding some processes from flowchart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Turn
   # p1 -> p2 -> p3 -> p4 -> p5
   p3.config.flowchart_hide = True
   # into:
   # p1 -> p2 -> p4 -> p5

Theming
^^^^^^^

In your configuration:

.. code-block::

   [default.flowchart]
   theme = "dark"

   # other configuration

We have two builtin themes: ``default`` and ``dark``\ :


.. image:: https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl.png
   :target: https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl.png
   :alt: default



.. image:: https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl_dark.png
   :target: https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl_dark.png
   :alt: dark


You can also default your own theme in the configuration:

.. code-block::

   [default.flowchart.theme]
   base = {
       shape = "box",
       style = "rounded,filled",
       fillcolor = "#ffffff",
       color = "#000000",
       fontcolor = "#000000"
   }
   start = { style = "filled", color = "#259229" }
   end = { style = "filled", color = "#d63125" }
   procset = { style = "filled", color: "#eeeeee" }
   edge = {}
   edge_hidden = { style = "dashed" } # for links with hidden processes
