
## test __init__.py
import sys
from itertools import chain
import pytest
from pathlib import Path
from simpleconf import Config
from diot import Diot
from pyppl import PyPPL, Proc, ProcSet
from pyppl.utils import fs
import pyppl_flowchart

def teardown_module(module):
	for fcfile in chain(Path('.').glob('*.dot'), Path('.').glob('*.svg')):
		fcfile.unlink()

# don't use fix_flowchart, as plugin won't be loaded
@pytest.fixture
def procs(request):
	return Diot(
		p1 = Proc('p1', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name),
		p2 = Proc('p2', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name),
		p3 = Proc('p3', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name),
		p4 = Proc('p4', input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	)

@pytest.fixture
def procset(procs):
	# pretend they are running
	procs.p1.runtime_config = procs.p2.runtime_config = procs.p3.runtime_config = Config()
	procs.p1.runtime_config._load({'default': {'dirsig': False}})
	return ProcSet(procs.p1, procs.p2, procs.p3, procs.p4)

@pytest.fixture
def pset(request):
	p14 = Proc(input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	p15 = Proc(input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	p16 = Proc(input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	p17 = Proc(input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	p18 = Proc(input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	p19 = Proc(input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	p20 = Proc(input = {'in:var':[0]}, output = 'out:var1', tag = request.node.name)
	# p15 -> p16  ->  p17 -> 19
	# p14 _/  \_ p18_/  \_ p20
	#           hide
	p18.config.flowchart_hide = True
	p20.depends = p17
	p19.depends = p17
	p17.depends = p16, p18
	p18.depends = p16
	p16.depends = p14, p15
	return Diot(p15 = p15, p16 = p16, p17 = p17, p18 = p18, p19 = p19, p20 = p20, p14 = p14)

def test_pyppl_flowchart_init(procs, tmp_path):
	fcfile = tmp_path / 'test_pyppl_flowchart_init.svg'
	procs.p2.depends = procs.p1
	procs.p3.depends = procs.p2
	procs.p4.depends = procs.p3
	PyPPL().start(procs.p1).flowchart(fcfile).run()

def test_procset(procset, tmp_path):
	fcfile = tmp_path / 'test_procset.svg'
	PyPPL().start(procset).flowchart(fcfile).run()

def test_flowchart(pset, caplog, tmp_path):
	for p in pset.values():
		p.input = {'a': [1]}
		p.output = 'a:var:{{i.a}}'
	ppl = PyPPL({'ppldir': tmp_path / 'test_flowchart_ppldir'}).start(pset.p14, pset.p15)
	ppl.counter = 0
	ppl.flowchart()
	assert 'Flowchart file saved to:' in caplog.text
	assert 'DOT file saved to:' in caplog.text
	assert fs.exists('./%s.pyppl.svg' % Path(ppl.name))
	assert fs.exists('./%s.pyppl.dot' % Path(ppl.name))

	dot = Path('./%s.pyppl.dot' % Path(ppl.name)).read_text()
	assert 'p17.test_flowchart" -> "p19.test_flowchart' in dot
	assert 'p17.test_flowchart" -> "p20.test_flowchart' in dot
	assert 'p16.test_flowchart" -> "p17.test_flowchart' in dot
	assert 'p16.test_flowchart" -> "p18.test_flowchart' not in dot # hidden
	assert 'p14.test_flowchart" -> "p16.test_flowchart' in dot
	assert 'p15.test_flowchart" -> "p16.test_flowchart' in dot

	fs.remove('./%s.pyppl.svg' % Path(ppl.name))
	fs.remove('./%s.pyppl.dot' % Path(ppl.name))

def test_hideerror(procs, tmp_path):
	procs.p1.config.flowchart_hide = True
	procs.p2.depends = procs.p1
	procs.p3.depends = procs.p2
	procs.p4.depends = procs.p3

	with pytest.raises(ValueError):
		PyPPL().start(procs.p1).flowchart(tmp_path / 'test_hideerror1.svg')

	procs.p1.config.flowchart_hide = False
	procs.p4.config.flowchart_hide = True
	with pytest.raises(ValueError):
		PyPPL().start(procs.p1).flowchart(tmp_path / 'test_hideerror2.svg')

	p5 = Proc()
	procs.p4.config.flowchart_hide = False
	procs.p2.depends = procs.p1, p5
	procs.p4.depends = procs.p2
	procs.p3.depends = procs.p2
	procs.p2.config.flowchart_hide = True
	with pytest.raises(ValueError):
		PyPPL().start(procs.p1, p5).flowchart(tmp_path / 'test_hideerror3.svg')
