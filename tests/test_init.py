
## test __init__.py
import pytest
from pyppl import PyPPL, Proc, Box

# don't use fix_flowchart, as plugin won't be loaded
@pytest.fixture
def procs():
	return Box(
		p1 = Proc('p1'),
		p2 = Proc('p2'),
		p3 = Proc('p3'),
		p4 = Proc('p4'),
	)

def test_pyppl_flowchart_init(procs, tmp_path):
	fcfile = tmp_path / 'test_pyppl_flowchart_init.svg'
	PyPPL().start(procs.p1).flowchart(fcfile).run()