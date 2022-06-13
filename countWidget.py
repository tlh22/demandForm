""" ***


*** """
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
    QProgressDialog, QProgressBar, QTextEdit
)

from qgis.PyQt.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelation, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlTableModel
)

from qgis.core import (
    Qgis
)

from TOMs.core.TOMsMessageLog import TOMsMessageLog

class countWidget():

    progressUpdated = pyqtSignal(int)
    startOperation = pyqtSignal()
    endOperation = pyqtSignal()

    def __init__(self, parent=None, db=None):
        super(countWidget, self).__init__(parent)
        TOMsMessageLog.logMessage("In countWidget:init ... ", level=Qgis.Info)
        self.dbConn = db
        self.demandModel = QSqlRelationalTableModel(self, db=self.dbConn)

    def populateDemandWidget(self, surveyID, GeometryID):

        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... surveyID: {}; GeometryID: {}".format(surveyID, GeometryID), level=Qgis.Info)

        if self.dbConn.driverName() == 'QPSQL':
            self.vrmModel.setTable('demand' + '.\"Count\"')
        else:
            self.vrmModel.setTable('Count')

        filterString = "\"SurveyID\" = {} AND \"GeometryID\" = \'{}\'".format(surveyID, GeometryID)
        TOMsMessageLog.logMessage("In countWidget:populateDemandWidget ... filterString: {}".format(filterString), level=Qgis.Info)

        countLayout = QHBoxLayout()
        col1_layout = QFormLayout()
        col2_layout = QFormLayout()

        col1_layout.addRow("Cars:", QLineEdit(objectName='NrCars'))
        col1_layout.addRow("LGVs:", QLineEdit(objectName='NrLGVs'))
        col1_layout.addRow("MCLs:", QLineEdit(objectName='NrMCLs'))
        col1_layout.addRow("Taxis:", QLineEdit(objectName='NrTaxis'))

        col2_layout.addRow("PCLs:", QLineEdit(objectName='NrPCLs'))
        col2_layout.addRow("OGVs:", QLineEdit(objectName='NrOGVs'))
        col2_layout.addRow("Buses:", QLineEdit(objectName='NrBuses'))
        col2_layout.addRow("Spaces:", QLineEdit(objectName='NrSpaces'))

        countLayout.addLayout(col1_layout)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        countLayout.addItem(verticalSpacer)
        countLayout.addLayout(col2_layout)

        # add validators
        # use of validator - https://stackoverflow.com/questions/54741145/i-use-qdoublevalidator-in-my-pyqt5-program-but-it-doesnt-seem-to-work

        for widget in countLayout.parentWidget().findChildren(QLineEdit):
            widget.setValidator(QIntValidator(
                    0,  # bottom
                    200  # top
                ))

        # Now add "Notes" widget
        notes_layout = QFormLayout()
        notes_layout.addRow("Notes:", QTextEdit(objectName='SurveyNotes'))

        demandLayout.addLayout(countLayout)
        demandLayout.addItem(QSpacerItem())
        demandLayout.addLayout(notes_layout)

        currGeometryID = currRestriction.attribute("GeometryID")

        demandForm.populateVrmWidget(self.surveyID, currGeometryID)