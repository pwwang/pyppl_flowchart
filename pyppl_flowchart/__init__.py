"""Flowchart plugin for PyPPL"""
# pylint: disable=invalid-name
import sys
from pathlib import Path
from pyppl.plugin import hookimpl, prerun, addmethod
from pyppl.logger import logger, THEMES, LEVELS_ALWAYS
from pyppl.proctree import ProcTree
from .flowchart import Flowchart

__version__ = "0.0.3"

LOGGER_THEME = dict(
	greenOnBlack   = dict(FCHART = '{f.GREEN}'),
	blueOnBlack    = dict(FCHART = '{f.BLUE}'),
	magentaOnBlack = dict(FCHART = '{f.MAGENTA}'),
	greenOnWhite   = dict(FCHART = '{f.GREEN}'),
	blueOnWhite    = dict(FCHART = '{f.BLUE}'),
	magentaOnWhite = dict(FCHART = '{f.MAGENTA}'),
)

class ProcHideError(Exception):
	"""Raise when a process cannot be hidden in the flowchart"""

@hookimpl
def setup(config):
	"""
	Setup the plugin
	"""
	for theme, colors in THEMES.items():
		colors.update(LOGGER_THEME.get(theme, {}))
	LEVELS_ALWAYS.add('FCHART')
	config['hide'] = False
	config['_flowchart'] = dict(theme = 'default')

def allPathsWithoutHidden(allpaths):
	"""
	Get all paths without hidden processes
	"""
	logger.debug('ALL ROUTES:')
	ret = []
	for apath in allpaths:
		# end -> start
		# check starts and ends, they cannot hide
		if apath[0].hide:
			raise ProcHideError(apath[0].name() + ': end process cannot hide.')
		if apath[-1].hide:
			raise ProcHideError(apath[-1].name() + ': start process cannot hide.')
		hidden = [proc for proc in apath if proc.hide]
		for hid in hidden:
			node = ProcTree.NODES[hid]
			if len(node.prev) > 1 and len(node.next) > 1:
				raise ProcHideError(hid.name() + ': cannot be hidden in flowchart as it has both more than 1 parents and offsprings.')
			apath.remove(hid)
		if apath not in ret:
			# merge procset
			paths = []
			for proc in reversed(apath):
				if not proc.procset:
					paths.append(proc.name())
				elif not paths or '[@' + proc.procset + ']' != paths[-1]:
					paths.append('[@' + proc.procset + ']')
			logger.debug('  %s', ' -> '.join(paths))
			ret.append(apath)
	return ret

@prerun
def pypplFlowchart (ppl, fcfile = None, dotfile = None):
	"""@API
	Generate graph in dot language and visualize it.
	@params:
		dotfile (file): Where to same the dot graph.
			- Default: `None` (`path.splitext(sys.argv[0])[0] + ".pyppl.dot"`)
		fcfile (file):  The flowchart file.
			- Default: `None` (`path.splitext(sys.argv[0])[0] + ".pyppl.svg"`)
			- For example: run `python pipeline.py` will save it to `pipeline.pyppl.svg`
	@returns:
		(PyPPL): The pipeline object itself.
	"""
	allpaths = allPathsWithoutHidden(ppl.tree.getAllPaths())
	fcfile  = fcfile or (Path('.') / Path(sys.argv[0]).stem).with_suffix(
		'%s.pyppl.svg' % ('.' + str(ppl.counter) if ppl.counter else ''))
	dotfile = dotfile if dotfile else Path(fcfile).with_suffix('.dot')
	fchart  = Flowchart(fcfile = fcfile, dotfile = dotfile)
	fchart.setTheme(ppl.config._flowchart.theme)

	for apath in allpaths:
		fchart.addNode(apath[0], 'end')
		fchart.addNode(apath[-1], 'start')
		for i, proc in enumerate(apath):
			if i == 0:
				continue
			if i < len(apath) - 1:
				fchart.addNode(proc)
			fchart.addLink(proc, apath[i-1])

	fchart.generate()
	logger.fchart('Flowchart file saved to: %s', fchart.fcfile)
	logger.fchart('DOT file saved to: %s', fchart.dotfile)

@hookimpl
def pypplInit(ppl):
	"""
	Initiate pipeline
	"""
	addmethod(ppl, 'flowchart', pypplFlowchart)
