'''
Created on 18 nov. 2022

@author: chk
'''
import time as t
import numpy as np
from PyQt5.QtCore import *
from avaspec import *
import avaspec as asp
class SPEC(object):
    '''
    classdocs
    '''


    def __init__(self, verb):
        self.verb = verb;
        spec = AVS_Init(0);
        
        self.spec_dict = {
            "0" : "ERR_SUCCESS",
            "-1" : "ERR_INVALID_PARAMETER",
            "-2" : "ERR_OPERATION_NOT_SUPPORTED",
            "-3" : "ERR_DEVICE_NOT_FOUND",
            "-4" : "ERR_INVALID_DEVICE_ID",
            "-5" : "ERR_OPERATION_PENDING",
            "-6" : "ERR_TIMEOUT",
            "-7" : "Reserved",
            "-8" : "ERR_INVALID_MEAS_DATA",
            "-9" : "ERR_INVALID_SIZE",
            "-10" : "ERR_INVALID_PIXEL_RANGE",
            "-11" : "ERR_INVALID_INT_TIME",
            "-12" : "ERR_INVALID_COMBINATION",
            "-13" : "Reserved",
            "-14" : "ERR_NO_MEAS_BUFFER_AVAIL",
            "-15" : "ERR_UNKNOWN",
            "-16" : "ERR_COMMUNICATION",
            "-17" : "ERR_NO_SPECTRA_IN_RAM",
            "-18" : "ERR_INVALID_DLL_VERSION",
            "-19" : "ERR_NO_MEMORY",
            "-20" : "ERR_DLL_INITIALISATION",
            "-21" : "ERR_INVALID_STATE",
            "-100" : "ERR_INVALID_PARAMETER_NR_PIXEL",
            "-101" : "ERR_INVALID_PARAMETER_ADC_GAIN",
            "-102" : "ERR_INVALID_PARAMETER_ADC_OFFSET",
            "-110" : "ERR_INVALID_MEASPARAM_AVG_SAT2",
            "-111" : "ERR_INVALID_MEASPARAM_AVG_RAM",
            "-112" : "ERR_INVALID_MEASPARAM_SYNC_RAM",
            "-113" : "ERR_INVALID_MEASPARAM_LEVEL_RAM",
            "-114" : "ERR_INVALID_MEASPARAM_SAT2_RAM",
            "-115" : "ERR_INVALID_MEASPARAM_FWVER_RAM",
            "-116" : "ERR_INVALID_MEASPARAM_DYNDARK",
            "-120" : "ERR_NOT_SUPPORTED_BY_SENSOR_TYPE ",
            "-121" : "ERR_NOT_SUPPORTED_BY_FW_VER",
            "-122" : "ERR_NOT_SUPPORTED_BY_FPGA_VER",
            "-140" : "ERR_SL_CALIBRATION_NOT_AVAILABLE",
            "-141" : "ERR_SL_STARTPIXEL_NOT_IN_RANGE",
            "-142" : "ERR_SL_ENDPIXEL_NOT_IN_RANGE",
            "-143" : "ERR_SL_STARTPIX_GT_ENDPIX",
            "-144" : "ERR_SL_MFACTOR_OUT_OF_RANGE"

        }

        self.nr = AVS_UpdateUSBDevices();
        if (self.nr > 0):
            mylist = AvsIdentityType * 1
            mylist = AVS_GetList(1)
            serienummer = str(mylist[0].SerialNumber.decode("utf-8"))
            self.spectro = AVS_Activate(mylist[0])
            # QMessageBox.information(self,"Info","AVS_Activate returned:  {0:d}".format(globals.dev_handle))
            devcon = DeviceConfigType()
            devcon = AVS_GetParameter(self.spectro, 63484)
            self.pixels = devcon.m_Detector_m_NrPixels
            self.wavelength = AVS_GetLambda(self.spectro)
            self.wavelengths = []
            x = 0
            while (x < self.pixels):   # 0 through 2047
               self.wavelengths.append(float(self.wavelength[x]))
               x += 1
        
    def prepSpectrometer(self, integrationtime, averages):
        ret = AVS_UseHighResAdc(self.spectro, True)
        measconfig = MeasConfigType()
        measconfig.m_StartPixel = 0
        measconfig.m_StopPixel = self.pixels - 1
        measconfig.m_IntegrationTime = float(integrationtime)
        measconfig.m_IntegrationDelay = 0
        measconfig.m_NrAverages = int(averages)
        measconfig.m_CorDynDark_m_Enable = 0  # nesting of types does NOT work!!
        measconfig.m_CorDynDark_m_ForgetPercentage = 0
        measconfig.m_Smoothing_m_SmoothPix = 0
        measconfig.m_Smoothing_m_SmoothModel = 0
        measconfig.m_SaturationDetection = 0
        measconfig.m_Trigger_m_Mode = 0
        measconfig.m_Trigger_m_Source = 0
        measconfig.m_Trigger_m_SourceType = 0
        measconfig.m_Control_m_StrobeControl = 0
        measconfig.m_Control_m_LaserDelay = 0
        measconfig.m_Control_m_LaserWidth = 0
        measconfig.m_Control_m_LaserWaveLength = 0.0
        measconfig.m_Control_m_StoreToRam = 0
        ret = AVS_PrepareMeasure(self.spectro, measconfig)
        if self.verb:
            if not(ret == 0):
                print("Something went wrong when preparing spectrometer, errorcode " + str(ret))
            else:
                print("Spectrometer successfully prepared");
                
    def measure(self):
        ret = AVS_Measure(self.spectro, 0, 1)
        self.waitForMeasurement()
        
    def waitForMeasurement(self):
        measuring = True;
        while measuring:
            if AVS_PollScan(self.spectro) == 1:
                #if (self.verb):
                    #print("Measurement is ready")
                measuring = False
            #else:
                #if (self.verb):
                    #print("no measurement yet")
                
    def retrieveMeasurement(self):
        spectraldata = [0.0] * self.pixels
        timestamp = 0
        ret = AVS_GetScopeData(self.spectro)
        timestamp = ret[0]
        x = 0
        while (x < self.pixels): # 0 through 2047
            spectraldata[x] = ret[1][x]
            x += 1
        return spectraldata
    
    def getLambdas(self):
        ret = AVS_GetLambda(self.spectro)
        return ret
    
    def closeComm(self):
        ret = AVS_Deactivate(self.spectro)
        return ret
        
