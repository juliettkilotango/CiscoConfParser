import os
import glob
import sys
import json
import confparser
import multiprocessing

if __name__ == '__main__':
#    auto = confparser.AutoDissector(raise_no_match=False)
    auto = confparser.AutoDissector()
#    dissector = confparser.Dissector.from_file('iosxr.yaml')
    auto.register(confparser.Dissector.from_file('iosxr.yaml'), 'RP/')
    auto.register(confparser.Dissector.from_file('ios.yaml'), 'version \d+.\d+$')
    pool = multiprocessing.Pool()
    result = pool.map(auto.from_file, glob.glob(os.path.join('./configs/', 'var*')), 1)
    with open('output.json', 'w') as f:
        json.dump({tree.source:tree for tree in result if tree}, f, indent=4)
