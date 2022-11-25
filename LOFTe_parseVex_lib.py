import numpy as np
from astropy import units as u

def parse_vex(vexfile,verbose=False):
    """
    This function parses an input vdif .vex file.
    
    INPUTS:
    
    vexfile : [str] .vex file name and location
    verbose : [Boolean] Option to output information for
              debugging. Default == False
    
    RETURNS:
    
    block_dict : [dict] dictionary of keys in the .vex file
                 the relevant data for each key is returned
                 as an array of strings, which requires
                 further processing to be useful.
    
    """
    
    print('Running parse_vex (verbose={0})'.format(verbose))
    
    ###################
    #Load the vex file#
    ###################
    
    #Load the vex file as an array of lines
    with open('cy13002.vex') as f:
        lines = f.readlines()
    lines = np.array(lines)
    
    ########################################
    #Extract information about the vex file#
    ########################################
    
    #get number of lines in the vex file
    n_lines = len(lines)
        
    #the string which divides data blocks
    #(Note: hard-coded based on an example vex file I had)
    divider_str = '*------------------------------------------------------------------------------\n'

    #get divides between blocks of the vex file
    block_divides = np.where(np.char.find(lines,divider_str)>=0)[0]
    print('Dividing indices: {0}\n'.format(block_divides) if verbose==True else "", end="")
    
    #get start, end indices containing the data for each block
    block_indices = [] #initialise
    
    #loop over each block divide, extract the start and end lines of the block information
    for i in range(len(block_divides)+1):
        if i==0:
            idx_start = 0
            idx_end = block_divides[0]
        elif i<=len(block_divides)-1:
            idx_start = block_divides[i-1]+1 #(+1 skips the dividing line)
            idx_end = block_divides[i]
        else:
            idx_start = block_divides[-1]+1 #(+1 skips the dividing line)
            idx_end = n_lines
        block_indices.append([idx_start,idx_end])

    print('All block start and end lines: {0}\n'.format(block_indices) if verbose==True else "", end="")
    
    #####################################################
    #create a dictionary based on the keys in the blocks#
    #####################################################
    
    block_dict = {} #initialise dictionary

    #loop over blocks
    for i in range(len(block_indices)):

        print('Block: {0}\n'.format(i) if verbose==True else "", end="")

        block_start_line = block_indices[i][0] #extract block start line
        block_end_line = block_indices[i][-1] #extract block end line

        #check whether block begins with a $ symbol, indicating
        #it is a key. The first block should not.
        if lines[block_start_line][0]!='$':
            print('Warning: Skipping block without "$" (this is probably only the first block).\n' if verbose==True else "", end="")
            pass

        #for other blocks, extract the key, store the data to dict
        else:

            #extract the key name
            key = lines[block_start_line].split('$')[-1].split(';')[0]
            print('Block key: {0}\n'.format(key) if verbose==True else "", end="")

            #store relevant data to dict entry
            block_dict[key]=lines[block_start_line+1:block_end_line]
            
    return block_dict

def get_vex_sched(block_dict,verbose=False):
    """
    This function takes the data blocks output by parse_vex()
    and extracts information for each scan in the observation
    
    INPUTS:
    
    block_dict : [data dictionary] output of parse_vex()
    
    RETURNS:
    
    scan_dict : [data dictionary] dict containing information
                about every scan of the observation in block_dict
    """
    
    print('Running get_vex_sched (verbose={0})'.format(verbose))

    #######################################################
    #Extract schedule information from the data dictionary#
    #######################################################
    
    schedule_info = block_dict['SCHED']

    #get the divider marker between scans in the schedule
    #note: it should read 'endscan;\n'
    scan_divider = schedule_info[-1]

    #get the divides between the scans
    scan_divides = np.where(np.char.find(schedule_info,scan_divider)>=0)[0]

    print('Scan indices: {0}\n'.format(scan_divides) if verbose==True else "", end="")
    
    ##########################################################
    #get start, end indices containing the data for each scan#
    ##########################################################
    
    scan_indices = [] #initialise

    #loop over each scan divide, extract the start and end lines of the scan information
    for i in range(len(scan_divides)):
        if i==0:
            idx_start = 0
            idx_end = scan_divides[0]
        elif i<=len(scan_divides):
            idx_start = scan_divides[i-1]+1 #(+1 skips the dividing line)
            idx_end = scan_divides[i]

        #append to array
        scan_indices.append([idx_start,idx_end])

    #calculate total number of scans in vex file
    n_scans = len(scan_indices)

    print('Number of scans in vex file: {0}\n'.format(n_scans) if verbose==True else "", end="")
    print('All scan start and end lines: {0}\n'.format(scan_indices) if verbose==True else "", end="")
    
    #######################################################
    #store information from each scan into data dictionary#
    #######################################################

    #initialise dict
    scan_dict = {}

    #loop over scans, extract scan numbers, store data

    #loop over scans
    print('Extracting scans...\n' if verbose==True else "", end="")
    for i in range(n_scans):

        #initialise dict for the scan
        scan_data_dict = {}

        scan_start_idx = scan_indices[i][0] #extract the idx of the first line of data for the scan
        scan_end_idx = scan_indices[i][1] #extract the idx of the last line of data for the scan

        #extract all data for the scan
        scan_data = schedule_info[scan_start_idx:scan_end_idx] 

        #extract the scan number
        scan_number_full_string = scan_data[np.where(np.char.find(scan_data,'scan No')>=0)][0]
        scan_number = scan_number_full_string.split('No')[-1].split(';')[0]
        #print(scan_number)

        #extract the scan start time, append to scan data dict
        scan_start_full_string = scan_data[np.where(np.char.find(scan_data,'start=')>=0)][0]
        scan_start = scan_start_full_string.split('start=')[1].split(';')[0]
        scan_data_dict['scan_start']=scan_start

        #print(scan_start)

        #extract the scan mode, append to scan data dict
        scan_mode_full_string = scan_data[np.where(np.char.find(scan_data,'mode=')>=0)][0]
        scan_mode = scan_mode_full_string.split('mode=')[1].split(';')[0]
        scan_data_dict['scan_mode']=scan_mode
        #print(scan_mode)

        #extract the scan source, append to scan data dict
        scan_source_full_string = scan_data[np.where(np.char.find(scan_data,'source=')>=0)][0]
        scan_source = scan_source_full_string.split('source=')[1].split(';')[0]
        scan_data_dict['scan_source']=scan_source
        #print(scan_source)

        #extract the telescopes used in the scan, append to scan data dict
        station_lines = scan_data[np.where(np.char.find(scan_data,'station=')>=0)]
        #print(station_lines)
        station_list = [] #initialise list to hold telescopes used
        for j in range(len(station_lines)): #loop over lines containing a station
            station_ID = station_lines[j].split('station=')[1].split(':')[0] #extract station ID
            station_list.append(station_ID) #append to array
        scan_data_dict['scan_stations']=station_list #append to dict
        
        #######################################################################
        #from the telescopes and mode, extract observing frequency information#
        #######################################################################
        
        #initialise arrays for bw, top, center, and bottom freqs
        bw_arr = []
        top_freq_arr = []
        bot_freq_arr = []
        cent_freq_arr = []
        
        #loop over stations in scan
        for j in range(len((station_list))):
            #extract station
            station_id = (station_list[j])
            print('Station: {0}\n'.format(station_id) if verbose==True else "", end="")

            #using the MODE key in the block_dict, find lines with observing
            #frequency information

            #define filters to extract correct information line
            filter_a = np.char.find(block_dict['MODE'],'$FREQ')>=0 #filter: must contain the line $FREQ
            filter_b = np.char.find(block_dict['MODE'],station_id)>=0 #filter: must contain the station ID

            #extract correct information line
            freq_info = block_dict['MODE'][np.where((filter_a) & (filter_b))][0]
            print('Frequency info: {0}\n'.format(freq_info) if verbose==True else "", end="")

            #get all info

            #Note: the frequency provided is the bottom frequency of the band according
            #to scheduler Justin Bray
            freq_bottom = float(freq_info.split('=')[-1].split('MHz')[0])*u.MHz
            bandwidth = float(freq_info.split('x')[-1].split('MHz')[0])*u.MHz
            freq_top = freq_bottom+bandwidth
            freq_cent = freq_bottom+(bandwidth/2)
            
            #append to arrays
            bw_arr.append(bandwidth)
            top_freq_arr.append(freq_top)
            bot_freq_arr.append(freq_bottom)
            cent_freq_arr.append(freq_cent)
            
        #append telescope frequency info to scan data dict
        scan_data_dict['station_bandwidths']=bw_arr
        scan_data_dict['station_ftops']= top_freq_arr
        scan_data_dict['station_fbots']= bot_freq_arr
        scan_data_dict['station_fcents'] = cent_freq_arr
            

        #append scan data dict to scan dict
        scan_dict[scan_number]=scan_data_dict
    
    
    return scan_dict
