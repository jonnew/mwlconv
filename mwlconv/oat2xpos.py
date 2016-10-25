import json
import numpy as np
import sys
import oat2x.json_parse as jp
import oat2x.utility as ut


# Generates data table that can be output to stdout, file, or combined with
# other data tables
class Oat2xpos():

    def __init__(self, *args):

        if len(args) > 2:
            raise ValueError("Up to two input position files "
                             "(front and back) can be processed.")

        # See line 984 of posextract.c
        dtype_spec = [("timestamp", np.int32), 
                      ("x_front", np.int16), 
                      ("y_front", np.int16), 
                      ("x_back", np.int16), 
                      ("y_back", np.int16)]

        self.sources = []
        for a in args:
            self.sources.append(a)

        self.data_type = np.dtype(dtype_spec)


    def parse(self, timescale):

        fields = ["tick", "pos_xy"]

        try: 

            with open(self.sources[0]) as fd:
                pos_data = jp.flat_parse(fields, fd)
                self.data = np.zeros((len(pos_data["tick"]), 1), 
                                      dtype=self.data_type)
                self.data["timestamp"][:,0] = timescale * np.asarray(pos_data["tick"])
                self.data["x_front"][:,0] = np.asarray(pos_data["pos_xy"])[:,0]
                self.data["y_front"][:,0] = np.asarray(pos_data["pos_xy"])[:,1]

            if (len(self.sources) is 1):
                self.data["x_back"] = self.data["x_front"]
                self.data["y_back"] = self.data["y_front"]
            else:
                with open(self.sources[1]) as fd:
                    pos_data = jp.flat_parse(fields, fd)
                    self.data["x_back"][:,0] = np.asarray(pos_data["pos_xy"])[:,0]
                    self.data["y_back"][:,0] = np.asarray(pos_data["pos_xy"])[:,1]

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


    def dump(self, fid):
       
        header_txt = ("%%BEGINHEADER\n"
                      "% Extraction type:\textended dual diode position\n"
                      "% Fields:\ttimestamp,8,4,1\txfront,2,2,1\tyfront,2,2,1\txback,2,2,1\tyback,2,2,1\n"
                      "%%ENDHEADER\n")

        if (fid is None):
            with sys.stdout as fd:
                fd.write(header_txt)
                fd.write(np.array_str(self.data))

        else:
            with open(fid, 'wb') as fd:
                fd.write(bytes(header_txt, 'ascii'))
                fd.write(self.data.tobytes())

