# -*- coding: utf-8 -*-

import numpy as np

# %%

def blackbox2(inp):
    binlist = [1,2,4,5,6,7,8,14,15,16,17] # Binary inputs
    analist = [9,10,11,12] # Analog inputs
    p = np.zeros_like(inp)
 
    bin_lower = -1; bin_upper = 6; bin_threshold = 2.5
    for pinnum in binlist:
    # Check Binaries
        if inp[pinnum] <bin_lower or inp[pinnum] >bin_upper: p[pinnum] = -1 # Destroyed
        if inp[pinnum] >= bin_lower and inp[pinnum] <= bin_threshold: p[pinnum] = 0
        if inp[pinnum] >bin_threshold and inp[pinnum] <= bin_upper: p[pinnum] = 1
     
        # Check Binaries
    ana_lower = -1; ana_upper = 11
    for pinnum in analist:
        if inp[pinnum] < ana_lower or inp[pinnum] >ana_upper: p[pinnum] = -1 # Destroyed
        else: p[pinnum] = inp[pinnum]
         
        if -1 in p: return 0 # Destroyed
     
    # Check Vcc - GND
    if inp[0] - inp[3] < -1 or inp[0] - inp[3] > 6: return 0 # Destroyed
    if inp[0] - inp[3] >= -1 and inp[0] - inp[3] < 4: return 0 # Off
    if inp[0] - inp[3] >= 4 and inp[0] - inp[3] <= 6: # Working
    # Input 1 and 2
        if p[1] == 0: return 0
        if p[2] == 0: return 0
        if p[1] == 1 and p[2] == 1:
            if p[4] == 1: 
                tmp = p[9] * p[10]
                return tmp
            if p[5] == 1: 
                tmp = (2 * p[11]) ** 2 + 0.1*p[11] ** 3 + 0.1*p[11] ** 4 + 7
                return tmp
            if p[6] == 1:
                tmp = 14 * np.sin(p[12]) * np.exp(-2 * p[12])
                return tmp
            if p[7] == 1:
                tmp1 = (2 * p[11]) ** 2 + 0.1 * p[11] ** 3 + 0.1*p[11] ** 4 + 7
                tmp2 = 14*np.sin(p[12]) * np.exp(-2 * p[12])
                return (tmp1 + tmp2) / 2
            if p[8] == 1:
                tmp = p[14] + 2 * p[15] + 4 * p[16] + 8 * p[17]
                return tmp
            if np.sum(p[4:9]) == 0:
                return 0

# Black Box 2 pin names
black_box2_pin_names = ["Vcc", "enb1", "enb2" ,"gnd" ,"sel1" ,"sel2" ,"sel3", "sel4", "sel5", "pin 10", "pin 11", "pin 12", "pin 13", "pin 14", "pin 15", "pin 16", "pin 17", "pin18"]

# %% 

def get_data(input_arr, output_arr, scale, enb1, enb2, enb3, vcc, gnd, no_mode, sel_mode):
    input_arr = input_arr*scale
    if enb1     == 1:               input_arr[:,1]          = 5
    if enb2     == 1:               input_arr[:,2]          = 5
    if enb3     == 1:               input_arr[:,3]          = 5
    if vcc      == 1:               input_arr[:,0]          = 5
    if gnd      == 1:               input_arr[:,3]          = 0
    if no_mode  == 1:               input_arr[:,4:9]        = 0
    if sel_mode in [4,5,6,7,8,9]:   input_arr[:,sel_mode]   = 5
    output_arr = np.zeros((input_arr.shape[0],1))
    for ind in range(input_arr.shape[0]): output_arr[ind,0] = blackbox2(input_arr[ind,:])
    return input_arr, output_arr

# %%
    
# Input Selection
scale       =       5
enb1        =       0 
enb2        =       0 
enb3        =       0
vcc         =       1
gnd         =       1
no_mode     =       0
sel_mode    =       0


# %%

X = np.random.rand(1000000,18) 
y = np.zeros((X.shape[0],1))
X,y = get_data(X, y, scale, enb1, enb2, enb3, vcc, gnd, no_mode, sel_mode) # Generates Inputs - X and Outputs - Y