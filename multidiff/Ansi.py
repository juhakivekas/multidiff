class Ansi:
	reset    = '\x1b[0m'
	bold     = '\x1b[1m'
	black    = '\x1b[30m'
	white    = '\x1b[37m'
	on_red   = '\x1b[41m'
	on_green = '\x1b[42m'
	on_blue  = '\x1b[44m'
	on_neonr = '\x1b[48;5;197m'
	on_neong = '\x1b[48;5;118m'
	on_neonb = '\x1b[48;5;30m'

	replace  = bold + white + on_neonb
	insert   = bold + black + on_neong
	delete   = bold + on_neonr
