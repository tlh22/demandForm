""" ***


*** """
from qgis.PyQt.QtCore import (
    QObject,
    QTimer,
    QThread,
    pyqtSignal,
    pyqtSlot, Qt, QModelIndex
)

from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QAction,
    QDialogButtonBox,
    QLabel,
    QDockWidget,
    QDialog,
    QLabel,
    QPushButton,
    QApplication,
    QComboBox, QSizePolicy, QGridLayout,
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QTableView, QTableWidgetItem, QListView, QGroupBox,
    QRadioButton, QButtonGroup, QDataWidgetMapper, QSpacerItem, QLineEdit, QSpacerItem,
    QProgressDialog, QProgressBar, QTextEdit, QTabWidget
)

from qgis.PyQt.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelation, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlTableModel
)

from qgis.PyQt.QtGui import (
    QIntValidator, QIcon,
    QPixmap,
    QImage, QPainter
)

from qgis.core import (
    Qgis
)

from TOMs.core.TOMsMessageLog import TOMsMessageLog

class countWidget(QTableView):

    progressUpdated = pyqtSignal(int)
    startOperation = pyqtSignal()
    endOperation = pyqtSignal()

    def __init__(self, parent=None, db=None):
        super(countWidget, self).__init__(parent)
        TOMsMessageLog.logMessage("In countWidget:init ... ", level=Qgis.Info)
        self.dbConn = db
        self.countModel = QSqlRelationalTableModel(self, db=self.dbConn)
        self.restrictionDialog = parent

    def getCountModel(self):
        return self.countModel

    def populateDemandWidget(self, surveyID, GeometryID, extraTabLabel=None):

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... surveyID: {}; GeometryID: {}; extraTabLabel: {}".format(surveyID, GeometryID, extraTabLabel), level=Qgis.Info)

        if self.dbConn.driverName() == 'QPSQL':
            self.countModel.setTable('demand' + '.\"Counts\"')
        else:
            self.countModel.setTable('Counts')

        filterString = "\"SurveyID\" = {} AND \"GeometryID\" = \'{}\'".format(surveyID, GeometryID)
        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... filterString: {}".format(filterString),
                                  level=Qgis.Warning)

        self.countModel.setFilter(filterString)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.countModel)

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... model set ...",
                                  level=Qgis.Warning)
        self.setupMainCountTab()

        if extraTabLabel:
            extraTab = self.setupExtraCountTab()
            TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... new tab added ...",
                                      level=Qgis.Warning)
            demandTab = self.restrictionDialog.findChild(QTabWidget, "Details")
            demandTab.insertTab(1, extraTab, extraTabLabel)  # 0 based index
            self.setupExtraCountTabMapping()

        result = self.countModel.select()
        if result == False:
            TOMsMessageLog.logMessage(
                "In populateDemandWidget: No result from select: {} ".format(self.countModel.lastError().text()),
                level=Qgis.Warning)

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... selected ...",
                                  level=Qgis.Warning)

        TOMsMessageLog.logMessage(
            "In populateDemandWidget: nr Rows: {} ".format(self.countModel.rowCount()),
            level=Qgis.Warning)

        self.mapper.toFirst()  # TODO: check if this fails ...

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... finishing ...",
                                  level=Qgis.Warning)

    def setupMainCountTab(self):

        demandTab = self.restrictionDialog.findChild(QWidget, "Demand")
        demandLayout = demandTab.layout()

        countLayout = QHBoxLayout()
        col1_layout = QFormLayout()
        col2_layout = QFormLayout()

        #spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        col1_layout.addRow("Cars:", QLineEdit(objectName='NrCars'))
        col1_layout.addRow("LGVs:", QLineEdit(objectName='NrLGVs'))
        col1_layout.addRow("MCLs:", QLineEdit(objectName='NrMCLs'))
        col1_layout.addRow("Taxis:", QLineEdit(objectName='NrTaxis'))
        col1_layout.addRow("OGVs:", QLineEdit(objectName='NrOGVs'))
        col1_layout.addRow("Mini Buses:", QLineEdit(objectName='NrMiniBuses'))

        col2_layout.addRow("PCLs:", QLineEdit(objectName='NrPCLs'))
        col2_layout.addRow("E-Scooters:", QLineEdit(objectName='NrEScooters'))
        col2_layout.addRow("Dockless PCLs:", QLineEdit(objectName='NrDocklessPCLs'))
        col2_layout.addRow("Buses:", QLineEdit(objectName='NrBuses'))
        #col2_layout.addRow(spacerItem)
        col2_layout.addRow("Spaces:", QLineEdit(objectName='NrSpaces'))

        countLayout.addLayout(col1_layout)
        verticalSpacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        countLayout.addItem(verticalSpacer)
        countLayout.addLayout(col2_layout)

        # Now add "Notes" widget
        notes_layout = QFormLayout()
        notes_layout.addRow("Notes:", QTextEdit(objectName='Notes'))

        demandLayout.addLayout(countLayout, 0, 0)
        # demandLayout.addItem(QSpacerItem(1, 1), 1, 0)
        demandLayout.addLayout(notes_layout, 2, 0)

        # add validators
        # use of validator - https://stackoverflow.com/questions/54741145/i-use-qdoublevalidator-in-my-pyqt5-program-but-it-doesnt-seem-to-work

        for widget in countLayout.parentWidget().findChildren(QLineEdit):
            widget.setValidator(QIntValidator(
                0,  # bottom
                200  # top
            ))

        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrCars"), self.countModel.fieldIndex('NrCars'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrLGVs"), self.countModel.fieldIndex('NrLGVs'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMCLs"), self.countModel.fieldIndex('NrMCLs'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrTaxis"), self.countModel.fieldIndex('NrTaxis'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrPCLs"), self.countModel.fieldIndex('NrPCLs'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrEScooters"), self.countModel.fieldIndex('NrEScooters'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrDocklessPCLs"), self.countModel.fieldIndex('NrDocklessPCLs'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrOGVs"), self.countModel.fieldIndex('NrOGVs'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMiniBuses"), self.countModel.fieldIndex('NrMiniBuses'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrBuses"), self.countModel.fieldIndex('NrBuses'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrSpaces"), self.countModel.fieldIndex('NrSpaces'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QTextEdit, "Notes"), self.countModel.fieldIndex('Notes'))

        TOMsMessageLog.logMessage("In countWidget:setupMainCountTab ... mapping added ...",
                                  level=Qgis.Warning)

    def setupExtraCountTab(self):

        TOMsMessageLog.logMessage("In countWidget:setupExtraCountTab ... starting ...",
                                  level=Qgis.Warning)

        extraTab = QWidget()
        demandLayout = QGridLayout(extraTab)

        countLayout = QHBoxLayout()
        col1_layout = QFormLayout()
        col2_layout = QFormLayout()

        #spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        col1_layout.addRow("Cars on YL:", QLineEdit(objectName='NrCars_Suspended'))
        col1_layout.addRow("LGVs on YL:", QLineEdit(objectName='NrLGVs_Suspended'))
        col1_layout.addRow("MCLs on YL:", QLineEdit(objectName='NrMCLs_Suspended'))
        col1_layout.addRow("Taxis on YL:", QLineEdit(objectName='NrTaxis_Suspended'))
        col1_layout.addRow("OGVs on YL:", QLineEdit(objectName='NrOGVs_Suspended'))
        col1_layout.addRow("Mini Buses on YL:", QLineEdit(objectName='NrMiniBuses_Suspended'))

        col2_layout.addRow("PCLs on YL:", QLineEdit(objectName='NrPCLs_Suspended'))
        col2_layout.addRow("E-Scooters on YL:", QLineEdit(objectName='NrEScooters_Suspended'))
        col2_layout.addRow("Dockless PCLs on YL:", QLineEdit(objectName='NrDocklessPCLs_Suspended'))
        col2_layout.addRow("Buses on YL:", QLineEdit(objectName='NrBuses_Suspended'))

        countLayout.addLayout(col1_layout)
        verticalSpacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        countLayout.addItem(verticalSpacer)
        countLayout.addLayout(col2_layout)

        demandLayout.addLayout(countLayout, 0, 0)

        # add validators
        # use of validator - https://stackoverflow.com/questions/54741145/i-use-qdoublevalidator-in-my-pyqt5-program-but-it-doesnt-seem-to-work

        for widget in countLayout.parentWidget().findChildren(QLineEdit):
            widget.setValidator(QIntValidator(
                0,  # bottom
                200  # top
            ))

        TOMsMessageLog.logMessage("In countWidget:setupExtraCountTab ... finishing ...",
                                  level=Qgis.Warning)

        return extraTab

    def setupExtraCountTabMapping(self):

        TOMsMessageLog.logMessage("In countWidget:setupExtraCountTabMapping ... starting ...",
                                  level=Qgis.Warning)

        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrCars_Suspended"),
                               self.countModel.fieldIndex('NrCars_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrLGVs_Suspended"),
                               self.countModel.fieldIndex('NrLGVs_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMCLs_Suspended"),
                               self.countModel.fieldIndex('NrMCLs_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrTaxis_Suspended"),
                               self.countModel.fieldIndex('NrTaxis_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrPCLs_Suspended"),
                               self.countModel.fieldIndex('NrPCLs_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrEScooters_Suspended"),
                               self.countModel.fieldIndex('NrEScooters_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrDocklessPCLs_Suspended"),
                               self.countModel.fieldIndex('NrDocklessPCLs_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrOGVs_Suspended"),
                               self.countModel.fieldIndex('NrOGVs_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMiniBuses_Suspended"),
                               self.countModel.fieldIndex('NrMiniBuses_Suspended'))
        self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrBuses_Suspended"),
                               self.countModel.fieldIndex('NrBuses_Suspended'))

        TOMsMessageLog.logMessage("In countWidget:setupExtraCountTab ... mapping added ...",
                                  level=Qgis.Warning)
