# Mi Create
# tostr 2023

# TODO
# Rewrite the quite bad tab system currently in place
# Opening multiple projects is useless
# And that allows the explorer to also display any apps placed in the project
# Plus, its more simpler for me to use

# Make so that data files are automatically created by the program, not manually bundled in.

# Also, bundle in higher quality icons or use SVG versions they look very bad on Windows scale > 100%

# Also add in a js/lua autocomplete to monaco, will be useful for turning the app into a full fledged IDE
# But thats against trying to make the project as simple as it possibly can, would it?
# Too many features, and new users immediately overwhelmed, need to open documentation for every feature lmao

# Make application compatible with Linux/macOS

import os
import pdb
import gettext

from PySide6.QtWidgets import (QMainWindow, QDialog, QMessageBox, QApplication, QGraphicsScene, QPushButton, 
                               QDialogButtonBox, QTreeWidgetItem, QFileDialog, QToolButton, QToolBar, QWidget, QVBoxLayout, 
                               QFrame, QColorDialog, QFontDialog, QSplashScreen)
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QSettings, QSize, QUrl, QFileInfo
from PySide6.QtWebEngineWidgets import QWebEngineView

from pprint import pprint
import xml.dom.minidom
import xmltodict
import threading
import logging
import subprocess
import json
import theme.styles as theme
import traceback

from updater.updater import Updater
from project.projectManager import watchData, fprjProject
from history.historyManager import historySystem
from widgets.canvas import Canvas, ObjectIcon
from widgets.properties import PropertiesWidget
from monaco.monaco_widget import MonacoWidget

# resource import required because it sets up the icons even though its not called later in program
import resources.icons_rc

from window_ui import Ui_MainWindow
from dialog.preferences_ui import Ui_Dialog as Ui_Preferences
from dialog.newProject_ui import Ui_Dialog as Ui_NewProject
from dialog.resourceDialog_ui import Ui_Dialog as Ui_ResourceDialog
from dialog.compileDialog_ui import Ui_Dialog as Ui_CompileDialog

logging.basicConfig(level=logging.DEBUG)

_ = gettext.gettext

#windll = ctypes.windll.kernel32
currentDir = os.getcwd()
currentVersion = '0.0.1-pre-alpha-2'
#currentLanguage = locale.windows_locale[windll.GetUserDefaultUILanguage()]

languages = ["English", "繁體中文", "简体中文", "Русский"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.debug("-- Starting Mi Create --")

        history = historySystem()

        self.fileChanged = False
        self.clipboard = None

        # Setup Preferences Dialog 
        logging.debug("Initializing dialogs")
        self.preferencesDialog = QDialog(self) 
        self.preferences = Ui_Preferences() 
        self.preferences.setupUi(self.preferencesDialog) 
 
        # Setup New Project Dialog 
        self.newProjectDialog = QDialog(self) 
        self.newProjectUi = Ui_NewProject() 
        self.newProjectUi.setupUi(self.newProjectDialog) 
 
        # Setup Compile Project Dialog 
        self.compileDialog = QDialog(self) 
        self.compileUi = Ui_CompileDialog() 
        self.compileUi.setupUi(self.compileDialog) 
 
        # Setup projects (tabs) 
        self.projects = {
            "Welcome": {
                "hasFileChanged": False
            }
        } 
 
        # Setup WatchData 
        logging.debug("Initializing watchData")
        self.watchData = watchData() 

        # Setup History System
        self.historySystem = historySystem()
 
        # Setup Project 
        self.project = None 
        self.projectXML = None 
 
        # Setup Main Window 
        logging.debug("Initializing MainWindow")
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self) 
        logging.debug("Loading Scaffold")
        self.setupScaffold() 
        logging.debug("Initializing Application Widgets")
        self.setupWidgets() 
        logging.debug("Initializing Workspace")
        self.setupWorkspace() 
        logging.debug("Initializing Explorer")
        self.setupExplorer() 
        logging.debug("Initializing Watch Properties")
        self.setupProperties()
        logging.debug("Initializing Misc") 
        self.setupNewProjectDialog() 
        self.loadWindowState() 
        logging.debug("Loading App Settings")
        self.loadSettings() 
        self.loadTheme() 
        logging.debug("Launch!!")
        self.statusBar().showMessage("Ready", 3000) 

    def closeEvent(self, event):
        logging.debug("Exit requested!") 
        def quitWindow():
            logging.debug("-- Exiting Mi Create --")
            logging.debug("Saving Window State")
            self.saveWindowState()
            logging.debug("Quitting")
            event.accept()

        if self.fileChanged == True: 
            # Ask user if they want to exit 
            quit_msg = "You have unsaved project(s) open. Save and quit?" 
            reply = QMessageBox.warning(self, 'Mi Create', quit_msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                logging.debug("Saving all unsaved projects") 
                self.saveProjects("all")
                quitWindow()
            
            elif reply == QMessageBox.No:
                quitWindow()

            else:
                event.ignore()
        else:
            quitWindow()

    def invokeHistory(self, invokeType):
        currentProject = self.getCurrentProject()
        entry = None
        
        if invokeType == "undo":
            entry = self.historySystem.undo()
        elif invokeType == "redo":
            entry = self.historySystem.redo()
        else:
            self.showDialogue("error", "Unknown history invoke type! Must be either 'undo' or 'redo'.")

        print(self.historySystem.index, self.historySystem.history, entry)

        propertyField = self.propertiesWidget.propertyItems[entry[1]]
        if type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == list:
            print("list")
            for widget in currentProject["data"]["FaceProject"]["Screen"]["Widget"]:
                if widget["@Name"] == entry[0]:
                    widget[entry[1]] == entry[2]
                    break
        elif type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == dict:
            print("dict")
            currentProject["data"]["FaceProject"]["Screen"]["Widget"][entry[1]] == entry[2]
        currentProject["canvas"].selectObject(widget["@Name"])

        if propertyField.metaObject().className() == "QSpinBox":
            propertyField.setValue(int(entry[2]))
        else:
            propertyField.setText(entry[2])

    def getCurrentProject(self):
        currentIndex = self.ui.workspace.currentIndex()
        currentProject = self.projects[self.ui.workspace.tabText(currentIndex)]
        return currentProject

    def saveWindowState(self):
        settings = QSettings("Mi Create", "Workspace")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())

    def loadWindowState(self):
        settings = QSettings("Mi Create", "Workspace")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("state"))

    def saveSettings(self):
        settings = QSettings("Mi Create", "Preferences")
        settings.setValue("theme", self.preferences.themeComboBox.currentText())
        settings.setValue("language", self.preferences.languageComboBox.currentText())

    def loadSettings(self):
        settings = QSettings("Mi Create", "Preferences")
        theme = settings.value("theme", "Dark")
        language = settings.value("language", "English")
        self.preferences.themeComboBox.setCurrentText(theme)
        self.preferences.languageComboBox.setCurrentText(language)

    def launchUpdater(self):
        self.closeWithoutWarning = True
        self.close()
        Updater().start()
        sys.exit()

    def checkForUpdates(self):
        # Contacts GitHub server for current version and compares installed to current version
        version = currentVersion
        if version > currentVersion:
            if version[-1] == 'u':
                self.showDialogue('info', f'An urgent update {version} was released! The app will now update.')
                self.launchUpdater()
            else:
                reply = QMessageBox.question(self, f'A new update has been found (v{version}). Would you like to update now?', QMessageBox.Yes, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    self.launchUpdater()


    def loadTheme(self):
        # Loads theme from themeComboBox element. Later on will load the theme from the QSettings directly
        themeName = self.preferences.themeComboBox.currentText()
        app = QApplication.instance()
        if themeName == "Light":
            theme.light(app)
            self.showDialogue('info', 'Icons in light theme have not been implemented yet. Sorry!')
        elif themeName == "Dark":
            theme.dark(app)

    def setupWorkspace(self):
        # Fires when tab closes
        def handleTabClose(index):
            def delWidget():
                if isinstance(currentWidget, MonacoWidget):
                    logging.debug("Monaco widget found! Deleting") 
                    currentWidget.setParent(None)
                    currentWidget.close()
                    currentWidget.deleteLater()
                elif isinstance(currentWidget, QGraphicsScene):
                    logging.debug("Project viewport found! Deleting") 
                    projectData = self.projects.pop(currentTabName)
                    project = projectData[0]
                    project.setParent(None)
                    project.close()
                    project.deleteLater()
                
                self.ui.workspace.removeTab(index)
                if self.projects.get(currentTabName):
                    del self.projects[currentTabName]
                self.fileChanged = False

            currentWidget = self.ui.workspace.widget(index)
            currentTabName = self.ui.workspace.tabText(index)
            if self.projects[currentTabName]["hasFileChanged"]:
                reply = QMessageBox.warning(self, 'Mi Create', 'This tab has unsaved changes. Save and close?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    self.saveProjects("current")
                    delWidget()
                elif reply == QMessageBox.No:
                    delWidget()
            else:
                delWidget()

        # Fires when tab changes
        def handleTabChange(index): 
            tabName = self.ui.workspace.tabText(index)
            self.setWindowTitle(tabName+" - Mi Create")
            if self.projects.get(tabName):
                tabData = self.projects[tabName]
                if tabData.get("canvas") != None:
                    logging.debug("Updating explorer with "+str(tabData["data"])) 
                    self.updateExplorer(tabData["data"])
                    self.propertiesWidget.imageFolder = tabData["imageFolder"]
                    threading.Thread(target=self.propertiesWidget.reloadResourceImages).start()
                    logging.debug("Thread started to reload resource dialog images")
                else:
                    self.clearExplorer()
                    self.updateProperties(False)
            else:
                self.clearExplorer()
                self.updateProperties(False)

        # setup compile dialog
        
        okButton = QPushButton()
        okButton.setText("OK")

        widget = QWebEngineView()
        widget.setUrl("")
        self.ui.workspace.addTab(widget, "init")

        self.compileUi.buttonBox.addButton(okButton, QDialogButtonBox.AcceptRole)
        
        # Connect objects in the Insert menu to actions
        self.ui.actionImage.triggered.connect(lambda: self.createCanvasWidget("30"))
        self.ui.actionImage_List.triggered.connect(lambda: self.createCanvasWidget("31"))
        self.ui.actionDigital_Number.triggered.connect(lambda: self.createCanvasWidget("32"))
        self.ui.actionAnalog_Display.triggered.connect(lambda: self.createCanvasWidget("27"))
        self.ui.actionArc_Progress.triggered.connect(lambda: self.createCanvasWidget("42"))

        # Connect links in the welcome screen to actions
        self.ui.NewProject.linkActivated.connect(lambda: self.ui.actionNewFile.trigger())
        self.ui.OpenProject.linkActivated.connect(lambda: self.ui.actionOpenFile.trigger())

        # Connect tab changes
        self.ui.workspace.tabCloseRequested.connect(handleTabClose)
        self.ui.workspace.currentChanged.connect(handleTabChange)

    def setupExplorer(self):
        def updateExplorerSelection():
            currentIndex = self.ui.workspace.currentIndex()
            if self.projects.get(self.ui.workspace.tabText(currentIndex)):
                selected = False
                currentProject = self.getCurrentProject()
                #print(currentProject["canvas"].getSelectedObject())
                for x in currentProject["canvas"].items():
                    if currentProject["canvas"].getSelectedObject() != []:
                        # check if current selected object is not already selected
                        if x.data(0) == currentProject["canvas"].getSelectedObject()[0]:
                            selected = True

                if not selected:
                    for x in self.ui.Explorer.selectedItems():
                        currentProject["canvas"].selectObject(x.text(0))

        self.ui.Explorer.itemSelectionChanged.connect(updateExplorerSelection)

    def clearExplorer(self):
        self.ui.Explorer.clear()

    def updateExplorer(self, data):
        def createItem(x):
            objectIcon = QIcon()
            if ObjectIcon().icon.get(x["@Shape"]):
                objectIcon.addFile(ObjectIcon().icon[x["@Shape"]], QSize(), QIcon.Normal, QIcon.Off)
                object = QTreeWidgetItem(root)
                object.setText(0, x["@Name"])
                object.setIcon(0, objectIcon)
                object.setFlags(object.flags() | Qt.ItemIsEditable)
                object.setData(0, 100, x["@Shape"])
                object.setData(0, 101, x["@Name"])
                self.explorer[x["@Name"]] = object
            else:
                self.showDialogue("error", f"Widget {x['@Shape']} not implemented in ObjectIcon(), please report as issue.")

        self.explorer = {}
        self.ui.Explorer.clear()
        self.ui.Explorer.setAnimated(True)
        icon = QIcon()
        icon.addFile(u":/Dark/watch.png", QSize(), QIcon.Normal, QIcon.Off)
        name = None
        if data["FaceProject"]["Screen"]["@Title"] == "":
            name = "Watchface"
        else:
            name = data["FaceProject"]["Screen"]["@Title"]
        root = QTreeWidgetItem(self.ui.Explorer)
        root.setText(0, name)
        root.setIcon(0, icon)
        root.setData(0, 100, "00")
        root.setFlags(root.flags() | Qt.ItemIsEditable)
        if data["FaceProject"]["Screen"].get("Widget") != None:
            if type(data["FaceProject"]["Screen"].get("Widget")) == list:
                for x in data["FaceProject"]["Screen"]["Widget"]:
                    createItem(x)      
            else:
                createItem(data["FaceProject"]["Screen"].get("Widget"))  
            
        self.ui.Explorer.expandAll()

    def setupProperties(self):
        def setProperty(args):
            currentProject = self.getCurrentProject()
            currentSelected = self.ui.Explorer.currentItem()
            currentItem = None
            currentProject["hasFileChanged"] = True
            self.fileChanged = True
            logging.debug(f"Set property {args[0]}, {args[1]} for widget {currentSelected.data(0,101)}" )
            if type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == list:
                for i in currentProject["data"]["FaceProject"]["Screen"]["Widget"]:
                    if i["@Name"] == currentSelected.data(0,101):
                        currentItem = i
                        break
                else:
                    self.showDialogue("error", "Failed to obtain currentItem", "No object found in widget list that has the name of currently selected graphics item: "+str(currentProject["data"]["FaceProject"]["Screen"]["Widget"]))
            else:
                currentItem = currentProject["data"]["FaceProject"]["Screen"]["Widget"]

            self.historySystem.addToHistory(currentSelected.data(0,101), args[0], args[1])
            
            if args[0] == "@Value_Src" or args[0] == "@Index_Src" or args[0] == "@Visible_Src":
                for x in self.watchData.modelSourceData[str(currentProject["data"]["FaceProject"]["@DeviceType"])]:
                    if x["@Name"] == args[1]:
                        try:
                            currentItem[args[0]] = int(x["@ID"], 0)
                        except:
                            currentItem[args[0]] = int(x["@ID"])

            else:
                currentItem[args[0]] = args[1]
                currentProject["canvas"].setObjectProperty(currentSelected.data(0,101), args[0], args[1])

        # Setup properties widget
        with open("data\\properties.json", encoding="utf8") as raw:
            propertiesSource = raw.read()
            self.propertyJson = json.loads(propertiesSource)
            self.propertiesWidget = PropertiesWidget(self, Ui_ResourceDialog, self.watchData.modelSourceList, self.watchData.modelSourceData, QApplication.instance().primaryScreen())
            self.propertiesWidget.propertyChanged.connect(lambda *args: setProperty(args))
            self.ui.propertiesWidget.setWidget(self.propertiesWidget)

    def updateProperties(self, item):
        if item:
            currentProject = self.getCurrentProject()
            # data(0,100) is objectID, data(0,101) is name
            if type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == list:
                for index, object in enumerate(currentProject["data"]["FaceProject"]["Screen"]["Widget"]):
                    if object["@Name"] == item.data(0,101):
                        self.propertiesWidget.loadProperties(self.propertyJson[item.data(0, 100)], currentProject["data"]["FaceProject"]["Screen"]["Widget"][index], currentProject["data"]["FaceProject"]["@DeviceType"])
                        break
                else:
                    self.showDialogue("error", "Error occured during property update: Object not found!", f'Unable to find {object["@Name"]}.')
            else:
                if currentProject["data"]["FaceProject"]["Screen"]["Widget"]["@Name"] == item.data(0,101):
                    self.propertiesWidget.loadProperties(self.propertyJson[item.data(0, 100)], currentProject["data"]["FaceProject"]["Screen"]["Widget"], currentProject["data"]["FaceProject"]["@DeviceType"])
        else:
            self.propertiesWidget.clearProperties() 

    def updateObjectProperty(self, name, property, value):
        currentProject = self.getCurrentProject()
        for index, object in enumerate(currentProject["data"]["FaceProject"]["Screen"]["Widget"]):
            if object["@Name"] == name:
                object[property] = value
                break
        self.propertiesWidget.propertyItems[property].setText(value)

    def setupScaffold(self):
        with open("data\\default\\defaultItems.json", encoding="utf8") as raw:
            self.defaultSource = raw.read()
        self.defaultScaffold = json.loads(self.defaultSource)

    def setupNewProjectDialog(self):
        def check():
            if self.newProjectUi.projectName.text() != "":
                if self.newProjectUi.folderLocation.text() != "":
                    self.newProjectUi.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
                else:
                    self.newProjectUi.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            else:
                self.newProjectUi.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        def openFolderDialog():
            location = QFileDialog.getExistingDirectory(self, 'Select Folder...', "")
            self.newProjectUi.folderLocation.setText(str(location))

        check()
        self.newProjectUi.deviceSelection.addItems(self.watchData.models)
        self.newProjectUi.projectName.textChanged.connect(check)
        self.newProjectUi.folderLocation.textChanged.connect(check)
        self.newProjectUi.folderShow.clicked.connect(openFolderDialog)

    def changeSelectionInExplorer(self, name):
        self.ui.Explorer.setCurrentItem(self.explorer[name])

    def createCanvasWidget(self, id):
        count = 0
        currentProject = self.getCurrentProject()
        if not currentProject["data"]["FaceProject"]["Screen"].get("Widget"):
            currentProject["data"]["FaceProject"]["Screen"]["Widget"] = []
        elif type(currentProject["data"]["FaceProject"]["Screen"].get("Widget")) == dict:
            currentProject["data"]["FaceProject"]["Screen"]["Widget"] = [currentProject["data"]["FaceProject"]["Screen"]["Widget"]]
        for key in currentProject["data"]["FaceProject"]["Screen"]["Widget"]:
            if "widget-" in key["@Name"]:
                count += 1
        defaultScaffold = json.loads(self.defaultSource)
        widgetData = defaultScaffold[id]
        widgetData["@Name"] = "widget-" + str(count)
        widgetData["@X"] = int(currentProject["canvas"].scene.sceneRect().width()/2 - int(widgetData["@Width"])/2)
        widgetData["@Y"] = int(currentProject["canvas"].scene.sceneRect().height()/2 - int(widgetData["@Height"])/2)
        currentProject["data"]["FaceProject"]["Screen"]["Widget"].append(widgetData) 
        currentProject["canvas"].loadObjectsFromData(currentProject["data"], currentProject["imageFolder"], self.preferences.AntialiasingEnabled.isChecked())
        self.updateExplorer(currentProject["data"])
        currentProject["canvas"].selectObject(widgetData["@Name"])

    def copyCanvasWidget(self):
        currentProject = self.getCurrentProject()
        selectedObjects = currentProject["canvas"].getSelectedObject()

        for object in selectedObjects:
            # replace all shitty for loops with code below 
            if type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == dict:
                currentProject["data"]["FaceProject"]["Screen"]["Widget"] = [currentProject["data"]["FaceProject"]["Screen"]["Widget"]]
            result = list(filter(lambda widget: widget["@Name"] == object.data(0),  currentProject["data"]["FaceProject"]["Screen"]["Widget"]))
            self.clipboard = result

    def pasteCanvasWidget(self):
        currentProject = self.getCurrentProject()
        if type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == dict:
                currentProject["data"]["FaceProject"]["Screen"]["Widget"] = [currentProject["data"]["FaceProject"]["Screen"]["Widget"]]

        for item in self.clipboard:
            result = list(filter(lambda widget: item["@Name"] == widget["@Name"],  currentProject["data"]["FaceProject"]["Screen"]["Widget"]))
            item["@Name"] = f"{item['@Name']}-{len(result)}"
            currentProject["data"]["FaceProject"]["Screen"]["Widget"].append(item)
            currentProject["canvas"].loadObjectsFromData(currentProject["data"], currentProject["imageFolder"], self.preferences.AntialiasingEnabled.isChecked())
            self.updateExplorer(currentProject["data"])
            currentProject["canvas"].selectObject(item["@Name"])

    def createNewWorkspace(self, name, isFprj, data, xml): 
        # data[0] is watchface data while data[1] is image data
        # projects are technically "tabs"
        self.previousSelected = None
        if not self.projects.get(name):
            def selectionChange(project):
                if project.scene.selectedItems() != []:
                    for x in project.scene.selectedItems():
                        if self.previousSelected != project.scene.selectedItems():
                            self.previousSelected = project.scene.selectedItems()
                            #print(project.scene.selectedItems())
                            self.changeSelectionInExplorer(x.data(0))
                            self.updateProperties(self.explorer[x.data(0)])
                            break
                else:
                    self.previousSelected = None
                    self.ui.Explorer.currentItem().setSelected(False)
                    self.updateProperties(False)

            def objectDeleted(objectName):
                print("del")
                currentProject = self.getCurrentProject()
                if type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == list:
                    for index, obj in enumerate(currentProject["data"]["FaceProject"]["Screen"]["Widget"]):
                        if obj["@Name"] == objectName:
                            currentProject["data"]["FaceProject"]["Screen"]["Widget"].pop(index)
                elif type(currentProject["data"]["FaceProject"]["Screen"]["Widget"]) == dict:
                    currentProject["data"]["FaceProject"]["Screen"]["Widget"] = []
                currentProject["canvas"].loadObjectsFromData(currentProject["data"], currentProject["imageFolder"], self.preferences.AntialiasingEnabled.isChecked())
                self.updateExplorer(currentProject["data"])

            def propertyChange(objectName, propertyName, propertyValue):
                propertyField = self.propertiesWidget.propertyItems[propertyName]

                if isinstance(propertyValue, list):
                    propertyValue = propertyValue[0]

                if propertyField.metaObject().className() == "QSpinBox":
                    propertyField.setValue(int(propertyValue))
                else:
                    propertyField.setText(propertyValue)

            # Setup Project
            self.projectXML = xml
            self.ui.Explorer.clear()
                
            # Create a Canvas (QGraphicsScene & QGraphicsView)
            project = Canvas(data[0]["FaceProject"]["@DeviceType"], self.preferences.AntialiasingEnabled.isChecked(), self.preferences.DeviceOutlineVisible.isChecked(), self.ui.menuInsert)

            # Create the project
            project.setAcceptDrops(True)
            project.scene.selectionChanged.connect(lambda: selectionChange(project))
            project.objectChanged.connect(propertyChange)
            project.objectDeleted.connect(objectDeleted)
            #project.objectAdded.connect(addObjectOnDrop)

            # Add Icons
            if isFprj:
                icon = QPixmap(":/Dark/folder-clock.png")
            else:
                icon = QPixmap(":/Dark/file-clock.png")

            success = True

            # Render objects onto the canvas
            if data is not False:
                success = project.loadObjectsFromData(data[0], data[1], self.preferences.AntialiasingEnabled.isChecked())
                
            if success[0]:
                self.projects[name] = {
                    "canvas": project, 
                    "data": data[0], 
                    "imageFolder": data[1], 
                    "hasFileChanged": False, 
                    "xml": xml
                }

                # Setup Insert Menu
                insertButton = QToolButton()
                insertButton.setMenu(self.ui.menuInsert)
                insertButton.setPopupMode(QToolButton.InstantPopup)
                insertButton.setIcon(QPixmap(":Dark/plus.png"))
                insertButton.setText("Create Widget")
                insertButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

                # Setup AOD Switch
                # AODSwitch = QToolButton()
                # AODSwitch.setIcon(QPixmap(":Dark/moon.png"))
                # AODSwitch.setIconSize(QSize(16,16))
                # AODSwitch.setText("Toggle AOD")
                # AODSwitch.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                # AODSwitch.setCheckable(True)

                canvasToolbar = QToolBar()
                canvasToolbar.setStyleSheet("background-color: palette(base); padding-left: 20px; ")
                canvasToolbar.addWidget(insertButton)
                # canvasToolbar.addWidget(AODSwitch)

                widget = QWidget()
                layout = QVBoxLayout()
                layout.addWidget(canvasToolbar)
                layout.addWidget(project)
                layout.setContentsMargins(0,0,0,0)
                layout.setSpacing(0)
                widget.setLayout(layout)

                index = self.ui.workspace.addTab(widget, icon, name)
                self.ui.workspace.setCurrentIndex(index)
                project.setFrameShape(QFrame.NoFrame)
            else:
                self.showDialogue("error", f"Cannot render project! {success[1]}", success[1])
        else:
           self.ui.workspace.setCurrentIndex(self.ui.workspace.indexOf(self.projects[name][0]))

    def createNewCodespace(self, name, text, language, options={"cursorSmoothCaretAnimation":"on"}):
        # Creates a new instance of Monaco in a Codespace (code workspace)
        editor = MonacoWidget()
        editor.setText(text)
        editor.setLanguage(language)
        editor.setEditorOptions(options)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(editor)
        widget.setLayout(layout)

        icon = QPixmap(":/Dark/file-code-2.png")
        index = self.ui.workspace.addTab(widget, icon, name)
        self.projects[name] = {
            "hasFileChanged": False
        }
        self.ui.workspace.setCurrentIndex(index)

    def setupWidgets(self):
        # Connect menu actions

        # file
        self.ui.actionNewFile.triggered.connect(self.newProject)
        self.ui.actionOpenFile.triggered.connect(self.openProject)
        self.ui.actionSave.triggered.connect(lambda: self.saveProjects("current"))
        self.ui.actionExit.triggered.connect(self.close)

        # edit
        self.ui.actionCopy.triggered.connect(self.copyCanvasWidget)
        self.ui.actionPaste.triggered.connect(self.pasteCanvasWidget)
        self.ui.actionUndo.triggered.connect(lambda: self.invokeHistory("undo"))
        self.ui.actionRedo.triggered.connect(lambda: self.invokeHistory("redo"))
        self.ui.actionProject_XML_File.triggered.connect(self.editProjectXML)
        self.ui.actionPreferences.triggered.connect(self.showPreferences)

        # compile
        self.ui.actionBuild.triggered.connect(self.compileProject)
        self.ui.actionUnpack.triggered.connect(self.decompileProject)

        # help
        self.ui.actionDocumentation.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://ooflet.github.io/docs", QUrl.TolerantMode)))
        self.ui.actionAbout_MiFaceStudio.triggered.connect(self.showAboutWindow)
        self.ui.actionAbout_Qt.triggered.connect(lambda: QMessageBox.aboutQt(self))
        self.ui.actionThirdPartyNotice.triggered.connect(self.showThirdPartyNotices)

        # preferences
        self.preferences.clearWindow.clicked.connect(self.clearWindowState)
        self.preferences.openDataFolder.clicked.connect(lambda *event: subprocess.Popen(f'explorer /select, data"'))
        self.preferences.reinstall.clicked.connect(self.launchUpdater)
        self.preferences.buttonBox.accepted.connect(self.saveAndLoadPreferences)

    def clearWindowState(self):
        reply = QMessageBox.question(self, 'Confirm Clear', "This will clear the positions of dock widgets/windows and restart the app. Confirm?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            settings = QSettings("Mi Create", "Workspace")
            settings.setValue("geometry", None)
            settings.setValue("state", None)
            os.execl(sys.executable, sys.executable, *sys.argv)

    def saveAndLoadPreferences(self):
        self.saveSettings()
        self.loadSettings()
        self.loadTheme()

    def newProject(self):
        self.newProjectDialogAccepted = False

        def accept():
            self.newProjectDialogAccepted = True

        self.newProjectDialog.accepted.connect(accept)

        # Get where to save the project
        self.newProjectDialog.exec()
        
        if self.newProjectDialogAccepted:
            # Get file location from dialog
            file = self.newProjectUi.folderLocation.text()
            projectName = self.newProjectUi.projectName.text()
            watchModel = self.newProjectUi.deviceSelection.currentText()

            # Clear dialog text
            self.newProjectUi.folderLocation.setText("")
            self.newProjectUi.projectName.setText("")
            
            file_extension = QFileInfo(file).suffix()
            isFprj = False

            # Check if file was selected
            if file:
                accepted = True
                if file[0] != "C" and file[0] != "/":
                    reply = QMessageBox.question(self, 'Confirm Path', "Your project will be created in the install directory of this program. Confirm?", QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        accepted = True
                    else:
                        accepted = False

                if accepted:
                    newProject = fprjProject.create(file, self.watchData.modelID[str(watchModel)], projectName)
                    if newProject[0]:
                        project = fprjProject.load(newProject[1])
                        if project[0]:
                            try:
                                self.createNewWorkspace(newProject[1], True, [project[1], project[2]], project[3])    
                            except Exception as e:
                                self.showDialogue("error", f"Failed to createNewWorkspace: {e}.", traceback.format_exc())
                        else:
                            self.showDialogue("error", f'Cannot open project: {project[1]}.', project[2])
                    else:
                        self.showDialogue("error", f"Failed to create a new project: {newProject[1]}.", newProject[2])

    def openProject(self): 
        # Get where to open the project from
        file = QFileDialog.getOpenFileName(self, 'Open Project...', "%userprofile%\\", "Watchface Project (*.fprj)")
        file_extension = QFileInfo(file[0]).suffix()

        # Check if file was selected
        if file[0]:
            if file_extension == "fprj":
                project = fprjProject.load(file[0])
                if project[0]:
                    try:
                        self.createNewWorkspace(file[0], True, [project[1], project[2]], project[3])    
                    except Exception as e:
                        self.showDialogue("error", f"Failed to open project: {e}.", traceback.format_exc())
                else:
                    self.showDialogue("error", f'Cannot open project: {project[1]}.', project[2])

    def saveProjects(self, projectsToSave):
        if projectsToSave == "all":
            for index, project in enumerate(self.projects):
                if project["hasFileChanged"]:
                    raw = xmltodict.unparse(project["data"])
                    dom = xml.dom.minidom.parseString(raw)
                    pretty_xml = dom.toprettyxml()
                    try:
                        with open(self.ui.workspace.tabText(index), "w", encoding="utf8") as file:
                            file.write(pretty_xml)
                        self.fileChanged = False
                        project["hasFileChanged"] = False
                    except Exception as e:
                        self.statusBar().showMessage("Failed to save: "+str(e), 10000)
                        self.showDialogue("error", "Failed to save project: "+str(e))
        elif projectsToSave == "current":
            currentIndex = self.ui.workspace.currentIndex()
            currentName = self.ui.workspace.tabText(currentIndex)
            currentProject = self.getCurrentProject()

            raw = xmltodict.unparse(currentProject["data"])
            dom = xml.dom.minidom.parseString(raw)
            pretty_xml = dom.toprettyxml()

            try:
                with open(currentName, "w", encoding="utf8") as file:
                    file.write(pretty_xml)
                self.statusBar().showMessage("Project saved at "+currentName, 2000)
            except Exception as e:
                self.statusBar().showMessage("Failed to save: "+str(e), 10000)
                self.showDialogue("error", "Failed to save project: "+str(e))
    
    def compileProject(self):
        if self.projects.get(self.ui.workspace.tabText(self.ui.workspace.currentIndex())):
            if self.ui.workspace.tabText(self.ui.workspace.currentIndex()) != "Welcome" and self.ui.workspace.tabText(self.ui.workspace.currentIndex()) != "Project XML":
                reply = QMessageBox.question(self, 'Mi Create', "Save project before building?", QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.saveProjects("current")
                QApplication.processEvents()
                
                currentIndex = self.ui.workspace.currentIndex()
                currentName = self.ui.workspace.tabText(currentIndex)
                compileDirectory = os.path.join(os.path.dirname(currentName), "output")

                self.compileUi.buttonBox.setDisabled(True)
                self.compileUi.textEdit.setReadOnly(True)
                self.compileUi.stackedWidget.setCurrentIndex(1)
                self.compileDialog.setModal(True)
                self.compileDialog.show()
                QApplication.processEvents()

                result = fprjProject.compile(currentName, compileDirectory, "compiler\\compile.exe")
                self.compileUi.buttonBox.setDisabled(False)
                self.compileUi.textEdit.setText(str(result))
                self.compileUi.stackedWidget.setCurrentIndex(2) 

    def decompileProject(self):
        self.showDialogue("error", "Will add later, apologies.")
        # self.showDialogue("warning", "Please note that images may be glitched when unpacking.")
        # file = QFileDialog.getOpenFileName(self, 'Unpack File...', "%userprofile%\\", "Compiled Watchface Binaries (*.face)")

        # subprocess.run(f'{currentDir}\\compiler\\unpack.exe  "{file[0]}"')
        # self.showDialogue("info", "Decompile success! Would you like to open")

    def editProjectXML(self):
        if self.projects.get(self.ui.workspace.tabText(self.ui.workspace.currentIndex())) and not self.ui.workspace.tabText == "Welcome":
            self.createNewCodespace("Project XML", self.getCurrentProject()["xml"], "xml")

    def showColorDialog(self):
        color = QColorDialog.getColor(Qt.white, self, "Select Color")

    def showFontSelect(self):
        font = QFontDialog.getFont(self, "Select Font")

    def showPreferences(self):
        self.loadSettings()
        self.preferencesDialog.exec()

    def showAboutWindow(self):
        dialog = QMessageBox(self)
        dialog.setText(f'<html><head/><body><p>Mi Create v{currentVersion}<br/><a href="https://github.com/ooflet/Mi-Create/"><span style=" text-decoration: underline; color:#55aaff;">https://github.com/ooflet/Mi-Create/</span></a></p><p>made with 💖 by tostr</p></body></html>')
        dialog.setIconPixmap(QPixmap(":/Images/MiCreate48x48.png"))
        dialog.setWindowTitle("About Mi Create")
        dialog.exec()

    def showThirdPartyNotices(self):
        dialog = QMessageBox(self)
        dialog.setText('<html><head/><body><p><span style=" text-decoration: underline;">Third Party Notices</span></p><p><a href="https://doc.qt.io/qtforpython-6/"><span style=" text-decoration: underline; color:#55aaff;"> Qt6 + PySide6</span></a> - Under LGPLv3 License<br/><a href="https://lucide.dev"><span style=" text-decoration: underline; color:#55aaff;">Lucide Icons</span></a> - Under MIT License<br/>      <a href="https://github.com/microsoft/monaco-editor"><span style=" text-decoration: underline; color:#55aaff;">Monaco Editor</span></a> - Under MIT License<br/><a href="https://github.com/DaelonSuzuka/monaco-qt"><span style=" text-decoration: underline; color:#55aaff;">monaco-qt</span></a> - Under MIT License<br/>m0tral\'s Compiler - Under explicit permission</p></body></html>')
        dialog.setWindowTitle("Third Party Notices")
        dialog.exec()

    def showDialogue(self, type, text, detailedText=""):
        MessageBox = QMessageBox(self)
        MessageBox.setWindowTitle("Mi Create")
        MessageBox.setWindowIcon(QPixmap(":/Images/MiCreate48x48.png"))
        MessageBox.setText(text)
        MessageBox.setDetailedText(detailedText)
        if type == "info":
            MessageBox.setIcon(QMessageBox.Information)
        elif type == "question":
            MessageBox.setIcon(QMessageBox.Question)
        elif type == "warning":
            logging.warning(text)
            MessageBox.setIcon(QMessageBox.Warning)
        elif type == "error":
            logging.error(text+"\nDetailed output: "+detailedText)
            MessageBox.setIcon(QMessageBox.Critical)
        MessageBox.exec()
            
if __name__ == "__main__":
    import sys

    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"
    app = QApplication(sys.argv)

    # splash
    pixmap = QPixmap(":/Images/MiCreateSplash.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    try:
        main_window = MainWindow()
        main_window.ui.workspace.removeTab(1)
    except Exception as e:
        error_message = f"Critical error during initialization: {traceback.format_exc()}"
        logging.error(error_message)
        QMessageBox.critical(None, 'Error', error_message, QMessageBox.Ok)
        sys.exit(1)

    main_window.show()
    
    splash.finish(main_window)
    main_window.checkForUpdates()

    sys.exit(app.exec())