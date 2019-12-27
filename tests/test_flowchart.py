import pytest
from itertools import chain
from pathlib import Path

try:
	from graphviz import Digraph
except ImportError:
	pytest.skip('graphviz is not installed', allow_module_level=True)

from pyppl import Proc
from pyppl_flowchart import Flowchart, THEMES, ROOTGROUP

@pytest.fixture
def p1(request):
	return Proc('p1', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)

@pytest.fixture
def p2(request):
	return Proc('p2', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)

@pytest.fixture
def p3(request):
	return Proc('p3', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)

@pytest.fixture
def p4(request):
	return Proc('p4', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)

@pytest.fixture
def p_procset1(request):
	p = Proc('p_procset1', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name + '@procset1')
	return p

@pytest.fixture
def p_procset2(request):
	p = Proc('p_procset2', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name + '@procset2')
	return p

@pytest.fixture
def p_procset3(request):
	p = Proc('p_procset3', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name + '@procset3')
	return p

@pytest.fixture
def p_tag_1st(request):
	return Proc('p_tag_1st', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)

@pytest.fixture
def p_desc(request):
	return Proc('p_desc', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name, desc = 'The description of p')

@pytest.fixture
def procs(p1, p2, p3, p4, p_procset1, p_procset2, p_procset3,
	p_tag_1st, p_desc):
	return dict(
		p1         = p1,
		p2         = p2,
		p3         = p3,
		p4         = p4,
		p_procset1 = p_procset1,
		p_procset2 = p_procset2,
		p_procset3 = p_procset3,
		p_tag_1st  = p_tag_1st,
		p_desc     = p_desc)

def teardown_module(module):
	for fcfile in chain(Path('.').glob('*.dot'), Path('.').glob('*.svg')):
		fcfile.unlink()

class TestFlowchart:
	@classmethod
	def setup_class(cls):
		cls.fc = Flowchart('', '')

	def test_init(self, tmpdir):
		self.dotfile = str(tmpdir / 'flowchart.dot')
		self.fcfile = str(tmpdir / 'flowchart.svg')
		self.fc.fcfile = self.fcfile
		self.fc.dotfile = self.dotfile
		assert isinstance(self.fc, Flowchart)
		assert isinstance(self.fc.graph, Digraph)
		assert self.fc.theme == THEMES['default']
		assert self.fc.nodes == {}
		assert self.fc.starts == []
		assert self.fc.ends == []
		assert self.fc.links == []

	@pytest.mark.parametrize('theme, tmbase, tmout', [
		('default', 'default', THEMES['default']),
		('dark', 'default', THEMES['dark']),
		({}, 'default', {
			'procset': {'color': '#eeeeee', 'style': 'filled'},
			'base': {'color': '#000000',
					'fillcolor': '#ffffff',
					'fontcolor': '#000000',
					'shape': 'box',
					'style': 'rounded,filled'},
			'edge': {},
			'edge_hidden': {'style': 'dashed'},
			'end': {'color': '#d63125', 'style': 'filled'},
			'start': {'color': '#259229', 'style': 'filled'}
		}),
		({'base': {'shape': 'circle'}}, 'dark', {
			'procset': {'color': '#eeeeee', 'style': 'filled'},
			'base': {'color': '#ffffff',
					'fillcolor': '#555555',
					'fontcolor': '#ffffff',
					'shape': 'circle',
					'style': 'rounded,filled'},
			'edge': {},
			'edge_hidden': {'style': 'dashed'},
			'end': {'color': '#ea7d75', 'penwidth': 2, 'style': 'filled'},
			'start': {'color': '#59b95d', 'penwidth': 2, 'style': 'filled'}
		})
	])
	def test_set_theme(self, theme, tmbase, tmout):
		self.fc.set_theme(theme, tmbase)
		assert self.fc.theme == tmout

	@pytest.mark.parametrize('proc, role, instarts, inends, group', [
		('p1', 'start', True, False, ROOTGROUP),
		('p2', 'end', False, True, ROOTGROUP),
		('p3', None, False, False, ROOTGROUP),
		('p_procset1', None, False, False, 'procset1'),
		('p_procset1', 'start', True, False, 'procset1'),
		('p_procset2', 'end', False, True, 'procset2'),
	])
	def test_add_node(self, procs, proc, role, instarts, inends, group):
		proc = procs[proc]
		self.fc.add_node(proc, role)
		assert (proc in self.fc.starts) == instarts
		assert (proc in self.fc.ends) == inends
		assert proc in self.fc.nodes[group]

	@pytest.mark.parametrize('n1, n2', [
		('p1', 'p2')
	])
	def test_add_link(self, procs, n1, n2):
		n1 = procs[n1]
		n2 = procs[n2]
		self.fc.add_link(n1, n2)
		assert (n1, n2, False) in self.fc.links

	@pytest.mark.parametrize('nodes, starts, ends, links, theme, basetheme, srcs', [
		(['p_tag_1st', 'p_desc', 'p1', 'p_procset1'],
		 ['p_tag_1st'],
		 ['p_procset1'],
		 [('p_tag_1st', 'p_desc'), ('p_desc', 'p1'), ('p1', 'p_procset1')],
		 'default', 'default',
		 ['digraph PyPPL {',
		  'p_tag_1st.test_assemble_and_generate', 'color="#259229"',
		  'p_desc', 'color="#000000"',
		  'p1', 'color="#000000"',
		  'subgraph cluster_procset1 {',
		  'p_procset1', 'color="#d63125"',
		  'color="#eeeeee"',
		  '"p_tag_1st.test_assemble_and_generate[',
		  ' -> "p_desc.test_assemble_and_generate[',
		  '"p_desc.test_assemble_and_generate[',
		  ' -> "p1.test_assemble_and_generate[',
		  '"p1.test_assemble_and_generate[',
		  ' -> "p_procset1.test_assemble_and_generate[']),

		(['p_tag_1st', 'p_desc', 'p1', 'p_procset1'],
		 ['p_tag_1st'],
		 ['p_procset1'],
		 [('p_tag_1st', 'p_desc'), ('p_desc', 'p1'), ('p1', 'p_procset1')],
		 'dark', 'default',
		 ['digraph PyPPL {',
		  'p_tag_1st.test_assemble_and_generate', 'color="#59b95d"',
		  'p_desc', 'color="#ffffff"',
		  'p1', 'color="#ffffff"',
		  'subgraph cluster_procset1 {',
		  'p_procset1', 'color="#ea7d75"',
		  'color="#eeeeee"',
		  '"p_tag_1st.test_assemble_and_generate', ' -> "p_desc',
		  '"p_desc', ' -> "p1',
		  '"p1', ' -> "p_procset1']),
	])
	def test_assemble_and_generate(self, tmpdir, procs, nodes, starts, ends, links, theme, basetheme, srcs):
		self.fc = Flowchart(str(tmpdir / 'flowchart.svg'), str(tmpdir / 'flowchart.dot'))
		self.fc.set_theme(theme, basetheme)
		starts = [procs[start] for start in starts]
		ends = [procs[end] for end in ends]
		for node in nodes:
			node = procs[node]
			self.fc.add_node(node, 'start' if node in starts else 'end' if node in ends else None)
		self.fc.add_link(procs[links[0][0]], procs[links[0][1]], True)
		for link in links:
			self.fc.add_link(procs[link[0]], procs[link[1]])
		self.fc.generate()
		source = self.fc.graph.source
		for src in srcs:
			assert src in source
			source = source[(source.find(src) + len(src)):]
		assert self.fc.fcfile.exists()
