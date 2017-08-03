from multidiff import MultidiffModel, AnsiView

def test_baseline_ansi_dump():
	objs = open("test/minimal.txt").read(-1).split('\n')
	m = MultidiffModel(objs)
	m.diff_baseline()
	res = AnsiView().dumps(m, printmode='utf8')
	base = open("test/minimal_res.txt").read(-1)
	assert res == base
