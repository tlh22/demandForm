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
    QProgressDialog, QProgressBar, QTextEdit, QTabWidget, QPlainTextEdit
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

    def __init__(self, parent, dbConn, demand_schema):
        super(countWidget, self).__init__(parent)
        TOMsMessageLog.logMessage("In countWidget:init ... ", level=Qgis.Info)
        self.dbConn = dbConn
        self.demand_schema = demand_schema
        self.countModel = QSqlRelationalTableModel(self, db=self.dbConn)
        self.restrictionDialog = parent

    def getCountModel(self):
        return self.countModel

    def populateDemandWidget(self, surveyID, GeometryID, extraTabLabel=None):

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... surveyID: {}; GeometryID: {}; extraTabLabel: {}".format(surveyID, GeometryID, extraTabLabel), level=Qgis.Info)

        if self.dbConn.driverName() == 'QPSQL':
            table = '"{}"."Counts"'.format(self.demand_schema)
            self.countModel.setTable(table)
            #self.countModel.setTable('demand' + '.\"Counts\"')
        else:
            self.countModel.setTable('Counts')

        filterString = "\"SurveyID\" = {} AND \"GeometryID\" = \'{}\'".format(surveyID, GeometryID)
        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... filterString: {}".format(filterString),
                                  level=Qgis.Info)

        self.countModel.setFilter(filterString)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.countModel)

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... model set ...",
                                  level=Qgis.Info)
        self.setupMainCountTab()

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... checking for extraTab ...",
                                  level=Qgis.Info)
                                  
        if extraTabLabel is not None:
            TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ...adding extraTab  ...",
                                  level=Qgis.Info)
            extraTab = self.setupExtraCountTab()
            TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... new tab added ...",
                                      level=Qgis.Warning)
            demandTab = self.restrictionDialog.findChild(QTabWidget, "Details")
            demandTab.insertTab(1, extraTab, extraTabLabel)  # 0 based index
            self.setupExtraCountTabMapping()

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... about to select ...",
                                  level=Qgis.Info)
                                  
        result = self.countModel.select()
        if result == False:
            TOMsMessageLog.logMessage(
                "In populateDemandWidget: No result from select: {} ".format(self.countModel.lastError().text()),
                level=Qgis.Info)

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... selected ...",
                                  level=Qgis.Info)

        TOMsMessageLog.logMessage(
            "In populateDemandWidget: nr Rows: {} ".format(self.countModel.rowCount()),
            level=Qgis.Info)

        self.mapper.toFirst()  # TODO: check if this fails ...

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... finishing ...",
                                  level=Qgis.Info)

    def setupMainCountTab(self):

        TOMsMessageLog.logMessage("In countWidget:setupMainCountTab ... ",
                                  level=Qgis.Info)
                                  
        demandTab = self.restrictionDialog.findChild(QWidget, "Demand")
        demandLayout = demandTab.layout()

        countLayout = QHBoxLayout()
        col1_layout = QFormLayout()
        col2_layout = QFormLayout()
        col3_layout = QFormLayout()
        col4_layout = QFormLayout()

        #spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        col1_layout.addRow(QLabel(""), QLabel("Correct"))
        col1_layout.addRow(QLabel("Cars:"), QLineEdit(objectName='NrCars'))
        col1_layout.addRow(QLabel("LGVs:"), QLineEdit(objectName='NrLGVs'))
        col1_layout.addRow(QLabel("MCLs:"), QLineEdit(objectName='NrMCLs'))
        col1_layout.addRow(QLabel("Taxis:"), QLineEdit(objectName='NrTaxis'))
        col1_layout.addRow(QLabel("OGVs:"), QLineEdit(objectName='NrOGVs'))
        col1_layout.addRow(QLabel("Mini Buses:"), QLineEdit(objectName='NrMiniBuses'))
        col1_layout.addRow(QLabel("Buses:"), QLineEdit(objectName='NrBuses'))
        
        col2_layout.addRow(QLabel("Idling"))
        col2_layout.addRow(QLineEdit(objectName='NrCarsIdling'))
        col2_layout.addRow(QLineEdit(objectName='NrLGVsIdling'))
        col2_layout.addRow(QLineEdit(objectName='NrMCLsIdling'))
        col2_layout.addRow(QLineEdit(objectName='NrTaxisIdling'))
        col2_layout.addRow(QLineEdit(objectName='NrOGVsIdling'))
        col2_layout.addRow(QLineEdit(objectName='NrMiniBusesIdling'))
        col2_layout.addRow(QLineEdit(objectName='NrBusesIdling'))
        
        col3_layout.addRow(QLabel("NOT Correct"))
        col3_layout.addRow(QLineEdit(objectName='NrCarsParkedIncorrectly'))
        col3_layout.addRow(QLineEdit(objectName='NrLGVsParkedIncorrectly'))
        col3_layout.addRow(QLineEdit(objectName='NrMCLsParkedIncorrectly'))
        col3_layout.addRow(QLineEdit(objectName='NrTaxisParkedIncorrectly'))
        col3_layout.addRow(QLineEdit(objectName='NrOGVsParkedIncorrectly'))
        col3_layout.addRow(QLineEdit(objectName='NrMiniBusesParkedIncorrectly'))
        col3_layout.addRow(QLineEdit(objectName='NrBusesParkedIncorrectly'))
        
        col4_layout.addRow(QLabel(""))
        col4_layout.addRow(QLabel("PCLs:"), QLineEdit(objectName='NrPCLs'))
        col4_layout.addRow("E-Scooters:", QLineEdit(objectName='NrEScooters'))
        col4_layout.addRow("Dockless PCLs:", QLineEdit(objectName='NrDocklessPCLs'))

        col4_layout.addRow(QLabel(""))
        col4_layout.addRow("Spaces:", QLineEdit(objectName='NrSpaces'))

        countLayout.addLayout(col1_layout)
        countLayout.addLayout(col2_layout)
        countLayout.addLayout(col3_layout)
        countLayout.addLayout(col4_layout)

        TOMsMessageLog.logMessage("In countWidget:setupMainCountTab. Finished adding bits ... ",
                                  level=Qgis.Info)
                                  
        # Now add "Notes" widget
        notes_layout = QFormLayout()
        demandNotes = QTextEdit(objectName='Notes')
        #demandNotes.setPlainText()
        notes_layout.addRow("Notes:", demandNotes)

        demandLayout.addLayout(countLayout, 0, 0)

        demandLayout.addLayout(notes_layout, 2, 0)

        # add validators
        # use of validator - https://stackoverflow.com/questions/54741145/i-use-qdoublevalidator-in-my-pyqt5-program-but-it-doesnt-seem-to-work

        TOMsMessageLog.logMessage("In countWidget:setupMainCountTab. Finished layouts ... ",
                                  level=Qgis.Info)
                                  
        for widget in countLayout.parentWidget().findChildren(QLineEdit):
            widget.setValidator(QIntValidator(
                0,  # bottom
                200  # top
            ))

        TOMsMessageLog.logMessage("In countWidget:setupMainCountTab. Starting mapping ... ",
                                  level=Qgis.Info)
                                  
        try:                                  
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrCars"), self.countModel.fieldIndex('NrCars'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrCarsIdling"), self.countModel.fieldIndex('NrCarsIdling'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrCarsParkedIncorrectly"), self.countModel.fieldIndex('NrCarsParkedIncorrectly'))

            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrLGVs"), self.countModel.fieldIndex('NrLGVs'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrLGVsIdling"), self.countModel.fieldIndex('NrLGVsIdling'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrLGVsParkedIncorrectly"), self.countModel.fieldIndex('NrLGVsParkedIncorrectly'))
            
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMCLs"), self.countModel.fieldIndex('NrMCLs'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMCLsIdling"), self.countModel.fieldIndex('NrMCLsIdling'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMCLsParkedIncorrectly"), self.countModel.fieldIndex('NrMCLsParkedIncorrectly'))
            
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrTaxis"), self.countModel.fieldIndex('NrTaxis'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrTaxisIdling"), self.countModel.fieldIndex('NrTaxisIdling'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrTaxisParkedIncorrectly"), self.countModel.fieldIndex('NrTaxisParkedIncorrectly'))
                   
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrOGVs"), self.countModel.fieldIndex('NrOGVs'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrOGVsIdling"), self.countModel.fieldIndex('NrOGVsIdling'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrOGVsParkedIncorrectly"), self.countModel.fieldIndex('NrOGVsParkedIncorrectly'))
            
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMiniBuses"), self.countModel.fieldIndex('NrMiniBuses'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMiniBusesIdling"), self.countModel.fieldIndex('NrMiniBusesIdling'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrMiniBusesParkedIncorrectly"), self.countModel.fieldIndex('NrMiniBusesParkedIncorrectly'))
            
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrBuses"), self.countModel.fieldIndex('NrBuses'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrBusesIdling"), self.countModel.fieldIndex('NrBusesIdling'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrBusesParkedIncorrectly"), self.countModel.fieldIndex('NrBusesParkedIncorrectly'))

            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrPCLs"), self.countModel.fieldIndex('NrPCLs'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrEScooters"), self.countModel.fieldIndex('NrEScooters'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrDocklessPCLs"), self.countModel.fieldIndex('NrDocklessPCLs'))
             
            self.mapper.addMapping(self.restrictionDialog.findChild(QLineEdit, "NrSpaces"), self.countModel.fieldIndex('NrSpaces'))
            self.mapper.addMapping(self.restrictionDialog.findChild(QTextEdit, "Notes"), self.countModel.fieldIndex('Notes'))
        except Exception as e:
            TOMsMessageLog.logMessage('countWidget:setupMainCountTab. Error with mapping: {}'.format(e),
                              level=Qgis.Warning)
            return
            
        TOMsMessageLog.logMessage("In countWidget:setupMainCountTab ... mapping added ...",
                                  level=Qgis.Info)

    def setupExtraCountTab(self):

        TOMsMessageLog.logMessage("In countWidget:setupExtraCountTab ... starting ...",
                                  level=Qgis.Info)

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
                                  level=Qgis.Info)

        return extraTab

    def setupExtraCountTabMapping(self):

        TOMsMessageLog.logMessage("In countWidget:setupExtraCountTabMapping ... starting ...",
                                  level=Qgis.Info)

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
                                  level=Qgis.Info)
