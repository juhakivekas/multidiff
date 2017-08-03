from multidiff import MultidiffModel, AnsiView

def test_sequence_ansi_dump():
	objs = open("test/pretty_json.txt").read(-1).split('\n\n')
	m = MultidiffModel(objs)
	m.diff_sequence()
	res = AnsiView().dumps(m, printmode='utf8')
	base = open("test/pretty_json_res.txt").read(-1)
	assert res == base
