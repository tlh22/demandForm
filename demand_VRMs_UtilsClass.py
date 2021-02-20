#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------
# Tim Hancock 2017

"""
Series of functions to deal with restrictionsInProposals. Defined as static functions to allow them to be used in forms ... (not sure if this is the best way ...)

"""
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
    QWidget, QVBoxLayout, QTableView
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
    pyqtSlot, Qt
)

from qgis.PyQt.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelation, QSqlRelationalTableModel, QSqlRelationalDelegate
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
#import cv2
import math

from abc import ABCMeta
from TOMs.generateGeometryUtils import generateGeometryUtils
from TOMs.restrictionTypeUtilsClass import (TOMsParams, TOMsLayers, originalFeature, RestrictionTypeUtilsMixin)
from restrictionsWithGNSS.fieldRestrictionTypeUtilsClass import (FieldRestrictionTypeUtilsMixin)

from TOMs.ui.TOMsCamera import (formCamera)
from restrictionsWithGNSS.ui.imageLabel import (imageLabel)

cv2_available = True
try:
    import cv2
except ImportError:
    QgsMessageLog.logMessage("Not able to import cv2 ...", tag="TOMs panel")
    cv2_available = False

import uuid
from TOMs.core.TOMsMessageLog import TOMsMessageLog
from .demand_form import VRM_DemandForm

ZOOM_LIMIT = 5

class vrmParams(TOMsParams):
    def __init__(self):
        TOMsParams.__init__(self)
        #self.iface = iface

        #TOMsMessageLog.logMessage("In gpsParams.init ...", level=Qgis.Info)

        self.TOMsParamsList.extend([
                          "CameraNr",
                          "DemandGpkg"
                               ])

class VRMsUtilsMixin(FieldRestrictionTypeUtilsMixin):
    def __init__(self, iface):
        #RestrictionTypeUtilsMixin.__init__(self, iface)
        self.iface = iface
        self.settings = QgsSettings()

        #self.params = gpsParams()

        #self.TOMsUtils = RestrictionTypeUtilsMixin(self.iface)

    def setDefaultFieldRestrictionDetails(self, currRestriction, currRestrictionLayer, currDate):
        TOMsMessageLog.logMessage("In VRM:setDefaultFieldRestrictionDetails: {}".format(currRestrictionLayer.name()), level=Qgis.Warning)

        # TODO: Need to check whether or not these fields exist. Also need to retain the last values and reuse
        # gis.stackexchange.com/questions/138563/replacing-action-triggered-script-by-one-supplied-through-qgis-plugin

        try:
            currRestriction.setAttribute("LastUpdateDateTime", currDate)
        except Exception as e:
            TOMsMessageLog.logMessage("In setDefaultFieldRestrictionDetails. Problem with setting LastUpdateDateTime: {}".format(e),
                                      level=Qgis.Info)

    def setupFieldRestrictionDialog(self, restrictionDialog, currRestrictionLayer, currRestriction):

        TOMsMessageLog.logMessage("In VRM:setupVRMDialog: {}".format(currRestrictionLayer.name()),
                                  level=Qgis.Warning)

        self.params.getParams()

        # Create a copy of the feature
        self.origFeature = originalFeature()
        self.origFeature.setFeature(currRestriction)

        if restrictionDialog is None:
            reply = QMessageBox.information(None, "Error",
                                            "setupFieldRestrictionDialog. Correct form not found",
                                            QMessageBox.Ok)
            TOMsMessageLog.logMessage(
                "In setupRestrictionDialog. dialog not found",
                level=Qgis.Warning)
            return

        restrictionDialog.attributeForm().disconnectButtonBox()
        button_box = restrictionDialog.findChild(QDialogButtonBox, "button_box")

        if button_box is None:
            TOMsMessageLog.logMessage(
                "In setupRestrictionDialog. button box not found",
                level=Qgis.Warning)
            return

        """
        button_box.accepted.connect(functools.partial(self.onSaveFieldRestrictionDetails, currRestriction,
                                      currRestrictionLayer, restrictionDialog))

        button_box.rejected.connect(functools.partial(self.onRejectFieldRestrictionDetailsFromForm, restrictionDialog, currRestrictionLayer))

        restrictionDialog.attributeForm().attributeChanged.connect(functools.partial(self.onAttributeChangedClass2_local, currRestriction, currRestrictionLayer))
        """

        self.photoDetails_field(restrictionDialog, currRestrictionLayer, currRestriction)

        TOMsMessageLog.logMessage("In setupFieldRestrictionDialog. Calling addVRMWidget ...", level=Qgis.Warning)

        self.addVRMWidget(restrictionDialog, currRestrictionLayer, currRestriction)

        #self.addScrollBars(restrictionDialog)

    def onAttributeChangedClass2_local(self, currFeature, layer, fieldName, value):

        #self.TOMsUtils.onAttributeChangedClass2(currFeature, layer, fieldName, value)

        TOMsMessageLog.logMessage(
            "In field:FormOpen:onAttributeChangedClass 2 - layer: " + str(layer.name()) + " (" + fieldName + "): " + str(value), level=Qgis.Info)


        # self.currRestriction.setAttribute(fieldName, value)
        try:

            currFeature[layer.fields().indexFromName(fieldName)] = value
            #currFeature.setAttribute(layer.fields().indexFromName(fieldName), value)

        except Exception as e:

            reply = QMessageBox.information(None, "Error",
                                                "onAttributeChangedClass2. Update failed for: " + str(layer.name()) + " (" + fieldName + "): " + str(value),
                                                QMessageBox.Ok)  # rollback all changes


        self.storeLastUsedDetails(layer.name(), fieldName, value)

        return

    def onSaveFieldRestrictionDetails(self, currFeature, currFeatureLayer, dialog):
        TOMsMessageLog.logMessage("In onSaveFieldRestrictionDetails:  currFeatureID: ".format(currFeature.id()), level=Qgis.Info)

        try:
            self.camera1.endCamera()
            self.camera2.endCamera()
            self.camera3.endCamera()
        except:
            None

        status = currFeatureLayer.updateFeature(currFeature)

        #status = dialog.attributeForm().close()

        try:
            currFeatureLayer.commitChanges()
        except Exception as e:
            reply = QMessageBox.information(None, "Information", "Problem committing changes: {}".format(e), QMessageBox.Ok)

        TOMsMessageLog.logMessage("In onSaveDemandDetails: changes committed", level=Qgis.Info)

        status = dialog.close()

    def onRejectFieldRestrictionDetailsFromForm(self, restrictionDialog, currFeatureLayer):
        TOMsMessageLog.logMessage("In onRejectFieldRestrictionDetailsFromForm", level=Qgis.Info)

        try:
            self.camera1.endCamera()
            self.camera2.endCamera()
            self.camera3.endCamera()
        except:
            None

        currFeatureLayer.rollBack()
        restrictionDialog.reject()

        #del self.mapTool

    def createConnection(self):
        con = QSqlDatabase.addDatabase("QSQLITE")
        # TODO ...

    def addVRMWidget(self, restrictionDialog, currRestrictionLayer, currRestriction):

        TOMsMessageLog.logMessage("In addVRMWidget ... ", level=Qgis.Warning)
        vrmsTab = restrictionDialog.findChild(QWidget, "VRMs")
        vrmsLayout = vrmsTab.layout()
        vrmForm = vrmWidget(vrmsTab)
        vrmForm.populateVrmWidget(self.surveyID, currRestriction.attribute("GeometryID"))

        vrmsLayout.addWidget(vrmForm)

        buttonLayout = QVBoxLayout()
        addButton = QPushButton("+")
        removeButton = QPushButton("-")
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(removeButton)
        vrmsLayout.addLayout(buttonLayout, 0, 1)

        addButton.clicked.connect(vrmForm.insertRow)
        removeButton.clicked.connect(vrmForm.deleteRow)



class vrmWidget(QWidget):
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

    def populateVrmWidget(self, surveyID, GeometryID):

        TOMsMessageLog.logMessage("In vrmWidget:populateVrmWidget ... ", level=Qgis.Warning)
        # keep pks
        #self.surveyID = surveyID
        #self.GeometryID = GeometryID
        surveyID = 1
        GeometryID = 5
        layout_box = QVBoxLayout(self)
        #
        vrmView = QTableView()

        vrmModel = QSqlRelationalTableModel(self)
        vrmModel.setTable("VRMs")

        filterString = "SurveyID = {} AND SectionID = {}".format(surveyID, GeometryID)
        TOMsMessageLog.logMessage("In vrmWidget:populateVrmWidget ... filterString: {}".format(filterString), level=Qgis.Warning)

        vrmModel.setFilter(filterString)
        #vrmModel.setFilter("SurveyID = 1 AND SectionID = 5")
        vrmModel.setSort(int(vrmModel.fieldIndex("PositionID")), Qt.AscendingOrder)
        vrmModel.setRelation(int(vrmModel.fieldIndex("VehicleTypeID")), QSqlRelation('VehicleTypes', 'Code', 'Description'))
        rel = vrmModel.relation(int(vrmModel.fieldIndex("VehicleTypeID")))
        if not rel.isValid():
            print ('Relation not valid ...')
            TOMsMessageLog.logMessage("In testWidget: Relation not valid ... {} ".format(vrmModel.lastError().text()),
                                      level=Qgis.Warning)

        result = vrmModel.select()
        if result == False:
            TOMsMessageLog.logMessage("In testWidget: No result: {} ".format(vrmModel.lastError().text()),
                                      level=Qgis.Warning)
            #print ('Select: {}'.format(my_model.lastError().text()))
        #show the view with model
        vrmView.setModel(vrmModel)
        vrmView.setColumnHidden(vrmModel.fieldIndex('fid'), True)
        vrmView.setColumnHidden(vrmModel.fieldIndex('ID'), True)
        vrmView.setColumnHidden(vrmModel.fieldIndex('SurveyID'), True)
        vrmView.setColumnHidden(vrmModel.fieldIndex('SectionID'), True)
        vrmView.setColumnHidden(vrmModel.fieldIndex('GeometryID'), True)
        vrmView.setItemDelegate(QSqlRelationalDelegate(vrmModel))

        self.vrmView = vrmView
        self.vrmModel = vrmModel

        # put view in layout_box area
        layout_box.addWidget(vrmView)

        #return layout_box

    def insertRow(self):
        TOMsMessageLog.logMessage("In vrmWidget:insertRow ... ", level=Qgis.Warning)
        print ("Inserting row ...")

        row = self.vrmModel.rowCount()
        record = self.vrmModel.record()
        #record.setGenerated('id', False)
        record.setValue('SurveyID', self.surveyID)
        record.setValue('GeometryID', self.GeometryID)
        #record.setValue('department', self.ui.department.currentText())

        #record.setValue('starttime', QDateTime.currentDateTime())
        #record.setValue('endtime', QDateTime.currentDateTime())

        self.vrmModel.insertRecord(row, record)
        #self.vrmModel.edit(QModelIndex(self.vrmModel.index(row, self.hours_model.fieldIndex('department'))))

    def deleteRow(self):
        TOMsMessageLog.logMessage("In vrmWidget:deleteRow ... ", level=Qgis.Warning)
        pass
