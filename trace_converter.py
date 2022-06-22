 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #
 # Author: Thomas Dahlmann 2022

import can
import sys
import os

class TraceConverter():
    def __init__(self, mode, infilename, outfilename):
        self.mode = mode
        self.infilename = infilename        
        self.outfilename = outfilename        

    def blf2asc(self):
        with open(self.infilename, 'rb') as f_in:
            log_in = can.io.BLFReader(f_in)
            #ln = 1
            with open(self.outfilename, 'w') as f_out:
                log_out = can.io.ASCWriter(f_out)
                for msg in log_in:
                    #print(f"processing line {ln} / x ...", end='\r')
                    log_out.on_message_received(msg)
                    #ln += 1
                log_out.stop()

    def asc2blf(self):
        with open(self.infilename, 'r') as f_in:
            log_in = can.io.ASCReader(f_in)

            with open(self.outfilename, 'wb') as f_out:
                log_out = can.io.BLFWriter(f_out)
                for msg in log_in:
                    log_out.on_message_received(msg)
                log_out.stop()

    def convert(self):
        print(f"{self.infilename} => {self.outfilename}")
        if self.mode == "blf2asc":
            self.blf2asc()
        elif self.mode == "asc2blf":
            self.asc2blf()

def usage():
    print("usage: trace_converter blf2asc|asc2blf <input_filename> [output_filename]")
    sys.exit(1)

# check opts min
if len(sys.argv) < 3:
    usage()

# mode
mode = sys.argv[1]
if mode not in ["blf2asc", "asc2blf"]:
    usage()

# get files
in_filename = sys.argv[2]
if len(sys.argv) > 3:
    out_filename = sys.argv[3]
else:
    out_filename = os.path.splitext(in_filename)[0]
    if mode == "blf2asc":
        out_filename += ".asc"
    else:
        out_filename += ".blf"

# convert
conv = TraceConverter(mode, in_filename, out_filename)
conv.convert()