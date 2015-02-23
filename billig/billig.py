'''
@author: Loïc Grobol <loic.grobol@gmail.com>
Copyright © 2014, Loïc Grobol <loic.grobol@gmail.com>
Permission is granted to Do What The Fuck You Want To
with this document.

See the WTF Public License, Version 2 as published by Sam Hocevar
at http://www.wtfpl.net if you need more details.

A gui for krampouezh
'''

import sys
from PyQt5.QtCore import QObject, QUrl, Qt, QMetaObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


if __name__ == "__main__":
  app = QApplication(sys.argv)
  engine = QQmlApplicationEngine()
  ctx = engine.rootContext()
  ctx.setContextProperty("main", engine)

  engine.load('billig.qml')

  win = engine.rootObjects()[0]
  win.show()
  
  button = win.findChild(QObject, "about_button")
  #button.about_text.connect(myFunction)


  sys.exit(app.exec_())
