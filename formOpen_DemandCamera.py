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
Adapted from http://nathanw.net/2011/09/05/qgis-tips-custom-feature-forms-with-python-logic/

and also ...

https://gis.stackexchange.com/questions/144427/how-to-display-a-picture-in-qgis-custom-form

https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv

"""

#DEBUGMODE = True

from PyQt4.QtGui import (
    QMessageBox,
    QPixmap,
    QDialog,
    QLabel,
    QPushButton,
    QDialogButtonBox,
    QImage,
    QApplication
)

from PyQt4.QtCore import (
    QObject,
    QThread,
    pyqtSignal,
    pyqtSlot
)

from qgis.core import (
    QgsMessageLog,
    QgsExpressionContextUtils
)

import sys, os, ntpath
import numpy as np
#import cv2
import functools
import datetime
import time

try:
    import cv2
except ImportError:
    None


#from demandFormUtils import cvCamera

def formOpen_CountDemand(dialog, layer, feature):
        
    """
    Code that runs when the form is opened.
    """

    if not feature.isValid():
        reply = QMessageBox.information(None, "Information", "Invalid feature", QMessageBox.Ok)
        return
    
    if layer.startEditing() == False:
        reply = QMessageBox.information(None, "Information", "Could not start transaction", QMessageBox.Ok)
        
    utils = demandFormUtils()
    
    utils.setupDemandDialog (dialog, layer, feature)

def formOpen_Signs(dialog, layer, feature):
        
    """
    Code that runs when the form is opened.
    """

    if not feature.isValid():
        return
    
    utils = demandFormUtils()
    
    utils.setupDemandDialog (dialog, layer, feature)
    
    """DIALOG = dialog
    FIELD1 = DIALOG.findChild(QLabel, "Photo_Widget_01")
    FIELD2 = DIALOG.findChild(QLabel, "Photo_Widget_02")
    
    START_CAMERA_1 = DIALOG.findChild(QPushButton, "startCamera1")
    TAKE_PHOTO_1 = DIALOG.findChild(QPushButton, "getPhoto1")
    TAKE_PHOTO_1.setEnabled(False)
    
    button_box = DIALOG.findChild(QDialogButtonBox, "button_box")
    
    path_absolute = QgsExpressionContextUtils.projectScope().variable('PhotoPath')
    if path_absolute == None:
        reply = QMessageBox.information(None, "Information", "Please set value for PhotoPath.", QMessageBox.Ok)
        return"""
    
    #camera1 = formCamera(path_absolute)
    #START_CAMERA_1.clicked.connect(functools.partial(camera1.useCamera, START_CAMERA_1, TAKE_PHOTO_1, FIELD1))

    
    """if button_box is None:
        QgsMessageLog.logMessage(
            "In setupDemandDialog. button box not found",
            tag="TOMs panel")
        reply = QMessageBox.information(None, "Information", "Please reset form. There are missing buttons", QMessageBox.Ok)
        return

    button_box.accepted.disconnect(DIALOG.accept)
    button_box.accepted.connect(functools.partial(utils.onSaveDemandDetails, feature,
                                  layer, DIALOG, camera1))
                                  
    #button_box.rejected.disconnect(DIALOG.reject)
    
    button_box.rejected.connect(functools.partial(utils.onRejectDemandDetailsFromForm, DIALOG, camera1))
    
    # Generate the full path to the file
    
    fileName1 = str(feature.attribute("Photos"))
    #fileName2 = str(feature.attribute("Photos"))
    
    newPhotoFileName1 = os.path.join(path_absolute, fileName1)
    #newPhotoFileName2 = os.path.join(path_absolute, fileName2)
    QgsMessageLog.logMessage("In formOpen_Bays: path: " + newPhotoFileName1, tag="TOMs panel")
    
    # Now link the file to the field
    
    pixmap1 = QPixmap(newPhotoFileName1)
    if pixmap1.isNull():
        pass
        #FIELD1.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName1))
    else:
        FIELD1.setPixmap(pixmap1)
        FIELD1.setScaledContents(True)
    
    # In FIELD2 set up the camera"""
    
    """pixmap2 = QPixmap(newPhotoFileName2)
    if pixmap2.isNull():
        pass
        #FIELD2.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName2))
    else:
        FIELD2.setPixmap(pixmap2)
        FIELD2.setScaledContents(True)"""


class demandFormUtils():
        
    def setupDemandDialog(self, demandDialog, currDemandLayer, currFeature):

        #self.restrictionDialog = restrictionDialog
        self.demandDialog = demandDialog
        self.currDemandLayer = currDemandLayer
        self.currFeature = currFeature
        #self.restrictionTransaction = restrictionTransaction

        if self.demandDialog is None:
            QgsMessageLog.logMessage(
                "In setupDemandDialog. dialog not found",
                tag="TOMs panel")

        button_box = self.demandDialog.findChild(QDialogButtonBox, "button_box")                


        if button_box is None:
            QgsMessageLog.logMessage(
                "In setupDemandDialog. button box not found",
                tag="TOMs panel")
            reply = QMessageBox.information(None, "Information", "Please reset form. There are missing buttons", QMessageBox.Ok)
            return
            
        self.demandDialog.disconnectButtonBox()
        try:
            button_box.accepted.disconnect()
        except:
            None
            
        button_box.accepted.connect(functools.partial(self.onSaveDemandDetails, currFeature,
                                      currDemandLayer, self.demandDialog))

        try:
            button_box.rejected.disconnect()
        except:
            None
            
        button_box.rejected.connect(self.onRejectDemandDetailsFromForm)
        
        self.demandDialog.attributeChanged.connect(functools.partial(self.onAttributeChangedClass2, self.currFeature, self.currDemandLayer))
        
        self.photoDetails()

    def onSaveDemandDetails(self, currFeature, currFeatureLayer, dialog):
        QgsMessageLog.logMessage("In onSaveDemandDetails: ", tag="TOMs panel")

        try:
            self.camera1.endCamera()
        except:
            None
        
        status = currFeatureLayer.updateFeature(currFeature)
        #status = dialog.save()
        
        if currFeatureLayer.commitChanges() == False:
            reply = QMessageBox.information(None, "Information", "Problem committing changes" + str(currFeatureLayer.commitErrors()), QMessageBox.Ok)
        else:
            QgsMessageLog.logMessage("In onSaveDemandDetails: changes committed", tag="TOMs panel")

    def onRejectDemandDetailsFromForm(self):
        QgsMessageLog.logMessage("In onRejectDemandDetailsFromForm", tag="TOMs panel")
        #self.currDemandLayer.destroyEditCommand()
        
        try:
            self.camera1.endCamera()
        except:
            None
        
        if self.currDemandLayer.rollBack() == False:
            reply = QMessageBox.information(None, "Information", "Problem rolling back changes", QMessageBox.Ok)       
        else:
            QgsMessageLog.logMessage("In onRejectDemandDetailsFromForm: rollBack successful ...", tag="TOMs panel")
            
        self.demandDialog.reject()
        
    def onAttributeChangedClass2(self, currFeature, layer, fieldName, value):
        QgsMessageLog.logMessage(
            "In FormOpen:onAttributeChangedClass 2 - layer: " + str(layer.name()) + " (" + fieldName + "): " + str(value), tag="TOMs panel")

        # self.currFeature.setAttribute(fieldName, value)
        try:

            currFeature[layer.fieldNameIndex(fieldName)] = value
            #currFeature.setAttribute(layer.fieldNameIndex(fieldName), value)

        except:

            reply = QMessageBox.information(None, "Error",
                                                "onAttributeChangedClass2. Update failed for: " + str(layer.name()) + " (" + fieldName + "): " + str(value),
                                                QMessageBox.Ok)  # rollback all changes
        return

    def photoDetails(self):

        # Function to deal with photo fields

        QgsMessageLog.logMessage("In photoDetails", tag="TOMs panel")

        FIELD1 = self.demandDialog.findChild(QLabel, "Photo_Widget_01")
        FIELD2 = self.demandDialog.findChild(QLabel, "Photo_Widget_02")
        FIELD3 = self.demandDialog.findChild(QLabel, "Photo_Widget_03")

        path_absolute = QgsExpressionContextUtils.projectScope().variable('PhotoPath')
        if path_absolute == None:
            reply = QMessageBox.information(None, "Information", "Please set value for PhotoPath.", QMessageBox.Ok)
            return
            
        # Check path exists ...
        if os.path.isdir(path_absolute) == false:
            reply = QMessageBox.information(None, "Information", "PhotoPath folder does not exist. Please check value.", QMessageBox.Ok)
            return
        
        layerName = self.currDemandLayer.name()

        # Generate the full path to the file

        #fileName1 = "Photos"
        fileName1 = "Photos_01"
        fileName2 = "Photos_02"
        fileName3 = "Photos_03"

        idx1 = self.currDemandLayer.fieldNameIndex(fileName1)
        idx2 = self.currDemandLayer.fieldNameIndex(fileName2)
        idx3 = self.currDemandLayer.fieldNameIndex(fileName3)

        QgsMessageLog.logMessage("In photoDetails. idx1: " + str(idx1) + "; " + str(idx2) + "; " + str(idx3),
                                 tag="TOMs panel")
        # if currFeatureFeature[idx1]:
        # QgsMessageLog.logMessage("In photoDetails. photo1: " + str(currFeatureFeature[idx1]), tag="TOMs panel")
        # QgsMessageLog.logMessage("In photoDetails. photo2: " + str(currFeatureFeature.attribute(idx2)), tag="TOMs panel")
        # QgsMessageLog.logMessage("In photoDetails. photo3: " + str(currFeatureFeature.attribute(idx3)), tag="TOMs panel")

        if FIELD1:
            QgsMessageLog.logMessage("In photoDetails. FIELD 1 exisits",
                                     tag="TOMs panel")
            if self.currFeature[idx1]:
                newPhotoFileName1 = os.path.join(path_absolute, self.currFeature[idx1])
            else:
                newPhotoFileName1 = None

            #QgsMessageLog.logMessage("In photoDetails. Photo1: " + str(newPhotoFileName1), tag="TOMs panel")
            pixmap1 = QPixmap(newPhotoFileName1)
            if pixmap1.isNull():
                pass
                # FIELD1.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName1))
            else:
                FIELD1.setPixmap(pixmap1)
                FIELD1.setScaledContents(True)
                QgsMessageLog.logMessage("In photoDetails. Photo1: " + str(newPhotoFileName1), tag="TOMs panel")

            START_CAMERA_1 = self.demandDialog.findChild(QPushButton, "startCamera1")
            TAKE_PHOTO_1 = self.demandDialog.findChild(QPushButton, "getPhoto1")
            TAKE_PHOTO_1.setEnabled(False)
            
            self.camera1 = formCamera(path_absolute, newPhotoFileName1)
            START_CAMERA_1.clicked.connect(functools.partial(self.camera1.useCamera, START_CAMERA_1, TAKE_PHOTO_1, FIELD1))
            self.camera1.notifyPhotoTaken.connect(functools.partial(self.savePhotoTaken, idx1))
            
        if FIELD2:
            QgsMessageLog.logMessage("In photoDetails. FIELD 2 exisits",
                                     tag="TOMs panel")
            if self.currFeature[idx2]:
                newPhotoFileName2 = os.path.join(path_absolute, self.currFeature[idx2])
            else:
                newPhotoFileName2 = None

            # newPhotoFileName2 = os.path.join(path_absolute, str(self.currFeature[idx2]))
            # newPhotoFileName2 = os.path.join(path_absolute, str(self.currFeature.attribute(fileName2)))
            #QgsMessageLog.logMessage("In photoDetails. Photo2: " + str(newPhotoFileName2), tag="TOMs panel")
            pixmap2 = QPixmap(newPhotoFileName2)
            if pixmap2.isNull():
                pass
                # FIELD1.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName1))
            else:
                FIELD2.setPixmap(pixmap2)
                FIELD2.setScaledContents(True)
                QgsMessageLog.logMessage("In photoDetails. Photo2: " + str(newPhotoFileName2), tag="TOMs panel")

            START_CAMERA_2 = self.demandDialog.findChild(QPushButton, "startCamera2")
            TAKE_PHOTO_2 = self.demandDialog.findChild(QPushButton, "getPhoto2")
            TAKE_PHOTO_2.setEnabled(False)
            
            self.camera2 = formCamera(path_absolute, newPhotoFileName2)
            START_CAMERA_2.clicked.connect(functools.partial(self.camera2.useCamera, START_CAMERA_2, TAKE_PHOTO_2, FIELD2))
            self.camera2.notifyPhotoTaken.connect(functools.partial(self.savePhotoTaken, idx2))
            
        if FIELD3:
            QgsMessageLog.logMessage("In photoDetails. FIELD 3 exisits",
                                     tag="TOMs panel")

            
            if self.currFeature[idx3]:
                newPhotoFileName3 = os.path.join(path_absolute, self.currFeature[idx3])
            else:
                newPhotoFileName3 = None

            # newPhotoFileName3 = os.path.join(path_absolute, str(self.currFeature[idx3]))
            # newPhotoFileName3 = os.path.join(path_absolute,
            #                                 str(self.currFeature.attribute(fileName3)))
            # newPhotoFileName3 = os.path.join(path_absolute, str(layerName + "_Photos_03"))
            
            #QgsMessageLog.logMessage("In photoDetails. Photo3: " + str(newPhotoFileName3), tag="TOMs panel")
            pixmap3 = QPixmap(newPhotoFileName3)
            if pixmap3.isNull():
                pass
                # FIELD1.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName1))
            else:
                FIELD3.setPixmap(pixmap3)
                FIELD3.setScaledContents(True)
                QgsMessageLog.logMessage("In photoDetails. Photo3: " + str(newPhotoFileName3), tag="TOMs panel")

            START_CAMERA_3 = self.demandDialog.findChild(QPushButton, "startCamera3")
            TAKE_PHOTO_3 = self.demandDialog.findChild(QPushButton, "getPhoto3")
            TAKE_PHOTO_3.setEnabled(False)
            
            self.camera3 = formCamera(path_absolute, newPhotoFileName3)
            START_CAMERA_3.clicked.connect(functools.partial(self.camera3.useCamera, START_CAMERA_3, TAKE_PHOTO_3, FIELD3))
            self.camera3.notifyPhotoTaken.connect(functools.partial(self.savePhotoTaken, idx3))
                        
        pass

    @pyqtSlot(str)   
    def savePhotoTaken(self, idx, fileName):
        QgsMessageLog.logMessage("In demandFormUtils::savePhotoTaken ... " + fileName + " idx: " + str(idx), tag="TOMs panel")             
        if len(fileName) > 0:
            simpleFile = ntpath.basename(fileName)
            QgsMessageLog.logMessage("In demandFormUtils::savePhotoTaken. Simple file: " + simpleFile, tag="TOMs panel")
            
            try:
                self.currFeature[idx] = simpleFile
                QgsMessageLog.logMessage("In demandFormUtils::savePhotoTaken. attrib value changed", tag="TOMs panel")
            except:
                QgsMessageLog.logMessage("In demandFormUtils::savePhotoTaken. problem changing attrib value", tag="TOMs panel")
                reply = QMessageBox.information(None, "Error",
                                                    "savePhotoTaken. problem changing attrib value",
                                                    QMessageBox.Ok)
    
    
class formCamera(QObject):

    notifyPhotoTaken = QtCore.pyqtSignal(str)
    
    def __init__(self, path_absolute, currFileName):
        QtCore.QObject.__init__(self)
        self.path_absolute = path_absolute
        self.currFileName = currFileName
        self.camera = cvCamera()            
        
    @pyqtSlot(QtGui.QPixmap)    
    def displayFrame(self, pixmap):         
        #QgsMessageLog.logMessage("In formCamera::displayFrame ... ", tag="TOMs panel")    
        self.FIELD.setPixmap(pixmap)
        self.FIELD.setScaledContents(True)
        QtGui.QApplication.processEvents()  # processes the event queue - https://stackoverflow.com/questions/43094589/opencv-imshow-prevents-qt-python-crashing
                
    def useCamera(self, START_CAMERA_BUTTON, TAKE_PHOTO_BUTTON, FIELD):
        QgsMessageLog.logMessage("In formCamera::useCamera ... ", tag="TOMs panel")         
        self.START_CAMERA_BUTTON = START_CAMERA_BUTTON
        self.TAKE_PHOTO_BUTTON = TAKE_PHOTO_BUTTON
        self.FIELD = FIELD
        
        #self.blockSignals(True)
        self.START_CAMERA_BUTTON.clicked.disconnect()
        self.START_CAMERA_BUTTON.clicked.connect(self.endCamera)
        
        """ Camera code  """
       
        self.camera.changePixmap.connect(self.displayFrame)
        self.camera.closeCamera.connect(self.endCamera)
        
        self.TAKE_PHOTO_BUTTON.setEnabled(True)        
        self.TAKE_PHOTO_BUTTON.clicked.connect(functools.partial(self.camera.takePhoto, self.path_absolute))
        self.camera.photoTaken.connect(self.checkPhotoTaken)
        self.photoTaken = False
        
        QgsMessageLog.logMessage("In formCamera::useCamera: starting camera ... ", tag="TOMs panel")
        
        self.camera.startCamera()


    def endCamera(self):
    
        QgsMessageLog.logMessage("In formCamera::endCamera: stopping camera ... ", tag="TOMs panel")          
        
        self.camera.stopCamera()
        self.camera.changePixmap.disconnect(self.displayFrame)
        self.camera.closeCamera.disconnect(self.endCamera)
        
        #del self.camera
        
        self.TAKE_PHOTO_BUTTON.setEnabled(False)
        self.START_CAMERA_BUTTON.setChecked(False)
        self.TAKE_PHOTO_BUTTON.clicked.disconnect()

        self.START_CAMERA_BUTTON.clicked.disconnect()        
        self.START_CAMERA_BUTTON.clicked.connect(functools.partial(self.useCamera, self.START_CAMERA_BUTTON, self.TAKE_PHOTO_BUTTON, self.FIELD))
        
        if self.photoTaken == False:
            self.resetPhoto()

    @pyqtSlot(str)   
    def checkPhotoTaken(self, fileName):
        QgsMessageLog.logMessage("In formCamera::photoTaken: file: " + fileName, tag="TOMs panel")
        
        if len(fileName) > 0:
            self.photoTaken = True
            self.notifyPhotoTaken.emit(fileName)
        else:
            self.resetPhoto()
            self.photoTaken = False
    
    def resetPhoto(self):    
        QgsMessageLog.logMessage("In formCamera::resetPhoto ... ", tag="TOMs panel")
        
        pixmap = QPixmap(self.currFileName)
        if pixmap.isNull():
            pass
        else:
            self.FIELD.setPixmap(pixmap)
            self.FIELD.setScaledContents(True)
        
class cvCamera(QThread):

    changePixmap = QtCore.pyqtSignal(QtGui.QPixmap)
    closeCamera = QtCore.pyqtSignal()
    photoTaken = QtCore.pyqtSignal(str)   
    
    def __init__(self):
        QtCore.QThread.__init__(self)

        
    def stopCamera(self):
        QgsMessageLog.logMessage("In cvCamera::stopCamera ... ", tag="TOMs panel")
        self.cap.release()
         
    def startCamera(self):

        QgsMessageLog.logMessage("In cvCamera::startCamera: ... ", tag="TOMs panel")
        
        self.cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

        self.cap.set(3,640) #width=640
        self.cap.set(4,480) #height=480
        
        while self.cap.isOpened():
            self.getFrame()
            #cv2.imshow('img1',self.frame) #display the captured image            
            #cv2.waitKey(1)  
            time.sleep(0.1) # QTimer::singleShot()    
        else:
            QgsMessageLog.logMessage("In cvCamera::startCamera: camera closed ... ", tag="TOMs panel")
            self.closeCamera.emit()
        
    def getFrame(self):
        
        """ Camera code  """

        #QgsMessageLog.logMessage("In cvCamera::getFrame ... ", tag="TOMs panel")

        ret, self.frame = self.cap.read() # return a single frame in variable `frame`
        
        if ret==True:           
            # Need to change from BRG (cv::mat) to RGB image
            cvRGBImg = cv2.cvtColor(self.frame, cv2.cv.CV_BGR2RGB)
            qimg = QtGui.QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QtGui.QImage.Format_RGB888)
            
            # Now display ...
            pixmap = QtGui.QPixmap.fromImage(qimg)
            
            self.changePixmap.emit(pixmap)
            
        else:

            QgsMessageLog.logMessage("In cvCamera::useCamera: frame not returned ... ", tag="TOMs panel")
            self.closeCamera.emit()
        

    def takePhoto(self, path_absolute):
    
        QgsMessageLog.logMessage("In cvCamera::takePhoto ... ", tag="TOMs panel")     
        # Save frame to file

        fileName = 'Photo_{}.png'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S%z'))
        newPhotoFileName = os.path.join(path_absolute, fileName)

        QgsMessageLog.logMessage("Saving photo: file: " + newPhotoFileName, tag="TOMs panel")
        writeStatus = cv2.imwrite(newPhotoFileName, self.frame)

        if writeStatus is True:
            reply = QMessageBox.information(None, "Information", "Photo captured.", QMessageBox.Ok)
            self.photoTaken.emit(newPhotoFileName)
        else:
            reply = QMessageBox.information(None, "Information", "Problem taking photo.", QMessageBox.Ok)
            self.photoTaken.emit()

        # Now stop camera (and display image)
        
        self.cap.release()


    
        """def fps(self):
            fps = int(cv.GetCaptureProperty(self._cameraDevice, cv.CV_CAP_PROP_FPS))
            if not fps > 0:
                fps = self._DEFAULT_FPS
            return fps"""
        # https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv
        