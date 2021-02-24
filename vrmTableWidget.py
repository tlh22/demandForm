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
    QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QLayout
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
    def __init__(self, parent=None):
        super(vrmWidget, self).__init__(parent)
        TOMsMessageLog.logMessage("In vrmWidget:init ... ", level=Qgis.Warning)
        self.vrmModel = QSqlRelationalTableModel(self)

    def populateVrmWidget(self, surveyID, GeometryID):

        TOMsMessageLog.logMessage("In vrmWidget:populateVrmWidget ... surveyID: {}; GeometryID: {}".format(surveyID, GeometryID), level=Qgis.Warning)

        self.vrmModel.setTable("VRMs")
        self.vrmModel.setJoinMode(QSqlRelationalTableModel.LeftJoin)
        self.vrmModel.setEditStrategy(QSqlTableModel.OnFieldChange)

        filterString = "SurveyID = {} AND SectionID = {}".format(surveyID, GeometryID)
        TOMsMessageLog.logMessage("In vrmWidget:populateVrmWidget ... filterString: {}".format(filterString), level=Qgis.Warning)

        self.vrmModel.setFilter(filterString)
        #vrmModel.setFilter("SurveyID = 1 AND SectionID = 5")
        self.vrmModel.setSort(int(self.vrmModel.fieldIndex("PositionID")), Qt.AscendingOrder)
        self.vrmModel.setRelation(int(self.vrmModel.fieldIndex("VehicleTypeID")), QSqlRelation('VehicleTypes', 'Code', 'Description'))
        rel = self.vrmModel.relation(int(self.vrmModel.fieldIndex("VehicleTypeID")))
        if not rel.isValid():
            print ('Relation not valid ...')
            TOMsMessageLog.logMessage("In populateVrmWidget: Relation not valid ... {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)

        result = self.vrmModel.select()
        if result == False:
            TOMsMessageLog.logMessage("In populateVrmWidget: No result from select: {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)

        TOMsMessageLog.logMessage(
            "In populateVrmWidget: nr Rows: {} ".format(self.vrmModel.rowCount()),
            level=Qgis.Warning)

        self.setModel(self.vrmModel)
        self.setColumnHidden(self.vrmModel.fieldIndex('fid'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('ID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('SurveyID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('SectionID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('GeometryID'), True)
        self.setItemDelegate(QSqlRelationalDelegate(self.vrmModel))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);

    def insertVrm(self, surveyID, GeometryID):
        TOMsMessageLog.logMessage("In vrmWidget:insertRow ... surveyID: {}; GeometryID: {}".format(surveyID, GeometryID), level=Qgis.Warning)

        row = self.vrmModel.rowCount()
        index = self.currentIndex()   # 0-based
        if not index.isValid():
            return

        TOMsMessageLog.logMessage("In vrmWidget:insertRow ... row: {}; index:{}".format(row, index.row()), level=Qgis.Warning)

        # add new record at position
        record = self.vrmModel.record()
        record.setGenerated('fid', False)
        record.setValue('SurveyID', surveyID)
        record.setValue('SectionID', GeometryID)
        record.setValue('GeometryID', GeometryID)
        record.setValue('PositionID', index.row()+2)

        TOMsMessageLog.logMessage("Record - surveyID: {}".format(record.value(record.indexOf("SurveyID"))),
                                      level=Qgis.Warning)

        res = self.vrmModel.insertRecord(index.row()+1, record)
        TOMsMessageLog.logMessage("Record - insert: {}".format(res),
                                      level=Qgis.Warning)
        if not res:
            TOMsMessageLog.logMessage("In insertVrm: issue with insert ... {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)

        # re-order positions
        for i in range (index.row()+2, self.vrmModel.rowCount()+2):
            TOMsMessageLog.logMessage("In insertVrm: changing positions ... {} ".format(i),
                                      level=Qgis.Warning)
            self.vrmModel.setData(QModelIndex(self.vrmModel.index(i, self.vrmModel.fieldIndex('PositionID'))), i+1)

        self.vrmModel.select()


    def deleteVrm(self):
        TOMsMessageLog.logMessage("In vrmWidget:deleteRow ... ", level=Qgis.Warning)

        index = self.currentIndex()
        if not index.isValid():
            return
        self.vrmModel.removeRow(index.row())

        # re-order positions
        for i in range (index.row()+1, self.vrmModel.rowCount()+2):
            TOMsMessageLog.logMessage("In insertVrm: changing positions ... {} ".format(i),
                                      level=Qgis.Warning)
            self.vrmModel.setData(QModelIndex(self.vrmModel.index(i, self.vrmModel.fieldIndex('PositionID'))), i)

        self.vrmModel.submitAll()
        self.vrmModel.select()
