
## test __init__.py
import sys
import pytest
from os import environ
from pathlib import Path
environ['PYPPL_default__log'] = 'py:{"leveldiffs": "DEBUG"}'
from pyppl import PyPPL, Proc, Box, ProcSet, ProcTree
from pyppl.utils import fs
pyppl_flowchart = __import__('pyppl_flowchart')

# don't use fix_flowchart, as plugin won't be loaded
@pytest.fixture
def procs():
	return Box(
		p1 = Proc('p1'),
		p2 = Proc('p2'),
		p3 = Proc('p3'),
		p4 = Proc('p4')
	)

@pytest.fixture
def procset(procs):
	return ProcSet(procs.p1, procs.p2, procs.p3, procs.p4)

@pytest.fixture
def pset():
	ProcTree.NODES.clear()
	p14 = Proc()
	p15 = Proc()
	p16 = Proc()
	p17 = Proc()
	p18 = Proc()
	p19 = Proc()
	p20 = Proc()
	# p15 -> p16  ->  p17 -> 19
	# p14 _/  \_ p18_/  \_ p20
	#           hide
	p18.hide = True
	p20.depends = p17
	p19.depends = p17
	p17.depends = p16, p18
	p18.depends = p16
	p16.depends = p14, p15
	return Box(p15 = p15, p16 = p16, p17 = p17, p18 = p18, p19 = p19, p20 = p20, p14 = p14)

def test_pyppl_flowchart_init(procs, tmp_path):
	fcfile = tmp_path / 'test_pyppl_flowchart_init.svg'
	procs.p2.depends = procs.p1
	procs.p3.depends = procs.p2
	procs.p4.depends = procs.p3
	PyPPL().start(procs.p1).flowchart(fcfile).run()

def test_procset(procset, tmp_path):
	fcfile = tmp_path / 'test_procset.svg'
	PyPPL().start(procset).flowchart(fcfile).run()


def test_showallroutes(pset, caplog, tmp_path):
	fcfile = tmp_path / 'test_showallroutes.svg'
	# p15 -> p16  ->  ps -> p19
	# p14 _/  \_ p18_/  \_ p20
	#           hide
	pset.p17.depends = []
	ps = ProcSet(Proc(id = 'p1'), Proc(id = 'p2'))
	ps.depends = pset.p16, pset.p18
	pset.p19.depends = ps
	pset.p20.depends = ps
	ppl = PyPPL().start(pset.p14, pset.p15)
	ppl.flowchart(fcfile)
	assert 'ALL ROUTES:' in caplog.text
	assert '  p14 -> p16 -> [@ps] -> p19' in caplog.text
	assert '  p14 -> p16 -> [@ps] -> p20' in caplog.text
	assert '  p15 -> p16 -> [@ps] -> p19' in caplog.text
	assert '  p15 -> p16 -> [@ps] -> p20' in caplog.text

def test_flowchart(pset, caplog, tmp_path):
	for p in pset.values():
		p.input = {'a': [1]}
		p.output = 'a:var:{{i.a}}'
	ppl = PyPPL({'ppldir': tmp_path / 'test_flowchart_ppldir'}).start(pset.p14, pset.p15)
	ppl.counter = 0
	ppl.flowchart()
	assert 'Flowchart file saved to:' in caplog.text
	assert 'DOT file saved to:' in caplog.text
	assert fs.exists('./%s.pyppl.svg' % Path(sys.argv[0]).stem)
	assert fs.exists('./%s.pyppl.dot' % Path(sys.argv[0]).stem)

	dot = Path('./%s.pyppl.dot' % Path(sys.argv[0]).stem).read_text()
	assert 'p17 -> p19' in dot
	assert 'p17 -> p20' in dot
	assert 'p16 -> p17' in dot
	#assert 'p16 -> p18' in dot # hidden
	assert 'p14 -> p16' in dot
	assert 'p15 -> p16' in dot

	fs.remove('./%s.pyppl.svg' % Path(sys.argv[0]).stem)
	fs.remove('./%s.pyppl.dot' % Path(sys.argv[0]).stem)

def test_hideerror(procs, tmp_path):
	procs.p1.hide = True
	procs.p2.depends = procs.p1
	procs.p3.depends = procs.p2
	procs.p4.depends = procs.p3

	with pytest.raises(pyppl_flowchart.ProcHideError):
		PyPPL().start(procs.p1).flowchart(tmp_path / 'test_hideerror1.svg')

	procs.p1.hide = False
	procs.p4.hide = True
	with pytest.raises(pyppl_flowchart.ProcHideError):
		PyPPL().start(procs.p1).flowchart(tmp_path / 'test_hideerror2.svg')

	p5 = Proc()
	procs.p4.hide = False
	procs.p2.depends = procs.p1, p5
	procs.p4.depends = procs.p2
	procs.p3.depends = procs.p2
	procs.p2.hide = True
	with pytest.raises(pyppl_flowchart.ProcHideError):
		PyPPL().start(procs.p1, p5).flowchart(tmp_path / 'test_hideerror3.svg')
