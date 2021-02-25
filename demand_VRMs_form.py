# -*- coding: latin1 -*-
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------
# Tim Hancock 2017

# https://www.opengis.ch/2016/09/07/using-threads-in-qgis-python-plugins/
# https://snorfalorpagus.net/blog/2013/12/07/multithreading-in-qgis-python-plugins/

# Initialize Qt resources from file resources.py
from .resources import *

from qgis.PyQt.QtCore import (
    QObject,
    QDate,
    pyqtSignal,
    QCoreApplication, pyqtSlot, QThread
)

from qgis.PyQt.QtGui import (
    QIcon,
    QPixmap, QColor
)

from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QAction,
    QDialogButtonBox,
    QLabel,
    QDockWidget, QComboBox, QActionGroup, QDialog, QInputDialog
)

from qgis.PyQt.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelation, QSqlRelationalTableModel, QSqlRelationalDelegate
)

from qgis.core import (
    Qgis,
    QgsExpressionContextUtils,
    QgsProject,
    QgsMessageLog,
    QgsFeature,
    QgsGeometry,
    QgsApplication, QgsCoordinateTransform, QgsCoordinateReferenceSystem,
    QgsGpsDetector, QgsGpsConnection, QgsGpsInformation, QgsPoint, QgsPointXY,
    QgsDataSourceUri
)

from qgis.gui import (
    QgsVertexMarker,
    QgsMapToolEmitPoint
)

import os, time

#from qgis.gui import *

# from .CadNodeTool.TOMsNodeTool import TOMsNodeTool
from TOMs.core.TOMsMessageLog import TOMsMessageLog
from TOMs.search_bar import searchBar

from .demand_VRMs_UtilsClass import VRMsUtilsMixin, vrmParams
from .SelectTool import GeometryInfoMapTool, RemoveRestrictionTool
from TOMs.restrictionTypeUtilsClass import TOMsLayers, TOMsConfigFile
from .SelectTool import demandVRMInfoMapTool
import functools

class demandVRMsForm(VRMsUtilsMixin):

    def __init__(self, iface, demandVRMsToolbar):

        TOMsMessageLog.logMessage("In captureGPSFeatures::init", level=Qgis.Info)

        VRMsUtilsMixin.__init__(self, iface)

        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        self.demandVRMsToolbar = demandVRMsToolbar
        #self.gpsMapTool = False
        self.marker = None

        # This will set up the items on the toolbar
        # Create actions

        self.demandVRMsGroup = QActionGroup(demandVRMsToolbar)

        self.actionRestrictionDetails = QAction(QIcon(":/plugins/featureswithgps/resources/mActionGetInfo.svg"),
                                         QCoreApplication.translate("MyPlugin", "Get Section Details"),
                                         self.iface.mainWindow())
        self.actionRestrictionDetails.setCheckable(True)
        self.demandVRMsGroup.addAction(self.actionRestrictionDetails)

        # Add actions to the toolbar

        self.demandVRMsToolbar.addAction(self.actionRestrictionDetails)

        self.demandVRMsGroup.addAction(self.actionRestrictionDetails)

        self.demandVRMsGroup.setExclusive(True)
        self.demandVRMsGroup.triggered.connect(self.onGroupTriggered)

        # Connect action signals to slots

        self.actionRestrictionDetails.triggered.connect(self.doRestrictionDetails)

        self.actionRestrictionDetails.setEnabled(False)

        #self.searchBar = searchBar(self.iface, self.demandVRMsToolbar)
        #self.searchBar.disableSearchBar()

        self.mapTool = None
        self.createMapToolDict = {}

    def enableVRMToolbarItems(self):

        TOMsMessageLog.logMessage("In enableVRMToolbarItems", level=Qgis.Warning)
        self.closeTOMs = False

        self.tableNames = TOMsLayers(self.iface)
        self.params = vrmParams()

        self.tableNames.TOMsLayersNotFound.connect(self.setCloseTOMsFlag)
        self.params.TOMsParamsNotFound.connect(self.setCloseDemandFlag)

        self.TOMsConfigFileObject = TOMsConfigFile(self.iface)
        self.TOMsConfigFileObject.TOMsConfigFileNotFound.connect(self.setCloseTOMsFlag)
        self.TOMsConfigFileObject.initialiseTOMsConfigFile()

        self.tableNames.getLayers(self.TOMsConfigFileObject)
        self.params.getParams()

        if self.closeTOMs:
            QMessageBox.information(self.iface.mainWindow(), "ERROR", ("Unable to start editing tool ..."))
            return   # TODO: allow function to continue without GPS enabled ...

        # new get the connection details for "VRMs"
        vrmsLayer = QgsProject.instance().mapLayersByName("VRMs")[0]
        vrmsUriName = vrmsLayer.dataProvider().dataSourceUri()  # this returns a string with the db name and layer, eg. 'Z:/Tim//SYS2012_Demand_VRMs.gpkg|layername=VRMs'
        dbName = vrmsUriName[:vrmsUriName.find('|')]

        self.dbConn = QSqlDatabase.addDatabase("QSQLITE")
        self.dbConn.setDatabaseName(dbName)
        if not self.dbConn.open():
            QMessageBox.critical(None, "Cannot open database",
                                 "Unable to establish a database connection.\n\n"
                                 "Click Cancel to exit.", QMessageBox.Cancel)

        # now get user / survey id details - and check previous pass and whether it is to be included ...

        #QMessageBox.information(self.iface.mainWindow(), "Info", ("This is were we get user / survey id details ..."))
        """
        Obtain user name
        Get list of surveys and set exclusive check list - and get selection
        Check whether there are any records for this survey. If not, if there are records for the previous survey ask whether they are to be brought forward
        if so, copy details from previous survey to current survey
        """
        self.checkEnumeratorName()  # sets self.enumerator
        self.surveyID = self.getCurrSurvey()
        self.checkPreviousSurvey(self.surveyID)

        self.enableToolbarItems()

        self.createMapToolDict = {}

    def enableToolbarItems(self):
        TOMsMessageLog.logMessage("In enableToolbarItems", level=Qgis.Warning)

        self.actionRestrictionDetails.setEnabled(True)

        self.currMapTool = None
        self.theCurrentMapTool = None

    def disableToolbarItems(self):

        self.actionRestrictionDetails.setEnabled(False)
        #self.searchBar.disableSearchBar()


    def setCloseTOMsFlag(self):
        self.closeTOMs = True
        QMessageBox.information(self.iface.mainWindow(), "ERROR", ("Now closing TOMs ..."))

    def disableVRMToolbarItems(self):

        TOMsMessageLog.logMessage("In disableVRMToolbarItems", level=Qgis.Warning)

        self.disableToolbarItems()

        # TODO: Need to delete any tools ...
        for layer, mapTool in self.createMapToolDict.items  ():
            try:
                status = layer.rollBack()
            except Exception as e:
                None
                """reply = QMessageBox.information(None, "Information",
                                                    "Problem rolling back changes" + str(self.currLayer.commitErrors()),
                                                    QMessageBox.Ok)"""
            del mapTool

        self.createMapToolDict = {}

        try:
            self.iface.currentLayerChanged.disconnect(self.changeCurrLayer2)
        except Exception as e:
            TOMsMessageLog.logMessage(
                "In disableVRMToolbarItems. Issue with disconnects for currentLayerChanged {}".format(e),
                level=Qgis.Warning)

        try:
            self.canvas.mapToolSet.disconnect(self.changeMapTool2)
        except Exception as e:
            TOMsMessageLog.logMessage(
                "In disableFeaturesWithGPSToolbarItems. Issue with disconnects for mapToolSet {}".format(
                    e),
                level=Qgis.Warning)

        try:
            self.canvas.extentsChanged.disconnect(self.changeExtents)
        except Exception as e:
            TOMsMessageLog.logMessage(
                "In disableFeaturesWithGPSToolbarItems. Issue with disconnects for extentsChanged {}".format(
                    e),
                level=Qgis.Warning)

        self.tableNames.removePathFromLayerForms()

    def setCloseDemandFlag(self):
        self.closeCaptureGPSFeatures = True
        self.gpsAvailable = True

    def onGroupTriggered(self, action):
        # hold the current action
        self.currGnssAction = action
        TOMsMessageLog.logMessage("In onGroupTriggered: curr action is {}".format(action.text()), level=Qgis.Info)


    def changeMapTool2(self):
        TOMsMessageLog.logMessage(
            "In changeMapTool2 ...", level=Qgis.Info)

        currMapTool = self.iface.mapCanvas().mapTool()

        if not self.isGnssTool(currMapTool):
            TOMsMessageLog.logMessage(
                "In changeMapTool2. Unchecking action ...", level=Qgis.Info)
            if self.currGnssAction:
                self.currGnssAction.setChecked(False)
        else:
            TOMsMessageLog.logMessage(
            "In changeMapTool2. No action for gnssTools.", level=Qgis.Info)

        TOMsMessageLog.logMessage(
            "In changeMapTool2. finished.", level=Qgis.Info)
        #print('tool unset')

    def changeCurrLayer2(self):
        TOMsMessageLog.logMessage("In changeLayer2 ... ", level=Qgis.Info)

        try:
            currMapTool = self.iface.mapCanvas().mapTool()
            self.currGnssAction.setChecked(False)
        except Exception as e:
            None

        TOMsMessageLog.logMessage(
            "In changeLayer2. finished.", level=Qgis.Info)
        print('layer changed')

    # -- end of tools for signals

    def changeExtents(self):
        TOMsMessageLog.logMessage("In changeExtents ... ", level=Qgis.Info)


    def doRestrictionDetails(self):
        """
            Select point and then display details. Assume that there is only one of these map tools in existence at any one time ??
        """
        TOMsMessageLog.logMessage("In doRestrictionDetails", level=Qgis.Info)

        self.supplyLayer = self.tableNames.setLayer("Supply")
        self.iface.setActiveLayer(self.supplyLayer)

        if self.actionRestrictionDetails.isChecked():

            TOMsMessageLog.logMessage("In doRestrictionDetails - tool activated", level=Qgis.Warning)

            self.showRestrictionMapTool = demandVRMInfoMapTool(self.iface, self.surveyID, self.enumerator)
            self.iface.mapCanvas().setMapTool(self.showRestrictionMapTool)
            self.showRestrictionMapTool.notifyFeatureFound.connect(self.showRestrictionDetails)

        else:

            TOMsMessageLog.logMessage("In doRestrictionDetails - tool deactivated", level=Qgis.Warning)

            if self.showRestrictionMapTool:
                self.iface.mapCanvas().unsetMapTool(self.showRestrictionMapTool)

            self.actionRestrictionDetails.setChecked(False)

    #@pyqtSlot(str)
    def showRestrictionDetails(self, closestLayer, closestFeature):

        TOMsMessageLog.logMessage(
            "In showRestrictionDetails ... Layer: " + str(closestLayer.name()),
            level=Qgis.Info)

        self.showRestrictionMapTool.notifyFeatureFound.disconnect(self.showRestrictionDetails)

        # TODO: could improve ... basically check to see if transaction in progress ...
        if closestLayer.isEditable() == True:
            reply = QMessageBox.question(None, "Information",
                                            "There is a transaction in progress on this layer. This action will rollback back any changes. Do you want to continue?",
                                            QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                return
            if closestLayer.commitChanges() == False:
                reply = QMessageBox.information(None, "Information",
                                                "Problem committing changes" + str(closestLayer.commitErrors()),
                                                QMessageBox.Ok)
            else:
                TOMsMessageLog.logMessage("In showRestrictionDetails: changes committed", level=Qgis.Info)

        self.dialog = self.iface.getFeatureForm(closestLayer, closestFeature)
        #self.TOMsUtils.setupRestrictionDialog(self.dialog, closestLayer, closestFeature)

        self.setupFieldRestrictionDialog(self.dialog, closestLayer, closestFeature)

        self.dialog.show()

    def checkEnumeratorName(self):
        # check user details
        self.enumerator = str(self.params.setParam("Enumerator"))
        #if len(self.enumerator) == 0:
        #    self.enumerator = ''

        enumeratorDialog = QInputDialog()
        enumeratorDialog.setLabelText("Please confirm your name")
        enumeratorDialog.setTextValue(self.enumerator)

        if enumeratorDialog.exec_() == QDialog.Accepted:
            self.enumerator = enumeratorDialog.textValue()
            TOMsMessageLog.logMessage("In checkEnumeratorName: {}".format(self.enumerator), level=Qgis.Warning)
            QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), 'Enumerator', self.enumerator)

    def getCurrSurvey(self):
        # display list

        currSurveyID = str(self.params.setParam("CurrentSurvey"))
        if len(currSurveyID) == 0:
            currSurveyID = 1
        newSurveyID = currSurveyID
        currSurveyName = ''
        newSurveyName = ''

        surveyList = list()

        query = QSqlQuery("SELECT SurveyID, BeatTitle FROM Surveys ORDER BY SurveyID ASC")
        query.exec()

        SurveyID, BeatTitle = range(2)  # ?? see https://realpython.com/python-pyqt-database/#executing-dynamic-queries-string-formatting

        while query.next():
            TOMsMessageLog.logMessage("In getCurrSurvey: surveyID: {}, BeatTitle: {}".format(query.value(SurveyID), query.value(BeatTitle)), level=Qgis.Warning)
            surveyList.append(query.value(BeatTitle))
            if int(currSurveyID) == int(query.value(SurveyID)):
                currSurveyName = query.value(BeatTitle)

        TOMsMessageLog.logMessage("In getCurrSurvey: surveyList: {}".format(surveyList), level=Qgis.Warning)
        surveyDialog = QInputDialog()
        surveyDialog.setLabelText("Please confirm the current survey")
        surveyDialog.setComboBoxItems(surveyList)
        surveyDialog.setTextValue(currSurveyName)

        if surveyDialog.exec_() == QDialog.Accepted:
            newSurveyName = surveyDialog.textValue()
            TOMsMessageLog.logMessage("In surveyName: {}".format(newSurveyName), level=Qgis.Warning)

            if currSurveyName != newSurveyName:
                for i in range (0, len(surveyList)):
                    if surveyList[i] == newSurveyName:
                        newSurveyID = i+1
                        TOMsMessageLog.logMessage("In surveyName: setting surveyID to {} ...".format(newSurveyID), level=Qgis.Warning)
                        QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), 'CurrentSurvey', newSurveyID)

                        # check for any details from earlier survey
                        #self.checkPreviousSurveys()
                        break

            reply = QMessageBox.information(None, "Information", "Setting survey to {}".format(newSurveyName),
                                                QMessageBox.Ok)

        return newSurveyID

    def checkPreviousSurvey(self, currSurveyID):

        currSurveyID = int(currSurveyID)

        queryString = "SELECT COUNT(*) FROM VRMs WHERE SurveyID = {}".format(currSurveyID)
        TOMsMessageLog.logMessage("In checkPreviousSurvey: queryString 1: {}".format(queryString), level=Qgis.Warning)
        query = QSqlQuery(queryString)
        #query.exec()
        query.next()
        nrVrmsInCurrSurvey = query.value(0)

        if nrVrmsInCurrSurvey == 0:
            # no details added to curren survey - check previous survey
            queryString = "SELECT s1.SurveyDay, s2.SurveyDay FROM Surveys s1, Surveys s2 WHERE s1.SurveyID = {} AND s2.SurveyID = {}".format(currSurveyID, currSurveyID-1)
            TOMsMessageLog.logMessage("In checkPreviousSurvey: queryString 2: {}".format(queryString),
                                      level=Qgis.Warning)
            query = QSqlQuery(queryString)
            #query.exec()
            query.next()
            if query.value(0) == query.value(1):
                # same day - check for VRMs
                queryString = "SELECT COUNT(*) FROM VRMs WHERE SurveyID = {}".format(currSurveyID - 1)
                TOMsMessageLog.logMessage("In checkPreviousSurvey: queryString 3: {}".format(queryString),
                                          level=Qgis.Warning)
                query = QSqlQuery(queryString)
                query.next()
                nrVrmsInPrevSurvey = query.value(0)
                TOMsMessageLog.logMessage("In checkPreviousSurvey: nrVrmsInPrevSurvey: {}".format(nrVrmsInPrevSurvey),
                                          level=Qgis.Warning)
                if nrVrmsInPrevSurvey > 0:

                    reply = QMessageBox.question(None, 'Add details from previous survey',
                                                 # How do you access the main window to make the popup ???
                                                 'Do you want to add the VRMs from the previous survey?.',
                                                 QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:

                        queryString = "INSERT INTO VRMs (SurveyID, SectionID, GeometryID, PositionID, VRM, VehicleTypeID, RestrictionTypeID, PermitType, Notes) " \
                                      "SELECT {}, SectionID, GeometryID, PositionID, VRM, VehicleTypeID, RestrictionTypeID, PermitType, Notes FROM VRMs WHERE SurveyID = {}".format(currSurveyID, currSurveyID-1)
                        TOMsMessageLog.logMessage("In checkPreviousSurvey: queryString 4: {}".format(queryString),
                                                  level=Qgis.Warning)
                        query = QSqlQuery(queryString)

