import numpy as np
import os
import sys
import oat2x.utility as ut

# Generates data table that can be output to stdout, file, or combined with
# other data tables
class Oe2xtt():

    def __init__(self, source):

        self.MAX_SPIKES = int(1e6)
        self.NUM_SAMP = 32
        self.NUM_ELEC = 4
        self.source = source

    def parse(self, invert):

        d = self._loadSpikes(self.source)

        #Make sure there are NUM_SAMP samples per waveform
        #A/D is constrained to 32 samples/waveform
        num_samp = d["waveform"].shape[1]
        diff_samp = self.NUM_SAMP - num_samp
        if diff_samp < 0: # Chop off end of waveform
            s = np.delete(d["waveform"], np.s_[diff_samp:num_samp:1],1)
        elif diff_samp > 0: # Pad with 0's
            s = np.pad(d["waveform"], 
                       ((0,0), (0,diff_samp), (0,0)), 
                       "constant", 
                       constant_values=((0,0), (0, 0), (0, 0)))
       
        x, y, z = s.shape 
        s = np.reshape(s, (x, y*z)) 

        dt = [("t", "int32"), ("w","int16",(self.NUM_SAMP * self.NUM_ELEC))]
        self.data = np.zeros(x, dtype=dt)
        self.data["t"][:] = d["timestamps"]
        self.data["w"][:] = (s - 32768)
        if invert:
            self.data["w"] = -self.data["w"] 

    def dump(self, fid):

        header_txt = ("%%BEGINHEADER\n"
                      "% Extraction type:\ttetrode waveforms\n"
                      "% Fields:\ttimestamp,8,4,1\twaveform,2,2,128\n"
                      "%%ENDHEADER\n")

        if (fid is None):
            with sys.stdout as fd:
                fd.write(header_txt)
                fd.write(np.array_str(self.data))

        else:
            with open(fid, 'wb') as fd:
                fd.write(bytes(header_txt, 'ascii'))
                fd.write(self.data.tobytes())


    # Taken from OpenEphys python lib
    def _loadSpikes(self, filepath):
        
        # doesn't quite work...spikes are transposed in a weird way    
        
        data = { }
        
        f = open(filepath,'rb')
        header = self._readHeader(f)
        
        if float(header[' version']) < 0.4:
            raise Exception('Loader is only compatible with .spikes files with version 0.4 or higher')
         
        data['header'] = header 
        numChannels = int(header['num_channels'])
        numSamples = 40 # **NOT CURRENTLY WRITTEN TO HEADER**
        
        spikes = np.zeros((self.MAX_SPIKES, numSamples, numChannels))
        timestamps = np.zeros(self.MAX_SPIKES)
        source = np.zeros(self.MAX_SPIKES)
        gain = np.zeros((self.MAX_SPIKES, numChannels))
        thresh = np.zeros((self.MAX_SPIKES, numChannels))
        sortedId = np.zeros((self.MAX_SPIKES, numChannels))
        recNum = np.zeros(self.MAX_SPIKES)
        
        currentSpike = 0
        
        while f.tell() < os.fstat(f.fileno()).st_size:
            
            eventType = np.fromfile(f, np.dtype('<u1'),1) #always equal to 4, discard
            timestamps[currentSpike] = np.fromfile(f, np.dtype('<i8'), 1)
            software_timestamp = np.fromfile(f, np.dtype('<i8'), 1)
            source[currentSpike] = np.fromfile(f, np.dtype('<u2'), 1)
            numChannels = np.fromfile(f, np.dtype('<u2'), 1)
            numSamples = np.fromfile(f, np.dtype('<u2'), 1)
            sortedId[currentSpike] = np.fromfile(f, np.dtype('<u2'),1)
            electrodeId = np.fromfile(f, np.dtype('<u2'),1)
            channel = np.fromfile(f, np.dtype('<u2'),1)
            color = np.fromfile(f, np.dtype('<u1'), 3)
            pcProj = np.fromfile(f, np.float32, 2)
            sampleFreq = np.fromfile(f, np.dtype('<u2'),1)
            
            waveforms = np.fromfile(f, np.dtype('<u2'), numChannels*numSamples)
            wv = np.reshape(waveforms, (numSamples, numChannels))
            
            gain[currentSpike,:] = np.fromfile(f, np.float32, numChannels)
            thresh[currentSpike,:] = np.fromfile(f, np.dtype('<u2'), numChannels)
            
            recNum[currentSpike] = np.fromfile(f, np.dtype('<u2'), 1)

            
            for ch in range(numChannels):
                spikes[currentSpike,:,ch] = wv[:,ch]
            
            currentSpike += 1
            
        data['waveform'] = spikes[:currentSpike,:,:]
        data['timestamps'] = timestamps[:currentSpike]

        return data

    def _readHeader(self, f):
        header = { }
        h = f.read(1024).decode().replace('\n','').replace('header.','')
        for i,item in enumerate(h.split(';')):
            if '=' in item:
                header[item.split(' = ')[0]] = item.split(' = ')[1]
        return header
