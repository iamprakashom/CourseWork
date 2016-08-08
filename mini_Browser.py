# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 11:33:23 2016

@author: Om Prakash
"""

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView, QWebSettings, QWebPage
from PyQt4.QtNetwork import QNetworkProxyFactory

url = ""


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.centralWidget = QtGui.QWidget(self)

        '''
        Address Bar
        '''
        self.addbar = QtGui.QLineEdit(self)
        self.addbar.setGeometry(200, 16, 840, 35)
        self.addbar.setStyleSheet("font-size:21px")
        self.addbar.setFont(QtGui.QFont("Times New Roman"))
        self.addbar.returnPressed.connect(self.goClicked)
        self.addbar.cursorPositionAt(QtCore.QPoint(0, 0))
        self.addbar.setFocus()
        self.addbar.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, True)

        '''
        Progress Bar
        '''
        self.progressbar = QtGui.QProgressBar(self)
        self.progressbar.setMaximumWidth(100)

        '''
        Web Page Action setting
        '''
        self.web = QWebView(loadProgress=self.progressbar.setValue,
                            loadFinished=self.progressbar.hide, loadStarted=
                            self.progressbar.show, titleChanged=self.
                            setWindowTitle)
        self.web.setGeometry(300, 100, 1099, 768)
        self.web.urlChanged.connect(self.goUrlChanged)
        self.web.page().linkHovered.connect(self.LinkHovered)
        self.web.loadStarted.connect(self.pageLoadStarted)
        self.web.loadFinished.connect(self.pageLoadFinished)

        '''
        Back, Forward, Reload and Stop Button
        '''
        self.toolbar = QtGui.QToolBar(self)
        self.toolbar.addAction(self.web.pageAction(QWebPage.Back))
        self.toolbar.addAction(self.web.pageAction(QWebPage.Forward))
        self.toolbar.addAction(self.web.pageAction(QWebPage.Reload))
        self.toolbar.addAction(self.web.pageAction(QWebPage.Stop))

        '''
        Global Web Page Setting
        '''
        self.setting = QWebSettings.globalSettings()
        self.setting.setAttribute(QWebSettings.PluginsEnabled, True)
        self.setting.setAttribute(QWebSettings.AutoLoadImages, True)
        self.setting.setAttribute(QWebSettings.JavaEnabled, True)
        self.setting.setAttribute(QWebSettings.DnsPrefetchEnabled, True)
        self.setting.setAttribute(QWebSettings.WebGLEnabled, True)
        self.setting.setAttribute(QWebSettings.LocalStorageEnabled, True)
        self.setting.setAttribute(QWebSettings.JavascriptEnabled, True)
        self.setting.setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
        self.setting.setAttribute(QWebSettings.
                                  OfflineWebApplicationCacheEnabled, True)
        self.setting.setAttribute(QWebSettings.ZoomTextOnly, True)
        self.setting.setAttribute(QWebSettings.AcceleratedCompositingEnabled,
                                  True)
        self.setting.setAttribute(QWebSettings.SpatialNavigationEnabled, True)
        self.setting.setAttribute(QWebSettings.LinksIncludedInFocusChain, True)
        self.setting.setAttribute(QWebSettings.LocalContentCanAccessFileUrls,
                                  True)

        '''
        Main Window Setting
        '''
        self.setGeometry(300, 100, 1099, 768)
        self.setWindowIcon(QtGui.QIcon(""))
        self.setStyleSheet("background-color:")
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.addPermanentWidget(self.progressbar)
        self.status.hide()
        self.setCentralWidget(self.centralWidget)
        grid = QtGui.QGridLayout()
        grid.addWidget(self.toolbar, 0, 0, 1, 1)
        grid.addWidget(self.addbar, 0, 1, 1, 1)
        grid.addWidget(self.web, 2, 0, 1, 6)
        self.centralWidget.setLayout(grid)

        '''
        Use system Proxy to load page
        '''
        QNetworkProxyFactory.setUseSystemConfiguration(True)

    def goClicked(self):
        '''
        When URL is entered in addressbar and enter is pressed
        '''
        global url
        url = self.addbar.text()
        http = "http://"
        www = "www."
        https = "https://"
        if www in url and http not in url:
            url = http + url
        elif "." not in url:
            url = "http://www.google.com/search?q=" + url
        elif http in url and www not in url:
            url = url[:7] + www + url[7:]
        elif https in url:
            url = url
        elif http and www not in url:
            url = http + www + url

        self.addbar.setText(url)
        self.web.load(QtCore.QUrl(url))
        self.status.show()
        self.web.setFocus(True)

    def goUrlChanged(self):
        '''
        Update URL in Address bar if link is clicked
        '''
        self.addbar.setText(self.web.url().toString())

    def LinkHovered(self, l):
        self.status.showMessage(l)

    def pageLoadStarted(self):
        self.status.showMessage("Loading")
        self.status.show()

    def pageLoadFinished(self):
        self.addbar.setText(self.web.url().toString())
        self.status.hide()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    browser = MainWindow()
    browser.show()
    sys.exit(app.exec_())
