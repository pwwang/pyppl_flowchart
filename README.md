# pyppl_flowchart

[![Pypi][3]][4] [![Github][5]][6] [![PyPPL][7]][1] [![PythonVers][8]][4] [![Travis building][10]][11] [![Codacy][12]][13] [![Codacy coverage][14]][13]

Flowchart generator for [PyPPL](https://github.com/pwwang/PyPPL).

## Installation
```shell
pip install pyppl_flowchart
```

## Usage

### Generating flowchart for your pipeline
```python
# process definition

PyPPL().start(...).flowchart(fcfile = '/path/to/your/flowchart.svg').run()
```

### Hiding some processes from flowchart
```python
# Turn
# p1 -> p2 -> p3 -> p4 -> p5
p3.config.flowchart_hide = True
# into:
# p1 -> p2 -> p4 -> p5
```

### Theming

In your configuration:
```toml
[default.flowchart]
theme = "dark"

# other configuration
```

We have two builtin themes: `default` and `dark`:

![default](https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl.png)

![dark](https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl_dark.png)

You can also default your own theme in the configuration:
```toml
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
```

[1]: https://github.com/pwwang/PyPPL
[2]: https://pyppl_flowchart.readthedocs.io/en/latest/
[3]: https://img.shields.io/pypi/v/pyppl_flowchart?style=flat-square
[4]: https://pypi.org/project/pyppl_flowchart/
[5]: https://img.shields.io/github/tag/pwwang/pyppl_flowchart?style=flat-square
[6]: https://github.com/pwwang/pyppl_flowchart
[7]: https://img.shields.io/github/tag/pwwang/pyppl?label=PyPPL&style=flat-square
[8]: https://img.shields.io/pypi/pyversions/pyppl_flowchart?style=flat-square
[10]: https://img.shields.io/travis/pwwang/pyppl_flowchart?style=flat-square
[11]: https://travis-ci.org/pwwang/pyppl_flowchart
[12]: https://img.shields.io/codeclimate/maintainability-percentage/pwwang/pyppl_flowchart?style=flat-square
[13]: https://app.codacy.com/project/pwwang/pyppl_flowchart/dashboard
[14]: https://img.shields.io/codeclimate/coverage/pwwang/pyppl_flowchart?style=flat-square
