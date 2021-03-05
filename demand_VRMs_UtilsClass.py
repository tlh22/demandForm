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
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QTableWidgetItem, QListView, QGroupBox, QRadioButton, QButtonGroup, QDataWidgetMapper
)

from qgis.PyQt.QtGui import (
    QIcon,
    QPixmap,
    QImage, QPainter, QStandardItem
)

from qgis.PyQt.QtCore import (
    QObject,
    QTimer,
    QThread,
    pyqtSignal,
    pyqtSlot, Qt,QModelIndex, QDateTime
)

from qgis.PyQt.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelation, QSqlRelationalTableModel, QSqlRelationalDelegate,QSqlTableModel
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
from .vrmTableWidget import vrmWidget

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
                          "Enumerator",
                          "CurrentSurvey"
                               ])

class VRMsUtilsMixin(FieldRestrictionTypeUtilsMixin):
    def __init__(self, iface):
        #RestrictionTypeUtilsMixin.__init__(self, iface)
        self.iface = iface
        self.settings = QgsSettings()

        self.params = vrmParams()

        #self.TOMsUtils = RestrictionTypeUtilsMixin(self.iface)

    def setDefaultFieldRestrictionDetails(self, currRestriction, currRestrictionLayer, currDate):
        TOMsMessageLog.logMessage("In VRM:setDefaultFieldRestrictionDetails: {}".format(currRestrictionLayer.name()), level=Qgis.Info)

        # TODO: Need to check whether or not these fields exist. Also need to retain the last values and reuse
        # gis.stackexchange.com/questions/138563/replacing-action-triggered-script-by-one-supplied-through-qgis-plugin

        try:
            currRestriction.setAttribute("LastUpdateDateTime", currDate)
        except Exception as e:
            TOMsMessageLog.logMessage("In setDefaultFieldRestrictionDetails. Problem with setting LastUpdateDateTime: {}".format(e),
                                      level=Qgis.Info)

    def setupFieldRestrictionDialog(self, restrictionDialog, currRestrictionLayer, currRestriction):

        TOMsMessageLog.logMessage("In VRM:setupVRMDialog: {}".format(currRestrictionLayer.name()),
                                  level=Qgis.Info)

        self.params.getParams()

        status = self.mapOtherFields(restrictionDialog, currRestrictionLayer, currRestriction)

        # Create a copy of the feature
        self.origFeature = originalFeature()
        self.origFeature.setFeature(currRestriction)

        if restrictionDialog is None:
            reply = QMessageBox.information(None, "Error",
                                            "setupFieldRestrictionDialog. Correct form not found",
                                            QMessageBox.Ok)
            TOMsMessageLog.logMessage(
                "In setupRestrictionDialog. dialog not found",
                level=Qgis.Info)
            return

        restrictionDialog.attributeForm().disconnectButtonBox()
        button_box = restrictionDialog.findChild(QDialogButtonBox, "button_box")

        if button_box is None:
            TOMsMessageLog.logMessage(
                "In setupRestrictionDialog. button box not found",
                level=Qgis.Warning)
            return

        button_box.accepted.connect(functools.partial(self.onSaveFieldRestrictionDetails, currRestriction,
                                      currRestrictionLayer, restrictionDialog))

        button_box.rejected.connect(functools.partial(self.onRejectFieldRestrictionDetailsFromForm, restrictionDialog, currRestrictionLayer))

        restrictionDialog.attributeForm().attributeChanged.connect(functools.partial(self.onAttributeChangedClass2_local, currRestriction, currRestrictionLayer))

        # setup widget mapping
        #currRestrictionModel = self.setupRestrictionInSurveyModel(self.surveyID, currRestriction)
        #self.setupRestrictionMapping(currRestrictionModel)

        self.photoDetails_field(restrictionDialog, currRestrictionLayer, currRestriction)

        TOMsMessageLog.logMessage("In setupFieldRestrictionDialog. Calling addVRMWidget ...", level=Qgis.Info)

        self.addVRMWidget(restrictionDialog, currRestrictionLayer, currRestriction)

        #self.addScrollBars(restrictionDialog)

    def mapOtherFields(self, restrictionDialog, currRestrictionLayer, currRestriction):

        # is there a better way ???
        currSurveyName = self.getCurrSurveyName(self.surveyID)
        SurveyBeatTitleWidget = restrictionDialog.findChild(QWidget, "SurveyBeatTitle")
        SurveyBeatTitleWidget.setText(currSurveyName)

        queryString = "SELECT RoadName, RestrictionLength, RestrictionTypeID FROM Supply WHERE \"GeometryID\" = '{}'".format(currRestriction.attribute("GeometryID"))
        TOMsMessageLog.logMessage(
            "In mapOtherFields: queryString: {}".format(queryString),
            level=Qgis.Warning)
        query = QSqlQuery(queryString)
        query.exec()

        RoadName, SectionLength, RestrictionTypeID = range(3)  # ?? see https://realpython.com/python-pyqt-database/#executing-dynamic-queries-string-formatting

        query.next()
        TOMsMessageLog.logMessage(
                "In mapOtherFields: RoadName: {}, SectionLength: {}".format(query.value(RoadName), query.value(SectionLength)),
                level=Qgis.Warning)

        RoadNameWidget = restrictionDialog.findChild(QWidget, "RoadName")
        RoadNameWidget.setText(query.value(RoadName))
        SectionLengthWidget = restrictionDialog.findChild(QWidget, "SectionLength")
        SectionLengthWidget.setText(str(query.value(SectionLength)))

        # get restriction details

        GeometryID = currRestriction.attribute('GeometryID')
        RestrictionDescription = self.getLookupDescription(self.RESTRICTION_TYPES, query.value(RestrictionTypeID))

        title = "{RestrictionDescription} [{GeometryID}]".format(RestrictionDescription=RestrictionDescription,
                                                             GeometryID=GeometryID)

        RestrictionDetailsWidget = restrictionDialog.findChild(QWidget, "RestrictionDetails")
        RestrictionDetailsWidget.setText(title)


    def onAttributeChangedClass2_local(self, currFeature, layer, fieldName, value):

        TOMsMessageLog.logMessage(
            "In field:FormOpen:onAttributeChangedClass 2 - layer: " + str(layer.name()) + " (" + fieldName + "): " + str(value), level=Qgis.Info)
        try:
            currFeature[layer.fields().indexFromName(fieldName)] = value
        except Exception as e:
            reply = QMessageBox.information(None, "Error",
                                                "onAttributeChangedClass2. Update failed for: " + str(layer.name()) + " (" + fieldName + "): " + str(value),
                                                QMessageBox.Ok)  # rollback all changes

        return

    def onSaveFieldRestrictionDetails(self, currFeature, currFeatureLayer, dialog):
        TOMsMessageLog.logMessage("In onSaveFieldRestrictionDetails:  currFeatureID: ".format(currFeature.id()), level=Qgis.Info)

        try:
            self.camera1.endCamera()
            self.camera2.endCamera()
            self.camera3.endCamera()
        except:
            None

        # set update time !!!

        try:
            currFeature.setAttribute("DemandSurveyDateTime", QDateTime.currentDateTime())
            currFeature.setAttribute("Enumerator", self.enumerator)
        except Exception as e:
            reply = QMessageBox.information(None, "Information", "Problem setting date/time: {}".format(e), QMessageBox.Ok)

        currFeatureLayer.updateFeature(currFeature)

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

        TOMsMessageLog.logMessage("In addVRMWidget ... ", level=Qgis.Info)
        vrmsTab = restrictionDialog.findChild(QWidget, "VRMs")
        vrmsLayout = vrmsTab.layout()
        vrmForm = vrmWidget(vrmsTab)

        currGeometryID = currRestriction.attribute("GeometryID")

        vrmForm.populateVrmWidget(self.surveyID, currGeometryID)

        vrmsLayout.addWidget(vrmForm)

        buttonLayout = QVBoxLayout()
        addButton = QPushButton("+")
        removeButton = QPushButton("-")
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(removeButton)

        vrmsLayout.addLayout(buttonLayout, 1, 1, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        addButton.clicked.connect(functools.partial(vrmForm.insertVrm, self.surveyID, currGeometryID))
        removeButton.clicked.connect(vrmForm.deleteVrm)

    def getCurrSurveyName(self, currSurveyID):
        # display list
        TOMsMessageLog.logMessage(
            "In getCurrSurveyName: currSurveyID: {}".format(currSurveyID), level=Qgis.Info)
        currSurveyName = ''

        surveyList = list()

        query = QSqlQuery("SELECT SurveyID, BeatTitle FROM Surveys ORDER BY SurveyID ASC")
        query.exec()

        SurveyID, BeatTitle = range(2)  # ?? see https://realpython.com/python-pyqt-database/#executing-dynamic-queries-string-formatting

        while query.next():
            TOMsMessageLog.logMessage("In getCurrSurveyName: surveyID: {}, BeatTitle: {}".format(query.value(SurveyID), query.value(BeatTitle)), level=Qgis.Info)
            surveyList.append(query.value(BeatTitle))
            if int(currSurveyID) == int(query.value(SurveyID)):
                currSurveyName = query.value(BeatTitle)
                break

        return currSurveyName

    def setupRestrictionInSurveyModel(self, surveyID, currRestriction):
        pass