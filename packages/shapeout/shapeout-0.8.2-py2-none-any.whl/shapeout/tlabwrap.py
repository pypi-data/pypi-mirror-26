#!/usr/bin/python
# -*- coding: utf-8 -*-
"""ShapeOut - more functionalities for dclab"""
from __future__ import division, unicode_literals

import copy
import io
import os
import pkg_resources

import numpy as np

import dclab
from dclab.rtdc_dataset.fmt_tdms import get_project_name_from_path, get_tdms_files
from dclab.rtdc_dataset import config as rt_config

from . import configuration
from .meta_tool import get_event_count, get_chip_region, get_flow_rate

        
def GetTDMSTreeGUI(directories):
    """Return projects (folders) and measurements therein
    
    This is a convenience function for the GUI
    """
    if not isinstance(directories, list):
        directories = [directories]
    
    directories = np.unique(directories)
    
    pathdict = dict()
    treelist = list()
    
    for directory in directories:
        files = get_tdms_files(directory)

        #to = os.path.getctime(f)
        #t = time.strftime("%Y-%m-%d %H:%M", time.gmtime(to))
        cols = ["Measurement"]

        for f in files:
            if not IsFullMeasurement(f):
                # Ignore broken measurements
                continue
            path, name = os.path.split(f)
            # try to find the path in pathdict
            if pathdict.has_key(path):
                i = pathdict[path]
            else:
                treelist.append([])
                i = len(treelist)-1
                pathdict[path] = i
                # The first element of a tree contains the measurement name
                project = get_project_name_from_path(path)
                treelist[i].append((project, path))
            # Get data from filename
            mx = name.split("_")[0]
            chip_region = get_chip_region(f)
            dn = u"{} {}".format(mx, chip_region)
            if not chip_region.lower() in ["reservoir"]:
                # outlet (flow rate is not important)
                dn += u"  {} µls⁻¹".format(get_flow_rate(f))
            dn += "  ({} events)".format(get_event_count(f))
                                   
            treelist[i].append((dn, f))
        
    return treelist, cols


def IsFullMeasurement(fname):
    """
    Check for existence of ini files and returns False if some
    files are missing.
    """
    is_ok = True
    path, name = os.path.split(fname)
    mx = name.split("_")[0]
    stem = os.path.join(path, mx)
    
    # Check if all config files are present
    if ( (not os.path.exists(stem+"_para.ini")) or
         (not os.path.exists(stem+"_camera.ini")) or
         (not os.path.exists(fname))                ):
        is_ok = False
    
    # Check if we can perform all standard file operations
    for test in [get_chip_region, get_flow_rate, get_event_count]:
        try:
            test(fname)
        except:
            is_ok = False
            break
    return is_ok


def get_config_entry_choices(key, subkey, ignore_axes=[]):
    """Return the choices for a parameter, if any"""
    key = key.lower()
    subkey = subkey.lower()
    ignore_axes = [a.lower() for a in ignore_axes]
    ## Manually defined types:
    choices = []
    
    if key == "plotting":
        if subkey == "kde":
            choices = list(dclab.kde_methods.methods.keys())
        elif subkey in ["axis x", "axis y"]:
            choices = copy.copy(dclab.dfn.feature_names)
            # remove unwanted axes
            for choice in ignore_axes:
                if choice in choices:
                    choices.remove(choice)
        elif subkey in ["rows", "columns"]:
            choices = [ str(i) for i in range(1,6) ]
        elif subkey in ["scatter marker size"]:
            choices = [ str(i) for i in range(1,5) ]
        elif subkey.count("scale "):
            choices = ["linear", "log"]
    elif key == "analysis":
        if subkey == "regression model":
            choices = ["lmm", "glmm"]
    elif key == "calculation":
        if subkey == "emodulus model":
            choices = ["elastic sphere"]
        if subkey == "emodulus medium":
            choices = ["CellCarrier", "CellCarrier B", "Other"]
    return choices


def get_config_entry_dtype(key, subkey, refcfg=None):
    """Return dtype of the parameter as defined in dclab.cfg"""
    key = key.lower()
    subkey = subkey.lower()
    #default
    dtype = str

    ## Define dtypes and choices of cfg content
    # Iterate through cfg to determine standard dtypes
    cfg_init = cfg.copy()  
    if refcfg is None:
        refcfg = cfg_init.copy()
   
    if key in cfg_init and subkey in cfg_init[key]:
        dtype = cfg_init[key][subkey].__class__
    else:
        try:
            dtype = refcfg[key][subkey].__class__
        except KeyError:
            dtype = float

    return dtype


def GetDefaultConfiguration(key=None):
    cfg = rt_config.load_from_file(cfg_file)
    if key is not None:
        return cfg[key]
    else:
        return cfg


def GetConfigurationKeys(cfgfilename, capitalize=True):
    """
    Load the configuration file and return the list of variables
    in the order they appear.
    """
    with io.open(cfgfilename, 'r') as f:
        code = f.readlines()
    
    cfglist = list()
    
    for line in code:
        # We deal with comments and empty lines
        # We need to check line length first and then we look for
        # a hash.
        line = line.split("#")[0].strip()
        if len(line) != 0 and not (line.startswith("[") and line.endswith("]")):
            var = line.split("=", 1)[0].strip()
            cfglist.append(var)
    
    return cfglist


def SortConfigurationKeys(cfgkeys):
    """
    Sort a list of configuration keys according to the appearance in the
    ShapeOut default.cfg configuration file.
    
    If items are not present in this file, then the will be sorted according to
    the string value.
    
    This function is used to determine the displayed order of parameters in
    ShapeOut using the configuration file `default.cfg`.
    
    `cfgkeys` may be a list of tuples where the first element is the key
    or a list of keys.
    
    This method uses the global variable `cfg_ordered_list` to loookup
    in which order the data should be sorted.
    """
    orderlist = cfg_ordered_list
    
    def compare(x, y):
        """
        Compare keys for sorting.
        """
        if isinstance(x, (list, tuple)):
            x = x[0]
        if isinstance(y, (list, tuple)):
            y = y[0]
        
        if x in orderlist:
            rx = orderlist.index(x)
        else:
            rx = len(orderlist) + 1
        if y in orderlist:
            ry = orderlist.index(y)
        else:
            ry = len(orderlist) + 1
        if rx == ry:
            if x<y:
                ry += 1
            else:
                rx += 1
        return rx-ry

    return sorted(cfgkeys, cmp=compare)

## Overwrite the dclab configuration with our own.
cfg_dir = pkg_resources.resource_filename("shapeout", "cfg")
cfg_file = os.path.join(cfg_dir, "default.cfg")
cfg = rt_config.load_from_file(cfg_file)
cfg_ordered_list = GetConfigurationKeys(cfg_file)

if configuration.ConfigurationFile().get_bool("expert mode"):
    IGNORE_AXES = []
else:
    # Axes that should not be displayed  by ShapeOut
    IGNORE_AXES = ["area_cvx", "area_msd", "frame"]
