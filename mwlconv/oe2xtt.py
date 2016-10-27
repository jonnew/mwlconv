import numpy as np
import math
import os
import sys
import oat2x.utility as ut

np.set_printoptions(threshold=np.nan)

# Generates data table that can be output to stdout, file, or combined with
# other data tables
class Oe2xtt():

    def __init__(self, source):

        self.MAX_SPIKES = int(1e6)
        self.NUM_SAMP = 40 #OE does not write this info in the header.
        self.source = source

    def parse(self, invert):

        d = self._loadSpikes(self.source)["data"]

        ##Make sure there are NUM_SAMP samples per waveform
        ad_waves = np.swapaxes(d["waveform"],1,2)

        nr, ns, nc = ad_waves.shape 
        ad_waves = np.reshape(ad_waves, (nr, ns * nc)) 

        dt = [("t", "int32"), ("w","int16",(self.NUM_SAMP * nc))]
        self.data = np.zeros(nr, dtype=dt)
        self.data["t"][:] = d["timestamp"]
        self.data["w"][:] = (ad_waves - 32768) 
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
                fd.flush()
                sys.stdout.buffer.write(self.data.tobytes())

        else:
            with open(fid, 'wb') as fd:
                fd.write(bytes(header_txt, 'ascii'))
                fd.write(self.data.tobytes())


    # Taken from OpenEphys python lib
    def _loadSpikes(self, filepath):
        
        data = { }
        
        f = open(filepath,'rb')
        header = self._readHeader(f)
        
        if float(header[' version']) < 0.4:
            raise Exception('Loader is only compatible with .spikes files with version 0.4 or higher')
         
        data['header'] = header 
        numChannels = int(header['num_channels'])

        # Record schema
        dt = [('type', '<u1'),
              ('timestamp', '<i8'),
              ('softtime', '<i8'),
              ('source', '<u2'),
              ('numchan', '<u2'),
              ('numsamp', '<u2'),
              ('sortid', '<u2'),
              ('electrodeid', '<u2'),
              ('channel', '<u2'),
              ('color', '<u1',(3)), # The color of a spike...
              ('pcproj', np.float32 ,(2)),
              ('sampfreq', '<u2'),
              ('waveform', '<u2', (numChannels, self.NUM_SAMP)),
              ('gain', np.float32, (numChannels)),
              ('thresh', '<u2', (numChannels)),
              ('recordid', '<u2')]

        record_type = np.dtype(dt); 
        record_bytes = record_type.itemsize
        bytes_left = os.fstat(f.fileno()).st_size - f.tell()
        records_to_read = math.floor(bytes_left/record_bytes)

        data['data'] = np.zeros(records_to_read, dtype=record_type)
        data['data'] = np.fromfile(f, record_type, records_to_read)

        return data

    def _readHeader(self, f):
        header = { }
        h = f.read(1024).decode().replace('\n','').replace('header.','')
        for i,item in enumerate(h.split(';')):
            if '=' in item:
                header[item.split(' = ')[0]] = item.split(' = ')[1]
        return header
