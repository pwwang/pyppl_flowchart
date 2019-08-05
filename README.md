# pyppl-flowchart
Flowchart generator for [PyPPL](https://github.com/pwwang/PyPPL).

## Installation
```shell
pip install pyppl-flowchart
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
p3.hide = True
# into:
# p1 -> p2 -> p4 -> p5
```

### Theming

In your configuration:
```yaml
default:
	_flowchart:
		theme: default
	# other default configurations
# other profiles
```

We have two builtin themes: `default` and `dark`:

![default](https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl.png)

![dark](https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl_dark.png)

You can also default your own theme in the configuration:
```yaml
default:
	_flowchart:
		theme:
			base:
				shape: box
				style: rounded,filled
				fillcolor: "#ffffff"
				color: "#000000"
				fontcolor: "#000000"
			start:
				style: filled
				color: "#259229"
			end:
				style: filled
				color: "#d63125"
			export:
				fontcolor: "#c71be4"
			skip:
				fillcolor: "#eaeaea"
			skip+:
				fillcolor: "#b5b3b3"
			resume:
				fillcolor: "#b9ffcd"
			resume+:
				fillcolor: "#58b773"
			procset:
				style: filled
				color: "#eeeeee"
```
