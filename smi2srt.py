# https://github.com/jh1104/Subtitle_Converter/blob/master/SMI_to_SRT.py


#-*- coding: utf-8 -*-
import os
import sys
import re
import datetime

def _num2time(num, format='%H:%M:%S.%f', micro2milliseconds=True):
    secs, ms = divmod(num, 1000)
    mins, s = divmod(secs, 60)
    hours, m = divmod(mins, 60)
    micros = ms * 1000
    t = datetime.time(hours, m, s, micros)    
    if not (format is None or len(format) == 0):
        t = t.strftime(format)
        if micro2milliseconds:
            t = t[:-3]
    return t

        
def _find_block(data, i=0):
    idx = i
    start_idx = None
    end_idx = len(data)
    start_time = None
    end_time = None
    while(idx < len(data)):
        if start_idx is None:
            if re.search('sync start=[0-9]+', data[idx].lower()):
                start_time = int(re.search('[0-9]+', data[idx]).group(0))
                start_idx = idx
        else:
            if re.search('sync start=[0-9]+', data[idx].lower()):
                end_time = int(re.search('[0-9]+', data[idx]).group(0))
                end_idx = idx
                break
        idx += 1            
    return start_idx, start_time, end_idx, end_time

    
def _read_block(data, start_idx, end_idx):
    fn_filter = lambda x: (len(x) > 0) and (x.lower().strip() != '&nbsp;')
    _data = list(filter(fn_filter, data[start_idx+1:end_idx]))
    return _data


def _read(lines):
    smi_data = []
    idx = 0
    while(idx < len(lines)):
        start_idx, start_time, end_idx, end_time = _find_block(lines, idx)
        if end_time is None:
            end_time = start_time + 100000
        _data = _read_block(lines, start_idx, end_idx)
        if len(_data) > 0:
            smi_data.append((start_time, end_time, _data))
        idx = end_idx
    return smi_data



def read(path_smi):
    smi_file = open(path_smi, 'br')
    data = smi_file.read()    
    # try to decode using cp949, utf-8 and utf-16
    try:
        encoding = 'cp949'
        data = data.decode(encoding)
    except:
        try:
            encoding = 'utf-8'
            data = data.decode(encoding)
        except:
            encoding = 'utf-16'
            data = data.decode(encoding, errors='ignore')
    
    data = data.replace('\r\n', '\n')
    data = data.split('\n')
            
    smi_data = []
    idx = 0
    while(idx < len(data)):
        start_idx, start_time, end_idx, end_time = _find_block(data, idx)
        if end_time is None:
            end_time = start_time + 100000
        _data = _read_block(data, start_idx, end_idx)
        if len(_data) > 0:
            smi_data.append((start_time, end_time, _data))
        idx = end_idx
    return smi_data
