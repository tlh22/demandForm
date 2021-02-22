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
        # this layout_box can be used if you need more widgets
        # I used just one named WebsitesWidget
        #layout_box = QVBoxLayout(self)
        #
        #vrmView = QTableView()
        # put view in layout_box area
        #layout_box.addWidget(vrmView)
        # create a table model
        """
        my_model = SqlQueryModel()
        q = QSqlQuery(query)
        my_model.setQuery(q)
        my_model.setFilter("SurveyID = 1 AND SectionID = 5")
        my_model.select()
        my_view.setModel(my_model)
        """

        #q = QSqlQuery()
        #result = q.prepare("SELECT PositionID, VRM, VehicleTypeID, RestrictionTypeID, PermitType, Notes FROM VRMs")
        #if result == False:
        #    print ('Prepare: {}'.format(q.lastError().text()))
        #my_model.setQuery(q)

        """
        result = my_model.select()
        if result == False:
            TOMsMessageLog.logMessage("In testWidget: No result: {} ".format(my_model.lastError().text()),
                                      level=Qgis.Warning)
            #print ('Select: {}'.format(my_model.lastError().text()))
        #show the view with model
        my_view.setModel(my_model)
        my_view.setColumnHidden(my_model.fieldIndex('fid'), True)
        my_view.setColumnHidden(my_model.fieldIndex('ID'), True)
        my_view.setColumnHidden(my_model.fieldIndex('SurveyID'), True)
        my_view.setColumnHidden(my_model.fieldIndex('SectionID'), True)
        my_view.setColumnHidden(my_model.fieldIndex('GeometryID'), True)
        my_view.setItemDelegate(QSqlRelationalDelegate(my_view))
        """

        #self.vrmView = QTableView()
        self.vrmModel = QSqlRelationalTableModel(self)

    def populateVrmWidget(self, surveyID, GeometryID):

        TOMsMessageLog.logMessage("In vrmWidget:populateVrmWidget ... surveyID: {}; GeometryID: {}".format(surveyID, GeometryID), level=Qgis.Warning)
        # keep pks
        #self.surveyID = surveyID
        #self.GeometryID = GeometryID
        #surveyID = 1
        #GeometryID = 5
        #layout_box = QVBoxLayout(self)
        #

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
            #print ('Select: {}'.format(my_model.lastError().text()))

        TOMsMessageLog.logMessage(
            "In populateVrmWidget: nr Rows: {} ".format(self.vrmModel.rowCount()),
            level=Qgis.Warning)

        #show the view with model
        """vrmView.setModel(self.vrmModel)
        vrmView.setColumnHidden(self.vrmModel.fieldIndex('fid'), True)
        vrmView.setColumnHidden(self.vrmModel.fieldIndex('ID'), True)
        vrmView.setColumnHidden(self.vrmModel.fieldIndex('SurveyID'), True)
        vrmView.setColumnHidden(self.vrmModel.fieldIndex('SectionID'), True)
        vrmView.setColumnHidden(self.vrmModel.fieldIndex('GeometryID'), True)
        vrmView.setItemDelegate(QSqlRelationalDelegate(self.vrmModel))
        #vrmView.resizeColumnsToContents()
        vrmView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);"""

        self.setModel(self.vrmModel)
        self.setColumnHidden(self.vrmModel.fieldIndex('fid'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('ID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('SurveyID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('SectionID'), True)
        self.setColumnHidden(self.vrmModel.fieldIndex('GeometryID'), True)
        self.setItemDelegate(QSqlRelationalDelegate(self.vrmModel))
        #vrmView.resizeColumnsToContents()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);

        #vrmModel.setEditStrategy(QSqlTableModel.OnRowChange) # actually want it for each cell

        #self.vrmView = vrmView
        #self.vrmModel = vrmModel

        # put view in layout_box area
        #layout_box.addChildWidget(vrmView)

        #return layout_box

    def insertVrm(self, surveyID, GeometryID):
        TOMsMessageLog.logMessage("In vrmWidget:insertRow ... surveyID: {}; GeometryID: {}".format(surveyID, GeometryID), level=Qgis.Warning)

        row = self.vrmModel.rowCount()
        #self.vrmModel.insertRow(row)
        index = self.currentIndex()   # 0-based
        if not index.isValid():
            return

        TOMsMessageLog.logMessage("In vrmWidget:insertRow ... row: {}; index:{}".format(row, index.row()), level=Qgis.Warning)

        """res = self.vrmModel.insertRow(row)
        if not res:
            print ('insert not valid ...')
            TOMsMessageLog.logMessage("In insertVrm: issue with insert ... {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)"""

        """self.vrmModel.setItem(row, self.vrmModel.fieldIndex('SurveyID'), QTableWidgetItem(surveyID))
        self.vrmModel.setItem(row, self.vrmModel.fieldIndex('SectionID'), QTableWidgetItem(GeometryID))
        self.vrmModel.setItem(row, self.vrmModel.fieldIndex('GeometryID'), QTableWidgetItem(GeometryID))
        self.vrmModel.setItem(row, self.vrmModel.fieldIndex('PositionID'), QTableWidgetItem(row))
        self.vrmModel.setItem(row, self.vrmModel.fieldIndex('VehicleTypeID'), QTableWidgetItem(1))"""

        """self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('SurveyID'))), surveyID)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('SectionID'))), GeometryID)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('GeometryID'))), GeometryID)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('PositionID'))), row)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('VehicleTypeID'))), 1)"""

        record = self.vrmModel.record()
        record.setGenerated('fid', False)
        record.setValue('SurveyID', surveyID)
        record.setValue('SectionID', GeometryID)
        record.setValue('GeometryID', GeometryID)
        record.setValue('PositionID', index.row()+2)
        #record.setValue('VehicleTypeID', 'Car')

        TOMsMessageLog.logMessage("Record - surveyID: {}".format(record.value(record.indexOf("SurveyID"))),
                                      level=Qgis.Warning)

        res1 = True
        #res1 = self.vrmModel.insertRow(row)



        #self.vrmModel.submitAll()

        #res1 = self.vrmModel.insertRecord(row, record)

        #self.hours_view.edit(QModelIndex(self.hours_model.index(row, self.hours_model.fieldIndex('department'))))

        #res = self.vrmModel.insertRecord(index.row(), record)

        res2 = True
        res2 = self.vrmModel.insertRecord(index.row()+1, record)
        TOMsMessageLog.logMessage("Record - insert: {}. {}".format(res1, res2),
                                      level=Qgis.Warning)
        if not res1 or not res2:
            #print ('insert not valid ...')
            TOMsMessageLog.logMessage("In insertVrm: issue with insert ... {} ".format(self.vrmModel.lastError().text()),
                                      level=Qgis.Warning)


        for i in range (index.row()+2, self.vrmModel.rowCount()+2):
            TOMsMessageLog.logMessage("In insertVrm: changing positions ... {} ".format(i),
                                      level=Qgis.Warning)
            self.vrmModel.setData(QModelIndex(self.vrmModel.index(i, self.vrmModel.fieldIndex('PositionID'))), i+1)

        """self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('SurveyID'))), surveyID)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('SectionID'))), GeometryID)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('GeometryID'))), GeometryID)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('PositionID'))), row)
        self.vrmModel.setData(QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('VehicleTypeID'))), 1)"""

        #self.vrmModel.submitAll()

        """vrmIndex = QModelIndex(self.vrmModel.index(row, self.vrmModel.fieldIndex('VRM')))
        #TOMsMessageLog.logMessage("In vrmWidget:insertRow ... index. row: {} column: {}".format(vrmIndex.row(), vrmIndex.column()), level=Qgis.Warning)
        #ndx = self.vrmModel.index(index.row(), 2)
        self.selectionModel().setCurrentIndex(vrmIndex, QtCore.QItemSelectionModel.Select)
        self.edit(vrmIndex)"""


        #index = self.vrmModel.index(row)
        #self.vrmView.setCurrentIndex(index)
        #self.vrmView.edit(index)

        self.vrmModel.select()

        #self.vrmModel.edit(QModelIndex(self.vrmModel.index(row, self.hours_model.fieldIndex('department'))))

        #submit = self.phone_model.submitAll()
        # self.phone_model.select()
        #phone_index_edit = QModelIndex(self.phone_model.index(row, self.phone_model.fieldIndex('phone_number')))
        #self.ui.phone_view.edit(phone_index_edit)

        #row = self.model.rowCount()
        #self.model.insertRecord(row, rec)
        #ndx = self.model.index(row, 2)
        #self.view.edit(ndx)
        #self.view.selectionModel().setCurrentIndex(ndx, QtCore.QItemSelectionModel.Select)


    def deleteVrm(self):
        TOMsMessageLog.logMessage("In vrmWidget:deleteRow ... ", level=Qgis.Warning)

        index = self.currentIndex()
        if not index.isValid():
            return
        self.vrmModel.removeRow(index.row())

        for i in range (index.row()+1, self.vrmModel.rowCount()+2):
            TOMsMessageLog.logMessage("In insertVrm: changing positions ... {} ".format(i),
                                      level=Qgis.Warning)
            self.vrmModel.setData(QModelIndex(self.vrmModel.index(i, self.vrmModel.fieldIndex('PositionID'))), i)

        self.vrmModel.submitAll()
        self.vrmModel.select()
