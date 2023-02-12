# Table of Contents
1. [ MULTIDIFF. ](#desc)
2. [ Installation Guide. ](#instal)
3. [Command-line interface](#CLI)
4. [Examples](#Exam)
5. [Contributions](#Contri)

<a name="desc"></a>
`M U L T I D I F F`
===================

> Multidiff is a sensory augmentation apparatus

Its purpose is to make machine friendly data easier to understand by humans that are looking at it.
Specifically multidiff helps in viewing the differences within a large set of objects by doing diffs between relevant objects and displaying them in a sensible manner.
This kind of visualization is handy when looking for patterns and structure in proprietary protocols or weird file formats.
The obvious use-cases are reverse engineering and binary data analysis.

![multidiff -p 8000 -i json -o hexdump](./hexdump_stream_mode.png)

At the core of multidiff is the python difflib library and multidiff wraps it in data providing mechanisms and visualization code.
The visualization is the most important part of the project and everything else is just utilities to make it easier to feed data for the visualizer.
At this time the tool can do basic format parsing such as hex decoding, hexdumping, and handling data as utf8 strings, as well as read from files, stdin, and sockets.
Any preprocessing such as cropping, indenting, decompression, etc. will have be done by the user before the objects are provided to multidiff.

<a name="instal"></a>
Installation Guide
----------------------
Before you begin Installing multidiff. Please ensure you have python and the pip manager installed.

To check the current version of python in your system you can type the following command on the CLI.

	python3 --version

To check the current version of pip in your system you can type in the following command on the CLI.

	pip --version

multidiff can be installed on your system using the following command on the CLI.

	pip install multidiff

multidiff is also dependent on other Python scientific modules such as numpy, scipy and matplotlib. 
These modules can be installed separately, or using a bundled distribution such as Anaconda or Canopy.

To use this with Anaconda, open the "Anaconda Prompt" and type in the following:

	conda install pip

<a name="CLI"></a>
Command-line interface
----------------------
The command line interface is the easiest way to use multidiff. It supports a few common use-cases and is installed by the setup script.

	python3 setup.py install
	multidiff -h

### --mode
This selects the diffing strategy, currently `sequence` and `baseline` are supported.
Sequence mode diffs every object with the object added just before it while baseline mode always diffs the most recent object with the first object.

### --informat & --outformat
The `infomrat` argument controls what kind of transformations should be done to the data before it gets diffed. `outformat` controls the view of the output data.
`informat` should mostly be selected based on what is the easiest way to provide data to multidiff while `outformat` should be selected based on how the content of the data is most pleasantly viewed.

### --port
There is an embedded tcp socket server that will listen to any packets coming to the specified port and print the diffs as more objects are sent to it.
The server supports a json mode in which objects are passed as json objects that may include metadata. This is useful if the client has done some analysis on the data and one would like to show those results in the view stream. The schema is pretty simple:

	{
		"data":"[data encoded as base64]",
		"info":"some useful note"
	}

Example object providers are in the `examples` directory.
These are specific use-cases where it has been helpful to have a stream of diffs visible when inspecting traffic.

<a name="Exam"></a>
Examples
--------

Check how much your shell history repeats:

	history | multidiff -s -o utf8
	
Diff a bunch of files and scroll through the results:

	multidiff interesting_file.bin folder_with_similar_files/ | less -r

Start a multidiff server, then send objects to it:

	multidiff -p 8000
	echo "interesting" | nc 127.0.0.1 8000
	echo "intersectional" | nc 127.0.0.1 8000

<a name="Contri"></a>
Contributions
-------------
👍🎉 First off, thanks for taking the time to contribute! 🎉👍
The following is a set of guidelines for contributing to multidiff.
Code of Conduct
Please participate and uphold respect for fellow contributors. Please report unacceptable behaviour.
### How can I contribute ?
This section berfiely goes over the ways you can contribute.
#### Before submiting a bug report or adding a new feature.
* **make sure you have the latest verion** of multidiff by fetching the latest version of the repo
#### Submiting a bug report
* **Use a clear and descriptive title.** for the issue to idenfity the problem.
*  **Desribe the exact steps you took** to find the problem.
*  **Include screen shots** of error messages and explain what you expected insted.
#### Submiting a feature report
* **Use a clear and descriptive title.** for the feature you want to add.
* **Desribe the exact steps you took** to add the feature.
* **Explain** what are the benfits of the feature.
#### Pull requests 
Pull requests are always welcomed, please feel free to raise a reueqst when you are compeleted with adding a feature or see a bug. I can be reached as "stilla" on Protonmail.
