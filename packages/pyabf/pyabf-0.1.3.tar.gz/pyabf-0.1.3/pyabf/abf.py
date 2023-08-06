"""Code to interact with ABF files. https://github.com/swharden/pyABF/ """

import sys
import numpy as np
np.set_printoptions(suppress=True) # don't use scientific notation
import matplotlib.pyplot as plt

from pyabf.header import ABFheader

class ABF:
    def __init__(self,abf):
        """The ABF class provides easy pythonic access to header and signal data in ABF2 files.
        
        * Although it is typically instantiated with a path (string), you can also use an ABF or ABFheader.
        
        Quick start:
            >>> abf = ABF("/path/to/file.abf")
            >>> abf.setSweep(0) # load data from the first sweep
            >>> print(abf.dataY) # signal data
            >>> print(abf.dataX) # timestamps
            >>> print(abf.dataC) # command waveform

        See all the properties available to you:
            >>> abf.help()
            
        Developers can access the ABFheader class features:
            >>> abf._abfHeader.saveHTML()
        
        """
        
        # get our abfHeader in order depending on what type of object we were given
        if type(abf) is str:
            self._abfHeader = ABFheader(abf)
        elif str(type(abf)).endswith(".ABF'>"):
            self._abfHeader = abf._abfHeader
        elif str(type(abf)).endswith(".ABFheader'>"):
            self._abfHeader = abf
        else:
            raise ValueError('abf must be a file path (str), ABF object, or ABFheader object.')
        
        ### Populate meaningful ABF attributes. Think about how you will use them: abf.something
        self.ID = self._abfHeader.header['abfID']
        self.filename = self._abfHeader.header['abfFilename']
        self.datetime = self._abfHeader.header['abfDatetime']
        self.pointDurSec = self._abfHeader.header['timeSecPerPoint']
        self.pointDurMS = self._abfHeader.header['timeSecPerPoint']*1000.0
        self.pointsPerSweep = self._abfHeader.header['sweepPointCount']
        self.pointsPerSec = self._abfHeader.header['rate']
        self.sweepCount = self._abfHeader.header['sweepCount']
        self.sweepList = np.arange(self.sweepCount)
        self.sweepLengthSec = self._abfHeader.header['sweepLengthSec']
        self.sweepPointCount = self._abfHeader.header['sweepPointCount']
        self.mode = self._abfHeader.header['mode']
        self.units = self._abfHeader.header['units']
        self.unitsLong = "Membrane Potential (mV)" if self.units is 'mV' else "Membrane Current (pA)"
        self.unitsCommand = self._abfHeader.header['unitsCommand']
        self.unitsCommandLong = "Clamp Potential (mV)" if self.unitsCommand is 'mV' else "Clamp Current (pA)"
        self.commandHoldingByDAC = self._abfHeader.header['commandHoldingByDAC']
        self.commandHold = self.commandHoldingByDAC[0]
        self.experimentLengthSec = self.sweepLengthSec*self.sweepCount
        self.unitsTime = "seconds"
        self.unitsTimeLong = "Signal Time (seconds)"
        
        ### Add information about the epochs / command waveform
        self.epochCount = len(self._abfHeader.header['nEpochType'])
        self.epochType = self._abfHeader.header['nEpochType']
        self.epochCommand = self._abfHeader.header['fEpochInitLevel']
        self.epochCommandDelta = self._abfHeader.header['fEpochLevelInc']
        self.epochDuration = self._abfHeader.header['lEpochInitDuration']
        self.epochDurationDelta = self._abfHeader.header['lEpochDurationInc']
        self.epochPulsePeriod = self._abfHeader.header['lEpochPulsePeriod']
        self.epochPulseWidth = self._abfHeader.header['lEpochPulseWidth']
        self.epochDigOut = self._abfHeader.header['nEpochDigitalOutput']
        
        ### Preload signal and time data (totalling ~10MB of memory per minute of 20kHz recording)
        self.signalData = self._abfHeader.data
        self.signalTimes = np.arange(len(self.signalData),dtype='float32')*self.pointDurSec
                                    
        ### Go ahead and set sweep zero to populate command signal trace
        self.setSweep(0)

    def help(self):
        """Launch the documentation in a web browser."""
        import webbrowser
        webbrowser.open('https://github.com/swharden/pyABF')
                                    
    def info(self,silent=False):
        """Display (and return) a long message indicating what you can access/do with the ABF class."""
        functions,attributes,lists,data=[],[],[],[]
        for itemName in dir(self):
            if itemName.startswith("_"):
                continue
            itemType=str(type(getattr(self,itemName))).split("'")[1]
            if itemType in ['str','float','int']:
                attributes.append(itemName)
            elif itemType =='list':
                lists.append(itemName)
            elif itemType =='numpy.ndarray':
                data.append(itemName)
            elif itemType =='method':
                functions.append(itemName)
            else:
                print(itemType,itemName)
            
        msg=""
        msg+="\n### INSTANTIATION ###\n"
        msg+="abf=pyabf.ABF(R'%s')\n"%self.filename
        
        msg+="\n### VALUES ###\n"
        for itemName in sorted(attributes):
            itemValue=str(getattr(self,itemName))
            msg+="* abf.%s = %s\n"%(itemName,itemValue)
        
        msg+="\n### LISTS ###\n"
        for itemName in sorted(lists):
            itemValue=str(getattr(self,itemName))
            msg+="* abf.%s = %s\n"%(itemName,itemValue)
            
        msg+="\n### SIGNAL STUFF###\n"
        for itemName in sorted(data):
            itemValue=getattr(self,itemName)
            if 'float' in str(itemValue.dtype):
                itemValue=np.array(getattr(self,itemName),dtype=np.float)
                itemValue=np.round(itemValue,decimals=5)
            msg+="* abf.%s = %s\n"%(itemName,itemValue)
            
        msg+="\n### FUNCTIONS ###\n"
        for itemName in sorted(functions):
            msg+="* abf.%s()\n"%(itemName)
        if not silent:
            print(msg)
        return msg
        
    def setSweep(self,sweepNumber=0,absoluteTime=False):
        """set all the self.data variables to contain data for a certain sweep"""
        self.dataSweepSelected = sweepNumber
        self.sweepSelected = sweepNumber
        pointStart=sweepNumber*self.pointsPerSweep
        pointEnd=pointStart+self.pointsPerSweep
        self.dataY = self.signalData[pointStart:pointEnd]
        if absoluteTime:
            self.dataX = self.signalTimes[pointStart:pointEnd]
        else:
            self.dataX = self.signalTimes[0:self.pointsPerSweep]
        self._updateCommandWaveform()
            
    def _updateCommandWaveform(self):
        """Read the epochs and figure out how to fill self.dataC with the command signal."""
        self.dataC = np.empty(self.dataX.size) # start as random data
        position=0 # start at zero here for clarity
        position+=int(self.pointsPerSweep/64) # the first 1/64th is pre-epoch (why???)
        self.dataC[:position]=self.commandHold # fill the pre-epoch with the command holding
        for epochNumber in range(self.epochCount):
            pointCount=self.epochDuration[epochNumber]
            deltaCommand=self.epochCommandDelta[epochNumber]*self.sweepSelected
            self.dataC[position:position+pointCount]=self.epochCommand[epochNumber]+deltaCommand
            position+=pointCount
        self.dataC[position:]=self.commandHold # set the post-epoch to the command holding
    
if __name__=="__main__":   
    abf=ABF(R"../../data/17o05028_ic_steps.abf")
    #abf=ABF(R"../../data/17o05024_vc_steps.abf")
    abf.info()
    print("DONE")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    