#coding:utf8
import json
import six
import pandas as pd
from collections import defaultdict

def get_data_from_dict(data, result=None):
    #如果key不存在，则设置为空
    for key in data:
        if key not in result:
            #如果一个key都不存在着直接加入一个key,否则选择第一个key的长度
            if not result.keys():
                result[key] = []
            else:
                result[key] = len(result[result.keys()[0]])*[""]
    #然后分别加入值
    for key in result:
        if key in data:
            result[key].append(data[key])
        else:
            result[key].append("")
    return result

def get_all_child(father_dict, spread_dict=None):
    '''将所有dict展开'''
    if spread_dict == None:
        spread_dict = {}
    for key in father_dict:
        if isinstance(father_dict[key], dict):
            spread_dict = get_all_child(father_dict[key], spread_dict)
        else:
            spread_dict[key] = father_dict[key]
    return spread_dict

def conversion(filename,outpath):
    with open(filename,"r") as fr:
        result = defaultdict(list)
        for line in fr:
            linedata = json.loads(line)
            spread_data = get_all_child(linedata)
            result = get_data_from_dict(spread_data, result)
        data = pd.DataFrame(result)
        data.to_excel(outpath,encoding="utf8")

if __name__ == "__main__":
    conversion(u"安居客新房0606.json", u"安居客.xls")
