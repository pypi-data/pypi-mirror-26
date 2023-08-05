import os
from collections import OrderedDict

import tifffile

from ... import Operation as opmod 
from ...Operation import Operation

class ReadImageAndHeader_SSRL15(Operation):
    """
    Read an image and header generated by beamline 1-5 at SSRL.
    Returns ndarray image and dictionary header.
    """

    def __init__(self):
        input_names = ['file_path']
        output_names = ['image_data', 'image_header', 'dir_path', 'filename']
        super(ReadImageAndHeader_SSRL15, self).__init__(input_names, output_names)
        self.input_doc['file_path'] = 'path to a tif file '\
        'produced by beamline 1-5 at SSRL. '\
        'A .txt header file is expected '\
        'in the same directory as this .tif file.'
        self.output_doc['image_data'] = 'the image pixel data as an ndarray'
        self.output_doc['image_header'] = 'the header file as a python dictionary'
        self.output_doc['dir_path'] = 'the directory portion of the input file_path'
        self.output_doc['filename'] = 'filename with path and extension stripped'

    def run(self):
        tif_path = self.inputs['file_path']
        if tif_path is None:
            return 
        dirpath,filename = os.path.split(tif_path)
        filename_noext = os.path.splitext(filename)[0]
        path_noext = os.path.splitext(tif_path)[0]
        hdr_file_path = path_noext + '.txt'
        self.outputs['dir_path'] = dirpath 
        self.outputs['filename'] = filename_noext 
        self.outputs['image_data'] = tifffile.imread(tif_path)
        d = OrderedDict()
        for l in open(hdr_file_path,'r').readlines():
            try:
                if not l.strip() == '' and not l.strip()[0] == '#':
                    kvs = l.split(',')
                    # special case for the string headers on line 1
                    if not kvs[0].find('User') == -1:
                        u_str = kvs[0].split('User:')[1].strip()
                        t_str = kvs[1].split('time:')[1].strip()
                        d['User'] = u_str
                        d['time'] = t_str
                    # and filter out the redundant temperature line
                    elif not (len(kvs)==1 and kvs[0].strip()[-1]=='C'):
                        for kv in kvs:
                            kv_arr = kv.split('=')
                            d[kv_arr[0].strip()] = float(kv_arr[1].strip())
                self.outputs['image_header'] = d
            except Exception as e:
                d['ERROR'] = e.message
                self.outputs['image_header'] = d
                raise e

