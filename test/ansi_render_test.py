from multidiff import MultidiffModel, Render

def test_sequence_ansi_utf_dump():
	objs = open("test/pretty_json.txt").read(-1).split('\n\n')
	objs = [bytes(x, 'utf8') for x in objs]
	m = MultidiffModel(objs)
	m.diff_sequence()
	res = Render(encoder='utf8').dumps(m)
	print(res) #for visual checking when tests fail
	base = open("test/pretty_json_res.txt").read(-1)
	assert res == base

def test_baseline_ansi_utf_dump():
	objs = open("test/minimal.txt").read(-1).split('\n')
	objs = [bytes(x, 'utf8') for x in objs]
	m = MultidiffModel(objs)
	m.diff_baseline()
	res = Render(encoder='utf8').dumps(m)
	print(res) #for visual checking when tests fail
	base = open("test/minimal_res.txt").read(-1)
	assert res == base
