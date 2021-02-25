# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VRMsDemand
                                 A QGIS plugin
 Start of TOMs
                              -------------------
        begin                : 2017-01-01
        git sha              : $Format:%H$
        copyright            : (C) 2017 by TH
        email                : th@mhtc.co.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QAction,
    QDialogButtonBox,
    QLabel,
    QDockWidget
)

from qgis.PyQt.QtGui import (
    QIcon,
    QPixmap
)

from qgis.PyQt.QtCore import (
    QObject, QTimer, pyqtSignal,
    QTranslator,
    QSettings,
    QCoreApplication,
    qVersion, QThread
)

from qgis.core import (
    Qgis,
    QgsExpressionContextUtils,
    QgsExpression,
    QgsFeatureRequest,
    # QgsMapLayerRegistry,
    QgsMessageLog, QgsFeature, QgsGeometry,
    QgsTransaction, QgsTransactionGroup,
    QgsProject,
    QgsApplication
)

from TOMs.core.TOMsMessageLog import TOMsMessageLog
from .demand_VRMs_form import demandVRMsForm


import os.path
import time
import datetime


class VRMsDemand:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        QgsMessageLog.logMessage("Starting VRMsDemand ... ", tag="TOMs panel")

        """Constructor.
        
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.actions = []   # ?? check - assume it initialises array of actions

        self.closeGPSToolsFlag = False
        # Set up log file and collect any relevant messages
        logFilePath = os.environ.get('QGIS_LOGFILE_PATH')

        if logFilePath:

            QgsMessageLog.logMessage("LogFilePath: " + str(logFilePath), tag="TOMs panel")

            logfile = 'qgis_' + datetime.date.today().strftime("%Y%m%d") + '.log'
            self.filename = os.path.join(logFilePath, logfile)
            QgsMessageLog.logMessage("Sorting out log file" + self.filename, tag="TOMs panel")
            QgsApplication.instance().messageLog().messageReceived.connect(self.write_log_message)

        # Set up local logging
        #loggingUtils = TOMsMessageLog()
        #loggingUtils.setLogFile()

        QgsMessageLog.logMessage("Finished init", tag="TOMs panel")
        #self.toolbar = self.iface.addToolBar(u'Test5Class')
        #self.toolbar.setObjectName(u'Test5Class')


    def write_log_message(self, message, tag, level):
        #filename = os.path.join('C:\Users\Tim\Documents\MHTC', 'qgis.log')
        with open(self.filename, 'a') as logfile:
            logfile.write('{dateDetails}:: {message}\n'.format(dateDetails= time.strftime("%Y%m%d:%H%M%S"), message=message))

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        QgsMessageLog.logMessage("Registering expression functions ... ", tag="TOMs panel")

        #self.hideMenusToolbars()

        # set up menu. Is there a generic way to do this? from an xml file?

        QgsMessageLog.logMessage("Adding toolbar", tag="TOMs panel")

        # Add toolbar 
        self.demandVRMsToolbar = self.iface.addToolBar("VRMsDemand Toolbar")
        self.demandVRMsToolbar.setObjectName("demandVRMsToolbar Toolbar")

        self.actionVRMToolbar = QAction(QIcon(""),
                                        QCoreApplication.translate("MyPlugin", "Start Demand"), self.iface.mainWindow())
        self.actionVRMToolbar.setCheckable(True)

        self.demandVRMsToolbar.addAction(self.actionVRMToolbar)

        self.actionVRMToolbar.triggered.connect(self.onInitVRMTools)
        
        # Now set up the toolbar

        self.demandTools = demandVRMsForm(self.iface, self.demandVRMsToolbar)
        #self.demandTools.disableFeaturesWithGPSToolbarItems()

    def onInitVRMTools(self):

        QgsMessageLog.logMessage("In onInitVRMTools", tag="TOMs panel")

        if self.actionVRMToolbar.isChecked():

            QgsMessageLog.logMessage("In onInitVRMTools. Activating ...", tag="TOMs panel")
            self.openVRMTools()

        else:

            QgsMessageLog.logMessage("In onInitVRMTools. Deactivating ...", tag="TOMs panel")
            self.closeVRMTools()

    def openVRMTools(self):
        # actions when the Proposals Panel is closed or the toolbar "start" is toggled

        QgsMessageLog.logMessage("In openGPSTools. Activating ...", tag="TOMs panel")

        if self.closeGPSToolsFlag:
            QMessageBox.information(self.iface.mainWindow(), "ERROR", ("Unable to start GPSTools ..."))
            self.actionVRMToolbar.setChecked(False)
            return

        self.demandTools.enableVRMToolbarItems()
        # TODO: connect close project signal to closeGPSTools

    def closeVRMTools(self):
        # actions when the Proposals Panel is closed or the toolbar "start" is toggled

        QgsMessageLog.logMessage("In closeGPSTools. Deactivating ...", tag="TOMs panel")

        # TODO: Delete any objects that are no longer needed

        #self.proposalTransaction.rollBackTransactionGroup()
        #del self.proposalTransaction  # There is another call to this function from the dock.close()

        # Now disable the items from the Toolbar

        self.demandTools.disableVRMToolbarItems()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        # remove the toolbar
        QgsMessageLog.logMessage("Clearing toolbar ... ", tag="TOMs panel")
        self.demandVRMsToolbar.clear()
        QgsMessageLog.logMessage("Deleting toolbar ... ", tag="TOMs panel")
        del self.demandVRMsToolbar
        #self.restoreMenusToolbars()

        QgsMessageLog.logMessage("Unload comnpleted ... ", tag="TOMs panel")

