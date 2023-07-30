# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDockWidget, QFrame,
    QGridLayout, QHeaderView, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QTabWidget, QToolBar,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from canvas_widget import Canvas
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1250, 750)
        MainWindow.setMinimumSize(QSize(1250, 750))
        icon = QIcon()
        icon.addFile(u":/Dark/MiFaceStudioFavicon.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/Dark/MiFaceStudioFavicon.png", QSize(), QIcon.Normal, QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionAbout_MiFaceStudio = QAction(MainWindow)
        self.actionAbout_MiFaceStudio.setObjectName(u"actionAbout_MiFaceStudio")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionCompile = QAction(MainWindow)
        self.actionCompile.setObjectName(u"actionCompile")
        self.actionshowAboutWindow = QAction(MainWindow)
        self.actionshowAboutWindow.setObjectName(u"actionshowAboutWindow")
        self.actionshowDefaultInfoDialog = QAction(MainWindow)
        self.actionshowDefaultInfoDialog.setObjectName(u"actionshowDefaultInfoDialog")
        self.actionshowOpenFile = QAction(MainWindow)
        self.actionshowOpenFile.setObjectName(u"actionshowOpenFile")
        self.actionshowSaveFile = QAction(MainWindow)
        self.actionshowSaveFile.setObjectName(u"actionshowSaveFile")
        self.actionThirdPartyNotice = QAction(MainWindow)
        self.actionThirdPartyNotice.setObjectName(u"actionThirdPartyNotice")
        self.actionExplorer = QAction(MainWindow)
        self.actionExplorer.setObjectName(u"actionExplorer")
        self.actionExplorer.setCheckable(True)
        self.actionExplorer.setChecked(True)
        self.actionAttributes = QAction(MainWindow)
        self.actionAttributes.setObjectName(u"actionAttributes")
        self.actionAttributes.setCheckable(True)
        self.actionAttributes.setChecked(True)
        self.actionResources = QAction(MainWindow)
        self.actionResources.setObjectName(u"actionResources")
        self.actionResources.setCheckable(True)
        self.actionResources.setChecked(True)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionshowToast = QAction(MainWindow)
        self.actionshowToast.setObjectName(u"actionshowToast")
        self.actionToolbox = QAction(MainWindow)
        self.actionToolbox.setObjectName(u"actionToolbox")
        self.actionToolbox.setCheckable(True)
        self.actionToolbox.setChecked(True)
        self.actionEdit = QAction(MainWindow)
        self.actionEdit.setObjectName(u"actionEdit")
        self.actionEdit.setCheckable(True)
        self.actionEdit.setChecked(True)
        self.actionFile = QAction(MainWindow)
        self.actionFile.setObjectName(u"actionFile")
        self.actionFile.setCheckable(True)
        self.actionFile.setChecked(True)
        self.actionLayout = QAction(MainWindow)
        self.actionLayout.setObjectName(u"actionLayout")
        self.actionLayout.setCheckable(True)
        self.actionLayout.setChecked(True)
        self.actionNewFile = QAction(MainWindow)
        self.actionNewFile.setObjectName(u"actionNewFile")
        icon1 = QIcon()
        icon1.addFile(u":/Dark/file-plus-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNewFile.setIcon(icon1)
        self.actionOpenFile = QAction(MainWindow)
        self.actionOpenFile.setObjectName(u"actionOpenFile")
        icon2 = QIcon()
        icon2.addFile(u":/Dark/folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpenFile.setIcon(icon2)
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        icon3 = QIcon()
        icon3.addFile(u":/Dark/undo-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionUndo.setIcon(icon3)
        self.actionUndo.setMenuRole(QAction.NoRole)
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        icon4 = QIcon()
        icon4.addFile(u":/Dark/redo-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRedo.setIcon(icon4)
        self.actionRedo.setMenuRole(QAction.NoRole)
        self.actionInstaller = QAction(MainWindow)
        self.actionInstaller.setObjectName(u"actionInstaller")
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.actionshowColorDialog = QAction(MainWindow)
        self.actionshowColorDialog.setObjectName(u"actionshowColorDialog")
        self.actionshowSelectFont = QAction(MainWindow)
        self.actionshowSelectFont.setObjectName(u"actionshowSelectFont")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(200, 0))
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 4, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.canvas = Canvas(self.tab)
        self.canvas.setObjectName(u"canvas")
        self.canvas.setAutoFillBackground(False)
        self.canvas.setStyleSheet(u"background-color: transparent")
        self.canvas.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_2.addWidget(self.canvas)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1250, 22))
        self.menubar.setContextMenuPolicy(Qt.NoContextMenu)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuCompile = QMenu(self.menubar)
        self.menuCompile.setObjectName(u"menuCompile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuAbout = QMenu(self.menuHelp)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuTest = QMenu(self.menubar)
        self.menuTest.setObjectName(u"menuTest")
        self.menuDialog = QMenu(self.menuTest)
        self.menuDialog.setObjectName(u"menuDialog")
        self.menuRun = QMenu(self.menuTest)
        self.menuRun.setObjectName(u"menuRun")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuToolbars = QMenu(self.menuView)
        self.menuToolbars.setObjectName(u"menuToolbars")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.explorerWidget = QDockWidget(MainWindow)
        self.explorerWidget.setObjectName(u"explorerWidget")
        self.explorerWidget.setMinimumSize(QSize(250, 250))
        self.explorerWidget.setStyleSheet(u"")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.treeWidget = QTreeWidget(self.dockWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setStyleSheet(u"")
        self.treeWidget.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.treeWidget)

        self.explorerWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.explorerWidget)
        self.attributesWidget = QDockWidget(MainWindow)
        self.attributesWidget.setObjectName(u"attributesWidget")
        self.attributesWidget.setMinimumSize(QSize(250, 250))
        self.attributesWidget.setStyleSheet(u"")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.gridLayout = QGridLayout(self.dockWidgetContents_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.attributesWidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.attributesWidget)
        self.resourceWidget = QDockWidget(MainWindow)
        self.resourceWidget.setObjectName(u"resourceWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resourceWidget.sizePolicy().hasHeightForWidth())
        self.resourceWidget.setSizePolicy(sizePolicy1)
        self.resourceWidget.setMinimumSize(QSize(300, 162))
        self.resourceWidget.setMaximumSize(QSize(524287, 200))
        self.resourceWidget.setStyleSheet(u"")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.gridLayout_4 = QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.listWidget_2 = QListWidget(self.dockWidgetContents_3)
        QListWidgetItem(self.listWidget_2)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setStyleSheet(u"background-color: transparent")
        self.listWidget_2.setFrameShape(QFrame.NoFrame)
        self.listWidget_2.setDragEnabled(True)
        self.listWidget_2.setFlow(QListView.LeftToRight)
        self.listWidget_2.setViewMode(QListView.ListMode)

        self.gridLayout_4.addWidget(self.listWidget_2, 0, 0, 1, 1)

        self.resourceWidget.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.resourceWidget)
        self.toolboxWidget = QDockWidget(MainWindow)
        self.toolboxWidget.setObjectName(u"toolboxWidget")
        self.toolboxWidget.setMinimumSize(QSize(250, 500))
        self.toolboxWidget.setMaximumSize(QSize(524287, 524287))
        self.toolboxWidget.setStyleSheet(u"")
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.ToolboxList = QListWidget(self.dockWidgetContents_4)
        icon5 = QIcon()
        icon5.addFile(u":/Dark/package.png", QSize(), QIcon.Normal, QIcon.Off)
        __qlistwidgetitem = QListWidgetItem(self.ToolboxList)
        __qlistwidgetitem.setIcon(icon5);
        self.ToolboxList.setObjectName(u"ToolboxList")
        self.ToolboxList.setEnabled(True)
        self.ToolboxList.setStyleSheet(u"background-color: transparent;")
        self.ToolboxList.setFrameShape(QFrame.NoFrame)
        self.ToolboxList.setDragEnabled(True)
        self.ToolboxList.setDragDropMode(QAbstractItemView.DragOnly)
        self.ToolboxList.setDefaultDropAction(Qt.MoveAction)
        self.ToolboxList.setGridSize(QSize(0, 19))
        self.ToolboxList.setViewMode(QListView.ListMode)

        self.verticalLayout_3.addWidget(self.ToolboxList)

        self.toolboxWidget.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.toolboxWidget)
        self.FileToolBar = QToolBar(MainWindow)
        self.FileToolBar.setObjectName(u"FileToolBar")
        self.FileToolBar.setMovable(False)
        self.FileToolBar.setIconSize(QSize(18, 18))
        self.FileToolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.FileToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuCompile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuTest.menuAction())
        self.menuFile.addAction(self.actionNewFile)
        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuCompile.addAction(self.actionCompile)
        self.menuHelp.addAction(self.menuAbout.menuAction())
        self.menuAbout.addAction(self.actionAbout_MiFaceStudio)
        self.menuAbout.addAction(self.actionAbout_Qt)
        self.menuAbout.addAction(self.actionThirdPartyNotice)
        self.menuTest.addAction(self.menuDialog.menuAction())
        self.menuTest.addAction(self.menuRun.menuAction())
        self.menuDialog.addAction(self.actionshowAboutWindow)
        self.menuDialog.addAction(self.actionshowDefaultInfoDialog)
        self.menuDialog.addAction(self.actionshowToast)
        self.menuDialog.addAction(self.actionshowColorDialog)
        self.menuDialog.addAction(self.actionshowSelectFont)
        self.menuRun.addAction(self.actionInstaller)
        self.menuView.addAction(self.actionExplorer)
        self.menuView.addAction(self.actionAttributes)
        self.menuView.addAction(self.actionToolbox)
        self.menuView.addAction(self.actionResources)
        self.menuView.addSeparator()
        self.menuView.addAction(self.menuToolbars.menuAction())
        self.menuToolbars.addAction(self.actionEdit)
        self.menuToolbars.addAction(self.actionFile)
        self.menuToolbars.addAction(self.actionLayout)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionPreferences)
        self.FileToolBar.addAction(self.actionNewFile)
        self.FileToolBar.addAction(self.actionOpenFile)
        self.FileToolBar.addAction(self.actionUndo)
        self.FileToolBar.addAction(self.actionRedo)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mi Face Studio", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save...", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as...", None))
#if QT_CONFIG(shortcut)
        self.actionSave_as.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout_MiFaceStudio.setText(QCoreApplication.translate("MainWindow", u"About Mi Face Studio", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
#if QT_CONFIG(shortcut)
        self.actionPreferences.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionCompile.setText(QCoreApplication.translate("MainWindow", u"Compile...", None))
#if QT_CONFIG(shortcut)
        self.actionCompile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+K", None))
#endif // QT_CONFIG(shortcut)
        self.actionshowAboutWindow.setText(QCoreApplication.translate("MainWindow", u"showAboutWindow", None))
        self.actionshowDefaultInfoDialog.setText(QCoreApplication.translate("MainWindow", u"showDefaultCriticalDialog", None))
        self.actionshowOpenFile.setText(QCoreApplication.translate("MainWindow", u"showOpenFile", None))
        self.actionshowSaveFile.setText(QCoreApplication.translate("MainWindow", u"showSaveFile", None))
        self.actionThirdPartyNotice.setText(QCoreApplication.translate("MainWindow", u"Third Party Notices", None))
        self.actionExplorer.setText(QCoreApplication.translate("MainWindow", u"Explorer", None))
        self.actionAttributes.setText(QCoreApplication.translate("MainWindow", u"Attributes", None))
        self.actionResources.setText(QCoreApplication.translate("MainWindow", u"Resources", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionshowToast.setText(QCoreApplication.translate("MainWindow", u"showToast", None))
        self.actionToolbox.setText(QCoreApplication.translate("MainWindow", u"Toolbox", None))
        self.actionEdit.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.actionFile.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.actionLayout.setText(QCoreApplication.translate("MainWindow", u"Layout", None))
        self.actionNewFile.setText(QCoreApplication.translate("MainWindow", u"New...", None))
#if QT_CONFIG(tooltip)
        self.actionNewFile.setToolTip(QCoreApplication.translate("MainWindow", u"New File", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionNewFile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpenFile.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
#if QT_CONFIG(tooltip)
        self.actionOpenFile.setToolTip(QCoreApplication.translate("MainWindow", u"Open File", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpenFile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Y, Ctrl+Shift+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionInstaller.setText(QCoreApplication.translate("MainWindow", u"Installer", None))
        self.actionAbout_Qt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.actionshowColorDialog.setText(QCoreApplication.translate("MainWindow", u"showColorDialog", None))
        self.actionshowSelectFont.setText(QCoreApplication.translate("MainWindow", u"showSelectFont", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuCompile.setTitle(QCoreApplication.translate("MainWindow", u"Compile", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
        self.menuTest.setTitle(QCoreApplication.translate("MainWindow", u"Test", None))
        self.menuDialog.setTitle(QCoreApplication.translate("MainWindow", u"Dialog...", None))
        self.menuRun.setTitle(QCoreApplication.translate("MainWindow", u"Run...", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuToolbars.setTitle(QCoreApplication.translate("MainWindow", u"Toolbars", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.explorerWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Explorer", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"project.fprj", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Watchface", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"bg.png", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.attributesWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Attributes", None))
        self.resourceWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Resources", None))

        __sortingEnabled1 = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget_2.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"test", None));
        self.listWidget_2.setSortingEnabled(__sortingEnabled1)

        self.toolboxWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Toolbox", None))

        __sortingEnabled2 = self.ToolboxList.isSortingEnabled()
        self.ToolboxList.setSortingEnabled(False)
        ___qlistwidgetitem1 = self.ToolboxList.item(0)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Element", None));
        self.ToolboxList.setSortingEnabled(__sortingEnabled2)

        self.FileToolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

