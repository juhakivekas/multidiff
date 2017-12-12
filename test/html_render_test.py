from multidiff import MultidiffModel, Render

"""
def test_sequence_html_dump():
	objs = open("test/pretty_json.txt").read(-1).split('\n\n')
	m = MultidiffModel(objs)
	m.diff_sequence()
	res = Render(outformat='html').dumps(m)
	base = open("test/pretty_json_res.txt").read(-1)
	#assert res == base
	assert False
"""

def test_baseline_html_utf_dump():
	objs = open("test/minimal.txt").read(-1).split('\n')[:-1]
	objs = [bytes(x, 'utf8') for x in objs]
	m = MultidiffModel(objs)
	m.diff_baseline()
	res = Render(encoder='utf8', color='html').dumps(m)
	print(res)
	base = open("test/minimal_res.html").read(-1)
	assert res == base
