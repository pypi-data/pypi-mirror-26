############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017
#
# Licence APL2.0
#
############################################################
import copy
import datetime
import logging
import math
import os
import platform
import random
import shutil
import sys
# threading
import threading
import time

# PyQt5
import PyQt5
# library for fits file handling
import pyfits

# for data storing
from analyse.analysedata import Analyse
# cameras
from camera import none
from camera import indicamera
if platform.system() == 'Windows':
    from camera import maximdl
    from camera import sgpro
if platform.system() == 'Windows' or platform.system() == 'Darwin':
    from camera import theskyx
# modelpoints
from modeling import modelpoints


class Modeling(PyQt5.QtCore.QThread):
    logger = logging.getLogger(__name__)                                                                                   # logging enabling
    signalModelConnected = PyQt5.QtCore.pyqtSignal(int, name='ModelConnected')                                             # message for errors
    signalModelRedraw = PyQt5.QtCore.pyqtSignal(bool, name='ModelRedrawPoints')

    BLUE = 'background-color: rgb(42, 130, 218)'
    RED = 'background-color: red;'
    DEFAULT = 'background-color: rgb(32,32,32); color: rgb(192,192,192)'
    REF_PICTURE = '/model001.fit'
    IMAGEDIR = os.getcwd().replace('\\', '/') + '/images'
    CAPTUREFILE = 'modeling'

    def __init__(self, app):
        super().__init__()
        # make main sources available
        self.app = app
        # make windows imaging applications available
        if platform.system() == 'Windows':
            self.SGPro = sgpro.SGPro(self.app)
            self.MaximDL = maximdl.MaximDLCamera(self.app)
        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            self.TheSkyX = theskyx.TheSkyX(self.app)
        # make non windows applications available
        self.NoneCam = none.NoneCamera(self.app)
        self.INDICamera = indicamera.INDICamera(self.app)
        # select default application
        self.imagingHandler = self.NoneCam
        # assign support classes
        self.analyse = Analyse(self.app)
        self.transform = self.app.mount.transform
        self.modelpoints = modelpoints.ModelPoints(self.transform)
        # class variables
        self.modelAnalyseData = []
        self.modelData = None
        self.results = []
        # counter for thread timing
        self.counter = 0
        self.chooserLock = threading.Lock()
        # finally initialize the class configuration
        self.initConfig()

    def initConfig(self):
        if self.NoneCam.appAvailable:
            self.app.ui.pd_chooseImagingApp.addItem('No Application')
        if self.INDICamera.appAvailable:
            self.app.ui.pd_chooseImagingApp.addItem('INDI Camera')
        if platform.system() == 'Windows':
            if self.SGPro.appAvailable:
                self.app.ui.pd_chooseImagingApp.addItem('SGPro - ' + self.SGPro.appName)
            if self.MaximDL.appAvailable:
                self.app.ui.pd_chooseImagingApp.addItem('MaximDL - ' + self.MaximDL.appName)
        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            if self.TheSkyX.appAvailable:
                self.app.ui.pd_chooseImagingApp.addItem('TheSkyX - ' + self.TheSkyX.appName)
        try:
            if 'ImagingApplication' in self.app.config:
                self.app.ui.pd_chooseImagingApp.setCurrentIndex(int(self.app.config['ImagingApplication']))
            if 'CheckSortPoints' in self.app.config:
                self.app.ui.checkSortPoints.setChecked(self.app.config['CheckSortPoints'])
            if 'CheckDeletePointsHorizonMask' in self.app.config:
                self.app.ui.checkDeletePointsHorizonMask.setChecked(self.app.config['CheckDeletePointsHorizonMask'])
        except Exception as e:
            self.logger.error('item in config.cfg not be initialize, error:{0}'.format(e))
        finally:
            pass
        self.app.ui.pd_chooseImagingApp.currentIndexChanged.connect(self.chooseImagingApp)

    def storeConfig(self):
        self.app.config['ImagingApplication'] = self.app.ui.pd_chooseImagingApp.currentIndex()
        self.app.config['CheckSortPoints'] = self.app.ui.checkSortPoints.isChecked()
        self.app.config['CheckDeletePointsHorizonMask'] = self.app.ui.checkDeletePointsHorizonMask.isChecked()

    def chooseImagingApp(self):
        self.chooserLock.acquire()
        if self.imagingHandler.cameraConnected:
            self.imagingHandler.disconnectCamera()
        if self.app.ui.pd_chooseImagingApp.currentText().startswith('No Application'):
            self.imagingHandler = self.NoneCam
            self.logger.info('actual camera / plate solver is None')
        elif self.app.ui.pd_chooseImagingApp.currentText().startswith('INDI Camera'):
            self.imagingHandler = self.INDICamera
            self.logger.info('actual camera / plate solver is INDI Camera')
        elif self.app.ui.pd_chooseImagingApp.currentText().startswith('SGPro'):
            self.imagingHandler = self.SGPro
            self.logger.info('actual camera / plate solver is SGPro')
        elif self.app.ui.pd_chooseImagingApp.currentText().startswith('TheSkyX'):
            self.imagingHandler = self.TheSkyX
            self.logger.info('actual camera / plate solver is TheSkyX')
        elif self.app.ui.pd_chooseImagingApp.currentText().startswith('MaximDL'):
            self.imagingHandler = self.MaximDL
            self.logger.info('actual camera / plate solver is MaximDL')
        self.imagingHandler.checkAppStatus()
        self.imagingHandler.connectCamera()
        self.chooserLock.release()

    def run(self):                                                                                                          # runnable for doing the work
        self.counter = 0                                                                                                    # cyclic counter
        self.chooseImagingApp()
        while True:                                                                                                         # thread loop for doing jobs
            command = ''
            if not self.app.modelCommandQueue.empty():
                command = self.app.modelCommandQueue.get()
            if self.app.mount.mountHandler.connected:
                if self.imagingHandler.cameraConnected:
                    if command == 'RunBaseModel':
                        self.app.imageWindow.disableExposures()
                        self.app.ui.btn_runBaseModel.setStyleSheet(self.BLUE)
                        self.runBaseModel()                                                                                 # should be refactored to queue only without signal
                        self.app.ui.btn_runBaseModel.setStyleSheet(self.DEFAULT)
                        self.app.ui.btn_cancelModel.setStyleSheet(self.DEFAULT)                                             # button back to default color
                        self.app.imageWindow.enableExposures()
                    elif command == 'RunRefinementModel':
                        self.app.imageWindow.disableExposures()
                        self.app.ui.btn_runRefinementModel.setStyleSheet(self.BLUE)
                        self.runRefinementModel()
                        self.app.ui.btn_runRefinementModel.setStyleSheet(self.DEFAULT)
                        self.app.ui.btn_cancelModel.setStyleSheet(self.DEFAULT)                                             # button back to default color
                        self.app.imageWindow.enableExposures()
                    elif command == 'PlateSolveSync':
                        self.app.imageWindow.disableExposures()
                        self.app.ui.btn_plateSolveSync.setStyleSheet(self.BLUE)
                        self.plateSolveSync()                                                                               # should be refactored to queue only without signal
                        self.app.ui.btn_plateSolveSync.setStyleSheet(self.DEFAULT)
                        self.app.imageWindow.enableExposures()
                    elif command == 'RunBatchModel':
                        self.app.ui.btn_runBatchModel.setStyleSheet(self.BLUE)
                        self.runBatchModel()
                        self.app.ui.btn_runBatchModel.setStyleSheet(self.DEFAULT)
                    elif command == 'RunCheckModel':
                        self.app.imageWindow.disableExposures()
                        self.app.ui.btn_runCheckModel.setStyleSheet(self.BLUE)                                              # button blue (running)
                        num = self.app.mount.numberModelStars()
                        if num > 2:
                            self.runCheckModel()
                        else:
                            self.app.modelLogQueue.put('Run Analyse stopped, not BASE modeling available !\n')
                            self.app.messageQueue.put('Run Analyse stopped, not BASE modeling available !\n')
                        self.app.ui.btn_runCheckModel.setStyleSheet(self.DEFAULT)
                        self.app.ui.btn_cancelModel.setStyleSheet(self.DEFAULT)                                             # button back to default color
                        self.app.imageWindow.enableExposures()
                    elif command == 'RunAllModel':
                        self.app.imageWindow.disableExposures()
                        self.app.ui.btn_runAllModel.setStyleSheet(self.BLUE)                                                # button blue (running)
                        self.runAllModel()
                        self.app.ui.btn_runAllModel.setStyleSheet(self.DEFAULT)
                        self.app.ui.btn_cancelModel.setStyleSheet(self.DEFAULT)                                             # button back to default color
                        self.app.imageWindow.enableExposures()
                    elif command == 'RunTimeChangeModel':
                        self.app.imageWindow.disableExposures()
                        self.app.ui.btn_runTimeChangeModel.setStyleSheet(self.BLUE)
                        self.runTimeChangeModel()
                        self.app.ui.btn_runTimeChangeModel.setStyleSheet(self.DEFAULT)
                        self.app.ui.btn_cancelAnalyseModel.setStyleSheet(self.DEFAULT)                                      # button back to default color
                        self.app.imageWindow.enableExposures()
                    elif command == 'RunHystereseModel':
                        self.app.imageWindow.disableExposures()
                        self.app.ui.btn_runHystereseModel.setStyleSheet(self.BLUE)
                        self.runHystereseModel()
                        self.app.ui.btn_runHystereseModel.setStyleSheet(self.DEFAULT)
                        self.app.ui.btn_cancelAnalyseModel.setStyleSheet(self.DEFAULT)                                      # button back to default color
                        self.app.imageWindow.enableExposures()
                    elif command == 'ClearAlignmentModel':
                        self.app.ui.btn_clearAlignmentModel.setStyleSheet(self.BLUE)
                        self.app.modelLogQueue.put('Clearing alignment modeling - taking 4 seconds.\n')
                        self.clearAlignmentModel()
                        self.app.modelLogQueue.put('Model cleared!\n')
                        self.app.ui.btn_clearAlignmentModel.setStyleSheet(self.DEFAULT)
                if command == 'GenerateDSOPoints':
                    self.app.ui.btn_generateDSOPoints.setStyleSheet(self.BLUE)
                    self.modelpoints.generateDSOPoints(int(float(self.app.ui.numberHoursDSO.value())),
                                                       int(float(self.app.ui.numberPointsDSO.value())),
                                                       int(float(self.app.ui.numberHoursPreview.value())),
                                                       copy.copy(self.app.mount.ra),
                                                       copy.copy(self.app.mount.dec))
                    if self.app.ui.checkSortPoints.isChecked():
                        self.modelpoints.sortPoints('refinement')
                    if self.app.ui.checkDeletePointsHorizonMask.isChecked():
                        self.modelpoints.deleteBelowHorizonLine()
                    self.signalModelRedraw.emit(True)
                    self.app.ui.btn_generateDSOPoints.setStyleSheet(self.DEFAULT)
                elif command == 'GenerateDensePoints':
                    self.app.ui.btn_generateDensePoints.setStyleSheet(self.BLUE)
                    self.modelpoints.generateDensePoints()
                    if self.app.ui.checkSortPoints.isChecked():
                        self.modelpoints.sortPoints('refinement')
                    if self.app.ui.checkDeletePointsHorizonMask.isChecked():
                        self.modelpoints.deleteBelowHorizonLine()
                    self.signalModelRedraw.emit(True)
                    self.app.ui.btn_generateDensePoints.setStyleSheet(self.DEFAULT)
                elif command == 'GenerateNormalPoints':
                    self.app.ui.btn_generateNormalPoints.setStyleSheet(self.BLUE)
                    self.modelpoints.generateNormalPoints()
                    if self.app.ui.checkSortPoints.isChecked():
                        self.modelpoints.sortPoints('refinement')
                    if self.app.ui.checkDeletePointsHorizonMask.isChecked():
                        self.modelpoints.deleteBelowHorizonLine()
                    self.signalModelRedraw.emit(True)
                    self.app.ui.btn_generateNormalPoints.setStyleSheet(self.DEFAULT)
                else:
                    pass
            if command == 'LoadBasePoints':
                self.modelpoints.loadBasePoints(self.app.ui.le_modelPointsFileName.text())
                self.signalModelRedraw.emit(True)
            elif command == 'LoadRefinementPoints':
                self.modelpoints.loadRefinementPoints(self.app.ui.le_modelPointsFileName.text())
                if self.app.ui.checkSortPoints.isChecked():
                    self.modelpoints.sortPoints('refinement')
                if self.app.ui.checkDeletePointsHorizonMask.isChecked():
                    self.modelpoints.deleteBelowHorizonLine()
                self.signalModelRedraw.emit(True)
            elif command == 'GenerateGridPoints':
                self.app.ui.btn_generateGridPoints.setStyleSheet(self.BLUE)
                self.modelpoints.generateGridPoints(int(float(self.app.ui.numberGridPointsRow.value())),
                                                    int(float(self.app.ui.numberGridPointsCol.value())),
                                                    int(float(self.app.ui.altitudeMin.value())),
                                                    int(float(self.app.ui.altitudeMax.value())))
                if self.app.ui.checkSortPoints.isChecked():
                    self.modelpoints.sortPoints('refinement')
                if self.app.ui.checkDeletePointsHorizonMask.isChecked():
                    self.modelpoints.deleteBelowHorizonLine()
                self.signalModelRedraw.emit(True)
                self.app.ui.btn_generateGridPoints.setStyleSheet(self.DEFAULT)                                              # color button back, routine finished
            elif command == 'GenerateBasePoints':
                self.modelpoints.generateBasePoints(float(self.app.ui.azimuthBase.value()),
                                                    float(self.app.ui.altitudeBase.value()))
                self.signalModelRedraw.emit(True)
            elif command == 'DeletePoints':
                self.modelpoints.deletePoints()
                self.signalModelRedraw.emit(True)
            elif command == 'CancelModel':
                # todo: send cancel to model run
                self.app.ui.btn_cancelModel.setStyleSheet(self.RED)                                                         # reset color of button
            elif command == 'CancelAnalyseModel':
                # todo: send cancel to model run
                self.app.ui.btn_cancelAnalyseModel.setStyleSheet(self.RED)
            if self.counter % 5 == 0:                                                                                       # standard cycles in modeling thread fast
                self.getStatusFast()                                                                                        # calling fast part of status
            if self.counter % 20 == 0:                                                                                      # standard cycles in modeling thread slow
                self.getStatusSlow()                                                                                        # calling slow part of status
            self.counter += 1                                                                                               # loop +1
            time.sleep(.1)                                                                                                  # wait for the next cycle
        self.app.modelCommandQueue.task_done()
        self.terminate()                                                                                                    # closing the thread at the end

    def __del__(self):                                                                                                      # remove thread
        self.wait()

    def getStatusFast(self):                                                                                                # check app is running
        self.imagingHandler.checkAppStatus()
        self.imagingHandler.getCameraStatus()
        self.signalModelConnected.emit(1)                                                                                   # send status to GUI
        if self.imagingHandler.appRunning:
            self.signalModelConnected.emit(2)                                                                               # send status to GUI
        if self.imagingHandler.cameraConnected:
            self.signalModelConnected.emit(3)

    def getStatusSlow(self):
        pass

    @staticmethod
    def timeStamp():
        return time.strftime("%H:%M:%S", time.localtime())

    def clearAlignmentModel(self):
        self.modelAnalyseData = []
        self.app.mountCommandQueue.put('ClearAlign')
        time.sleep(4)                                                                                                       # we are waiting 4 seconds like Per did (don't know if necessary)

    def plateSolveSync(self):
        self.app.modelLogQueue.put('delete')                                                                                # deleting the logfile view
        self.app.modelLogQueue.put('{0} - Start Sync Mount Model\n'.format(self.timeStamp()))                               # Start informing user
        modelData = {}
        scaleSubframe = self.app.ui.scaleSubframe.value() / 100                                                             # scale subframe in percent
        modelData['base_dir_images'] = self.IMAGEDIR + '/platesolvesync'                                                    # define subdirectory for storing the images
        suc, mes, sizeX, sizeY, canSubframe, gainValue = self.imagingHandler.getCameraProps()                                     # look for capabilities of cam
        modelData['gainValue'] = gainValue
        if suc:
            self.logger.info('camera props: {0}, {1}, {2}'.format(sizeX, sizeY, canSubframe))            # debug data
        else:
            self.logger.warning('runModel       -> SgGetCameraProps with error: {0}'.format(mes))                           # log message
            self.app.modelLogQueue.put('{0} -\t {1} Model canceled! Error: {2}\n'.format(self.timeStamp(), 'Base', mes))
            return {}                                                                                                       # if cancel or failure, that empty dict has to returned
        modelData = self.prepareCaptureImageSubframes(scaleSubframe, sizeX, sizeY, canSubframe, modelData)                  # calculate the necessary data
        if modelData['sizeX'] == 800 and modelData['sizeY'] == 600:
            simulation = True
        else:
            simulation = False
        if not self.app.ui.checkDoSubframe.isChecked():                                                                     # should we run with subframes
            modelData['canSubframe'] = False                                                                                # set default values
        self.logger.info('modelData: {0}'.format(modelData))
        self.app.mountCommandQueue.put('PO')                                                                                # unpark to start slewing
        self.app.mountCommandQueue.put('AP')                                                                                # tracking on during the picture taking
        if not os.path.isdir(modelData['base_dir_images']):                                                                 # if analyse dir doesn't exist, make it
            os.makedirs(modelData['base_dir_images'])                                                                       # if path doesn't exist, generate is
        if self.app.ui.checkFastDownload.isChecked():
            modelData['speed'] = 'HiSpeed'
        else:
            modelData['speed'] = 'Normal'
        modelData['file'] = 'platesolvesync.fit'
        modelData['binning'] = int(float(self.app.ui.cameraBin.value()))
        modelData['exposure'] = int(float(self.app.ui.cameraExposure.value()))
        modelData['iso'] = int(float(self.app.ui.isoSetting.value()))
        modelData['blind'] = self.app.ui.checkUseBlindSolve.isChecked()
        modelData['scaleHint'] = float(self.app.ui.pixelSize.value()) * modelData['binning'] * 206.6 / float(self.app.ui.focalLength.value())
        modelData['sidereal_time'] = self.app.mount.sidereal_time[0:9]
        modelData['sidereal_time_float'] = self.transform.degStringToDecimal(self.app.mount.sidereal_time[0:9])
        modelData['ra_J2000'] = self.app.mount.ra
        modelData['dec_J2000'] = self.app.mount.dec
        modelData['ra_Jnow'] = self.app.mount.raJnow
        modelData['dec_Jnow'] = self.app.mount.decJnow
        modelData['pierside'] = self.app.mount.pierside
        modelData['refractionTemp'] = self.app.mount.refractionTemp
        modelData['refractionPress'] = self.app.mount.refractionPressure
        modelData['azimuth'] = 0
        modelData['altitude'] = 0
        self.app.modelLogQueue.put('{0} -\t Capturing image\n'.format(self.timeStamp()))
        suc, mes, imagepath = self.capturingImage(modelData, simulation)
        self.logger.info('suc:{0} mes:{1}'.format(suc, mes))
        if suc:
            self.app.modelLogQueue.put('{0} -\t Solving Image\n'.format(self.timeStamp()))
            suc, mes, modelData = self.solveImage(modelData, simulation)
            self.app.modelLogQueue.put('{0} -\t Image path: {1}\n'.format(self.timeStamp(), modelData['imagepath']))
            if suc:
                suc = self.syncMountModel(modelData['ra_sol_Jnow'], modelData['dec_sol_Jnow'])
                if suc:
                    self.app.modelLogQueue.put('{0} -\t Mount Model Synced\n'.format(self.timeStamp()))
                else:
                    self.app.modelLogQueue.put('{0} -\t Mount Model could not be synced - please check!\n'.format(self.timeStamp()))
            else:
                self.app.modelLogQueue.put('{0} -\t Solving error: {1}\n'.format(self.timeStamp(), mes))
        if not self.app.ui.checkKeepImages.isChecked():
            shutil.rmtree(modelData['base_dir_images'], ignore_errors=True)
        self.app.modelLogQueue.put('{0} - Sync Mount Model finished !\n'.format(self.timeStamp()))

    def setupRunningParameters(self):
        settlingTime = int(float(self.app.ui.settlingTime.value()))
        directory = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
        return settlingTime, directory

    def runBaseModel(self):
        if self.app.ui.checkClearModelFirst.isChecked():
            self.app.modelLogQueue.put('Clearing alignment modeling - taking 4 seconds.\n')
            self.clearAlignmentModel()
            self.app.modelLogQueue.put('Model cleared!\n')
        settlingTime, directory = self.setupRunningParameters()
        if len(self.modelpoints.BasePoints) > 0:
            self.modelData = self.runModel('Base', self.modelpoints.BasePoints, directory, settlingTime)
            self.modelData = self.app.mount.retrofitMountData(self.modelData)
            name = directory + '_base.dat'                                                                                  # generate name of analyse file
            if len(self.modelData) > 0:
                self.app.ui.le_analyseFileName.setText(name)                                                                # set data name in GUI to start over quickly
                self.analyse.saveData(self.modelData, name)                                                                 # save the data according to date
                self.app.mount.saveBaseModel()                                                                              # and saving the modeling in the mount
        else:
            self.logger.warning('There are no Basepoints for modeling')

    def runRefinementModel(self):
        num = self.app.mount.numberModelStars()
        suc, mes, sizeX, sizeY, canSubframe, gainValue = self.imagingHandler.getCameraProps()
        if sizeX == 800 and sizeY == 600 and suc:
            simulation = True
            self.modelData = []
        else:
            simulation = False
        if num > 2 or simulation:
            settlingTime, directory = self.setupRunningParameters()
            if len(self.modelpoints.RefinementPoints) > 0:
                if self.app.ui.checkKeepRefinement.isChecked():
                    self.app.mount.loadRefinementModel()
                else:
                    self.app.mount.loadBaseModel()
                refinePoints = self.runModel('Refinement', self.modelpoints.RefinementPoints, directory, settlingTime)
                for i in range(0, len(refinePoints)):
                    refinePoints[i]['index'] += len(self.modelData)
                self.modelData = self.modelData + refinePoints
                self.modelData = self.app.mount.retrofitMountData(self.modelData)
                name = directory + '_refinement.dat'                                                                        # generate name of analyse file
                if len(self.modelData) > 0:
                    self.app.ui.le_analyseFileName.setText(name)                                                            # set data name in GUI to start over quickly
                    self.analyse.saveData(self.modelData, name)                                                             # save the data
                    self.app.mount.saveRefinementModel()                                                                    # and saving the modeling in the mount
            else:
                self.logger.warning('There are no Refinement Points to modeling')
        else:
            self.app.modelLogQueue.put('Refine stopped, no BASE model available !\n')
            self.app.messageQueue.put('Refine stopped, no BASE model available !\n')

    def runCheckModel(self):
        settlingTime, directory = self.setupRunningParameters()
        points = self.modelpoints.BasePoints + self.modelpoints.RefinementPoints
        if len(points) > 0:                                                                                                 # there should be some points
            self.modelAnalyseData = self.runModel('Check', points, directory, settlingTime)                                 # run the analyse
            name = directory + '_check.dat'                                                                                 # generate name of analyse file
            if len(self.modelAnalyseData) > 0:
                self.app.ui.le_analyseFileName.setText(name)                                                                # set data name in GUI to start over quickly
                self.analyse.saveData(self.modelAnalyseData, name)                                                          # save the data
        else:                                                                                                               # otherwise omit the run
            self.logger.warning('There are no Refinement or Base Points to modeling')

    def runAllModel(self):
        self.runBaseModel()
        self.runRefinementModel()

    def runTimeChangeModel(self):
        settlingTime, directory = self.setupRunningParameters()
        points = []                                                                                                         # clear the points
        for i in range(0, int(float(self.app.ui.numberRunsTimeChange.value()))):                                            # generate the points
            points.append((int(self.app.ui.azimuthTimeChange.value()), int(self.app.ui.altitudeTimeChange.value()),
                           PyQt5.QtWidgets.QGraphicsTextItem(''), True))
        self.modelAnalyseData = self.runModel('TimeChange', points, directory, settlingTime)                                # run the analyse
        name = directory + '_timechange.dat'                                                                                # generate name of analyse file
        if len(self.modelAnalyseData) > 0:
            self.app.ui.le_analyseFileName.setText(name)                                                                    # set data name in GUI to start over quickly
            self.analyse.saveData(self.modelAnalyseData, name)                                                              # save the data

    def runHystereseModel(self):
        waitingTime, directory = self.setupRunningParameters()
        alt1 = int(float(self.app.ui.altitudeHysterese1.value()))
        alt2 = int(float(self.app.ui.altitudeHysterese2.value()))
        az1 = int(float(self.app.ui.azimuthHysterese1.value()))
        az2 = int(float(self.app.ui.azimuthHysterese2.value()))
        numberRunsHysterese = int(float(self.app.ui.numberRunsHysterese.value()))
        points = []
        for i in range(0, numberRunsHysterese):
            points.append((az1, alt1, PyQt5.QtWidgets.QGraphicsTextItem(''), True))
            points.append((az2, alt2, PyQt5.QtWidgets.QGraphicsTextItem(''), False))
        self.modelAnalyseData = self.runModel('Hysterese', points, directory, waitingTime)                                  # run the analyse
        name = directory + '_hysterese.dat'                                                                                 # generate name of analyse file
        self.app.ui.le_analyseFileName.setText(name)                                                                        # set data name in GUI to start over quickly
        if len(self.modelAnalyseData) > 0:
            self.app.ui.le_analyseFileName.setText(name)                                                                    # set data name in GUI to start over quickly
            self.analyse.saveData(self.modelAnalyseData, name)                                                              # save the data

    def runBatchModel(self):
        nameDataFile = self.app.ui.le_analyseFileName.text()
        self.logger.info('modeling from {0}'.format(nameDataFile))
        data = self.analyse.loadData(nameDataFile)                                                                          # load data
        if not('ra_Jnow' in data and 'dec_Jnow' in data):                                                                   # you need stored mount positions
            self.logger.warning('ra_Jnow or dec_Jnow not in data file')
            self.app.modelLogQueue.put('{0} - mount coordinates missing\n'.format(self.timeStamp()))                        # Gui Output
            return
        if not('ra_sol_Jnow' in data and 'dec_sol_Jnow' in data):                                                           # you need solved star positions
            self.logger.warning('ra_sol_Jnow or dec_sol_Jnow not in data file')
            self.app.modelLogQueue.put('{0} - solved data missing\n'.format(self.timeStamp()))                              # Gui Output
            return
        if not('pierside' in data and 'sidereal_time' in data):                                                             # you need sidereal time and pierside
            self.logger.warning('pierside and sidereal time not in data file')
            self.app.modelLogQueue.put('{0} - time and pierside missing\n'.format(self.timeStamp()))                        # Gui Output
            return
        self.app.mount.saveBackupModel()
        self.app.modelLogQueue.put('{0} - Start Batch modeling. Saving Actual modeling to BATCH\n'.format(self.timeStamp()))    # Gui Output
        self.app.mount.mountHandler.sendCommand('newalig')
        self.app.modelLogQueue.put('{0} - \tOpening Calculation\n'.format(self.timeStamp()))                                # Gui Output
        for i in range(0, len(data['index'])):
            command = 'newalpt{0},{1},{2},{3},{4},{5}'.format(self.transform.decimalToDegree(data['ra_Jnow'][i], False, True),
                                                              self.transform.decimalToDegree(data['dec_Jnow'][i], True, False),
                                                              data['pierside'][i],
                                                              self.transform.decimalToDegree(data['ra_sol_Jnow'][i], False, True),
                                                              self.transform.decimalToDegree(data['dec_sol_Jnow'][i], True, False),
                                                              self.transform.decimalToDegree(data['sidereal_time_float'][i], False, True))
            reply = self.app.mount.mountHandler.sendCommand(command)
            if reply == 'E':
                self.logger.warning('point {0} could not be added'.format(reply))                           # debug output
                self.app.modelLogQueue.put('{0} - \tPoint could not be added\n'.format(self.timeStamp()))                   # Gui Output
            else:
                self.app.modelLogQueue.put('{0} - \tAdded point {1} @ Az:{2}, Alt:{3} \n'
                                           .format(self.timeStamp(), reply, int(data['azimuth'][i]), int(data['altitude'][i])))  # Gui Output
        reply = self.app.mount.mountHandler.sendCommand('endalig')
        if reply == 'V':
            self.app.modelLogQueue.put('{0} - Model successful finished! \n'.format(self.timeStamp()))                      # Gui Output
            self.logger.info('Model successful finished!')                                               # debug output
        else:
            self.app.modelLogQueue.put('{0} - Model could not be calculated with current data! \n'.format(self.timeStamp()))    # Gui Output
            self.logger.warning('Model could not be calculated with current data!')                         # debug output

    def slewMountDome(self, az, alt):                                                                                       # slewing mount and dome to alt az point
        self.app.mountCommandQueue.put('Sz{0:03d}*{1:02d}'.format(int(az), int((az - int(az)) * 60 + 0.5)))                 # Azimuth setting
        self.app.mountCommandQueue.put('Sa+{0:02d}*{1:02d}'.format(int(alt), int((alt - int(alt)) * 60 + 0.5)))             # Altitude Setting
        self.app.mountCommandQueue.put('MS')                                                                                # initiate slewing with stop tracking
        self.logger.info('Connected:{0}'.format(self.app.dome.connected))
        break_counter = 0
        while not self.app.mount.slewing:                                                                                   # wait for mount starting slewing
            time.sleep(0.1)                                                                                                 # loop time
            break_counter += 1
            if break_counter == 30:
                break
        if self.app.dome.connected == 1:                                                                                    # if there is a dome, should be slewed as well
            if az >= 360:
                az = 359.9
            elif az < 0.0:
                az = 0.0
            try:
                self.app.dome.ascom.SlewToAzimuth(float(az))                                                                # set azimuth coordinate
            except Exception as e:
                self.logger.error('value: {0}, error: {1}'.format(az, e))
            self.logger.info('Azimuth:{0}'.format(az))
            while not self.app.mount.slewing:                                                                               # wait for mount starting slewing
                time.sleep(0.1)                                                                                             # loop time
            while self.app.mount.slewing or self.app.dome.slewing:                                                          # wait for stop slewing mount or dome not slewing
                time.sleep(0.1)                                                                                             # loop time
        else:
            while self.app.mount.slewing:                                                                                   # wait for tracking = 7 or dome not slewing
                time.sleep(0.1)                                                                                             # loop time
        # self.app.mountCommandQueue.put('AP')                                                                              # tracking on

    def prepareCaptureImageSubframes(self, scale, sizeX, sizeY, canSubframe, modelData):                                    # get camera data for doing subframes
        modelData['sizeX'] = 0                                                                                              # size inner window
        modelData['sizeY'] = 0                                                                                              # size inner window
        modelData['offX'] = 0                                                                                               # offset is half of the rest
        modelData['offY'] = 0                                                                                               # same in y
        modelData['canSubframe'] = False
        if canSubframe:                                                                                                     # if camera could do subframes
            modelData['sizeX'] = int(sizeX * scale)                                                                         # size inner window
            modelData['sizeY'] = int(sizeY * scale)                                                                         # size inner window
            modelData['offX'] = int((sizeX - modelData['sizeX']) / 2)                                                       # offset is half of the rest
            modelData['offY'] = int((sizeY - modelData['sizeY']) / 2)                                                       # same in y
            modelData['canSubframe'] = True                                                                                 # same in y
        else:                                                                                                               # otherwise error
            self.logger.warning('Camera does not support subframe.')
        if 'binning' in modelData:                                                                                          # if binning, we have to respects
            modelData['sizeX'] = int(modelData['sizeX'] / modelData['binning'])
            modelData['sizeY'] = int(modelData['sizeY'] / modelData['binning'])
        return modelData                                                                                                    # default without subframe

    def capturingImage(self, modelData, simulation):                                                                        # capturing image
        st_fits_header = modelData['sidereal_time'][0:10]                                                                   # store local sideral time as well
        ra_fits_header = self.transform.decimalToDegree(modelData['ra_J2000'], False, False, ' ')                           # set the point coordinates from mount in J2000 as hint precision 2
        dec_fits_header = self.transform.decimalToDegree(modelData['dec_J2000'], True, False, ' ')                          # set dec as well
        raJnow_fits_header = self.transform.decimalToDegree(modelData['ra_Jnow'], False, True, ' ')                         # set the point coordinates from mount in J2000 as hint precision 2
        decJnow_fits_header = self.transform.decimalToDegree(modelData['dec_Jnow'], True, True, ' ')                        # set dec as well
        if modelData['pierside'] == '1':
            pierside_fits_header = 'E'
        else:
            pierside_fits_header = 'W'
        self.logger.info('modelData: {0}'.format(modelData))
        suc, mes, modelData = self.imagingHandler.getImage(modelData)                                                       # imaging app specific abstraction
        if suc:
            if simulation:
                if getattr(sys, 'frozen', False):
                    bundle_dir = sys._MEIPASS                                                                               # we are running in a bundle
                else:
                    bundle_dir = os.path.dirname(sys.modules['__main__'].__file__)                                          # we are running in a normal Python environment
                shutil.copyfile(bundle_dir + self.REF_PICTURE, modelData['imagepath'])                                      # copy reference file as simulation target
            else:
                self.logger.info('getImagePath-> suc: {0}, modelData{1}'.format(suc, modelData))
                fitsFileHandle = pyfits.open(modelData['imagepath'], mode='update')                                         # open for adding field info
                fitsHeader = fitsFileHandle[0].header                                                                       # getting the header part
                if 'FOCALLEN' in fitsHeader and 'XPIXSZ' in fitsHeader:
                    modelData['scaleHint'] = float(fitsHeader['XPIXSZ']) * 206.6 / float(fitsHeader['FOCALLEN'])
                fitsHeader['DATE-OBS'] = datetime.datetime.now().isoformat()                                                # set time to current time of the mount
                fitsHeader['OBJCTRA'] = ra_fits_header                                                                      # set ra in header from solver in J2000
                fitsHeader['OBJCTDEC'] = dec_fits_header                                                                    # set dec in header from solver in J2000
                fitsHeader['CDELT1'] = str(modelData['scaleHint'])                                                          # x is the same as y
                fitsHeader['CDELT2'] = str(modelData['scaleHint'])                                                          # and vice versa
                fitsHeader['PIXSCALE'] = str(modelData['scaleHint'])                                                        # and vice versa
                fitsHeader['SCALE'] = str(modelData['scaleHint'])                                                           # and vice versa
                fitsHeader['MW_MRA'] = raJnow_fits_header                                                                   # reported RA of mount in JNOW
                fitsHeader['MW_MDEC'] = decJnow_fits_header                                                                 # reported DEC of mount in JNOW
                fitsHeader['MW_ST'] = st_fits_header                                                                        # reported local sideral time of mount from GS command
                fitsHeader['MW_MSIDE'] = pierside_fits_header                                                               # reported pierside of mount from SD command
                fitsHeader['MW_EXP'] = modelData['exposure']                                                                # store the exposure time as well
                fitsHeader['MW_AZ'] = modelData['azimuth']                                                                  # x is the same as y
                fitsHeader['MW_ALT'] = modelData['altitude']                                                                # and vice versa
                self.logger.info('DATE-OBS:{0}, OBJCTRA:{1} OBJTDEC:{2} CDELT1:{3} MW_MRA:{4} '
                                 'MW_MDEC:{5} MW_ST:{6} MW_PIER:{7} MW_EXP:{8} MW_AZ:{9} MW_ALT:{10}'
                                 .format(fitsHeader['DATE-OBS'], fitsHeader['OBJCTRA'], fitsHeader['OBJCTDEC'],
                                         fitsHeader['CDELT1'], fitsHeader['MW_MRA'], fitsHeader['MW_MDEC'],
                                         fitsHeader['MW_ST'], fitsHeader['MW_MSIDE'], fitsHeader['MW_EXP'],
                                         fitsHeader['MW_AZ'], fitsHeader['MW_ALT']))                                        # write all header data to debug
                fitsFileHandle.flush()                                                                                      # write all to disk
                fitsFileHandle.close()                                                                                      # close FIT file
            self.app.imageQueue.put(modelData['imagepath'])
            return True, 'OK', modelData                                                                                    # return true OK and imagepath
        else:                                                                                                               # otherwise
            return False, mes, modelData                                                                                    # image capturing was failing, writing message from SGPro back

    def addSolveRandomValues(self, modelData):
        modelData['dec_sol'] = modelData['dec_J2000'] + (2 * random.random() - 1) / 360
        modelData['ra_sol'] = modelData['ra_J2000'] + (2 * random.random() - 1) / 3600
        modelData['scale'] = 1.3
        modelData['angle'] = 90
        modelData['timeTS'] = 2.5
        ra, dec = self.transform.transformERFA(modelData['ra_sol'], modelData['dec_sol'], 3)
        modelData['ra_sol_Jnow'] = ra
        modelData['dec_sol_Jnow'] = dec
        modelData['raError'] = (modelData['ra_sol'] - modelData['ra_J2000']) * 3600
        modelData['decError'] = (modelData['dec_sol'] - modelData['dec_J2000']) * 3600
        modelData['modelError'] = math.sqrt(modelData['raError'] * modelData['raError'] + modelData['decError'] * modelData['decError'])
        return modelData

    def solveImage(self, modelData, simulation):                                                                            # solving image based on information inside the FITS files, no additional info
        modelData['usefitsheaders'] = True
        suc, mes, modelData = self.imagingHandler.solveImage(modelData)                                                     # abstraction of solver for image
        self.logger.info('suc:{0} mes:{1}'.format(suc, mes))                                                                # debug output
        if suc:
            ra_sol_Jnow, dec_sol_Jnow = self.transform.transformERFA(modelData['ra_sol'], modelData['dec_sol'], 3)          # transform J2000 -> Jnow
            modelData['ra_sol_Jnow'] = ra_sol_Jnow                                                                          # ra in Jnow
            modelData['dec_sol_Jnow'] = dec_sol_Jnow                                                                        # dec in  Jnow
            modelData['raError'] = (modelData['ra_sol'] - modelData['ra_J2000']) * 3600                                     # calculate the alignment error ra
            modelData['decError'] = (modelData['dec_sol'] - modelData['dec_J2000']) * 3600                                  # calculate the alignment error dec
            modelData['modelError'] = math.sqrt(modelData['raError'] * modelData['raError'] + modelData['decError'] * modelData['decError'])
            fitsFileHandle = pyfits.open(modelData['imagepath'], mode='update')                                             # open for adding field info
            fitsHeader = fitsFileHandle[0].header                                                                           # getting the header part
            fitsHeader['MW_PRA'] = modelData['ra_sol_Jnow']
            fitsHeader['MW_PDEC'] = modelData['dec_sol_Jnow']
            fitsHeader['MW_SRA'] = modelData['ra_sol']
            fitsHeader['MW_SDEC'] = modelData['dec_sol']
            fitsHeader['MW_PSCAL'] = modelData['scale']
            fitsHeader['MW_PANGL'] = modelData['angle']
            fitsHeader['MW_PTS'] = modelData['timeTS']
            self.logger.info('MW_PRA:{0} MW_PDEC:{1} MW_PSCAL:{2} MW_PANGL:{3} MW_PTS:{4}'.
                             format(fitsHeader['MW_PRA'], fitsHeader['MW_PDEC'], fitsHeader['MW_PSCAL'],
                                    fitsHeader['MW_PANGL'], fitsHeader['MW_PTS']))                                          # write all header data to debug
            fitsFileHandle.flush()                                                                                          # write all to disk
            fitsFileHandle.close()                                                                                          # close FIT file
            if simulation:
                modelData = self.addSolveRandomValues(modelData)
            return True, mes, modelData
        else:
            return False, mes, modelData

    def addRefinementStar(self, ra, dec):                                                                                   # add refinement star during modeling run
        self.logger.info('ra:{0} dec:{1}'.format(ra, dec))                                               # debug output
        self.app.mount.mountHandler.sendCommand('Sr{0}'.format(ra))                                                         # Write jnow ra to mount
        self.app.mount.mountHandler.sendCommand('Sd{0}'.format(dec))                                                        # Write jnow dec to mount
        starNumber = self.app.mount.numberModelStars()
        reply = self.app.mount.mountHandler.sendCommand('CMS')                                                              # send sync command (regardless what driver tells)
        starAdded = self.app.mount.numberModelStars() - starNumber
        if reply == 'E':                                                                                                    # 'E' says star could not be added
            if starAdded == 1:
                self.logger.error('star added, but return value was E')
                return True
            else:
                self.logger.error('error adding star')
                return False
        else:
            self.logger.info('refinement star added')
            return True                                                                                                     # simulation OK

    def syncMountModel(self, ra, dec):                                                                                      # add refinement star during modeling run
        self.logger.info('ra:{0} dec:{1}'.format(ra, dec))
        self.app.mount.mountHandler.sendCommand('Sr{0}'.format(ra))                                                         # Write jnow ra to mount
        self.app.mount.mountHandler.sendCommand('Sd{0}'.format(dec))                                                        # Write jnow dec to mount
        self.app.mount.mountHandler.sendCommand('CMCFG0')
        reply = self.app.mount.mountHandler.sendCommand('CM')                                                               # send sync command (regardless what driver tells)
        if reply[:5] == 'Coord':
            self.logger.info('mount modeling synced')
            return True
        else:
            self.logger.warning('error in sync mount modeling')
            return False                                                                                                    # simulation OK

    # noinspection PyUnresolvedReferences
    def runModel(self, modeltype, runPoints, directory, settlingTime):                                                      # modeling run routing
        self.app.modelLogQueue.put('status-- of --')
        self.app.modelLogQueue.put('percent0')
        self.app.modelLogQueue.put('timeleft--:--')
        modelData = dict()                                                                                                  # all modeling data
        results = list()                                                                                                    # results
        self.app.modelLogQueue.put('delete')                                                                                # deleting the logfile view
        self.app.modelLogQueue.put('#BW{0} - Start {1} Model\n'.format(self.timeStamp(), modeltype))                        # Start informing user
        numCheckPoints = 0                                                                                                  # number og checkpoints done
        modelData['base_dir_images'] = self.IMAGEDIR + '/' + directory                                                      # define subdirectory for storing the images
        scaleSubframe = self.app.ui.scaleSubframe.value() / 100                                                             # scale subframe in percent
        suc, mes, sizeX, sizeY, canSubframe, gainValue = self.imagingHandler.getCameraProps()                                     # look for capabilities of cam
        modelData['gainValue'] = gainValue
        if suc:
            self.logger.info('camera props: {0}, {1}, {2}'.format(sizeX, sizeY, canSubframe))
        else:
            self.logger.warning('SgGetCameraProps with error: {0}'.format(mes))
            self.app.modelLogQueue.put('#BW{0} -\t {1} Model canceled! Error: {2}\n'.format(self.timeStamp(), modeltype, mes))
            return {}                                                                                                       # if cancel or failure, that empty dict has to returned
        modelData = self.prepareCaptureImageSubframes(scaleSubframe, sizeX, sizeY, canSubframe, modelData)                  # calculate the necessary data
        if modelData['sizeX'] == 800 and modelData['sizeY'] == 600:
            simulation = True
        else:
            simulation = False
        if not self.app.ui.checkDoSubframe.isChecked():                                                                     # should we run with subframes
            modelData['canSubframe'] = False                                                                                # set default values
        self.logger.info('modelData: {0}'.format(modelData))
        self.app.mountCommandQueue.put('PO')                                                                                # unpark to start slewing
        self.app.mountCommandQueue.put('AP')                                                                                # tracking on during the picture taking
        if not os.path.isdir(modelData['base_dir_images']):                                                                 # if analyse dir doesn't exist, make it
            os.makedirs(modelData['base_dir_images'])                                                                       # if path doesn't exist, generate is
        timeStart = time.time()
        for i, (p_az, p_alt, p_item, p_solve) in enumerate(runPoints):                                                      # run through all modeling points
            modelData['azimuth'] = p_az
            modelData['altitude'] = p_alt
            if p_item.isVisible():                                                                                          # is the modeling point to be run = true ?
                # todo: put the code to multi thread modeling
                if False:                                                                                                   # here is the entry point for canceling the modeling run
                    self.app.modelLogQueue.put('#BW{0} -\t {1} Model canceled !\n'.format(self.timeStamp(), modeltype))     # we keep all the stars before
                    self.app.mountCommandQueue.put('AP')                                                                    # tracking on during the picture taking
                    self.app.modelLogQueue.put('status-- of --')
                    self.app.modelLogQueue.put('percent0')
                    self.app.modelLogQueue.put('timeleft--:--')
                    break                                                                                                   # finally stopping modeling run
                self.app.modelLogQueue.put('#BG{0} - Slewing to point {1:2d}  @ Az: {2:3.0f}\xb0 Alt: {3:2.0f}\xb0\n'
                                           .format(self.timeStamp(), i+1, p_az, p_alt))                                     # Gui Output
                self.logger.info('point {0:2d}  Az: {1:3.0f} Alt: {2:2.0f}'.format(i+1, p_az, p_alt))
                if modeltype in ['TimeChange']:                                                                             # in time change there is only slew for the first time, than only track during imaging
                    if i == 0:
                        self.slewMountDome(p_az, p_alt)                                                                     # slewing mount and dome to az/alt for first slew only
                        self.app.mountCommandQueue.put('RT9')                                                                    # stop tracking until next round
                else:
                    self.slewMountDome(p_az, p_alt)                                                                         # slewing mount and dome to az/alt for modeling point and analyse
                self.app.modelLogQueue.put('{0} -\t Wait mount settling / delay time:  {1:02d} sec'
                                           .format(self.timeStamp(), settlingTime))                                         # Gui Output
                timeCounter = settlingTime
                while timeCounter > 0:                                                                                      # waiting for settling time and showing data
                    time.sleep(1)                                                                                           # only step n seconds
                    timeCounter -= 1                                                                                        # count down
                    self.app.modelLogQueue.put('backspace')
                    self.app.modelLogQueue.put('{0:02d} sec'.format(timeCounter))                                           # write to gui
                self.app.modelLogQueue.put('\n')                                                                            # clear gui for next line
            if p_item.isVisible() and p_solve:                                                                              # is the modeling point to be run = visible and to be evaluated p_solve = True
                if self.app.ui.checkFastDownload.isChecked():                                                               # if camera is supporting high speed download
                    modelData['speed'] = 'HiSpeed'
                else:                                                                                                       # otherwise
                    modelData['speed'] = 'Normal'
                modelData['file'] = self.CAPTUREFILE + '{0:03d}'.format(i) + '.fit'                                         # generate filename for storing image
                modelData['binning'] = int(float(self.app.ui.cameraBin.value()))
                modelData['exposure'] = int(float(self.app.ui.cameraExposure.value()))
                modelData['iso'] = int(float(self.app.ui.isoSetting.value()))
                modelData['blind'] = self.app.ui.checkUseBlindSolve.isChecked()
                modelData['scaleHint'] = float(self.app.ui.pixelSize.value()) * modelData['binning'] * 206.6 / float(self.app.ui.focalLength.value())
                modelData['sidereal_time'] = self.app.mount.sidereal_time[0:9]
                modelData['sidereal_time_float'] = self.transform.degStringToDecimal(self.app.mount.sidereal_time[0:9])
                modelData['ra_J2000'] = self.app.mount.ra
                modelData['dec_J2000'] = self.app.mount.dec
                modelData['ra_Jnow'] = self.app.mount.raJnow
                modelData['dec_Jnow'] = self.app.mount.decJnow
                modelData['pierside'] = self.app.mount.pierside
                modelData['index'] = i
                modelData['refractionTemp'] = self.app.mount.refractionTemp                                                 # set it if string available
                modelData['refractionPress'] = self.app.mount.refractionPressure                                            # set it if string available
                if modeltype in ['TimeChange']:
                    self.app.mountCommandQueue.put('AP')                                                                    # tracking on during the picture taking
                self.app.modelLogQueue.put('{0} -\t Capturing image for modeling point {1:2d}\n'.format(self.timeStamp(), i + 1))   # gui output
                suc, mes, imagepath = self.capturingImage(modelData, simulation)                                            # capturing image and store position (ra,dec), time, (az,alt)
                if modeltype in ['TimeChange']:
                    self.app.mountCommandQueue.put('RT9')                                                                   # stop tracking until next round
                self.logger.info('suc:{0} mes:{1}'.format(suc, mes))
                if suc:                                                                                                     # if a picture could be taken
                    self.app.modelLogQueue.put('{0} -\t Solving Image\n'.format(self.timeStamp()))                          # output for user GUI
                    suc, mes, modelData = self.solveImage(modelData, simulation)                                            # solve the position and returning the values
                    self.app.modelLogQueue.put('{0} -\t Image path: {1}\n'.format(self.timeStamp(), modelData['imagepath']))     # Gui output
                    if suc:                                                                                                 # solved data is there, we can sync
                        if modeltype in ['Base', 'Refinement', 'All']:                                                      #
                            suc = self.addRefinementStar(modelData['ra_sol_Jnow'], modelData['dec_sol_Jnow'])               # sync the actual star to resolved coordinates in JNOW
                            if suc:
                                self.app.modelLogQueue.put('{0} -\t Point added\n'.format(self.timeStamp()))
                                numCheckPoints += 1                                                                         # increase index for synced stars
                                results.append(copy.copy(modelData))                                                        # adding point for matrix
                                p_item.setVisible(False)                                                                    # set the relating modeled point invisible
                            else:
                                self.app.modelLogQueue.put('{0} -\t Point could not be added - please check!\n'.format(self.timeStamp()))
                                self.logger.info('raE:{0} decE:{1} star could not be added'
                                                 .format(modelData['raError'], modelData['decError']))                      # generating debug output
                        self.app.modelLogQueue.put('{0} -\t RA_diff:  {1:2.1f}    DEC_diff: {2:2.1f}\n'
                                                   .format(self.timeStamp(), modelData['raError'], modelData['decError']))  # data for User
                        self.logger.info('modelData: {0}'.format(modelData))                             # log output
                    else:                                                                                                   # no success in solving
                        self.app.modelLogQueue.put('{0} -\t Solving error: {1}\n'.format(self.timeStamp(), mes))            # Gui output
                self.app.modelLogQueue.put('status{0} of {1}'.format(i+1, len(runPoints)))                                  # show status on screen
                modelBuildDone = (i + 1) / len(runPoints)
                self.app.modelLogQueue.put('percent{0}'.format(modelBuildDone))                                             # show status on screen
                actualTime = time.time() - timeStart
                timeCalculated = actualTime / (i + 1) * (len(runPoints) - i - 1)
                mm = int(timeCalculated / 60)
                ss = int(timeCalculated - 60 * mm)
                self.app.modelLogQueue.put('timeleft{0:02d}:{1:02d}'.format(mm, ss))                                        # show status on screen
        if not self.app.ui.checkKeepImages.isChecked():                                                                     # check if the modeling images should be kept
            shutil.rmtree(modelData['base_dir_images'], ignore_errors=True)                                                 # otherwise just delete them
        self.app.modelLogQueue.put('#BW{0} - {1} Model run finished. Number of modeled points: {2:3d}\n\n'
                                   .format(self.timeStamp(), modeltype, numCheckPoints))                                    # GUI output
        return results                                                                                                      # return results for analysing
