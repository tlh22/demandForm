# -*- coding: utf-8 -*-
"""
/***************************************************************************
 movingTrafficSigns
                                 A QGIS plugin
 movingTrafficeSigns
                              -------------------
        begin                : 2019-05-08
        git sha              : $Format:%H$
        copyright            : (C) 2019 by TH
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

#import resources
# Import the code for the dialog

import os.path

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
    QMenu
)

from qgis.PyQt.QtGui import (
    QIcon,
    QPixmap,
    QImage
)


from qgis.PyQt.QtCore import (
    QObject,
    QThread,
    pyqtSignal,
    pyqtSlot,
    Qt,
    QSettings, QTranslator, qVersion, QCoreApplication,
    QDateTime
)

from qgis.core import (
    QgsMessageLog,
    QgsExpressionContextUtils,
    QgsWkbTypes,
    QgsMapLayer, Qgis, QgsRectangle, QgsFeatureRequest, QgsVectorLayer, QgsFeature, QgsProject
)
from qgis.gui import (
    QgsMapToolIdentify
)
#from qgis.core import *
#from qgis.gui import *
from TOMs.core.TOMsMessageLog import TOMsMessageLog
from .demand_VRMs_UtilsClass import VRMsUtilsMixin, vrmParams
from restrictionsWithGNSS.SelectTool import (GeometryInfoMapTool, RemoveRestrictionTool)
#from .formUtils import demandFormUtils

#############################################################################

class demandVRMInfoMapTool(VRMsUtilsMixin, GeometryInfoMapTool):

    notifyFeatureFound = pyqtSignal(QgsVectorLayer, QgsFeature)

    def __init__(self, iface, surveyID):
        GeometryInfoMapTool.__init__(self, iface)
        self.iface = iface
        VRMsUtilsMixin.__init__(self, iface)

        self.surveyID = surveyID
        TOMsMessageLog.logMessage("In demandVRMInfoMapTool ... surveyID: " + str(self.surveyID), level=Qgis.Warning)

    def showRestrictionDetails(self, closestLayer, closestFeature):

        TOMsMessageLog.logMessage(
            "In demandVRMInfoMapTool.showRestrictionDetails ... Layer: " + str(closestLayer.name()),
            level=Qgis.Warning)

        GeometryID = closestFeature[closestLayer.fields().indexFromName("gid")]

        # Now want to swap to use "RestrictionsInSurveys"
        # get relevant feature ...
        restrictionsInSurveysLayer = QgsProject.instance().mapLayersByName("RestrictionsInSurveys")[0]

        filterString = '"SurveyID" = {} AND "GeometryID" = {}'.format(self.surveyID, GeometryID)

        request = QgsFeatureRequest().setFilterExpression(filterString)
        for currRestriction in restrictionsInSurveysLayer.getFeatures(request):
            TOMsMessageLog.logMessage(
                "In demandVRMInfoMapTool.showRestrictionDetails ... restriction found: ",
                level=Qgis.Warning)
            break  # take the first one (assuming only one!)

        # TODO: could improve ... basically check to see if transaction in progress ...
        if restrictionsInSurveysLayer.isEditable() == True:
            if restrictionsInSurveysLayer.commitChanges() == False:
                reply = QMessageBox.information(None, "Information",
                                                "Problem committing changes" + str(restrictionsInSurveysLayer.commitErrors()),
                                                QMessageBox.Ok)
            else:
                TOMsMessageLog.logMessage("In showRestrictionDetails: changes committed", level=Qgis.Info)

        status = restrictionsInSurveysLayer.startEditing()

        dialog = self.iface.getFeatureForm(restrictionsInSurveysLayer, currRestriction)

        self.setupFieldRestrictionDialog(dialog, restrictionsInSurveysLayer, currRestriction)

        dialog.show()
