#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMenu, QTextEdit
from PyQt5.QtGui import QTextDocument

class BaselineView(QTextEdit):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		#self.resize(250, 150)
		#self.move(300, 300)
		self.setWindowTitle('baseline diff')
		self.show()	

	def contextMenuEvent(self, event):
		cmenu = QMenu(self)
		newact = cmenu.addAction("new")
		action = cmenu.exec_(self.mapToGlobal(event.pos()))
		if action == newact:
			self.setHtml("<span>foobar</span>")
