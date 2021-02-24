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
    QDockWidget, QComboBox, QActionGroup
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
from .mapTools import CreateRestrictionTool, CreatePointTool
from .gnss_thread import GPS_Thread
#from TOMsUtils import *

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
        """self.actionCreateVRM = QAction(QIcon(":/plugins/featureswithgps/resources/mActionAddTrack.svg"),
                                       QCoreApplication.translate("MyPlugin", "Add VRM"),
                                       self.iface.mainWindow())
        self.actionCreateVRM.setCheckable(True)

        self.actionRemoveVRM = QAction(QIcon(":plugins/featureswithgps/resources/mActionDeleteTrack.svg"),
                                       QCoreApplication.translate("MyPlugin", "Remove VRM"),
                                       self.iface.mainWindow())
        self.actionRemoveVRM.setCheckable(True)
        """

        self.actionRestrictionDetails = QAction(QIcon(":/plugins/featureswithgps/resources/mActionGetInfo.svg"),
                                         QCoreApplication.translate("MyPlugin", "Get Section Details"),
                                         self.iface.mainWindow())
        self.actionRestrictionDetails.setCheckable(True)
        self.demandVRMsGroup.addAction(self.actionRestrictionDetails)

        # Add actions to the toolbar

        #self.demandVRMsToolbar.addAction(self.actionCreateVRM)
        self.demandVRMsToolbar.addAction(self.actionRestrictionDetails)
        #self.demandVRMsToolbar.addAction(self.actionRemoveVRM)


        #self.demandVRMsGroup.addAction(self.actionCreateVRM)
        #self.demandVRMsGroup.addAction(self.actionRemoveVRM)
        self.demandVRMsGroup.addAction(self.actionRestrictionDetails)

        self.demandVRMsGroup.setExclusive(True)
        self.demandVRMsGroup.triggered.connect(self.onGroupTriggered)

        # Connect action signals to slots

        #self.actionCreateVRM.triggered.connect(self.doCreateRestriction)
        self.actionRestrictionDetails.triggered.connect(self.doRestrictionDetails)
        #self.actionRemoveVRM.triggered.connect(self.doRemoveRestriction)

        #self.actionCreateVRM.setEnabled(False)
        self.actionRestrictionDetails.setEnabled(False)
        #self.actionRemoveVRM.setEnabled(False)

        self.searchBar = searchBar(self.iface, self.demandVRMsToolbar)
        self.searchBar.disableSearchBar()

        self.mapTool = None
        #self.currGnssAction = None
        #self.gpsConnection = None
        self.createMapToolDict = {}

    def enableVRMToolbarItems(self):

        TOMsMessageLog.logMessage("In enableVRMToolbarItems", level=Qgis.Warning)
        #self.gpsAvailable = False
        self.closeTOMs = False

        self.tableNames = TOMsLayers(self.iface)
        self.params = vrmParams()

        self.tableNames.TOMsLayersNotFound.connect(self.setCloseTOMsFlag)
        #self.tableNames.gpsLayersNotFound.connect(self.setCloseCaptureGPSFeaturesFlag)
        self.params.TOMsParamsNotFound.connect(self.setCloseDemandFlag)

        self.TOMsConfigFileObject = TOMsConfigFile(self.iface)
        self.TOMsConfigFileObject.TOMsConfigFileNotFound.connect(self.setCloseTOMsFlag)
        self.TOMsConfigFileObject.initialiseTOMsConfigFile()

        self.tableNames.getLayers(self.TOMsConfigFileObject)
        self.params.getParams()

        if self.closeTOMs:
            QMessageBox.information(self.iface.mainWindow(), "ERROR", ("Unable to start editing tool ..."))
            #self.actionProposalsPanel.setChecked(False)
            return   # TODO: allow function to continue without GPS enabled ...

        # new get the connection details for "VRMs"
        vrmsLayer = QgsProject.instance().mapLayersByName("VRMs")[0]
        #uri = QgsDataSourceUri(vrmsLayer.dataProvider().dataSourceUri())
        #vrmsProvider = vrmsLayer.dataProvider()
        #vrmsUri = vrmsProvider.uri()
        vrmsUriName = vrmsLayer.dataProvider().dataSourceUri()  # this returns a string with the db name and layer, eg. 'Z:/Tim//SYS2012_Demand_VRMs.gpkg|layername=VRMs'
        dbName = vrmsUriName[:vrmsUriName.find('|')]

        self.dbConn = QSqlDatabase.addDatabase("QSQLITE")
        self.dbConn.setDatabaseName(dbName)
        if not self.dbConn.open():
            QMessageBox.critical(None, "Cannot open memory database",
                                 "Unable to establish a database connection.\n\n"
                                 "Click Cancel to exit.", QMessageBox.Cancel)

        # now get user / survey id details - and check previous pass and whether it is to be included ...

        QMessageBox.information(self.iface.mainWindow(), "Info", ("This is were we get user / survey id details ..."))
        """
        Obtain user name
        Get list of surveys and set exclusive check list - and get selection
        Check whether there are any records for this survey. If not, if there are records for the previous survey ask whether they are to be brought forward
        if so, copy details from previous survey to current survey
        """
        self.currUser = self.getCurrUser()
        self.surveyID = self.getCurrSurvey()
        status = self.checkDetailsFromPreviousSurvey(self.surveyID)

        self.surveyID = 1

        self.enableToolbarItems()

        self.createMapToolDict = {}

    def enableToolbarItems(self):
        TOMsMessageLog.logMessage("In enableToolbarItems", level=Qgis.Warning)
        #self.actionCreateVRM.setEnabled(True)
        self.actionRestrictionDetails.setEnabled(True)
        #self.actionRemoveVRM.setEnabled(True)

        #self.searchBar.enableSearchBar()

        self.currMapTool = None
        self.theCurrentMapTool = None

        #self.createConnection()

        #self.iface.currentLayerChanged.connect(self.changeCurrLayer2)
        #self.canvas.mapToolSet.connect(self.changeMapTool2)
        #self.canvas.extentsChanged.connect(self.changeExtents)

    def disableToolbarItems(self):

        #self.actionCreateVRM.setEnabled(False)
        self.actionRestrictionDetails.setEnabled(False)
        #self.actionRemoveVRM.setEnabled(False)

        self.searchBar.disableSearchBar()

        """if self.gpsConnection:
            self.actionAddGPSLocation.setEnabled(False)"""

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

    """ 
        Using signals for ChangeTool and ChangeLayer to manage the tools - with the following functions
    """
    """def isGnssTool(self, mapTool):

        if (isinstance(mapTool, CreateRestrictionTool) or
           isinstance(mapTool, GeometryInfoMapTool) or
           isinstance(mapTool, RemoveRestrictionTool)):
            return True

        return False"""

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

        """if self.isGnssTool(currMapTool):
            TOMsMessageLog.logMessage("In changeLayer2. Action triggered ... ", level=Qgis.Info)
            self.currGnssAction.trigger()  # assumption is that there is an action associated with the tool
        else:
            TOMsMessageLog.logMessage(
            "In changeLayer2. No action for currentMapTool.", level=Qgis.Info)"""

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

        # TODO: Check whether or not there is a create maptool available. If so, stop this and finish using that/those tools

        if not self.iface.activeLayer():
            reply = QMessageBox.information(self.iface.mainWindow(), "Information", "Please choose a layer ...",
                                            QMessageBox.Ok)
            return

        if self.actionRestrictionDetails.isChecked():

            TOMsMessageLog.logMessage("In doRestrictionDetails - tool activated", level=Qgis.Warning)

            self.showRestrictionMapTool = demandVRMInfoMapTool(self.iface, self.surveyID)
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

        """if self.iface.activeLayer().readOnly() == True:
            TOMsMessageLog.logMessage("In showSignDetails - Not able to start transaction ...",
                                     level=Qgis.Info)
        else:
            if self.iface.activeLayer().startEditing() == False:
                reply = QMessageBox.information(None, "Information",
                                                "Could not start transaction on " + self.currLayer.name(),
                                                QMessageBox.Ok)
                return"""

        self.dialog = self.iface.getFeatureForm(closestLayer, closestFeature)
        #self.TOMsUtils.setupRestrictionDialog(self.dialog, closestLayer, closestFeature)

        self.setupFieldRestrictionDialog(self.dialog, closestLayer, closestFeature)

        self.dialog.show()

