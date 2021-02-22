import os
import sys
import json
import time
import numpy as np
import pandas as pd

def pdf(frame):
    outfile = 'rts_info_' + str(int(time.time())) + '.csv'
    config_df = pd.DataFrame(frame, columns = ['Hostname', 'VRF', 'I/E', 'RT'])
    config_df.to_csv(outfile, index = False)
    print("Saved config extract to ", outfile)

def parse_xr(config):
    with open(config) as f:
        r_info = []
        data = json.load(f)
        # iterate over each configuration file in the JSON dump
        for r in data:
            # confirm we have a vrf defined, then iterate over them
            if data[r].get('vrf'):
                for v in data[r]['vrf']:
                    # confirm there is an ipv4 section, then iterate over the route targets
                    if data[r]['vrf'][v].get('ipv4'):
                        # confirm there is an import stanza
                        if data[r]['vrf'][v]['ipv4']['route-target'].get('import'):
                            for rti in data[r]['vrf'][v]['ipv4']['route-target']['import']:
                                r_data = []
                                r_data.extend((data[r]['hostname'], v, 'import', rti))
                                r_info.append(r_data)
                        # confirm there is an export stanza
                        if data[r]['vrf'][v]['ipv4']['route-target'].get('export'):
                            for rte in data[r]['vrf'][v]['ipv4']['route-target']['export']:
                                r_data = []
                                r_data.extend((data[r]['hostname'], v, 'export', rte))
                                r_info.append(r_data)
        pdf(r_info)

def parse_xe(config):
    with open(config) as f:
        r_info = []
        data = json.load(f)
        # iterate over each configuration file in the JSON dump
        for r in data:
            # confirm we have a vrf defined, then iterate over them
            if data[r].get('vrf'):
                for v in data[r]['vrf']:
                    # confirm there is an import stanza
                    if data[r]['vrf'][v].get('import'):
                        # In the case of a single RT, this is a string instead of a list
                        if type(data[r]['vrf'][v]['import']) == list:
                            for rti in data[r]['vrf'][v]['import']:
                                r_data = []
                                r_data.extend((data[r]['hostname'], v, 'import', rti))
                                r_info.append(r_data)
                        else:
                            r_data = []
                            r_data.extend((data[r]['hostname'], v, 'import', data[r]['vrf'][v]['import']))
                            r_info.append(r_data)
                    # confirm there is an export stanza
                    if data[r]['vrf'][v].get('export'):
                        # In the case of a single RT, this is a string instead of a list
                        if type(data[r]['vrf'][v]['export']) == list:
                            for rte in data[r]['vrf'][v]['export']:
                                r_data = []
                                r_data.extend((data[r]['hostname'], v, 'export', rte))
                                r_info.append(r_data)
                        else:
                            r_data = []
                            r_data.extend((data[r]['hostname'], v, 'export', data[r]['vrf'][v]['export']))
                            r_info.append(r_data)
        pdf(r_info)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        conf = input("Filename?: ")
        val = input("Processing IOS[XR] or IOS[XE] file?: ")
    else:
        conf = sys.argv[1]
        val = sys.argv[2]
    if val == 'XR':
        print("Processing IOS XR configuration file.")
        parse_xr(conf)
    elif val == 'XE':
        print("Processing IOS XE configuration file.")
        parse_xe(conf)
    else:
        print("Extraction not supported.")
