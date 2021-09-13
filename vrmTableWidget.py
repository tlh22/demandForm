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
    QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QLayout, QItemDelegate, QStyledItemDelegate, QLineEdit
)

from qgis.PyQt.QtGui import (
    QIcon,
    QPixmap,
    QImage, QPainter
)

from qgis.PyQt.QtCore import (
    QObject,
    QTimer,
    QThread,
    pyqtSignal,
    pyqtSlot, Qt,QModelIndex
)

from qgis.PyQt.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelation, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlTableModel
)

from qgis.core import (
    Qgis,
    QgsExpressionContextScope,
    QgsExpressionContextUtils,
    QgsExpression,
    QgsFeatureRequest,
    QgsMessageLog,
    QgsFeature,
    QgsGeometry,
    QgsTransaction,
    QgsTransactionGroup,
    QgsProject,
    QgsSettings
)

from qgis.gui import *
import functools
import time, datetime
import os, uuid
import math

from abc import ABCMeta
from TOMs.generateGeometryUtils import generateGeometryUtils
from TOMs.restrictionTypeUtilsClass import (TOMsParams, TOMsLayers, originalFeature, RestrictionTypeUtilsMixin)
from restrictionsWithGNSS.fieldRestrictionTypeUtilsClass import (FieldRestrictionTypeUtilsMixin)

from TOMs.ui.TOMsCamera import (formCamera)
from restrictionsWithGNSS.ui.imageLabel import (imageLabel)

import uuid
from TOMs.core.TOMsMessageLog import TOMsMessageLog
from .demand_form import VRM_DemandForm

class vrmWidget(QTableView):

    progressUpdated = pyqtSignal(int)
    startOperation = pyqtSignal()
    endOperation = pyqtSignal()

    #data_changed = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None, db=None):
        super(vrmWidget, self).__init__(parent)
        TOMsMessageLog.logMessage("In vrmWidget:init ... ", level=Qgis.Info)
        self.dbConn = db
        self.vrmModel = QSqlRelationalTableModel(self, db=self.dbConn)
        #vrmsLayer = QgsProject.instance().mapLayersByName("VRMs")[0]
        #self.provider = vrmsLayer.dataProvider()

    def populateVrmWidget(self, surveyID, GeometryID):

        TOMsMessageLog.logMessage("In vrmWidget:populateVrmWidget ... surveyID: {}; GeometryID: {}".format(surveyID, GeometryID), level=Qgis.Info)

        if self.dbConn.driverName() == 'QPSQL':
            self.vrmModel.setTable('demand' + '.\"VRMs\"')
        else:
            self.vrmModel.setTable('VRMs')

        self.vrmModel.setJoinMode(QSqlRelationalTableModel.LeftJoin)
        self.vrmModel.setEditStrategy(QSqlTableModel.OnFieldChange)

        filterString = "\"SurveyID\" = {} AND \"GeometryID\" = \'{}\'".format(surveyID, GeometryID)
        TOMsMessageLog.logMessage("In vrmWidget:populateVrmWidget ... filterString: {}".format(filterString), level=Qgis.Info)

        self.vrmModel.setFilter(filterString)
        #vrmModel.setFilter("SurveyID = 1 AND SectionID = 5")
        self.vrmModel.setSort(int(self.vrmModel.fieldIndex("PositionID")), Qt.AscendingOrder)
        self.vrmModel.setHeaderData(self.vrmModel.fieldIndex("PositionID"), Qt.Horizontal, 'Pos')

        """
        It was a challenge to work out the required structure/format for accessing postgres records. The clue came from here - https://osgeo-fr.github.io/presentations_foss4gfr/2016/J2/SylvainPierre.pdf
        (slide 9) with the setTable instruction.
        """

        if self.dbConn.driverName() == 'QPSQL':
            self.vrmModel.setRelation(int(self.vrmModel.fieldIndex("VehicleTypeID")), QSqlRelation('demand_lookups'+'.\"VehicleTypes\"', '\"Code\"', '\"Description\"'))
        else:
            self.vrmModel.setRelation(int(self.vrmModel.fieldIndex("VehicleTypeID")),
                                      QSqlRelation('VehicleTypes', 'Code',
                                                   'Description'))

        rel = self.vrmModel.relation(int(self.vrmModel.fieldIndex('VehicleTypeID')))
        if not rel.isValid():
            #print ('Relation not valid ...')
            TOMsMessageLog.logMessage("In populateVrmWidget: Relation not valid ... {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)
        self.vrmModel.setHeaderData(self.vrmModel.fieldIndex('VehicleTypeID'), Qt.Horizontal, 'VehicleType')

        if self.dbConn.driverName() == 'QPSQL':
            self.vrmModel.setRelation(int(self.vrmModel.fieldIndex('PermitTypeID')), QSqlRelation('demand_lookups'+'.\"PermitTypes\"', '\"Code\"', '\"Description\"'))
        else:
            self.vrmModel.setRelation(int(self.vrmModel.fieldIndex('PermitTypeID')), QSqlRelation('PermitTypes', 'Code', 'Description'))
        rel = self.vrmModel.relation(int(self.vrmModel.fieldIndex('PermitTypeID')))

        if not rel.isValid():
            #print ('Relation not valid ...')
            TOMsMessageLog.logMessage("In populateVrmWidget: Relation not valid ... {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)
        self.vrmModel.setHeaderData(self.vrmModel.fieldIndex('PermitTypeID'), Qt.Horizontal, 'PermitType')

        result = self.vrmModel.select()
        if result == False:
            TOMsMessageLog.logMessage("In populateVrmWidget: No result from select: {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)

        TOMsMessageLog.logMessage(
            "In populateVrmWidget: nr Rows: {} ".format(self.vrmModel.rowCount()),
            level=Qgis.Info)

        self.setModel(self.vrmModel)
        try:
            self.setColumnHidden(self.vrmModel.fieldIndex('fid'), True)  # Not present within postgres
        except:
            None

        self.setColumnHidden(self.vrmModel.fieldIndex('ID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('SurveyID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('SectionID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('GeometryID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('RestrictionTypeID'), True)
        self.verticalHeader().hide()
        self.setItemDelegate(QSqlRelationalDelegate(self.vrmModel))
        self.setItemDelegateForColumn(self.vrmModel.fieldIndex("PositionID"), readOnlyDelegate(self));
        self.setItemDelegateForColumn(self.vrmModel.fieldIndex("VRM"), vrmDelegate(self));
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.resizeColumnsToContents()
        self.setColumnWidth(self.vrmModel.fieldIndex("VRM"), 120)

        self.vrmModel.dataChanged.connect(self.cascadeChangeToRecord)

    def cascadeChangeToRecord(self, idx1, idx2, roles):
        TOMsMessageLog.logMessage("In vrmWidget:cascadeChangeToVRM ... {}; {}; {}".format(idx1, idx2, roles),
                                  level=Qgis.Warning)

        index = self.currentIndex()   # 0-based
        currRow = index.row()

        TOMsMessageLog.logMessage("In vrmWidget:cascadeChangeToVRM ... record 1: {}".format(currRow),
                                  level=Qgis.Warning)

        record = self.vrmModel.record(currRow)
        surveyID = record.value('SurveyID')
        GeometryID = record.value('GeometryID')
        PositionID = record.value('PositionID')

        TOMsMessageLog.logMessage("In vrmWidget:cascadeChangeToVRM ... record 2: {}; {}; {}; {}".format(index, surveyID, GeometryID, PositionID),
                                  level=Qgis.Warning)

        """
        Need to check previous time periods (within the same day) and find those that are "almost" the same??. Not quite sure how to get details from previous period
        Might be able to use "import difflib" to help ...
        
        Issue is to find the VRM in the previous period. It may not be at the same position (but it will be in the same GeometryID). Need to be able to obtain the "pre-change" value.
        """

    def insertVrm(self, surveyID, GeometryID):
        TOMsMessageLog.logMessage("In vrmWidget:insertRow ... surveyID: {}; GeometryID: {}".format(surveyID, GeometryID), level=Qgis.Info)

        rowCount = self.vrmModel.rowCount()
        index = self.currentIndex()   # 0-based

        if not index.isValid():  # typically this is for no rows being present ...
            currRow = 0
        else:
            currRow = index.row()

        TOMsMessageLog.logMessage("In vrmWidget:insertRow ... row: {}; index:{}".format(rowCount, currRow), level=Qgis.Info)

        # add new record at position
        record = self.vrmModel.record()
        if self.dbConn.driverName() == 'QPSQL':
            record.setGenerated('ID', False)
        else:
            record.setGenerated('fid', False)

        #record.setGenerated('fid', False)

        record.setValue('SurveyID', surveyID)
        record.setValue('SectionID', None)
        record.setValue('GeometryID', GeometryID)


        TOMsMessageLog.logMessage("Record - surveyID: {}".format(record.value(record.indexOf("SurveyID"))),
                                      level=Qgis.Info)

        if currRow == 0 and rowCount == 0:
            record.setValue('PositionID', currRow + 1)
            res = self.vrmModel.insertRecord(currRow, record)
        else:
            record.setValue('PositionID', currRow + 2)
            res = self.vrmModel.insertRecord(currRow+1, record)

        TOMsMessageLog.logMessage("Record - insert: {}".format(res),
                                      level=Qgis.Info)
        if not res:
            TOMsMessageLog.logMessage("In insertVrm: issue with insert ... {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)

        # re-order positions
        extent = (self.vrmModel.rowCount()+2) - (currRow+2)
        self.startOperation.emit()
        for i in range (currRow+2, self.vrmModel.rowCount()+2):
            TOMsMessageLog.logMessage("In insertVrm: changing positions ... {} ".format(i),
                                      level=Qgis.Info)
            self.vrmModel.setData(QModelIndex(self.vrmModel.index(i, self.vrmModel.fieldIndex('PositionID'))), i+1)
            percentComplete = int((i-currRow+2) / float(extent) * 100)
            self.progressUpdated.emit(percentComplete)
            #self.iface.statusBarIface().showMessage("Processed {} %".format(int(percentComplete)))

        #self.iface.statusBarIface().clearMessage()
        self.endOperation.emit()

        self.vrmModel.select()


    def deleteVrm(self):
        TOMsMessageLog.logMessage("In vrmWidget:deleteRow ... ", level=Qgis.Info)

        index = self.currentIndex()

        if not index.isValid():  # typically this is for no rows being present ...
            currRow = 0
        else:
            currRow = index.row()

        self.vrmModel.removeRow(currRow)

        # re-order positions
        extent = (self.vrmModel.rowCount() + 2) - (currRow + 1)
        self.startOperation.emit()
        for i in range (currRow+1, self.vrmModel.rowCount()+2):
            TOMsMessageLog.logMessage("In insertVrm: changing positions ... {} ".format(i),
                                      level=Qgis.Info)
            self.vrmModel.setData(QModelIndex(self.vrmModel.index(i, self.vrmModel.fieldIndex('PositionID'))), i)
            percentComplete = (i-currRow+1) / float(extent) * 100
            self.progressUpdated.emit(percentComplete)
            #self.iface.statusBarIface().showMessage("Processed {} %".format(int(percentComplete)))

        #self.iface.statusBarIface().clearMessage()
        self.endOperation.emit()

        self.vrmModel.submitAll()
        self.vrmModel.select()

# https://stackoverflow.com/questions/24024815/set-a-whole-column-in-qtablewidget-read-only-in-python
class readOnlyDelegate(QItemDelegate):

    def createEditor(self, *args):
        return None

class vrmDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):

        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setInputMask('>nnnn-nnnn')

        return editor