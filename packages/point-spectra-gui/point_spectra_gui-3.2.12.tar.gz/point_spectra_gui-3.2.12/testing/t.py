import multiprocessing as mp
import os.path
import pickle
import sys
import time
import warnings

from point_spectra_gui.util.themes import braceyourself, default

try:
    import qtmodern.styles

    q = True
except:
    q = False
    warnings.warn("You're missing the qtmodern package."
                  "to install it use pip install qtmodern")

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSettings

from point_spectra_gui import core
from point_spectra_gui.ui import MainWindow
from point_spectra_gui.util import delete
from point_spectra_gui.util.BasicFunctionality import Basics
from point_spectra_gui.util.excepthook import my_exception_hook


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class TitleWindow:
    def __init__(self, mainName):
        self.mainName = mainName
        self.fileName = ''
        self.debugName = ''

    def setMainName(self, name):
        self.mainName = name

    def setFileName(self, name):
        self.fileName = name

    def setDebugName(self, bool):
        if bool:
            self.debugName = "Debug Mode"
        else:
            self.debugName = ''

    def display(self):
        if self.fileName == '' and self.debugName == '':
            return "{}".format(self.mainName)
        elif self.fileName == '':
            return "{} - {}".format(self.mainName, self.debugName)
        elif self.debugName == '':
            return "{} - {}".format(self.mainName, self.fileName)
        else:
            return "{} - {} - {}".format(self.mainName, self.fileName, self.debugName)


class Ui_MainWindow(MainWindow.Ui_MainWindow, QtCore.QThread, Basics):
    taskFinished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgetList = []
        self.leftOff = 0

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)  # Run the basic window UI
        self.MainWindow = MainWindow
        self.MainWindow.closeEvent = self.closeEvent
        self.title = TitleWindow(self.MainWindow.windowTitle())
        self._readAndApplyWindowAttributeSettings()
        self.menu_item_shortcuts()  # set up the shortcuts
        self.connectWidgets()

        # Check the mode for debugging
        if self.settings.value("debug") == 'true':
            self.debug_mode()
        else:
            self.normal_mode()

        # Check the theme for the UI
        if self.settings.value('theme') == 'braceyourself':
            braceyourself(self.MainWindow)

    def normal_mode(self):
        """
        Change the direction of stdout to print to the UI console instead
        :return:
        """
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = sys.__stderr__
        # sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)
        self._mode(self.actionOn, self.actionOff, False)

    def debug_mode(self):
        """
        Change the direction of stdout to print to the original console
        :return:
        """
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
        self._mode(self.actionOff, self.actionOn, True)

    def _mode(self, obj1, obj2, debug):
        """
        Set the UI in debug or non-debug mode
        Save all the settings and grey out the necessary boxes
        :param obj1:
        :param obj2:
        :param debug:
        :return:
        """
        obj1.setDisabled(False)
        obj2.setDisabled(True)
        self.debug = debug
        self.title.setDebugName(debug)
        self.settings.setValue("debug", self.debug)
        self.MainWindow.setWindowTitle(self.title.display())

    def theme(self, name):
        """
        We have 3 themes
        each has a different situation
                   __________________
                 /__               __\ new()   Something to note:
               v    \            v    \ new()  As you can see whenever moving into or out of
        default     braceyourself    qtmodern  qtmodern we will have to start a new session
               \___^             \___^ new()   default and braceyourself can simply change
                \___________________/ new()    there styling on the spot

        :param name:
        :return:
        """
        settings = self.settings.value('theme')
        if name == settings:
            print("This is already your current theme")

        if name == 'qtmodern':  # User is entering into qtmodern
            self.settings.setValue('theme', name)
            self.new()

        elif settings == 'qtmodern':  # User is leaving qtmodern
            self.settings.setValue('theme', name)
            self.new()

        elif name == 'default':
            self.settings.setValue('theme', name)
            default(self.MainWindow)

        elif name == 'braceyourself':
            self.settings.setValue('theme', name)
            braceyourself(self.MainWindow)
        else:
            print("Something went horribly wrong with your theme, try again?")

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def addWidget(self, obj):
        """
        Organize our widgets using a list
        Each widget is addressed separately due to being in a list
        :param obj:
        :return:
        """
        self.widgetList.append(obj())
        self.widgetList[-1].setupUi(self.centralwidget)
        self.widgetLayout = QtWidgets.QVBoxLayout()
        self.widgetLayout.setObjectName("widgetLayout")
        self.verticalLayout_3.addLayout(self.widgetLayout)
        self.widgetLayout.addWidget(self.widgetList[-1].get_widget())

    def menu_item_shortcuts(self):
        self.actionExit.setShortcut("ctrl+Q")
        self.actionCreate_New_Workflow.setShortcut("ctrl+N")
        self.actionRestore_Workflow.setShortcut("ctrl+O")
        self.actionSave_Current_Workflow.setShortcut("ctrl+S")
        self.okPushButton.setShortcut("Ctrl+Return")

    def connectWidgets(self):
        """
        Connect all the widgets associated with the MainWindow UI
        :return:
        """
        # TODO figure out how to get this code into `MainWindow.py`
        self.addWidget(core.ReadChemCamData.ReadChemCamData)
        self.addWidget(core.BaselineRemoval.BaselineRemoval)
        self.addWidget(core.CrossValidation.CrossValidation)
        self.addWidget(core.DimensionalityReduction.DimensionalityReduction)
        self.addWidget(core.Interpolation.Interpolation)
        self.addWidget(core.LoadData.LoadData)
        self.addWidget(core.WriteToCSV.WriteToCSV)
        self.addWidget(core.RenameData.RenameData)
        self.addWidget(core.MaskData.MaskData)
        self.addWidget(core.MultiplyByVector.MultiplyByVector)
        self.addWidget(core.Normalization.Normalization)
        self.addWidget(core.OutputFolder.OutputFolder)
        self.addWidget(core.PeakAreas.PeakAreas)
        self.addWidget(core.Plot.Plot)
        self.addWidget(core.Plot_ICA_PCA.Plot_ICA_PCA)
        self.addWidget(core.PlotSpectra.PlotSpectra)
        self.addWidget(core.RegressionTrain.RegressionTrain)
        self.addWidget(core.RegressionPredict.RegressionPredict)
        self.addWidget(core.RemoveRows.RemoveRows)
        self.addWidget(core.SplitDataset.SplitDataset)
        self.addWidget(core.StratifiedFolds.StratifiedFolds)
        self.addWidget(core.SubmodelPredict.SubmodelPredict)
        time.sleep(5)
        sys.exit()

    def closeEvent(self, event):
        """
        Write window size and position to config file
        """
        self._writeWindowAttributeSettings()
        event.accept()

    def getWidgetItems(self):
        """
        This function iterates through widgetList
        gets the name of all the fuctions
        and then all of the parameters in the UI
        and write it to a list to be returned

        Iterate through widgetList
        get the names of core, add it to a temp l
        add f list to be the first item in ui_items
        """
        f = []
        ui_items = []
        for f_items in self.widgetList:
            f.append(type(f_items).__name__)
        ui_items.append(f)

        for dat in self.widgetList:
            ui_items.append(dat.getGuiParams())
        return ui_items

    def setWidgetItems(self, dict):
        """
        This function iterates through a `dict`
        and restores the UI
        :param dict:
        :return:
        """
        for f_items in dict[0]:
            """
            Really complex way of running essentially this:
            `self.addWidget(core.SplitDataset.SplitDataset))`
            Part of the reason why we're doing this is because we're saving function
            names to a list, you can't save function instances. So this is the next
            best thing.
            """
            self.addWidget(getattr(getattr(core, f_items), f_items))

        for i in range(1, len(dict)):
            self.widgetList[i - 1].setGuiParams(dict[i])

    def on_save_clicked(self):
        """
        Save the workflow to a *.wrf file
        :return:
        """
        try:
            filename, _filter = QtWidgets.QFileDialog.getSaveFileName(None,
                                                                      "Choose where you want save your file",
                                                                      self.outpath,
                                                                      '(*.wrf)')
            print(filename)
            with open(filename, 'wb') as fp:
                pickle.dump(self.getWidgetItems(), fp)
            self.title.setFileName(filename.split('/')[-1])
            self.MainWindow.setWindowTitle(self.title.display())
        except Exception as e:
            print("File not loaded {}".format(e))

    def on_restore_clicked(self):
        """
        Choose a file
        Set the file to be read
        Pickle load our data and push it through the function setWidgetItems
        :return:
        """
        try:
            filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None,
                                                                      "Open Workflow File",
                                                                      self.outpath,
                                                                      '(*.wrf)')
            print(filename)
            with open(filename, 'rb') as fp:
                self.setWidgetItems(pickle.load(fp))
            self.title.setFileName(filename.split('/')[-1])
            self.MainWindow.setWindowTitle(self.title.display())
        except Exception as e:
            print("File not loaded: {}".format(e))

    def on_delete_module_clicked(self):
        """
        Check to see if the last item is enabled
        If it is, delete the last item in the list
        And then call the del_layout function, which will remove the item from the UI
        :return:
        """
        try:
            if self.widgetList[-1].isEnabled():
                del self.widgetList[-1]
                delete.del_layout(self.verticalLayout_3)
            else:
                print("Cannot delete")
        except:
            print("Cannot delete")

    def on_okButton_clicked(self):
        self.onStart()
        self.taskFinished.connect(self.onFinished)

    def on_undoButton_clicked(self):
        """
        Check to see if the last item in the list is enabled
        subtract 1 from leftOff
        enable the current leftOff item
        :return:
        """
        try:
            if not self.widgetList[-1].isEnabled():
                self.leftOff -= 1
                self.widgetList[self.leftOff].setDisabled(False)
        except:
            pass

    def on_stopButton_clicked(self):
        if self.isRunning():
            self.terminate()
            self.taskFinished.emit()
        else:
            print("There is nothing running right now")

    def _writeWindowAttributeSettings(self):
        '''
        Save window attributes as settings.

        Called when window moved, resized, or closed.
        '''
        self.settings.beginGroup("mainWindow")
        self.settings.setValue("pos", self.MainWindow.pos())
        self.settings.setValue("maximized", self.MainWindow.isMaximized())
        self.settings.setValue('splitter', self.splitter.saveState())
        if not self.MainWindow.isMaximized():
            self.settings.setValue("size", self.MainWindow.size())

        self.settings.endGroup()

    def _readAndApplyWindowAttributeSettings(self):
        '''
        Read window attributes from settings,
        using current attributes as defaults (if settings not exist.)

        Called at QMainWindow initialization, before show().
        '''
        self.settings.beginGroup("mainWindow")
        # No need for toPoint, etc. : PySide converts types
        try:
            self.splitter.restoreState(self.settings.value('splitter'))
            self.MainWindow.move(self.settings.value("pos"))
            if self.settings.value("maximized") in 'true':
                self.MainWindow.showMaximized()
            else:
                self.MainWindow.resize(self.settings.value("size"))
        except:
            pass
        self.settings.endGroup()

    def onStart(self):  # onStart function
        self.progressBar.setRange(0, 0)  # make the bar pulse green
        self.start()  # TaskThread.start()
        # This is multithreading thus run() == start()

    def onFinished(self):  # onFinished function
        self.progressBar.setRange(0, 1)  # stop the bar pulsing green
        self.progressBar.setValue(1)  # displays 100% after process is finished.

    def clear(self):
        while len(self.widgetList) > 0 and self.widgetList[-1].isEnabled():
            self.on_delete_module_clicked()
        self.title.setFileName('')
        self.MainWindow.setWindowTitle(self.title.display())
        self.textBrowser.clear()

    def new(self):
        p = mp.Process(target=main, args=())
        p.start()

    def run(self):
        if self.debug:
            for modules in range(self.leftOff, len(self.widgetList)):
                name_ = type(self.widgetList[modules]).__name__
                s = time.time()
                print("{} Module is Running...".format(name_))
                self.widgetList[modules].function()
                e = time.time()
                print("Module {} executed in: {} seconds".format(name_, e - s))
                self.widgetList[modules].setDisabled(True)
                self.leftOff = modules + 1
            self.taskFinished.emit()

        else:
            try:
                for modules in range(self.leftOff, len(self.widgetList)):
                    name_ = type(self.widgetList[modules]).__name__
                    s = time.time()
                    print("{} Module is Running...".format(name_))
                    self.widgetList[modules].function()
                    e = time.time()
                    print("Module {} executed in: {} seconds".format(name_, e - s))
                    self.widgetList[modules].setDisabled(True)
                    self.leftOff = modules + 1
                self.taskFinished.emit()
            except Exception as e:
                print("Your module broke: please fix.", e)
                self.widgetList[self.leftOff].setDisabled(False)
                self.taskFinished.emit()


def get_splash(app):
    """
    Get the splash screen for the application
    But check to see if the image even exists
    :param app:
    :return:
    """
    dirs = ['../images/', '/point_spectra_gui/images', './point_spectra_gui/images']
    for dir in dirs:
        if os.path.exists(dir + 'splash.png'):
            splash_pix = QPixmap(dir + 'splash.png')  # default
            app_icon = QtGui.QIcon(dir + 'icon.png')
            app.setWindowIcon(app_icon)
            splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
            splash.setMask(splash_pix.mask())
            splash.show()
            time.sleep(0.5)
            app.processEvents()
            return 0


def setDarkmode(app):
    settings = QSettings('USGS', 'PPSG')
    p = settings.value('theme') == 'qtmodern'
    if q and p:
        qtmodern.styles.dark(app)


def main():
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook
    app = QtWidgets.QApplication(sys.argv)
    get_splash(app)
    setDarkmode(app)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
