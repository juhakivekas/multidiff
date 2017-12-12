<pre>
<b>N E O N S E N S E</b>
augmentations inc 
┌───────────────┐
│<b> M  U  L  T  I </b>│
│<b> D   I   F   F </b>│
│ sensor module │
└───────────────┘
</pre>
Purpose
-------
Multidiff is a sensory augmentation apparatus.
It's purpose is to enable visual parsing of machine data for humans.
Specifically multidiff helps in viewing the differences within a large set of objects by doing diffs between relevant objects and displaying them in a sensible manner.
This is handy when wanting to see the similarities in structure of proprietary protocols or weird file formats.
The most obvious use-cases are reverse engineering and binary data analysis.

Scope
-----
At the core of multidiff is the python difflib library and multidiff wraps it in data providing mechanisms and visualisation code.
The visualization is the most important part of the apparatus and everything else is just utilities to enable simpler use.
At this time the tool can only do basic format parsing such as hex decoding, hexdumping, and handling data as utf8 strings.
Most of the time preprocessing such as cropping, indenting, decompression, etc. will be done by the data provider before the objects are sent to multidiff.

mdcli
-----
The command line interface is the primary use-case for most of the code. It has a few handy options to make data collecting and displaying nice and easy.
The help is pretty useful and most of the arguments are quite intuitive.

	mdcli.py -h

### --mode
This selects the diffing strategy, currently `sequence` and `baseline` are supported.
Sequence mode diffs every object with the object added just before it while baseline mode always diffs the most recent object with the first object.

### --informat & --outformat
The `infomrat` argument controls what kind of transformations should be done to the data before it gets diffed. `outformat` controls the view of the output data.
`informat` should mostly be selected based on what is the easiest way to provide data to multidiff while `outformat` should be selected based on how the content of the data is most pleasantly viewed.

### --port
There is an embedded tcp socket server that will listen to any packets coming to the specified port and print the diffs as more objects become available.
The server supports a json mode in which objects are passed as json objects that may include metadata. This is useful if the client has done some analysis on the data and one would like to show those results in the view stream. The schema is pretty simple:

	{
		"data":"[data encoded as urlbase64]",
		"info":"some useful note"
	}
