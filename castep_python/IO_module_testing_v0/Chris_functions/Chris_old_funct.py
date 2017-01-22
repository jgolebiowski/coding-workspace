#!/usr/bin/python

#import config

#****************************************************************************

class MaxError(Exception): pass

class CheckError(Exception): pass

class MemError(Exception): pass

#****************************************************************************

# Make the values of all common parameters global variables and print to screen
def checkparam(chem):
    global kpoints
    global offset
    global cutoff_Energy
    global taskEnergy
    global spin
    global functional
    global cell_constraints
    global sedc
    global c
    global a
    global charge
    global spectral_task
    
    # Checking .cell parameters e.g. kpoints, kpoints-offset
    cell_check = open('%s.cell' % chem,'r')
    lines_cell_check = cell_check.readlines()
    
    for line in lines_cell_check:
        if 'KPOINTS_MP_GRID' in line and 'SPECTRAL' not in line and 'bs' not in line:
            kpoints = [line.split()[1],line.split()[2],line.split()[3]]
            kpoints_spacing = 0
        elif 'kpoint_mp_grid' in line and 'spectral' not in line and 'bs' not in line:
            kpoints = [line.split()[1],line.split()[2],line.split()[3]]
            kpoints_spacing = 0
        elif 'kpoint_mp_spacing' in line and 'spectral' not in line and 'bs' not in line:
            kpoints = [0,0,0]
            kpoints_spacing = line.split()[1]
            
    for line in lines_cell_check:
        if 'kpoint_mp_offset' in line and 'spectral' not in line and 'bs' not in line:
            offset = [line.split()[1],line.split()[2],line.split()[3]]

    cell_check.seek(0,0)
    for num, line in enumerate(cell_check):
        if '%BLOCK CELL_CONSTRAINTS' in line:
            l = num
    cell_constraints = [lines_cell_check[l+1].split()[0], lines_cell_check[l+1].split()[1], lines_cell_check[l+1].split()[2], lines_cell_check[l+2].split()[0], lines_cell_check[l+2].split()[1], lines_cell_check[l+2].split()[2]]
    
    a = str(lines_cell_check[1].split()[0])

    c = str(lines_cell_check[3].split()[2])
    
    # Checking .param parameters e.g. task, cutoff_Energy, xc_functional
    param_check = open('%s.param' %chem,'r')
    lines_param_check = param_check.readlines()
    
    for line in lines_param_check:
        if 'task :' in line and 'SPECTRAL' not in line:
            task = line.split()[2]
        elif 'TASK :' in line and 'spectral' not in line:
            task = line.split()[2]
            
    for line in lines_param_check:
        if 'cut_off_energy' in line:
            cutoff_Energy = line.split()[2]
        elif 'basis_precision' in line:
            cutoff_Energy = line.split()[2]
        elif 'CUT_OFF_ENERGY' in line:
            cutoff_Energy = line.split()[2]
        elif 'BASIS_PRECISION' in line:
            cutoff_Energy = line.split()[2]

    for line in lines_param_check:
        if 'xc_functional' in line:
            functional = line.split()[2]
        elif 'XC_FUNCTIONAL' in line:
            functional = line.split()[2]

    for line in lines_param_check:
        if 'continuation' in line:
            continuation = line.split()[2]

    spin = str(0)                    
    for line in lines_param_check:
        if 'spin :' in line:
            spin = line.split()[2]
        elif 'spin_polarised : false' in line:
            spin = str(0)

    for line in lines_param_check:
        if 'sedc_scheme :' in line:
            sedc = line.split()[2]
        elif 'sedc_apply : false' in line:
            sedc = 'none'

    for line in lines_param_check:
        if 'charge :' in line:
            charge = line.split()[2]

    if task == 'spectral':
        for line in lines_param_check:
            if 'spectral_task:' in line:
                spectral_task = line.split()[1]
    else:
        spectral_task = 'none'

    for line in lines_param_check:
        if 'nextra_bands :' in line and 'spectral' not in line:
            nextra_bands = line.split()[2]

    for line in lines_param_check:
        if 'spectral_nextra_bands :' in line:
            spectral_nextra_bands = line.split()[2]

    # Print to screen of user
    print 'task : ' + task + ', functional : ' + functional + ', cut off Energy : ' + cutoff_Energy + ', kpoints : ' + str(kpoints[0]) + ' ' +  str(kpoints[1]) + ' ' + str(kpoints[2]) + ', kpoint spacing: ' + str(kpoints_spacing) +  ', offset : ' + str(offset[0]) + ' ' +  str(offset[1]) + ' ' +  str(offset[2]) + ', spin : ' + spin + ', sedc : ' + sedc + ', a : ' + str(a) + ', c : ' + str(c) + ',  cell contraints : a = ' + str(cell_constraints[0]) + ' b = ' + str(cell_constraints[1]) + ' c = ' + str(cell_constraints[2]) + ' alpha = ' + str(cell_constraints[3]) + ' beta = ' + str(cell_constraints[4]) + ' gamma = ' + str(cell_constraints[5]) + ' charge = ' + charge + ' spectral task = ' + spectral_task + ' number of extra bands in SCF calculation = ' + nextra_bands + ' number of extra bands in CORE EELS calculation  = ' + spectral_nextra_bands + ' continuation = ' + continuation

    # Update global variables in config module
    config.kpoints              = kpoints
    config.kpoints_spacing      = kpoints_spacing
    config.offset               = offset
    config.cutoff_Energy        = cutoff_Energy
    config.task                 = task
    config.spin                 = spin
    config.functional           = functional
    config.cell_constraints     = cell_constraints
    config.sedc                 = sedc
    config.c                    = c
    config.a                    = a
    config.charge               = charge
    config.spectral_task        = spectral_task
    config.nextra_bands         = nextra_bands
    config.spectral_nextra_bands = spectral_nextra_bands
    return

#****************************************************************************

# Change Geometry dependence in CORE EELS calculation
def ch_core_geom(chem, geom):
    f = open('%s.odi' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'CORE_GEOM' in line:
            l = num
    lines_f[l]    = 'CORE_GEOM          : ' + geom + '  # Default\n'
    f = open('%s.odi' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'Core geometry changed to: ' + str(geom)
    config.core_geom = geom
    if geom == 'polycrystalline':
        ch_e_beam_vector(chem, [0,0,0])
    return

#****************************************************************************

# Change electron beam vector in EELS calculation
def ch_e_beam_vector(chem, e_vector,spect_task='core'):
    vector = [float(e_vector[0]),float(e_vector[1]),float(e_vector[2])]
    f = open('%s.odi' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if spect_task + '_qdir' in line:
            l = num
    if vector == [0,0,0]:
        lines_f[l]    = '#' + spect_task + '_qdir          : ' + str(dp(vector[0],3)) + ' ' + str(dp(vector[1],3)) + ' ' + str(dp(vector[2],3)) + '\n'
    else:
        lines_f[l]    = spect_task + '_qdir          : ' + str(dp(vector[0],3)) + ' ' + str(dp(vector[1],3)) + ' ' + str(dp(vector[2],3)) + '\n'
    f = open('%s.odi' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'Electron beam vector for ' + spect_task + ' EELS calculation changed to: ' + str(dp(vector[0],3)) + ' ' + str(dp(vector[1],3)) + ' ' + str(dp(vector[2],3))
    config.e_vector = vector
    return

#****************************************************************************

# Change cutoff_Energy in .param file
def ch_cutoff_Energy( chem, cutoff_Energy_temp ):
    global cutoff_Energy
    cutoff_Energy = str(cutoff_Energy_temp)
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'cut_off_energy' in line:
            l = num
    lines_f[l]    = 'cut_off_energy : ' + str(cutoff_Energy_temp) + ' eV\n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'cutoff_Energy changed to: ' + str(cutoff_Energy_temp) + ' eV'
    config.cutoff_Energy = cutoff_Energy
    return

#****************************************************************************

# Change kpoints in .cell file, if kpoints in c direction = 0 then those in .cell file are left unchanged
def ch_kpoints( chem, kpoints_temp, hexag=1):
    global kpoints
    f = open('%s.cell' % chem,'r')   
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'kpoint_mp_grid' in line and 'spectral' not in line and 'bs' not in line:
            l = num
            kpoints_z = lines_f[l].split()[3]
        elif 'kpoint_mp_spacing' in line and 'spectral' not in line:
            l = num
            kpoints_z = 1
    if int(kpoints_temp[2]) == 0:
        lines_f[l]    = 'kpoint_mp_grid ' + str(kpoints_temp[0]) + ' ' + str(kpoints_temp[1]) + ' ' + str(kpoints_z) + ' \n'
        kpoints       = [str(kpoints_temp[0]), str(kpoints_temp[1]), str(kpoints_z)]
    else:
        lines_f[l]    = 'kpoint_mp_grid ' + str(kpoints_temp[0]) + ' ' + str(kpoints_temp[1]) + ' ' + str(kpoints_temp[2]) + ' \n'
        kpoints = [str(kpoints_temp[0]), str(kpoints_temp[1]), str(kpoints_temp[2])]
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    if int(kpoints_temp[2]) == 0:
        print 'kpoints changed to: ' + str(kpoints_temp[0]) + ' ' + str(kpoints_temp[1]) + ' ' + str(kpoints_z)
    else:
        print 'kpoints changed to: ' + str(kpoints_temp[0]) + ' ' + str(kpoints_temp[1]) + ' ' + str(kpoints_temp[2])
    config.kpoints = kpoints
    
    # Update kpoint offset accordingly
    if hexag == 1:
        calc_offset(kpoints)
        ch_offset(chem, offset)
    else:
        ch_offset(chem, [0,0,0])
    return

#****************************************************************************

# Change kpoint spacing
def ch_kpoints_spacing( chem, kpoints_spacing_temp, hexag=1):
    global kpoints_spacing
    kpoints_spacing = kpoints_spacing_temp
    f = open('%s.cell' % chem,'r')   
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'kpoint_mp_grid' in line and 'spectral' not in line:
            l = num
        elif 'kpoint_mp_spacing' in line and 'spectral' not in line:
            l = num
    lines_f[l]    = 'kpoint_mp_spacing ' + str(kpoints_spacing) + ' \n' 
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'kpoint spacing changed to: ' + str(kpoints_spacing)
    print 'WARNING: kpoint offset has NOT been changed automatically, please update the offset manually for a gamma centred MP kpoint grid'
    config.kpoints_spacing = kpoints_spacing
    return

#****************************************************************************

# Change kpoint spacing
def ch_spectral_kpoints_spacing( chem, spectral_kpoints_spacing_temp ):
    global spectral_kpoints_spacing
    spectral_kpoints_spacing = spectral_kpoints_spacing_temp
    f = open('%s.cell' % chem,'r')   
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_kpoint_mp_grid' in line:
            l = num
        elif 'spectral_kpoint_mp_spacing' in line:
            l = num
    lines_f[l]    = 'spectral_kpoint_mp_spacing ' + str(spectral_kpoints_spacing) + ' \n' 
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'spectral kpoint spacing changed to: ' + str(spectral_kpoints_spacing)
    print 'WARNING: kpoint offset has NOT been changed automatically, please update the offset manually for a gamma centred MP kpoint grid'
    config.spectral_kpoints_spacing = spectral_kpoints_spacing
    return

#****************************************************************************

# Change kpoint spacing
def ch_bs_kpoints_spacing( chem, bs_kpoints_spacing_temp ):
    global bs_kpoints_spacing
    bs_kpoints_spacing = bs_kpoints_spacing_temp
    f = open('%s.cell' % chem,'r')   
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'bs_kpoint_mp_grid' in line:
            l = num
        elif 'bs_kpoint_mp_spacing' in line:
            l = num
    lines_f[l]    = 'bs_kpoint_mp_spacing ' + str(bs_kpoints_spacing) + ' \n' 
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'bs kpoint spacing changed to: ' + str(bs_kpoints_spacing)
    print 'WARNING: kpoint offset has NOT been changed automatically, please update the offset manually for a gamma centred MP kpoint grid'
    config.bs_kpoints_spacing = bs_kpoints_spacing
    return

#****************************************************************************

# Change spectral kpoints in .cell file, if spectral kpoints in c direction = 0 then those in .cell file are left unchanged
def ch_spectral_kpoints( chem, spectral_kpoints_temp, hexag=1):
    global spectral_kpoints
    f = open('%s.cell' % chem,'r')   
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_kpoint_mp_grid' in line or 'bs_kpoint_mp_grid' in line:
            l = num
            spectral_kpoints_z = lines_f[l].split()[3]
        elif 'spectral_kpoint_mp_spacing' in line or 'bs_kpoint_mp_spacing':
            l = num
            spectral_kpoints_z = 1
    if int(spectral_kpoints_temp[2]) == 0:
        lines_f[l]       = 'spectral_kpoint_mp_grid ' + str(spectral_kpoints_temp[0]) + ' ' + str(spectral_kpoints_temp[1]) + ' ' + str(spectral_kpoints_z) + ' \n'
        spectral_kpoints = [str(spectral_kpoints_temp[0]), str(spectral_kpoints_temp[1]), str(spectral_kpoints_z)]
    else:
        lines_f[l]       = 'spectral_kpoint_mp_grid ' + str(spectral_kpoints_temp[0]) + ' ' + str(spectral_kpoints_temp[1]) + ' ' + str(spectral_kpoints_temp[2]) + ' \n'
        spectral_kpoints = [str(spectral_kpoints_temp[0]), str(spectral_kpoints_temp[1]), str(spectral_kpoints_temp[2])]
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    if int(spectral_kpoints_temp[2]) == 0:
        print 'spectral_kpoints changed to: ' + str(spectral_kpoints_temp[0]) + ' ' + str(spectral_kpoints_temp[1]) + ' ' + str(spectral_kpoints_z)
    else:
        print 'spectral_kpoints changed to: ' + str(spectral_kpoints_temp[0]) + ' ' + str(spectral_kpoints_temp[1]) + ' ' + str(spectral_kpoints_temp[2])
    config.spectral_kpoints = spectral_kpoints

    # Update spectral kpoint offset accordingly
    if hexag == 1:
        calc_offset(spectral_kpoints)
        ch_spectral_offset(chem, offset)
    else:
        ch_spectral_offset(chem, [0,0,0])
    return

#****************************************************************************

# Change bs kpoints in .cell file, if bs kpoints in c direction = 0 then those in .cell file are left unchanged
def ch_bs_kpoints( chem, bs_kpoints_temp, hexag=1):
    global bs_kpoints
    f = open('%s.cell' % chem,'r')   
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_kpoint_mp_grid' in line or 'bs_kpoint_mp_grid' in line:
            l = num
            bs_kpoints_z = lines_f[l].split()[3]
        elif 'spectral_kpoint_mp_spacing' in line or 'bs_kpoint_mp_spacing':
            l = num
            bs_kpoints_z = 1
    if int(bs_kpoints_temp[2]) == 0:
        lines_f[l]       = 'bs_kpoint_mp_grid ' + str(bs_kpoints_temp[0]) + ' ' + str(bs_kpoints_temp[1]) + ' ' + str(bs_kpoints_z) + ' \n'
        bs_kpoints = [str(bs_kpoints_temp[0]), str(bs_kpoints_temp[1]), str(bs_kpoints_z)]
    else:
        lines_f[l]       = 'bs_kpoint_mp_grid ' + str(bs_kpoints_temp[0]) + ' ' + str(bs_kpoints_temp[1]) + ' ' + str(bs_kpoints_temp[2]) + ' \n'
        bs_kpoints = [str(bs_kpoints_temp[0]), str(bs_kpoints_temp[1]), str(bs_kpoints_temp[2])]
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    if int(bs_kpoints_temp[2]) == 0:
        print 'bs_kpoints changed to: ' + str(bs_kpoints_temp[0]) + ' ' + str(bs_kpoints_temp[1]) + ' ' + str(bs_kpoints_z)
    else:
        print 'bs_kpoints changed to: ' + str(bs_kpoints_temp[0]) + ' ' + str(bs_kpoints_temp[1]) + ' ' + str(bs_kpoints_temp[2])
    config.bs_kpoints = bs_kpoints

    # Update bs kpoint offset accordingly
    if hexag == 1:
        calc_offset(bs_kpoints)
        ch_bs_offset(chem, offset)
    else:
        ch_bs_offset(chem, [0,0,0])
    return

#****************************************************************************

# Change offset in .cell file
def ch_offset( chem, offset_temp ):
    global offset
    offset = [str(offset_temp[0]), str(offset_temp[1]), str(offset_temp[2])]
    f = open('%s.cell' % chem,'r')      
    lines_f  = f.readlines()
    f.seek(0,0)
    l = 0
    for num, line in enumerate(f):
        if 'kpoint_mp_offset' in line and 'spectral' not in line and 'bs' not in line:
            l = num
    if l != 0:
        lines_f[l]    = 'kpoint_mp_offset ' + str(offset_temp[0]) + ' ' + str(offset_temp[1]) + ' ' + str(offset_temp[2]) + ' \n'
    else:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'kpoint' in line:
                l = num
        lines_f.insert(l+1,'kpoint_mp_offset ' + str(offset_temp[0]) + ' ' + str(offset_temp[1]) + ' ' + str(offset_temp[2]) + ' \n')
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'kpoint offset changed to: ' + str(offset_temp[0]) + ' ' + str(offset_temp[1]) + ' ' + str(offset_temp[2])
    config.offset = offset
    return

#****************************************************************************

# Change spectral offset in .cell file
def ch_spectral_offset( chem, spectral_offset_temp ):
    global spectral_offset
    spectral_offset = [str(spectral_offset_temp[0]), str(spectral_offset_temp[1]), str(spectral_offset_temp[2])]
    f = open('%s.cell' % chem,'r')      
    lines_f  = f.readlines()
    f.seek(0,0)
    l = 0
    for num, line in enumerate(f):
        if 'spectral_kpoint_mp_offset' in line or 'bs_kpoint_mp_offset' in line:
            l = num
    if l != 0:
        lines_f[l]    = 'spectral_kpoint_mp_offset ' + str(spectral_offset_temp[0]) + ' ' + str(spectral_offset_temp[1]) + ' ' + str(spectral_offset_temp[2]) + ' \n'
    else:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'kpoint' in line:
                l = num
        lines_f.insert(l+1, 'spectral_kpoint_mp_offset ' + str(spectral_offset_temp[0]) + ' ' + str(spectral_offset_temp[1]) + ' ' + str(spectral_offset_temp[2]) + ' \n')
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'spectral kpoint offset changed to: ' + str(spectral_offset_temp[0]) + ' ' + str(spectral_offset_temp[1]) + ' ' + str(spectral_offset_temp[2])
    config.spectral_offset = spectral_offset
    return

#****************************************************************************

# Change bandstructure offset in .cell file
def ch_bs_offset( chem, bs_offset_temp ):
    global bs_offset
    bs_offset = [str(bs_offset_temp[0]), str(bs_offset_temp[1]), str(bs_offset_temp[2])]
    f = open('%s.cell' % chem,'r')      
    lines_f  = f.readlines()
    f.seek(0,0)
    l = 0
    for num, line in enumerate(f):
        if 'spectral_kpoint_mp_offset' in line or 'bs_kpoint_mp_offset' in line:
            l = num
    if l != 0:
        lines_f[l]    = 'bs_kpoint_mp_offset ' + str(bs_offset_temp[0]) + ' ' + str(bs_offset_temp[1]) + ' ' + str(bs_offset_temp[2]) + ' \n'
    else:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'kpoint' in line:
                l = num
        lines_f.insert(l+1, 'bs_kpoint_mp_offset ' + str(bs_offset_temp[0]) + ' ' + str(bs_offset_temp[1]) + ' ' + str(bs_offset_temp[2]) + ' \n')
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'bs kpoint offset changed to: ' + str(bs_offset_temp[0]) + ' ' + str(bs_offset_temp[1]) + ' ' + str(bs_offset_temp[2])
    config.bs_offset = bs_offset
    return

#****************************************************************************

# Run a castep dryrun and automatically adjust all kpoint offsets for the number of kpoints generated
# Also update config with numbers of kpoints calculated and kpoint grid in the calculation
def auto_offset(chem, cores, hexag=1):

    # If running a script on kittel, don't run any dryrun calculations
    host_comp()
    if 'kittel' in config.computer or 'ironman' in config.computer:
        print '***** Not running dryrun calculation on kittel, it is a waste of queing time, carrying on calculation without adjusting offsets *****'

    else:
        
        # Run a dryrun calculation whatever the symmetry because it might be required by the script to check numbers of kpoints
        castep_parallel(chem, cores, test=1)
        no_kpoints = get_no_kpoints(chem + '.castep')
        k_grid = get_kpoint_grid(chem + '.castep')
        config.kpoints = k_grid
        config.no_kpoints = no_kpoints

        # If hexagonal symmetry see what mp kpoint grid is generated by the kpoint spacing given and update the offset accordingly
        if hexag == 1:
            calc_offset(k_grid)
            ch_offset(chem, config.offset)

        # Non-hexagonal symmetries shouldn't require an offset
        else:
            ch_offset(chem, [0, 0, 0])

        # Open the .cell file
        f = open('%s.cell' % chem,'r')
        lines_f  = f.readlines()
        spectral_kpoint_spacing = 0
        bs_kpoint_spacing = 0
        kpoint_spacing = 0

        # Note the kpoint spacing and update config
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'kpoint_mp_spacing' in line and 'spectral' not in line and 'bs' not in line:
                l = num
                kpoint_spacing = float(lines_f[l].split()[1])
                config.kpoints_spacing = kpoint_spacing

        # Note the spectral kpoint spacing and update config
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'spectral_kpoint_mp_spacing' in line:
                l = num
                spectral_kpoint_spacing = float(lines_f[l].split()[1])
                config.spectral_kpoints_spacing = spectral_kpoint_spacing

        # Note the bandstructure kpoint spacing and update config
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'bs_kpoint_mp_spacing' in line:
                l = num
                bs_kpoint_spacing = float(lines_f[l].split()[1])
                config.bs_kpoints_spacing = bs_kpoint_spacing

        # If a spectral kpoint spacing is given, update the spectral kpoint offset according to symmetry, running a dry run if necessary
        # Be sure to correct the kpoint spacing after the dry run
        if spectral_kpoint_spacing != 0:
            ch_kpoints_spacing(chem, spectral_kpoint_spacing)
            castep_parallel(chem, cores, test=1)
            no_spect_kpoints = get_no_kpoints(chem + '.castep')
            spect_k_grid = get_kpoint_grid(chem + '.castep')
            config.spectral_kpoints = spect_k_grid
            config.no_spect_kpoints = no_spect_kpoints
            ch_kpoints_spacing(chem, kpoint_spacing)
            if hexag == 1:
                calc_offset(spect_k_grid)
                ch_spectral_offset(chem, config.offset)
            else:
                ch_spectral_offset(chem, [0, 0, 0])

        # If a spectral kpoint spacing is given, update the spectral kpoint offset according to symmetry, running a dry run if necessary
        # Be sure to correct the kpoint spacing after the dry run
        if bs_kpoint_spacing != 0:
            ch_kpoints_spacing(chem, bs_kpoint_spacing)
            castep_parallel(chem, cores, test=1)
            no_bs_kpoints = get_no_kpoints(chem + '.castep')
            bs_k_grid = get_kpoint_grid(chem + '.castep')
            config.bs_kpoints = bs_k_grid
            config.no_bs_kpoints = no_bs_kpoints
            ch_kpoints_spacing(chem, kpoint_spacing)
            if hexag == 1:
                calc_offset(bs_k_grid)
                ch_bs_offset(chem, config.offset)
            else:
                ch_bs_offset(chem, [0, 0, 0])

        print 'all kpoint offsets updated according to the symmetry present and kpoint grid generated by the kpoint spacings in the .cell file'
    
    return

#****************************************************************************

# Change functional in .param file
def ch_functional( chem, functional_temp ):
    global functional
    functional = functional_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'xc_functional' in line:
            l = num
    lines_f[l]    = 'xc_functional : ' + functional_temp + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'xc_functional changed to: ' +  functional_temp
    config.functional = functional
    return

#****************************************************************************

# Change functional in .param file
def ch_continuation( chem, continuation_temp ):
    global continuation
    continuation = continuation_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    if 'continuation' in f.read():
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'continuation' in line:
                l = num
        del lines_f[l]
        f = open('%s.param' % chem,'w')
        f.writelines( lines_f )
        f.close()
        f = open('%s.param' % chem,'r')
        lines_f  = f.readlines()
    f.seek(0,0)
    if continuation_temp != 'none':
        lines_f.insert(2,'continuation : ' + continuation_temp + ' \n')
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'continuation changed to: ' +  continuation_temp
    return

#****************************************************************************

# Change optimisation strategy in .param file
def ch_opt_strategy( chem, opt_strategy ):
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'opt_strategy' in line:
            l = num
    lines_f[l]    =  'opt_strategy : ' + opt_strategy + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'opt_strategy changed to: ' + opt_strategy
    return

#****************************************************************************

# Change force tolerance in .param file
def ch_force_tol( chem, force_tol_temp ):
    global force_tol
    force_tol = force_tol_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'geom_force_tol' in line:
            l = num
    lines_f[l]    = 'geom_force_tol : ' + str(force_tol_temp) + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'force tolerance changed to: ' + str(force_tol_temp)
    config.force_tol = force_tol
    return

#****************************************************************************

# Change force tolerance in .param file
def ch_geom_energy_tol( chem, geom_energy_tol_temp ):
    global geom_energy_tol
    geom_energy_tol = geom_energy_tol_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'geom_energy_tol' in line:
            l = num
    lines_f[l]    = 'geom_energy_tol : ' + str(geom_energy_tol_temp) + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'geom_energy tolerance changed to: ' + str(geom_energy_tol_temp)
    config.geom_energy_tol = geom_energy_tol
    return

#****************************************************************************

# Change energy tolerance for the SCF part of the calculation in .param file
def ch_SCF_energy_tol(chem, SCF_energy_tol_temp):
    global SCF_energy_tol
    SCF_energy_tol = SCF_energy_tol_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'elec_energy_tol' in line:
            l = num
    lines_f[l]    = 'elec_energy_tol : ' + str(SCF_energy_tol_temp) + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'SCF energy tolerance changed to: ' + str(SCF_energy_tol_temp)
    config.SCF_energy_tol = SCF_energy_tol
    return

#****************************************************************************

# Change maxium geometry iterations in geometry optimisation
def ch_max_BFGS( chem, BFGS ):
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'geom_max_iter' in line:
            l = num
    lines_f[l]    = 'geom_max_iter : ' + str(BFGS) + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'maximum number of geometry optimisation iterations changed to: ' + str(BFGS)
    return

#****************************************************************************

# Change whether the material is treated as an insulator
def ch_fix_occupancy( chem, fix_occ_temp ):
    global fix_occ
    fix_occ = fix_occ_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'fix_occupancy' in line:
            l = num
    lines_f[l]    = 'fix_occupancy : ' + fix_occ + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'fix_occupancy changed to: ' + str(fix_occ)
    config.fix_occ = fix_occ
    return

#****************************************************************************

# Change the percentage of nextra bands
def ch_perc_nextra_bands_spect( chem, perc_spect_nbands ):
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_perc_extra_bands :' in line:
            l = num
    lines_f[l]    = 'spectral_perc_extra_bands : ' + str(perc_spect_nbands) + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'percentage spectral extra bands updated to ' + str(perc_spect_nbands)
    return

#****************************************************************************

# Change the percentage of nextra bands
def ch_perc_nextra_bands( chem, perc_nbands_temp, perc_spect_nbands_temp ):
    global perc_nbands
    global perc_spect_nbands
    perc_nbands = perc_nbands_temp
    perc_spect_nbands = perc_spect_nbands_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()

    # Remove all extra bands info if already present
    f.seek(0,0)
    lines_del = []
    
    # Record the lines which refer to extra bands (there may be a number of them)
    for num, line in enumerate(f):
        if 'extra_bands' in line:
            lines_del.append(num)

    # Now delete these lines in REVERSE ORDER to how they appear in the .param file (so not as to mess up the ordering)
    for l_d in reversed(lines_del):
        del lines_f[l_d]

    # NOW PRINT THE CHANGES TO FILE AND REREAD THE FILE!
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()    
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()

    # Update both sets of percentage extra bands, providing extra bands are desired
    f.seek(0,0)
    if perc_nbands_temp != 'none':
        lines_f.insert(4, 'perc_extra_bands : ' + str(perc_nbands) + '\n')
        lines_f.insert(4, 'spectral_perc_extra_bands : ' + str(perc_spect_nbands) + '\n')

    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'percentage extra bands updated to ' + str(perc_nbands) + ' and percentage spectral extra bands updated to ' + str(perc_spect_nbands)
    config.perc_nbands = perc_nbands
    config.perc_spect_nbands = perc_spect_nbands
    
    #if perc_nbands_temp != 'none':
    #    ch_fix_occupancy(chem, 'false')
    #elif perc_nbands_temp == 'none':
    #    ch_fix_occupancy(chem, 'true')
    return

#****************************************************************************

# Change task in .param file
def ch_task( chem, task_temp ):
    global task
    task = task_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()

    # Remove DOS info if already present
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'pdos_calculate_weights' in line:
            del lines_f[num]

    # NOW PRINT THE CHANGES TO FILE AND REREAD THE FILE!
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()    
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()

    # Remove more DOS info if already present
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_task' in line:
            del lines_f[num]

    # NOW PRINT THE CHANGES TO FILE AND REREAD THE FILE!
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()    
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()

    # Replace task
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'task :' in line or 'task                 :' in line:
            l = num
    lines_f[l]    = 'task : ' + task_temp + ' \n'

    # Add in additional DOS info if needed
    if task_temp == 'spectral':
        f.seek(0,0)
        lines_f.insert(4, 'spectral_task: DOS \n')
        lines_f.insert(4, 'pdos_calculate_weights : TRUE\n')

    # Now able to rewrite the entire file since no problems with index
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'task changed to: ' +  task_temp
    config.task = task
    return

#****************************************************************************

# Change spectral task (note this will only work if the task is set to spectral)
def ch_spectral_task(chem,spectral_task_temp):
    global task
    task = task_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()

    # Change the spectral task in the .param file
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_task' in line:
            l = num
    lines_f[l]    = 'spectral_task:' + spectral_task_temp + ' \n'

    # Now able to rewrite the entire file since no problems with index
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'spectral task changed to: ' +  spectral_task_temp
    config.spectral_task = spectral_task
    return

#****************************************************************************

# Run castep
def castep(chem, test=0):
    import os
    castep_cleanup(chem)
    if test == 0:
        print 'starting castep calculation'
        os.system("/home/ablitt/bin/castep %s" % chem)
    else:
        print 'starting castep calculation in dryrun (test) mode'
        os.system("/home/ablitt/bin/castep %s -dryrun" % chem)
    print 'castep calulation complete'
    return

#****************************************************************************

def check_cores(computer, cores):
    too_many = 0
    wrong_multiple = 0

    if 'scarlet' == computer:
        if cores > 8:
            too_many = 1
    elif 'rabi' in computer:
        if cores > 12:
            too_many = 1
    elif 'zener' in computer:
        if cores > 8:
            too_many = 1
        elif cores/8 != float(cores)/8:
            wrong_multiple = 1
    elif 'kittel' in computer:
        if cores/8 != float(cores)/8:
            wrong_multiple = 1
    elif 'ironman' in computer:                    # Only if running in parallel.q but like Chris suggested use multiples of 24 cores to be safe 
        if cores/8 != float(cores)/8:
            wrong_multiple = 1

    if too_many == 1:
        print '\n\n******* WARNING: NUMBER OF CORES USED HAS EXCEEDED THE NUMBER AVAILABLE FOR THE MACHINE ******\n\n'
        send_email('Incorrect number of cores on ' + computer,'\n\n******* WARNING: NUMBER OF CORES USED HAS EXCEEDED THE NUMBER AVAILABLE FOR THE MACHINE ******\n\n Consider aborting the process and restarting with the correct number of cores immediately!')
    elif wrong_multiple == 1:
        print '\n\n******* WARNING: NUMBER OF CORES USED IS NOT A MULTIPLE OF THOSE AVAILABLE ON EACH NODE ******\n\n'
        send_email('Incorrect number of cores on ' + computer,'\n\n******* WARNING: NUMBER OF CORES USED IS NOT A MULTIPLE OF THOSE AVAILABLE ON EACH NODE ******\n\n Consider aborting the process and restarting with the correct number of cores immediately!')

    return

#****************************************************************************

# Run castep in parallel
def castep_parallel( chem, cores, test=0, cont=0, queue='parallel.q', mem_alloc='default',time_lim='default', pypid=0, cleanup=0):

    if cont == 1:
        ch_continuation(chem,'default')

    # Check if run is a continuation
    if cleanup==1:
        castep_cleanup(chem)
    host_comp()

    check_cores(config.computer, cores)

    import subprocess
    import time

    # For jobs on scarlet or rabi (straightforward!)
    if 'scarlet' == computer or 'rabi' in computer:
        
        procpid = 1

        # Set commands for what job to run
        print 'castep starting running in parallel on ' + config.computer + ' using ' + str(cores) + ' cores at ' + print_time()
        if 'scarlet' == computer:
            if test==0:
                cmd =  ['mpirun','-np',str(cores),'/home/ablitt/bin/castep.parallel',chem]
            else:
                cmd = ['mpirun','-np',str(cores),'/home/ablitt/bin/castep.parallel',chem,'-dryrun']
                print 'running castep in dryrun (test) mode'
        elif 'rabi' in computer:
            if test==0:
                cmd = ['mpirun','-np',str(cores),'castep.mpi',chem]
            else:
                cmd = ['mpirun','-np',str(cores),'castep.mpi',chem,'-dryrun']
                print 'running castep in dryrun (test) mode'
                
        # Start running the job
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
        # Monitor the running of the calculation
        ended = 0
        cas = 0
        start_time = time.time()
        loc_start = time.localtime()
        total_mem = '0'
        while ended < 1:
            
            # Check that the calculation output file (i.e. the .castep file) is being altered
            while cas < 1:
                try:
                    g = open(chem + '.castep','r')
                    filename = chem+'.castep'
                    output = subprocess.Popen( ['ls','-l',filename],stdout=subprocess.PIPE).communicate()[0]
                    cas_time = output.split()[5] + ' ' + output.split()[6] + ' ' + output.split()[7] + ' 2014'
                    if time.strptime(cas_time, "%b %d %H:%M %Y") > loc_start:
                        print 'Now printing output to Castep output file ' + chem + '.castep'
                        cas = 1
                    else:
                        break
                except IOError:
                    break
                
            # Print the memory requirements by different parts of the calculation (for spectral calculations this is also an indication of the stage the process is at)
            if cas == 1:
                memory = assess_mem(chem + '.castep',cores,computer)
                if str(memory[0]) != total_mem:
                    total_mem = str(memory[0])
                    available_mem = str(memory[1])
                    print 'Castep calculation running using ' + total_mem + 'GB of memory out of an available ' + available_mem + 'GB'
                    if float(total_mem) > float(available_mem):
                        print '\n\n******* WARNING: MEMORY REQUIRED BY CALCULATION IS LARGER THAN THAT AVAILABLE SO CALCULATION LIKELY TO FAIL ******\n\n'
                        send_email('Process exceeds memory allocation on ' + computer,'\n\n******* WARNING: MEMORY REQUIRED BY CALCULATION for ' + chem + ' on ' + computer + ' IS LARGER THAN THAT AVAILABLE SO CALCULATION LIKELY TO FAIL ******\n\n Consider aborting the process and restarting with the correct number of cores immediately!\n\n Calulation requires a memory of ' + str(total_mem) + 'GB whereas only ' + str(available_mem) + 'GB of RAM is available on ' + str(cores) + ' cores which have been selected on ' + computer)
                time.sleep(30)

            time.sleep(10)
    
            exitcode = proc.poll()
            if exitcode != None:
                print 'exitcode is ' +str(exitcode)
                ended = 1

        # Finish running the job and check whether it completed
        finished = check_complete(chem + '.castep')

    # For jobs on zener or kittel or ironman (much much more complicated!)
    if 'zener' in computer:
        import os
        os.system('cp ~/mypy/run_temp.sh ./' + chem + '.sh')
        f = open(chem + '.sh','r')
        lines_f = f.readlines()
        f.seek(0,0)
        
        max_time_str = lines_f[5].split()[2].replace('h_rt=','')     # Read the maximum time allowed by mpi from the input file
        max_time = time_in_s( max_time_str )
        print 'max time on calculation is : ' + str(max_time_str)
        if time_lim != 'default':
            lines_f[5] = '#$ -l h_rt=' + str(time_lim) + ':00:00\n'
            print 'changed max time on calculation to : ' + str(time_lim) + ' hours'
        lines_f[6] = '#$ -l qname=\'' + queue + '\'\n'
        lines_f[3] = '#$ -pe orte  ' + str(cores) + '\n'
        lines_f[9] = 'echo ' + str(cores) + '\n'
        if test == 0:
            lines_f[12] = 'mpirun -np ' + str(cores) + ' castep.mpi ' + chem + '\n'
        else:
            lines_f[12] = 'mpirun -np ' + str(cores) + ' castep.mpi ' + chem + ' -dryrun \n'
            print 'running castep in dryrun (test) mode'
            
        # Include any memory allocation information
        if mem_alloc != 'default':
            #mem_per_core = float(mem_alloc)/8
            lines_f.insert(6,'#$ -l mem_free=' + str(mem_alloc) + 'G\n')
            print 'Requested memory allocation on calculation changed to ' + str(mem_alloc)
            config.mem_alloc = mem_alloc
            
        f.close()
        f = open(chem + '.sh','w')
        f.writelines( lines_f )
        f.close()

    elif 'kittel' in computer:
        import os
        os.system('cp ~/mypy/run_temp.sh ./' + chem + '.sh')
        f = open(chem + '.sh','r')
        lines_f = f.readlines()
        f.seek(0,0)
        lines_f[3] = '#$ -pe orte ' + str(cores) + '\n'
        max_time_str = lines_f[5].split()[2].replace('h_rt=','')     # Read the maximum time allowed by mpi from the input file
        max_time = time_in_s( max_time_str )
        print 'max time on calculation is : ' + str(max_time_str)
        lines_f[7] = '#$ -l qname=' + queue + '\n'
        lines_f[16] = 'echo ' + str(cores) + '\n'
        if test == 0:
            lines_f[18] = 'mpirun --mca btl self,openib,tcp -np ' + str(cores) + ' castep.mpi ' + chem + '\n'
        else:
            lines_f[18] = 'mpirun --mca btl self,openib,tcp -np ' + str(cores) + ' castep.mpi ' + chem + ' -dryrun \n'
            print 'running castep in dryrun (test) mode'
        f.close()
        f = open(chem + '.sh','w')
        f.writelines( lines_f )
        f.close()

    elif 'ironman' in computer:
        import os
        os.system('cp ~/mypy/run_temp.sh ./' + chem + '.sh')
        f = open(chem + '.sh','r')
        lines_f = f.readlines()
        f.seek(0,0)
        lines_f[3] = '#$ -pe orte ' + str(cores) + '\n'
        max_time_str = lines_f[5].split()[2].replace('h_rt=','')     # Read the maximum time allowed by mpi from the input file
        max_time = time_in_s( max_time_str )
        print 'max time on calculation is : ' + str(max_time_str)
        if queue == 'parallel.q':
            v_mem = int(cores/8)*23
        elif queue == 'newpara.q':
            v_mem = int(cores/12)*63
        lines_f[6] = '#$ -l h_vmem=' + str(v_mem) + 'G\n'
        lines_f[7] = '#$ -l qname=' + queue + '\n'
        lines_f[16] = 'echo ' + str(cores) + '\n'
        if test == 0:
            lines_f[18] = 'mpirun --mca btl self,openib,tcp -np ' + str(cores) + ' castep.mpi ' + chem + '\n'
        else:
            lines_f[18] = 'mpirun --mca btl self,openib,tcp -np ' + str(cores) + ' castep.mpi ' + chem + ' -dryrun \n'
            print 'running castep in dryrun (test) mode'
        f.close()
        f = open(chem + '.sh','w')
        f.writelines( lines_f )
        f.close()
        
    if 'zener' in computer or 'kittel' in computer or 'ironman' in computer:
        cmd = 'qsub ' + chem + '.sh'
        finished = 0
        a = 0
        while finished < 1 and a < 10:
            
            output = subprocess.Popen( cmd, shell = 'true', stdout=subprocess.PIPE ).communicate()[0]
            procpid = output.split()[2]
            aborted = 0
            printed = 0
            cas = 0
            total_mem = '0'
            
            while aborted < 1:
                
                # Try to open the results file
                try:
                    f = open(chem + '.sh.o' + procpid,'r')
                    lines_f = f.readlines()
                    f.seek(0,0)
                    
                    # if the file opens the process must be running
                    while printed < 1:
                        # On zener, nodes have different RAM so will need to know which node you are on
                        if 'zener' in computer:
                            output = subprocess.Popen( 'qstat', shell = 'true', stdout=subprocess.PIPE ).communicate()[0]
                            lines = output.split('\n')
                            for line in lines:
                                try:
                                    random_proc_id = line.split()[0]
                                    if random_proc_id == str(procpid):
                                        try:
                                            node = int(''.join([i for i in line.split()[7].replace('-0-','') if i.isdigit()]))
                                        except IndexError:
                                            node = 'default'
                                except IndexError:
                                    pass
                        else:
                            node = 'default'

                        if node == 'default':
                            print 'mpi castep job for ' + chem + ' has started running with pid ' + procpid + ' on ' + config.computer + ' using ' + str(cores) + ' cores with monitering script pid ' + str(pypid) + ' at ' + print_time()
                        else:
                            print 'mpi castep job for ' + chem + ' has started running with pid ' + procpid + ' on node ' + str(node) + ' on ' + config.computer + ' using ' + str(cores) + ' cores with monitering script pid ' + str(pypid) + ' at ' + print_time()
                            
                        proc_log(chem, pypid, procpid, 0)
                        start_time = time.time()
                        loc_start = time.localtime()
                        printed = 1

                    # Check that the calculation output file (i.e. the .castep file) is being altered
                    while cas < 1:
                        try:
                            g = open(chem + '.castep','r')
                            lines_g = g.readlines()
                            output = subprocess.Popen( 'ls -l ' + chem + '.castep', shell = 'true', stdout=subprocess.PIPE ).communicate()[0]
                            cas_time = output.split()[5] + ' ' + output.split()[6] + ' ' + output.split()[7] + ' 2014'
                            if time.strptime(cas_time, "%b %d %H:%M %Y") > loc_start:
                                print 'Now printing output to Castep output file ' + chem + '.castep'
                                cas = 1
                            else:
                                time.sleep(5)
                                break
                        except IOError:
                            break

                    # Print the memory requirements by different parts of the calculation (for spectral calculations this is also an indication of the stage the process is at)
                    if cas == 1:
                        
                        memory = assess_mem(chem + '.castep',cores,computer,node,queue)
                        if str(memory[0]) != total_mem:
                            total_mem = str(memory[0])
                            available_mem = str(memory[1])
                            print 'Castep calculation running using ' + total_mem + 'GB of memory out of an available ' + available_mem + 'GB'
                            if float(total_mem) > float(available_mem):
                                print '\n\n******* WARNING: MEMORY REQUIRED BY CALCULATION IS LARGER THAN THAT AVAILABLE SO CALCULATION LIKELY TO FAIL ******\n\n'
                                send_email('Process exceeds memory allocation on ' + computer,'\n\n******* WARNING: MEMORY REQUIRED BY CALCULATION for ' + chem + ' on ' + computer + ' with PID '+ str(procpid) + ' IS LARGER THAN THAT AVAILABLE SO CALCULATION LIKELY TO FAIL ******\n\n Consider aborting the process and restarting with the correct number of cores immediately!\n\n Calulation requires a memory of ' + str(total_mem) + 'GB whereas only ' + str(available_mem) + 'GB of RAM is available on ' + str(cores) + ' cores which have been selected on ' + computer)
                    time.sleep(15)


                    # if the final line in the results file contains 'ended' then the process has finished
                    # But if 'Fatal error' is in the results file then something has gone wrong so the process should be abandoned regardless
                    f.seek(0,0)
                    f_read = f.read()
                    if 'Fatal Error:' in f_read or 'error reading job context from "qlogin_starter"' in f_read or 'libibverbs: Fatal: couldn\'t read uverbs ABI version.' in f_read:
                        import os
                        os.system('qdel ' + str(procpid))
                        print 'Fatal error caused process to fail'
                        aborted = 1
                        a = a + 1
                    elif 'mpirun has exited due to process' in f_read:
                        aborted = 1
                        a = 11
                        finished = 0.5
                    elif 'Job ended at:' in f_read:
                        finished = 1
                        aborted = 1
                        print 'process finished'
                    else:
                        # if the calculation has not finished or failed, make sure that it has not gone over time and been killed
                        process_time = time.time() - start_time
                        if process_time > max_time - 60:
                            aborted = 1
                            a = 11
                            finished = 0.5
                            print "Process was unable to complete in the maximum allocated time and therefore has been killed by mpi"
                        
                        if cas == 1:
                            # check that the process is still running and hasn't got stuck
                            output = subprocess.Popen( 'qstat', shell = 'true', stdout=subprocess.PIPE ).communicate()[0]
                            lines = output.split('\n')
                            for line in lines:
                                try:
                                    random_proc_id = line.split()[0]
                                    if random_proc_id == str(procpid):
                                        state = line.split()[4]
                                        if state != 'r' and 'Job ended at:' not in f_read:
                                            print 'calculation is nolonger running but did not finish successfully'
                                            a = 11
                                            aborted = 1
                                            if 'exited on signal 9 (Killed)' in f_read:
                                                raise MemError('calculation exceeded available free RAM')
                                except IndexError:
                                    pass
                                            
                        time.sleep(5)
                        
                # If process hasn't started yet, wait a few seconds and check again
                except IOError:
                    time.sleep(5)
            
                    # Make sure process hasn't got stuck and been suspended, if it has, try again
                    output = subprocess.Popen( 'qstat', shell = 'true', stdout=subprocess.PIPE ).communicate()[0]
                    lines = output.split('\n')
                    for line in lines:
                        try:
                            random_proc_id = line.split()[0]
                            if random_proc_id == str(procpid):
                                state = line.split()[4]
                                if state == 'Eqw':
                                    import os
                                    os.system('qdel ' + str(procpid))
                                    print 'Process became suspended so trying again'
                                    a = a + 1
                                    aborted = 1
                        except IndexError:
                            pass
                        
        if a == 10:
            print 'Process became suspended 10 times and therefore attempts at this simulation have been aborted'

    print 'castep finished running in parallel using ' + str(cores) + ' cores at ' + print_time()

    temp_file_cleanup()

    if finished == 1:
        proc_log(chem, pypid, procpid, 1)

    return finished, procpid

#****************************************************************************

# Creates and keeps a log file in the current working directory of all the castep jobs which have been run with their pids
def proc_log(chem, pypid, procpid, finished):
    import os
    try:
        f = open('all_procs.log','r')
        f.close()
    except IOError:
        f = open('all_procs.log','w')
        cwd = os.getcwd()
        f.write('All CASTEP processes in directory: ' + cwd + '\n')
        f.close()

    f = open('all_procs.log','a')
    f.write(chem + '\t' + str(pypid) + '\t' + str(procpid) + '\t' + str(finished) + '\n')
    f.close()
    return

#****************************************************************************

# Get the volume
def get_cell_volume(filename):
    h = open( filename,'r')
    lines_h  = h.readlines()
    for line in lines_h:
        if 'Current cell volume' in line:
            vol = line.split()[4]
    h.close()
    return vol

#****************************************************************************

# Find total energy
def get_total_Energy( filename ):
    h = open( filename,'r')
    lines_h  = h.readlines()
    for line in lines_h:
        if 'Final energy =' in line:
            total_Energy = line.split()[3]
        elif 'NB est. 0K energy (E-0.5TS)' in line:
            total_Energy = line.split()[6]
    h.close()
    return total_Energy

#****************************************************************************

# Find valance energy of oxygen atom
def get_O_energy(filename, state):
    h = open( filename,'r')
    lines_h  = h.readlines()
    h.seek(0,0)

    if state == 'excited':
        O_config = '1s1 2s2 2p4'
    elif state == 'ground':
        O_config = '1s2 2s2 2p4'

    l_a = 0
    for num, line in enumerate(h):
        if 'Atomic calculation performed for' in line and O_config in line:
            O_atom = line.split()[4][:-1]
            l_a = num
    h.seek(0,0)

    if l_a != 0:
        E_at = float(lines_h[l_a + 2].split()[9])
    elif l_a == 0:
        if 'Local Density Approximation' in h.read():
            if state == 'excited':
                E_at = -1477.212
            elif state == 'ground':
                E_at = -2027.926
        h.seek(0,0)
        if 'Perdew Burke Ernzerhof' in h.read():
            if state == 'excited':
                E_at = -1486.074
            elif state == 'ground':
                E_at = -2040.902
        h.seek(0,0)
        for line in lines_h:
            if 'Pseudo atomic calculation performed for' in line and 'O' in line and '2s2 2p4' in line:
                O_atom = line.split()[5]
        
    for num, line in enumerate(h):
        if 'Pseudo atomic calculation performed for' in line and O_atom in line:
            l_p = num

    E_val = float(lines_h[l_p + 2].split()[9])

    h.close()
    return E_at, E_val

#****************************************************************************

def calculate_shift(ex_energy, ground_energy, supercell, functional='LDA'):

    # If a filename is stated, extract the quantities from the output files
    if '.castep' in str(ex_energy):
        E_ex = get_total_Energy(ex_energy)
        (O_at_ex, O_val_ex) = get_O_energy(ex_energy, 'excited')
    else:
        E_ex = ex_energy
        print 'no castep file has been given for excited energies so using default O energies for ' + functional
        if functional == 'LDA':
            O_at_ex  = -1477.212
            O_val_ex = -623.2211
        elif functional == 'PBE':
            O_at_ex  = -1486.074
            O_val_ex = -625.9282
    if '.castep' in str(ground_energy):
        E_gr = get_total_Energy(ground_energy)
        (O_at_gr, O_val_gr) = get_O_energy(ground_energy, 'ground')
    else:
        E_gr = ground_energy
        print 'no castep file has been given for ground energies so using default O energies for ' + functional
        if functional == 'LDA':
            O_at_gr  = -2027.926
            O_val_gr = -432.56
        elif functional == 'PBE':
            O_at_gr  = -2040.902
            O_val_gr = -433.8089

    # Make sure all values are numbers
    E_ex = float(E_ex)
    E_gr = float(E_gr)
    supercell = float(supercell)

    # Note supercell is the number by which the VOLUME of the ground state calculation would need to be MULTIPLIED to match that of the supercell

    # Calculate the overall shift for an excited Oxygen atom
    shift = E_ex - E_gr*supercell + (O_at_ex - O_at_gr) - (O_val_ex - O_val_gr)
    return shift

#****************************************************************************

# Find Fermi energy (function works for both .castep and .odo filetypes)
def get_Fermi_Energy( filename ):
    global Fermi_Energy
    try:
        h = open( filename,'r')
        finished = 1
        lines_h  = h.readlines()
        if '.odo' in filename:
            for line in lines_h:
                if 'Fermi energy from DOS :' in line:
                    Fermi_Energy = line.split()[6]
        elif '.castep' in filename:
            for line in lines_h:
                if 'Fermi energy for spin-degenerate system:' in line:
                    Fermi_Energy = line.split()[6]
        h.close()
        config.Fermi_Energy = Fermi_Energy
    except IOError:
        print 'file ' + filename + ' does not exist'
        finished = 0
    return finished

#****************************************************************************

# Find Band gap
def get_bandgap( filename ):
    global bandgap
    global bandgap_nature
    h = open( filename,'r')
    lines_h  = h.readlines()
    for line in lines_h:
        if 'Thermal Bandgap :' in line:
            bandgap = line.split()[4]
    for line in lines_h:
        if 'Indirect Gap' in line or 'Direct Gap' in line:
            bandgap_nature = line.split()[2]
    h.close()
    config.bandgap = bandgap
    config.bandgap_nature = bandgap_nature
    return

#****************************************************************************

# Find the total number of kpoints used in a calculation (doesn't matter if it's a dry run)
def get_no_kpoints(filename):
    f = open(filename,'r')
    lines = f.readlines()
    f.seek(0,0)
    for line in lines:
        if 'Number of kpoints used' in line:
            no_kpoints = line.split()[5]
    f.close()
    return no_kpoints

#****************************************************************************

# Find the grid of kpoints used in a calculation (doesn't matter if it's a dry run)
def get_kpoint_grid(filename):
    f = open(filename,'r')
    lines = f.readlines()
    f.seek(0,0)
    for line in lines:
        if 'MP grid size for' in line:
            kpoints = [line.split()[7],line.split()[8],line.split()[9]]
    f.close()
    return kpoints

#****************************************************************************

# Find the total number of kpoints used in a calculation (doesn't matter if it's a dry run)
def get_kpoints(filename):
    f = open(filename,'r')
    lines = f.readlines()
    f.seek(0,0)
    for line in lines:
        if 'MP grid size for SCF calculation is' in line:
            kpoints = [int(line.split()[7]),int(line.split()[8]),int(line.split()[9])]
    f.close()
    return kpoints

#****************************************************************************

# Change the lattice parameter c 
def ch_c_2D( chem, c_temp ):
    global c
    c = c_temp
    f = open('%s.cell' % chem,'r')

    # Record old c and print new c to file
    lines_f  = f.readlines()
    c_old = lines_f[3].split()[2]
    lines_f[3]    = '0.00 0.00 ' + str(c) + '\n'

    # Count total number of atoms
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_B = num
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_E = num
    n_atoms = l_E - l_B

    # Cycle through all atoms only atoms where z = 0.5 will remain unaffected
    i = 1  
    while i < n_atoms:
        
        # Read old fractional coordinates for atoms
        atom = lines_f[l_B + i].split()[0]
        S_x  = lines_f[l_B + i].split()[1]
        S_y  = lines_f[l_B + i].split()[2]
        S_z  = lines_f[l_B + i].split()[3]
        
        # Calcultate absolute distance between X atom and M atom plane (from old c value)
        delta = float(c_old)*(0.5-float(S_z))
            
        # Print new fractional coordinates of S atom
        lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(0.5-delta/float(c)) + '\n'

        i = i + 1

    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'lattice paramater c changed to: ' + str(c_temp)
    config.c = c
    return

#****************************************************************************

# Change DFT+D correction in .param file
def ch_sedc( chem, sedc_temp ):
    global sedc
    sedc = sedc_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    
    # Remove sedc_scheme line if already present
    for num, line in enumerate(f):
        if 'sedc_scheme' in line:
             del lines_f[num]

    # Specify whether DFT+D corrections are being used at all
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'sedc_apply' in line:
            l = num
    if sedc_temp == 'none':
        lines_f[l]    = 'sedc_apply : false\n'
    else:
        lines_f[l]    = 'sedc_apply : true\n'
        lines_f.insert(l, 'sedc_scheme : ' + sedc_temp + '\n')
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'DFT+D correction scheme changed to: ' + sedc_temp
    config.sedc = sedc
    return

#****************************************************************************

# Extract entire cell (all atoms and positions) from an existing .cell file
def get_cell_from_cell( old_cell ):
    global a
    global b
    global c
    global cell_complete 
    f = open(old_cell + '.cell','r')
    lines_f  = f.readlines()
    f.seek(0,0)
    
    # Get the real lattice and the lattice parameters
    real_lattice = []
    i = 1
    while i < 4:
        RL = [lines_f[i].split()[0], lines_f[i].split()[1], lines_f[i].split()[2]]  # line i of RL
        real_lattice.append(RL)
        i = i + 1

    a = str((float(real_lattice[0][0])**2 + float(real_lattice[0][1])**2 + float(real_lattice[0][2])**2 )**0.5)
    b = str((float(real_lattice[1][0])**2 + float(real_lattice[1][1])**2 + float(real_lattice[1][2])**2 )**0.5)
    c = str((float(real_lattice[2][0])**2 + float(real_lattice[2][1])**2 + float(real_lattice[2][2])**2 )**0.5)

    lattice_params = [ a, b, c]
    
    # Count number of atoms in the original cell file, n_atoms
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num

    # Read complete atom positions
    cell_complete = lines_f[l_1+1:l_2]

    f.close()
        
    print 'Final lattice parameters a = ' + a + ', b = ' + b + ' and c = ' + c + ' and all atom positions recorded in cell_complete'
    config.a               = a
    config.b               = b
    config.c               = c
    config.lattice_params  = lattice_params
    config.real_lattice    = real_lattice
    config.cell_complete   = cell_complete
    return

#****************************************************************************

# gets relaxed geom and updates cell file in one function
def relaxed(filename, cell=1):
    try:
        get_cell_geom_complete(filename)
    except UnboundLocalError:
        BFGS = get_BFGS_iterations(filename)
        get_cell_geom_complete(filename,BFGS_iteration=BFGS)

    if cell == 1:
        cell = filename.replace('.castep','')
    update_cell_complete(cell,config.real_lattice,config.cell_complete)
    return

#****************************************************************************

# Extract entire cell (all atoms and positions) from a geometry optimisation .castep output file
def get_cell_geom_complete(filename, BFGS_iteration='final'):
    global a
    global b
    global c
    global cell_complete
    f = open(filename,'r')
    lines_f  = f.readlines()
    f.seek(0,0)

    l_end = 10000000
    # Find finalised cell information
    if BFGS_iteration == 'final':
        for num, line in enumerate(f):
            if 'BFGS : Final Configuration:' in line:
                l_start = num

    # If the BFGS iteration of interest is not just the last one in the .castep file
    else:
        BFGS_tot = 0
        BFGS = 0
        # Need to cycle through counting manually because the index is reset to 0 if the calculation is restarted
        for num, line in enumerate(f):
            if 'BFGS: starting iteration' in line:
                BFGS = int(line.split()[3])
                if BFGS_tot == int(BFGS_iteration):
                    l_start = num
                    break

            elif BFGS_tot < int(BFGS_iteration):
                if 'BFGS: finished iteration' in line and int(line.split()[3]) == BFGS:
                    BFGS_tot = BFGS_tot + 1
                
        # Take a maximum line as well if the BFGS iteration of interest is not the last one
        f.seek(0,0)
        BFGS_tot = 0
        BFGS = 0
        for num, line in enumerate(f):
            if 'BFGS: starting iteration' in line:
                BFGS = int(line.split()[3])
                if BFGS_tot == int(BFGS_iteration + 1):
                    l_end = num
                    break

            elif BFGS_tot < int(BFGS_iteration + 1):
                if 'BFGS: finished iteration' in line and int(line.split()[3]) == BFGS:
                    BFGS_tot = BFGS_tot + 1

    # Extract Real lattice
                
    f.seek(0,0)
    l_RL = 0
    for num, line in enumerate(f):
        if 'Real Lattice(A)' in line and num > l_start and num < l_end:
            l_RL = num

    # If the cell is fixed (as may be the case for geometry optimisation of an isolated molcule) then the real lattice is not displayed every iteration and therefore the real lattice will need to be taken from the start of the output .castep file
    if l_RL == 0:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'Real Lattice(A)' in line:
                l_RL = num
    
    real_lattice = []
    i = 1
    while i < 4:
        RL = [lines_f[l_RL+i].split()[0], lines_f[l_RL+i].split()[1], lines_f[l_RL+i].split()[2]]  # line i of RL
        real_lattice.append(RL)
        i = i + 1

    # Extract lattice parameters
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'alpha =' in line and num > l_RL and num < l_end:
            l_a = num
    a = lines_f[l_a].split()[2] # lattice parameter a

    f.seek(0,0)
    for num, line in enumerate(f):
        if 'beta  =' in line and num > l_RL and num < l_end:
            l_b = num
    b = lines_f[l_b].split()[2] # lattice parameter b

    f.seek(0,0)
    for num, line in enumerate(f):
        if 'gamma =' in line and num > l_RL and num < l_end:
            l_c = num
    c = str(lines_f[l_c].split()[2]) # lattice parameter c (for the cell!)
    
    lattice_params = [ a, b, c]

    # Extract total number of atoms
    f.seek(0,0)
    for line in lines_f:
        if 'Total number of ions in cell' in line:
            n_atoms = int(line.split()[7])
            
    # Extract |F|max
    f.seek(0,0)
    Fmax = 0
    for num, line in enumerate(f):
        if '|F|max' in line and num > l_start and num < l_end:
            Fmax = float(line.split()[3])

    # Extract Atom positions
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'Element' in line and num > l_start and num < l_end:
            l_El = num

    i = 0 
    cell_complete = []
    while i < n_atoms:
        
        # Read old fractional coordinates for atoms
        atom = lines_f[l_El + 3 + i].split()[1]
        X_x  = lines_f[l_El + 3 + i].split()[3]
        X_y  = lines_f[l_El + 3 + i].split()[4]
        X_z  = lines_f[l_El + 3 + i].split()[5]
        
        # Append all atomic fractional coordinates to cell_complete
        cell_complete.append(atom + '\t' + X_x + '\t' + X_y + '\t' + X_z + '\n')

        i = i + 1

    f.close()
        
    if BFGS_iteration == 'final':
        print 'Final lattice parameters a = ' + a + ', b = ' + b + ' and c = ' + c + ' and all atom positions recorded in cell_complete'
    else:
        print 'BFGS iteration: ' + str(BFGS_iteration) +  ' lattice parameters a = ' + a + ', b = ' + b + ' and c = ' + c + ' and all atom positions recorded in cell_complete'
    config.a               = a
    config.b               = b
    config.c               = c
    config.lattice_params  = lattice_params
    config.real_lattice    = real_lattice
    config.cell_complete   = cell_complete
    config.Fmax            = Fmax
    return

#****************************************************************************

# Update any .cell file with lattice parameters and atomic positions
def update_cell_complete( chem, real_lattice_temp, cell_complete_temp ):
    global real_lattice
    global cell_complete
    real_lattice = real_lattice_temp
    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()

    # Update lattice parameters
    i = 1
    for line in real_lattice:
        lines_f[i]    = str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) + '\n'
        i = i + 1

    # Get rid of old atomic coordinates
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num        
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
    n = l_2 - l_1
    del lines_f[7:6+n]

    lines_f[7:7] = cell_complete_temp

    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'Lattice parameters and all atom positions updated in .cell file'
    return

#****************************************************************************

# Extract the full set of real bondlengths from a geometry optimisation
# Note that this only gives the bondlengths which are printed in the .castep file and therefore if a bondlength is deemed too long by castep then it will not be in the list
# Also note that this is only possible from a complete geometry optimisation
def get_bondlengths_complete(filename, simplify=1):
    global bondlengths
    f = open(filename,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    dryrun = 0

    # Find finalised cell information
    l_start = 0
    for num, line in enumerate(f):
        if 'Bond' in line:
            l_start = num

    if l_start == 0:
        print '\nBondlengths could not be found in file ' + filename + ' and therefore could not be extracted.\n'

    else:

        # Count total number of bondlengths
        f.seek(0,0)
        l_end = 0
        for num, line in enumerate(f):
            if 'Writing model to' in line and num > l_start:
                l_end = num

        f.seek(0,0)
        if l_end == 0:
            dryrun = 1
            for num, line in enumerate(f):
                if '==================================================' in line and num > l_start:
                    l_end = num
            n_atoms = l_end - l_start - 2
        else:
            n_atoms = l_end - l_start - 5

        # Cycle through the bondlengths and collect them in a dictionary called bondlengths
        i = 0 
        bondlengths = {}
        while i < n_atoms:
            l = lines_f[l_start + 2 + i].split()
            bond_name = l[0] + ' ' + l[1] + ' ' + l[2] + ' ' + l[3] + ' ' + l[4]

            if dryrun == 0:
                bondlengths[bond_name] = float(l[6])
            elif dryrun == 1:
                bondlengths[bond_name] = float(l[5])
            i = i + 1

        print 'Complete set of bondlengths taken from file '  + filename
        config.bondlengths = bondlengths

        if simplify == 1:
            bondlengths = simplify_bondlengths(bondlengths)

    return bondlengths

#****************************************************************************

# Simply complete bondlengths into a set on bondlengths between two different atom types
def simplify_bondlengths(bondlengths, atoms=['Mo','O']):
    bl_list = []
    for bond in bondlengths:
        if all(atom in bond for atom in atoms):
            bl_list.append(dp(bondlengths[bond],2))
    simple_bl = sorted(list(set(bl_list)))
    return simple_bl

#****************************************************************************

# Finds an RMS average difference between the bondlengths of two geometries of the same cell - useful as a geometric convergence parameter
def compare_bondlengths(bondlengths_1, bondlengths_2):

    # First compare the two sets of bondlengths to check that they are the same
    if set(bondlengths_1.keys()) ^ set(bondlengths_2.keys()) != set([]):
        print 'could not compare bondlengths since different bondlengths exist in the two sets'
        info = 'N/A'

    # If the two sets do turn out to be the same, find the RMS ave of the differences between them
    else:
        all_diffs = []
        tot_diffs_sq = 0

        bonds_sort1 = sorted(bondlengths_1.values())
        bonds_sort2 = sorted(bondlengths_2.values())

        for bl in bonds_sort1:
            diff_sq = (bl - bonds_sort2[bonds_sort1.index(bl)])**2

        #for bond_name in bondlengths_1:
        #    diff_sq = (bondlengths_1[bond_name] - bondlengths_2[bond_name])**2
            all_diffs.append(diff_sq**0.5)
            tot_diffs_sq = tot_diffs_sq + diff_sq
            
        max_diff = max(all_diffs)
        RMS_diff = (float(tot_diffs_sq)/len(bondlengths_1))**0.5
        info = [RMS_diff, max_diff]

    return info

#****************************************************************************

# Finds an RMS average difference between the atomic positions of two geometries of the same cell - useful as a geometric convergence parameter
# Cell complete should be in ABSOLUTE CELL POSITIONS!
def compare_atom_positions(cell_complete_1, cell_complete_2):
    i=0
    tot_diffs_sq = 0
    all_diffs = []
    for atom_complete in cell_complete_1:
        atom_1 = atom_complete.split()[0]
        x_1 = float(atom_complete.split()[1])
        y_1 = float(atom_complete.split()[2])
        z_1 = float(atom_complete.split()[3])
        atom_2 = atom_complete.split()[0]
        x_2 = float(cell_complete_2[i].split()[1])
        y_2 = float(cell_complete_2[i].split()[2])
        z_2 = float(cell_complete_2[i].split()[3])
        if atom_1 != atom_2:
            print 'could not compare positions of atoms since two cells describe different sets of atoms'
            break
        diffs_sq = (x_1-x_2)**2 + (y_1-y_2)**2 + (z_1-z_2)**2
        all_diffs.append(diffs_sq**0.5)
        tot_diffs_sq = tot_diffs_sq + diffs_sq
        i = i + 1

    max_diff = max(all_diffs)
    RMS_diff = (float(tot_diffs_sq)/(len(cell_complete_1)*3))**0.5
    info = [RMS_diff, max_diff]

    return info

#****************************************************************************

# Compare two sets of atomic positions from geometry optimisations
def compare_BFGS_iterations(filename, BFGS_1, BFGS_2, filename_2=0):
    if filename_2 == 0:
        filename_2 = filename
    get_cell_geom_complete(filename, BFGS_iteration=BFGS_1)
    RL_1 = config.real_lattice
    CC_1 = frac2abs(config.real_lattice, config.cell_complete)
    get_cell_geom_complete(filename_2, BFGS_iteration=BFGS_2)
    RL_2 = config.real_lattice
    CC_2 = frac2abs(config.real_lattice, config.cell_complete)
    diffs_RL = compare_lattice_consts(RL_1, RL_2)
    diffs_CC = compare_atom_positions(CC_1, CC_2)
    info = [diffs_RL[0], diffs_RL[1], diffs_CC[0], diffs_CC[1]]
    #print 'In castep geometry optimisation for ' + filename + ' the structures for BFGS iterations ' + str(BFGS_1) + ' and ' + str(BFGS_2) + ' have an RMS difference in lattice parameters of ' + str(diffs_RL[0]) + ' with the maximum difference ' + str(diffs_RL[1]) + ' and an RMS difference in all atomic positions of ' + str(diffs_CC[0]) + ' with the maximum difference ' + str(diffs_CC[1]) 
    return info

#****************************************************************************

# Finds an RMS average difference between the bondlengths of two geometries of the same cell - useful as a geometric convergence parameter
def compare_lattice_consts(real_lattice_1, real_lattice_2):

    # Find the RMS ave of the differences between them
    tot_diffs_sq = 0
    all_diffs = []
    i_1 = 0
    i_2 = 0
    while i_1 < 3:
        while i_2 < 3:
            l_1 = float(real_lattice_1[i_1][i_2])
            l_2 = float(real_lattice_2[i_1][i_2])
            diffs_sq = (l_1 - l_2)**2
            all_diffs.append(diffs_sq**0.5)
            tot_diffs_sq = tot_diffs_sq + diffs_sq
            i_2 = i_2 + 1
        i_2 = 0
        i_1 = i_1 + 1
            
    max_diff = max(all_diffs)
    RMS_diff = (float(tot_diffs_sq)/9)**0.5
    info = [RMS_diff, max_diff]

    return info

#****************************************************************************

# For a python list of fractional atomic positions, generate the absolute positions of atoms
def frac2abs(real_lattice, cell_complete):    
    RL = []
    for a in real_lattice:
        RL_i = []
        for a_i in a:
            RL_i.append(float(a_i))
        RL.append(RL_i)

    abs_cell_complete = []
    for atom_complete in cell_complete:
        atom = atom_complete.split()[0]
        x = float(atom_complete.split()[1])
        y = float(atom_complete.split()[2])
        z = float(atom_complete.split()[3])
        pos_x = str(x*RL[0][0] + y*RL[1][0] + z*RL[2][0])
        pos_y = str(x*RL[0][1] + y*RL[1][1] + z*RL[2][1])
        pos_z = str(x*RL[0][2] + y*RL[1][2] + z*RL[2][2])
        abs_cell_complete.append(atom + '\t' + pos_x + '\t' + pos_y + '\t' + pos_z + '\n')

    return abs_cell_complete

#****************************************************************************

# Converts absolute coordinates to fractional coordinates in the .cell file (as are expected by most functions in this module)
def abs2frac(chem):
    import numpy
    f = open(chem + '.cell','r')
    lines_f  = f.readlines()
    f.seek(0,0)

    # Get the real lattice for the cell (in cartesian coordinates)
    real_lattice = []
    i = 1
    while i < 4:
        RL = [float(lines_f[i].split()[0]), float(lines_f[i].split()[1]), float(lines_f[i].split()[2])]  # line i of RL
        real_lattice.append(RL)
        i = i + 1

    # Find the inverse of the real lattice matrix and call this the new lattice matrix
    RL = numpy.matrix( [real_lattice[0], real_lattice[1], real_lattice[2]] )
    NL = RL.I

    # Count the number of atoms in the cell
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_ABS' in line:
            l_B = num
    lines_f[l_B] = '%BLOCK POSITIONS_FRAC\n'

    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_ABS' in line:
            l_E = num
    lines_f[l_E] = '%ENDBLOCK POSITIONS_FRAC\n'
    n_atoms = l_E - l_B

    # Cylce through atoms
    i = 1  
    while i < n_atoms:
        
        # Read old fractional coordinates for atoms
        atom = lines_f[l_B + i].split()[0]
        S_x  = lines_f[l_B + i].split()[1]
        S_y  = lines_f[l_B + i].split()[2]
        S_z  = lines_f[l_B + i].split()[3]

        # Now need to project the real positions of atoms onto the lattice vector basis set
        # Since S' = S.A^(-1).a if a is the new basis set defined from cartesian coordinates ,c, by matrix A: a = A.c
        S_old = numpy.matrix( [ float(S_x), float(S_y), float(S_z) ] )
        S_new = numpy.dot( S_old, NL )
        S_str = numpy.array(S_new).reshape(-1,).tolist()      # Convert the matrix to a list so that the terms can be printed

        # Terms are printed to a precision of 9 decimal places to avoid over accuracy
        lines_f[l_B + i] = atom + '\t' + str("{0:.9f}".format(S_str[0])) + '\t' + str("{0:.9f}".format(S_str[1])) + '\t' + str("{0:.9f}".format(S_str[2])) + '\n'

        i = i + 1

    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'All atom positions in previously absolute cartesian coordinates have now all been transformed into new fractional coordinates defined by the basis set of the cell vectors'
    return

#****************************************************************************

# Converts angles in degrees to radians
def d2r(x):
    from math import pi
    y = (x*2*pi)/360.0
    return y

# Converts angles in radians to degrees
def r2d(x):
    from math import pi
    y = (x*360)/(2*pi)
    return y

#****************************************************************************

# Converts lattice parameters and angles to cartesian lattice vectors (real_lattice)
def lat2vect(lat_params, angles):
    # angles in degrees, lat_params in angstroms
    
    from math import sin, cos, pi

    (a,b,c) = (float(lat_params[0]),float(lat_params[1]),float(lat_params[2]))
    (alp, bet, gam) = (d2r(float(angles[0])),d2r(float(angles[1])),d2r(float(angles[2])))

    # a_v is a vector [a_x, a_y, a_z]
    # let a_v align to the x-axis

    b_x = b*cos(gam)
    b_y = b*sin(gam)

    c_x = c*cos(bet)
    c_y = (c/b_y)*(b*cos(alp)-b_x*cos(bet))
    c_z = ( c**2 - c_x**2 - c_y**2 )**0.5

    real_lattice = [[a, 0, 0],[b_x, b_y, 0],[c_x, c_y, c_z]]

    for vec in real_lattice:
        for num in vec:
            if abs(num) < 1e-4:
                real_lattice[real_lattice.index(vec)][vec.index(num)] = 0

    return real_lattice

#****************************************************************************

# Convert a .res file to a .cell file
def res2cell(filename, chem):
    g = open(filename, 'r')
    lines_g = g.readlines()
    g.seek(0,0)
    cell = lines_g[1].split()
    lat_params = [float(cell[2]),float(cell[3]),float(cell[4])]
    angles     = [float(cell[5]),float(cell[6]),float(cell[7])]
    
    real_lattice = lat2vect(lat_params, angles)

    complete_cell = []

    for line in lines_g:
        if lines_g.index(line) > 3 and 'END' not in line:
            at = line.split()
            complete_cell.append(at[0] + '\t' + at[2] + '\t' + at[3] + '\t' + at[4] + '\n')
        else:
            pass

    printed_RL = []
    for RL in real_lattice:
        printed_RL.append(str(RL[0]) + '\t' + str(RL[1]) + '\t' + str(RL[2]) + '\n')

    lines_f = []
    lines_f.append('%BLOCK LATTICE_CART\n')
    lines_f.append('%ENDBLOCK LATTICE_CART\n')
    lines_f.append('\n')
    lines_f.append('%BLOCK POSITIONS_FRAC\n')
    lines_f.append('%ENDBLOCK POSITIONS_FRAC\n')

    lines_f[1:1] = printed_RL
    lines_f[-1:-1] = complete_cell

    lines_f.append('\n')
    lines_f.append('%BLOCK SPECIES_POT\n')
    lines_f.append('Mo Mo_OTF.usp\n')
    lines_f.append('O  O_OTF.usp\n')
    lines_f.append('%ENDBLOCK SPECIES_POT\n')
    lines_f.append('\n')
    lines_f.append('KPOINTS_MP_SPACING 0.03\n')
    lines_f.append('\n')


    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'A .cell file has been formed for a single unit cell from the .res file with all fractional atomic positions given'
    return 

#****************************************************************************

# Convert a .cif file to a .cell file
def cif2cell(filename, chem, real_lattice):
    import subprocess
    command = 'jmol -n -i -o ' + filename + ' -j \'load "" {1 1 1}; print all.atomtype;\''
    output = subprocess.Popen( command, shell = 'true',stdout=subprocess.PIPE ).communicate()[0]
    lines = output.split('\n')
    
    del lines[-1]
    
    n = lines.count(lines[0])
    m = len(lines)

    j = 0
    k = 1
    atoms = []
    commands = ''
    while k < n + 1:
        while j < m/n:
            if ''.join([i for i in lines[j] if i.isdigit()]).isdigit():
                atoms.append(''.join([i for i in lines[j] if not i.isdigit()]) + ':' + ''.join([i for i in lines[j] if i.isdigit()]))
            else:
                atoms.append(''.join([i for i in lines[j] if not i.isdigit()]))
            commands += 'print {(' + str(lines[j]) + ')[' + str(k) + ']}.xyz;'
            j = j + 1
        k = k + 1
        j = 0

    command = 'jmol -n -i -o ' + filename + ' -j \'load "" {1 1 1};' + commands + '\''
    output = subprocess.Popen( command, shell = 'true',stdout=subprocess.PIPE ).communicate()[0]
    lines = output.split('\n')

    del lines[-1]

    complete_cell = []
    i = 0
    for line in lines:
        line = line.replace('{','').replace('}','')
        complete_cell.append(atoms[i] + '\t' + line + '\n')
        i = i + 1

    printed_RL = []
    for RL in real_lattice:
        printed_RL.append(str(RL[0]) + '\t' + str(RL[1]) + '\t' + str(RL[2]) + '\n')

    lines_f = []
    lines_f.append('%BLOCK LATTICE_CART\n')
    lines_f.append('%ENDBLOCK LATTICE_CART\n')
    lines_f.append('\n')
    lines_f.append('%BLOCK POSITIONS_ABS\n')
    lines_f.append('%ENDBLOCK POSITIONS_ABS\n')

    lines_f[1:1] = printed_RL
    lines_f[-1:-1] = complete_cell

    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'A .cell file has been formed for a single unit cell from the .cif file with all absolute atomic positions given'
    return 

#****************************************************************************

# Update any .cell file with lattice parameters and atomic positions
def update_cell_MX2( chem, a, c, bondlength='fixed', layers=1, spacing='bulk' ):

    # Get the original bondlength
    if bondlength == 'fixed':
        get_cell_from_cell(chem)
        S_heights = []
        for atom in config.cell_complete:
            if 'S' in atom:
                S_z = float(atom.split()[3])
                S_heights.append(S_z)

        # In the case of bulk or monolayer MX2 M layer height is easy
        if spacing == 'bulk' or layers == 1:
            Mo_z  = float(config.c)/(2*int(layers))

        # In multilayered samples it's more tricky
        else:
            Mo_z  = 0.5*(float(config.c) - (int(layers) - 1)*float(spacing))

        delta = Mo_z - min(S_heights)*float(config.c)
        bondlength = (delta**2 + 0.3333333333333*(float(config.a)**2))**0.5

    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()

    # Update a and b lattice parameters
    lines_f[1]    = str(a) + ' 0.00 0.00\n'
    b_x           = str(-float(a)*0.5)
    b_y           = str(float(a)*0.866025403784)
    lines_f[2]    = b_x + ' ' + b_y + ' ' + '0.00\n'
    c_old = lines_f[3].split()[2]
    lines_f[3]    = '0.00 0.00 ' + str(c) + '\n'

    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_B = num        
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_E = num
    n_atoms = l_E - l_B

    delta = ( float(bondlength)**2 - ( (2/float(3))*float(b_y) )**2 )**0.5

    # MULTILAYER: Need to work out the 'height' of the Mo planes given the number of layers and their spacing
    if spacing != 'bulk':
        planes = []
        layer = 0
        spacing_frac = float(spacing)/float(c)
        while layer < layers:
            height = 0.5*(1 + spacing_frac)
            planes.append(height)
            height = 0.5*(1 - spacing_frac)
            planes.append(height)
            layer = layer + 2
        spacing = spacing_frac

    # BULK: Need to work out the 'height' of the Mo planes given the number of equally spaced layers in the cell
    if spacing == 'bulk':
        planes = []
        bulk_spacing = float(1)/int(layers)
        height = 0.5*bulk_spacing
        while height < 1:
            planes.append(height)
            height = height + bulk_spacing
        spacing = bulk_spacing
            
    i = 1  
    while i < n_atoms:
        
        # Read old fractional coordinates for atoms
        atom = lines_f[l_B + i].split()[0]
        S_x  = lines_f[l_B + i].split()[1]
        S_y  = lines_f[l_B + i].split()[2]
        S_z  = lines_f[l_B + i].split()[3]
            
        for plane in planes:
            if plane - 0.001 < float(S_z) < plane + 0.001:
                pass
            elif float(S_z) < plane + 0.5*float(spacing):
                if planes.index(plane) == 0 or float(S_z) > plane - 0.5*float(spacing):
                    if float(S_z) < plane:
                        lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(plane - delta/float(c)) + '\n'
                    elif float(S_z) > plane:
                        lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(plane + delta/float(c)) + '\n'

        i = i + 1
            
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'Final lattice parameters a = b = ' + str(a) + ' and c = ' + str(c) + ' and M-X bond length is ' + str(bondlength)
    return

#****************************************************************************

# Update the .cell file with optimised cell geometry (ONLY TO BE USED FOR BULK MATERIALS!!!!)
def update_cell_bulk( chem, cell_info ):
    global a
    global c
    global bond_length
    a = cell_info[0]
    c = cell_info[1]
    bond_length = cell_info[2]
    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()
    lines_f[1]    = str(a) + ' 0.00 0.00\n'
    b_x           = str(-float(a)*0.5)
    b_y           = str(float(a)*0.866025403784)
    lines_f[2]    = b_x + ' ' + b_y + ' ' + '0.00\n'
    lines_f[3]    = '0.00 0.00 ' + str(c) + '\n'
    delta = ( float(bond_length)**2 - ( (2/float(3))*float(b_y) )**2 )**0.5

    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_B = num
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_E = num
    n_atoms = l_E - l_B

    # Since M atoms are unaffected by the c length change, cylce through atoms
    i = 1  
    while i < n_atoms:
        
        # Read old fractional coordinates for atoms
        atom = lines_f[l_B + i].split()[0]
        S_x  = lines_f[l_B + i].split()[1]
        S_y  = lines_f[l_B + i].split()[2]
        S_z  = lines_f[l_B + i].split()[3]
            
        # Update S atoms
        if float(S_z) < 0.25:
            lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(0.25 - delta/float(c)) + '\n'
        elif float(S_z) > 0.25 and float(S_z) < 0.5:
            lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(0.25 + delta/float(c)) + '\n'
        elif float(S_z) > 0.5 and float(S_z) < 0.75:
            lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(0.75 - delta/float(c)) + '\n'
        elif float(S_z) > 0.75:
            lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(0.75 + delta/float(c)) + '\n'
        elif float(S_z) == 0.25:
            pass
        elif float(S_z) == 0.75:
            pass
                
        i = i + 1

    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'Final lattice parameters a = b = ' + str(a) + ' and c = ' + str(c) + ' and Mo - X bondlength is ' +  str(bond_length) + ' in .cell file'
    config.a           = a
    config.c           = c
    config.cell_info   = cell_info
    config.bond_length = bond_length
    return

#****************************************************************************

# Impose cell constraints within a geometry optimisation
def ch_cell_constraints( chem, cell_constraints_temp ):
    global cell_constraints
    cell_constraints = cell_constraints_temp
    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK CELL_CONSTRAINTS' in line:
            l = num
    lines_f[l+1]    = str(cell_constraints[0]) + ' ' + str(cell_constraints[1]) + ' ' + str(cell_constraints[2]) + ' \n'
    lines_f[l+2]  = str(cell_constraints[3]) + ' ' + str(cell_constraints[4]) + ' ' + str(cell_constraints[5]) + ' \n'
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'cell constraints changed to: a = ' + str(cell_constraints[0]) + ', b = ' + str(cell_constraints[1]) + ', c = ' + str(cell_constraints[2]) + ', alpha = ' + str(cell_constraints[3]) + ', beta = ' + str(cell_constraints[4]) + ', gamma = ' + str(cell_constraints[5])
    config.cell_constraints = cell_constraints
    return   

#****************************************************************************

# Adjust Spin polarisation
def ch_spin( chem, spin_temp ):
    global spin
    spin = str(spin_temp)
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)

    # Remove spin line if already present
    for num, line in enumerate(f):
        if 'spin :' in line:
             del lines_f[num]
 
    f.close()
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()

    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)

    # Specify whether spin polarisation is being used at all
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spin_polarised' in line:
            l = num
    if spin == '0':
        lines_f[l]    = 'spin_polarised : false\n'
    else:
        lines_f[l]    = 'spin_polarised : true\n'
        if spin != 'true':
            lines_f.insert(l, 'spin : ' + str(spin_temp) + '\n')
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    if spin == 'true':
        print 'spin polarisation activated'
    else:
        print 'Spin changed to: ' + str(spin_temp)
    config.spin = spin
    return

#****************************************************************************

# Change the number of empty bands for SCF calculation
def ch_nextra_bands( chem, nextra_bands_temp ):

    global nextra_bands
    nextra_bands = str(nextra_bands_temp)
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)

    # Remove spin line if already present
    for num, line in enumerate(f):
        if 'nextra_bands :' in line and 'spectral' not in line:
             l = num
    lines_f[l] = 'nextra_bands : ' + nextra_bands + '\n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'number of empty extra bands changed to: ' + str(nextra_bands_temp)
    config.nextra_bands = nextra_bands
    return

#****************************************************************************

# Change the number of empty bands for a core EELS calculation
def ch_spectral_nextra_bands( chem, spectral_nextra_bands_temp ):

    global spectral_nextra_bands
    spectral_nextra_bands = str(spectral_nextra_bands_temp)
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)

    # Remove spin line if already present
    for num, line in enumerate(f):
        if 'spectral_nextra_bands :' in line:
             l = num
    lines_f[l] = 'spectral_nextra_bands : ' + spectral_nextra_bands + '\n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'number of empty nextra bands in spectral calculation changed to: ' + str(spectral_nextra_bands_temp)
    config.spectral_nextra_bands = spectral_nextra_bands
    return

#****************************************************************************

# Run optados
def optados(chem, cores):
    import os
    f = open("%s.odo" % chem,'a')
    f.write('\n     \n')
    f.close
    os.system("rm %s.odo" % chem)
    print 'starting optados calculation'
    os.system('mpirun -np ' + str(cores) + ' optados.mpi ' + chem)
    print 'optados calculation complete'
    return

#****************************************************************************

# Run optados on Zener in parallel
def optados_zener( chem, cores ):
    host_comp()
    import subprocess
    import time
    import os
    os.system('cp ~/mypy/run_temp.sh ./' + chem + '.sh')
    f = open(chem + '.sh','r')
    lines_f = f.readlines()

    f.seek(0,0)
    lines_f[3] = '#$ -pe orte  ' + str(cores) + '\n'
    max_time_str = lines_f[5].split()[2].replace('h_rt=','')     # Read the maximum time allowed by mpi from the input file
    max_time = time_in_s( max_time_str )
    lines_f[9] = 'echo ' + str(cores) + '\n'
    lines_f[12] = 'mpirun -np ' + str(cores) + ' optados.mpi ' + chem + '\n'
    f.close()
    f = open(chem + '.sh','w')
    f.writelines( lines_f )
    f.close()
    cmd = 'qsub ' + chem + '.sh'
    finished = 0
    a = 0
    while finished < 1 and a < 10:

        output = subprocess.Popen( cmd, shell = 'true', stdout=subprocess.PIPE ).communicate()[0]
        procpid = output.split()[2]
        aborted = 0
        printed = 0
        start_time = time.time()

        while aborted < 1:

            # Try to open the results file
            try:
                f = open(chem + '.sh.o' + procpid,'r')
                lines_f = f.readlines()
                f.seek(0,0)

                # if the file opens the process must be running
                while printed < 1:
                    print 'mpi job has started running'
                    printed = 1

                # if the final line in the results file contains 'ended' then the process has finished
                # But if 'Fatal error' is in the results file then something has gone wrong so the process should be abandoned regardless
                f.seek(0,0)
                f_read = f.read()
                try:
                    if 'Fatal Error:' in f_read:
                        os.system('qdel ' + str(procpid))
                        print 'Fatal error caused process to fail'
                        aborted = 1
                        a = a + 1
                    elif 'Job ended at:' in f_read:
                        finished = 1
                        aborted = 1
                        print 'process finished'
                    else:
                        time.sleep(5)

                # if the process has not finished, make sure that it has not gone over time and been killed
                except IndexError:
                    time.sleep(5)
                    process_time = time.time() - start_time
                    if process_time > max_time:
                        aborted = 1
                        a = 11
                        print "Process was unable to complete in the maximum allocated time and therefore has been killed by mpi"
                        
            # If process hasn't started yet, wait a few seconds and check again
            except IOError:
                time.sleep(5)
            
                # Make sure process hasn't got stuck and been suspended, if it has, try again
                output = subprocess.Popen( 'qstat', shell = 'true', stdout=subprocess.PIPE ).communicate()[0]
                lines = output.split('\n')
                for line in lines:
                    try:
                        random_proc_id = line.split()[0]
                        if random_proc_id == str(procpid):
                            state = line.split()[4]
                            if state == 'Eqw':
                                os.system('qdel ' + str(procpid))
                                print 'Process became suspended so trying again'
                                a = a + 1
                                aborted = 1
                    except IndexError:
                        pass
                        
    if finished == 1:
        print 'optados finished running in parallel using ' + str(cores) + ' cores'
    elif a == 10:
        print 'Process became suspended 10 times and therefore attempts at this simulation have been aborted'
    return finished

#****************************************************************************

# Update 2D cell a and bond length (ONLY TO BE USED FOR 2D NANOMATERIALS!)
def update_cell_2D( chem, cell_info ):
    global a
    global c
    global bond_length
    a = cell_info[0]
    c = cell_info[1]
    c_actual = c
    bond_length = cell_info[2]
    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()
    lines_f[1]    = str(a) + ' 0.00 0.00\n'
    b_x           = str(-float(a)*0.5)
    b_y           = str(float(a)*0.866025403784)
    lines_f[2]    = b_x + ' ' + b_y + ' ' + '0.00\n'
    lines_f[3]    = '0.00 0.00 ' + str(c_actual) + '\n'
    delta = ( float(bond_length)**2 - ( (2/float(3))*float(b_y) )**2 )**0.5

    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_B = num
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_E = num
    n_atoms = l_E - l_B

    # Since Mo atoms are unaffected by the c length change, cylce through atoms
    i = 1  
    while i < n_atoms:
        
        # Read old fractional coordinates for atoms
        atom = lines_f[l_B + i].split()[0]
        S_x  = lines_f[l_B + i].split()[1]
        S_y  = lines_f[l_B + i].split()[2]
        S_z  = lines_f[l_B + i].split()[3]
        
        # Update atoms
        if float(S_z) < 0.5:
            lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(0.5 - delta/float(c_actual)) + '\n'
        elif float(S_z) > 0.5:
            lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(0.5 + delta/float(c_actual)) + '\n'
        elif float(S_z) == 0.5:
            pass
                
        i = i + 1

    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'Final lattice parameters a = b = ' + str(a) + ' and c = ' + str(c) + ' and Mo - X bondlength is ' +  str(bond_length) + ' in .cell file'
    print '****** NOTE: C PARAMETER IS FOR ENTIRE UNIT CELL ********' 
    config.a           = a
    config.c           = c
    config.cell_info   = cell_info
    config.bond_length = bond_length
    return

#****************************************************************************

# Extract cell information from a geometry optimisation .castep output file
def get_cell_info_geom( filename ):
    global a
    global c
    global bond_length
    global cell_info
    f = open(filename,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    
    # Find finalised cell information
    for num, line in enumerate(f):
        if 'BFGS : Final Configuration:' in line:
            l_start = num
    
    # Extract lattice parameters
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'alpha =' in line and num > l_start:
            l_a = num
    a = lines_f[l_a].split()[2] # lattice parameter a

    f.seek(0,0)
    for num, line in enumerate(f):
        if 'gamma =' in line and num > l_start:
            l_c = num
    c = str(lines_f[l_c].split()[2]) # lattice parameter c (for the cell!)
    
    # Extract Bond lengths
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'S 1 -- Mo 1' in line and num > l_start:
            l_bl = num
            bonding = 'S 1 -- Mo 1'
            bondlength = str(lines_f[l_bl].split()[6])
        elif 'O 1 -- Mo 1' in line and num > l_start:
            l_bl = num
            bonding = 'O 1 -- Mo 1'
            bondlength = str(lines_f[l_bl].split()[6])
        elif 'S 1 -- W 1' in line and num > l_start:
            l_bl = num
            bonding = 'S 1 -- W 1'
            bondlength = str(lines_f[l_bl].split()[6])
        elif 'O 1 -- W 1' in line and num > l_start:
            l_bl = num
            bonding = 'O 1 -- W 1'
            bondlength = str(lines_f[l_bl].split()[6])

    f.close()
    cell_info = [a, c, bondlength]
    
    print 'Final lattice parameters a = b = ' + a + ' and c = ' + c + ' and ' + bonding + ' bondlength is ' +  bondlength
    config.a           = a
    config.c           = c
    config.cell_info   = cell_info
    config.bondlength = bondlength
    return

#****************************************************************************

# Get interplanar spacing from .castep output file for H-MX2 type compound
def get_interplanar_spacing(filename, BFGS_iteration='final',plane=0):
    global interplanar_spacing
    get_cell_geom_complete(filename, BFGS_iteration)

    Mo_list = []
    W_list  = []

    for element in config.cell_complete:
        atom = element.split()[0]
        z    = float(element.split()[3])

        if atom == 'Mo':
            Mo_list.append(z)
            
        if atom == 'W':
            W_list.append(z)

    # Interplanar Spacing
    if Mo_list != []:
        atom_list = Mo_list
    elif W_list != []:
        atom_list = W_list
    if max(atom_list) - min(atom_list) > 1.0/float(config.c):
        atom_0 = sorted(atom_list)[plane]
        for atom in sorted(atom_list):
            if atom > atom_0 + 1.0/float(config.c):
                interplanar_spacing = (atom - atom_0)*float(config.c)
                break
    else:
        interplanar_spacing = float(config.c)

    config.interplanar_spacing = interplanar_spacing
    return interplanar_spacing


#****************************************************************************

# Extract cell info from a .cell file
def get_cell_info( chem ):
    global a
    global c
    global bond_length
    global cell_info
    global interplanar_spacing
    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()

    a = lines_f[1].split()[0] # lattice parameter a
    c = lines_f[3].split()[2] # lattice parameter c
    d = (3**(-0.5))*float(a)

    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_B = num
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_E = num
    n_atoms = l_E - l_B

    # Cylce through atoms
    Mo_list = [1]
    W_list  = [1]
    S_list  = [1]
    O_list  = [1]
    i = 1  

    while i < n_atoms:
        
        atom = lines_f[l_B + i].split()[0]
        z    = float(lines_f[l_B + i].split()[3])

        if atom == 'Mo':
            Mo_list.append(z)

        if atom == 'W':
            W_list.append(z)

        if atom == 'S':
            S_list.append(z)
            
        if atom == 'O':
            O_list.append(z)
        
        i = i + 1

    Mo_z = min(Mo_list)
    W_z  = min(W_list)
    S_z  = min(S_list)
    O_z  = min(O_list)

    if S_z != 1 and Mo_z != 1:
        delta_S = (Mo_z - S_z)*float(c)
        bond_length_S = str((delta_S**2 + d**2)**0.5)
    elif O_z != 1 and Mo_z != 1:
        delta_S = (Mo_z - O_z)*float(c)
        bond_length_O = str((delta_O**2 + d**2)**0.5)
    elif S_z != 1 and W_z != 1:
        delta_S = (W_z - S_z)*float(c)
        bond_length_S = str((delta_S**2 + d**2)**0.5)
    elif O_z != 1 and W_z != 1:
        delta_S = (W_z - O_z)*float(c)
        bond_length_O = str((delta_O**2 + d**2)**0.5)

    bond_length_S = str((delta_S**2 + d**2)**0.5)
    bond_length_O = str((delta_O**2 + d**2)**0.5)

    if Mo_z != 1:
        if O_z != 1 and S_z == 1:
            bond_length = bond_length_O
            bonding = 'Mo - O'
        else:
            bond_length = bond_length_S
            bonding = 'Mo - S'
    elif W_z != 1:
        if O_z != 1 and S_z == 1:
            bond_length = bond_length_O
            bonding = 'W - O'
        else:
            bond_length = bond_length_S
            bonding = 'W - S'

    # Interplanar Spacing
    if Mo_z != 1:
        atom_list = Mo_list
    elif W_z != 1:
        atom_list = W_list
    if max(atom_list) - min(atom_list) > 1:
        atom_0 = min(atom_list)
        for atom in sorted(atom_list):
            if atom > atom_O + 1:
                interplanar_spacing = atom - atom_O
                break
    else:
        interplanar_spacing = c

    f.close()
    cell_info = [a, c, bond_length, interplanar_spacing]
    print 'Final lattice parameters a = b = ' + a + ' and c = ' + c + ' and ' + bonding + ' bondlength is ' +  bond_length + ' and interplanar spacing is ' + str(interplanar_spacing)
    config.a                   = a
    config.c                   = c
    config.cell_info           = cell_info
    config.bond_length         = bond_length
    config.interplanar_spacing = interplanar_spacing
    return

#****************************************************************************

# Change an arbitary input parameter
def ch_ipar( chem, ipar, ipar_value ):
    if ipar == 'cutoff_Energy':
        ch_cutoff_Energy( chem, ipar_value )
    elif ipar == 'kpoints':
        ch_kpoints( chem, [ipar_value, ipar_value, ipar_value] )
    elif ipar == 'spectral_kpoints':
        ch_spectral_kpoints( chem, [ipar_value, ipar_value, ipar_value] )
    elif ipar == 'offset':
        ch_offset( chem, [ipar_value, ipar_value, ipar_value] )
    elif ipar == 'kpoints_xy':
        ch_kpoints( chem, [ipar_value, ipar_value, 0] )
    elif ipar == 'spectral_kpoints_xy':
        ch_spectral_kpoints( chem, [ipar_value, ipar_value, 0] )
    elif ipar == 'c_2D':
        ch_c_2D( chem, ipar_value )
    elif ipar == 'c_bi':
        ch_c_bi( chem, ipar_value )
    elif ipar == 'c_bulk':
        ch_c_bulk( chem, ipar_value )
    elif ipar == 'nextra_bands':
        ch_nextra_bands( chem, ipar_value )
    return

#****************************************************************************

#  Retrieve an arbitary output parameter
def get_opar( opar, filename ):
    global opar_value

    if opar == 'a':
        global a
        f = open(filename,'r')
        lines_f  = f.readlines()
        f.seek(0,0)
        
        # Find finalised cell information
        for num, line in enumerate(f):
            if 'BFGS : Final Configuration:' in line:
                l_start = num
                
        # Extract lattice parameters
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'alpha =' in line and num > l_start:
                l_a = num
        a = lines_f[l_a].split()[2] # lattice parameter a
        opar_value = a
        f.close()

    elif opar == 'bond_length':
        global bond_length
        f = open(filename,'r')
        lines_f  = f.readlines()
        f.seek(0,0)
        # Extract Bond lengths
        for num, line in enumerate(f):
            if 'S 1 -- Mo 1' in line and num > l_start:
                l_bl = num
            elif 'O 1 -- Mo 1' in line and num > l_start:
                l_bl = num
            elif 'S 1 -- W 1' in line and num > l_start:
                l_bl = num
            elif 'O 1 -- W 1' in line and num > l_start:
                l_bl = num
        bond_length = lines_f[l_bl].split()[6]
        opar_value = bond_length
        f.close()

    elif opar == 'total_Energy':
        get_total_Energy( filename)
        opar_value = total_Energy
        
    config.opar_value = opar_value
    return

#****************************************************************************

# Changes the c parameter for a bulk material (only to be used for bulk materials with 2 LAYERS PER CELL for equal layer separation!)
def ch_c_bulk( chem, c_temp, layers=2):
    global c
    c = c_temp
    f = open('%s.cell' % chem,'r')

    # Record old c and print new c to file
    lines_f  = f.readlines()
    c_old = lines_f[3].split()[2]
    lines_f[3]    = '0.00 0.00 ' + str(c) + '\n'

    # Write new fractional cell coordinates of atoms
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_B = num
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_E = num
    n_atoms = l_E - l_B

    # Need to work out the 'height' of the Mo planes given the number of equally spaced layers in the cell
    planes = []
    spacing = float(1)/int(layers)
    height = 0.5*spacing
    while height < 1:
        planes.append(height)
        height = height + spacing

    # Cylce through atoms
    i = 1  
    while i < n_atoms:
        
        # Read old fractional coordinates for S atom
        atom = lines_f[l_B + i].split()[0]
        S_x  = lines_f[l_B + i].split()[1]
        S_y  = lines_f[l_B + i].split()[2]
        S_z  = lines_f[l_B + i].split()[3]
            
        for plane in planes:
            if float(S_z) < plane + 0.5*spacing:
                if planes.index(plane) == 0 or float(S_z) > plane - 0.5*spacing:
                    delta = float(c_old)*(plane-float(S_z))
                    lines_f[l_B + i] = atom + '\t' + S_x + '\t' + S_y + '\t' + str(plane - delta/float(c)) + '\n'
            elif float(S_z) == plane + 0.5*spacing:
                pass

        i = i + 1

    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'c lattice parameter changed to: ' + str(c) + ' for ' + str(layers) + ' layered bulk structure in .cell file'
    config.c = c
    return

#****************************************************************************

# Remove any file (whether it exists or not)
def file_remove( filename ):
    import os
    f = open(filename,'a')
    f.write('\n     \n')
    f.close
    os.system("rm %s" % filename)
    return

#****************************************************************************

# Copy any file
def file_copy( filename, dirname, new_filename ):
    import os
    tag = filename + ' ' + dirname + '/' + new_filename
    try:
        f = open(filename,'r')
        os.system("cp %s" % tag)
    except IOError:
        pass
    return

#****************************************************************************

# Automaticically transfer files to a directory on different machine
# Requires a key to be set up otherwise a password will be requested
# Note dirname includes directory path
def file_transfer( filename, dest_comp, dirname, new_filename ):
    import os
    if dest_comp == 'same machine':
        file_copy( filename, dirname, new_filename )
    else:
        tag = filename + ' ' + dest_comp + ':' + dirname + '/' + new_filename
        try:
            f = open(filename,'r')
            os.system("scp %s" % tag)
        except IOError:
            pass
    return

#****************************************************************************

# Remove all output files from a castep calculation (to tidy up the workspace)
def castep_cleanup(chem):
    import os
    
    # List all the file endings
    L = ['.castep', '.castep_bin', '.bands', '-out.cell', '.chdiff','.check', '.check_bak', '.den_fmt', '.dome_bin', '.cst_esp', '.bib', '.pdos_bin', '.odo', '.adaptive.agr', '.adaptive.dat', '.orbitals', '.geom', '.elnes_bin', '.pdos.dat', '.DOS.odo', '.PDOS.odo', '.core.odo', '_core_edge.agr', '_core_edge.dat','.0001.err','.ome_bin']
    
    # Remove each file
    for item in L:
             filename = chem + item
             file_remove( filename )
  
    print 'old castep output files removed'
    return

#****************************************************************************

# Remove all OptaDOS output files which would have been copied in optaos_copy
def optados_cleanup(chem):

    # List all the file endings
    L = ['.pdos_bin','.odo', '.pdos.dat', '.DOS.odo', '.PDOS.odo', '.core.odo', '_core_edge.agr', '_core_edge.dat', '.opt_err']
    graphs = ['_conductivity','.adaptive','_absorption','_epsilon','_loss_fn','_reflection','_refractive_index']
    graph_extns = ['.agr','.dat']

    for graph in graphs:
        for extn in graph_extns:
            L.append(graph + extn)


    # Remove each file
    for item in L:
             filename = chem + item
             file_remove( filename )
  
    print 'old OptaDOS output files removed'
    return

#****************************************************************************

# Removes all temporary unreadable files used for disc memory during calculations
def temp_file_cleanup():
    import os

    # Remove temporary disc storage files
    L = ['fort','core.']

    # Remove all files
    for item in L:
             filename = item + '*'
             file_remove( filename )
    
    print 'all temporary disc storage files removed'
    return

#****************************************************************************

# Copy all output files to a new directory (to save for later inspection)
def castep_copy(chem, dirname, new_tag, comp='same machine', check=1, DOS_calc=''):
    import os
    
    # List all the file endings
    L = ['.bands', '.odi', '.param', '.castep', '.cell', '-out.cell', '.chdiff', '.den_fmt', '.dome_bin', '.cst_esp', '.bib', '.pdos_bin', '.odo', '.adaptive.agr', '.adaptive.dat', '.orbitals', '.geom', '.elnes_bin', '.pdos.dat', '.DOS.odo', '.PDOS.odo', '.core.odo', '_core_edge.agr', '_core_edge.dat','.0001.err','.opt_err']

    if check == 1:
        L.append('.check')

    # Copy each file
    for item in L:
        filename = chem + item
        new_filename = new_tag + DOS_calc + item
        if comp == 'same machine':
            file_copy( filename, dirname, new_filename )
        else:
            file_transfer( filename, comp, dirname, new_filename )

    print 'old castep output files copied to directory: ' + dirname + ' on ' + comp
    return

#****************************************************************************

# Copy all output files originating only from an optados calculation
def optados_copy(chem, dirname, new_tag, comp='same machine', DOS_calc=''):
    import os
    
    # List all the file endings
    L = ['.pdos_bin', '.odi', '.odo', '.pdos.dat', '.DOS.odo', '.PDOS.odo', '.core.odo', '_core_edge.agr', '_core_edge.dat', '.opt_err']
    graphs = ['_conductivity','.adaptive','_absorption','_epsilon','_loss_fn','_reflection','_refractive_index']
    graph_extns = ['.agr','.dat']

    for graph in graphs:
        for extn in graph_extns:
            L.append(graph + extn)

    # Copy each file
    for item in L:
        filename = chem + item
        new_filename = new_tag  + DOS_calc + item
        if comp == 'same machine':
            file_copy( filename, dirname, new_filename )
        else:
            file_transfer( filename, comp, dirname, new_filename )

    print 'old optados output files copied to directory: ' + dirname + ' on ' + comp
    return

#****************************************************************************

# Plot Bandstructure of only interesting bands around the bandgap
def plot_BS( filename, bg_min_temp, bg_max_temp, output='xg', Fermi_Energy_temp='.castep' ):
    global bg_min
    global bg_max
    bg_min = bg_min_temp
    bg_max = bg_max_temp

    # Get Fermi Energy and calculate min and max Energy values
    if Fermi_Energy_temp == '.castep':
        Fermi_file = filename.replace('.bands','.castep')
        get_Fermi_Energy(Fermi_file)
        Fermi_Energy = config.Fermi_Energy
    elif Fermi_Energy_temp == '.odo':
        Fermi_file = filename.replace('.bands','.odo')
        get_Fermi_Energy(Fermi_file)
        Fermi_Energy = config.Fermi_Energy
    else:
        Fermi_Energy = Fermi_Energy_temp
    ymin = float(Fermi_Energy) - float(bg_min)
    ymax = float(Fermi_Energy) + float(bg_max)

    # Import and rewrite dispersion.pl file
    import os
    os.system("cp /home/ablitt/bin/dispersion_BG.pl dispersion_temp.pl")
    f = open('dispersion_temp.pl','r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $ymin ' in line:
            l = num
    lines_f[l]    = 'my $ymin = ' + str(ymin) + ';\n'
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $ymax ' in line:
            l = num
    lines_f[l]    = 'my $ymax = ' + str(ymax) + ';\n'

    f.close()
    f = open('dispersion_temp.pl','w')
    f.writelines( lines_f )
    f.close()
    os.system("cp dispersion_temp.pl /home/ablitt/bin/dispersion_BG.pl")

    # Run dispersion.pl file
    if output == 'jpg':
        os.system("dispersion_BG.pl -jpg -bs -symmetry hexagonal " + filename )
    elif output == 'xg':
        os.system("dispersion_BG.pl -xg -bs -symmetry hexagonal " + filename )

    # Remove dispersion.pl file so as not to clutter/confuse directory
    os.system("rm dispersion_temp.pl")    
    
    return

#****************************************************************************

def plot_EELS_PDOS(EELS_filename, PDOS_filename, bands_filename, Emax, DOS_filename=0, output='xg', Fermi_Energy_temp='.castep', Emin=-2):
    lines_bat = []

    # Plot the CORE-LOSS EELS graph
    if bands_filename != 0 and PDOS_filename != 0:
        lines_bat.append('ARRANGE(3, 1, 0.1, 0.35, 0.1)\n')
    else:
        lines_bat.append('ARRANGE(2, 1, 0.1, 0.35, 0.1)\n')
    lines_bat.append('READ BLOCK "' + EELS_filename + '"\n')
    lines_bat.append('BLOCK xy "1:2"\n')
    lines_bat.append('BLOCK xy "1:3"\n')
    if bands_filename != 0 and PDOS_filename != 0:
        lines_bat.append('view 0.090000, 0.560000, 1.090000, 0.880000\n')
    elif bands_filename != 0 and PDOS_filename == 0:
        lines_bat.append('view 0.090000, 0.260000, 1.090000, 0.880000\n')
    elif bands_filename == 0 and PDOS_filename != 0:
        lines_bat.append('view 0.090000, 0.5050000, 1.090000, 0.880000\n')
    get_Fermi_Energy(EELS_filename.replace('_core_edge.dat','.odo'))
    EELS_Fermi_offset = str(config.Fermi_Energy)
    lines_bat.append('S0.x = S0.x - ' + EELS_Fermi_offset + '\n')
    lines_bat.append('S0 LINEWIDTH 2\n')
    lines_bat.append('S1.x = S1.x - ' + EELS_Fermi_offset + '\n')
    lines_bat.append('S1.y = S1.y*6\n')
    lines_bat.append('S1 LINEWIDTH 2\n')
    lines_bat.append('S1 LINESTYLE 3\n')
    lines_bat.append('S1 LINE COLOR 1\n')
    lines_bat.append('S0 LEGEND "\\f{Helvetica}Unbroadened"\n')
    lines_bat.append('S1 LEGEND "\\f{Helvetica}Broadened"\n')
    lines_bat.append('LEGEND 0.8, 0.8\n')
    lines_bat.append('LEGEND fram linewidth 2\n')
    lines_bat.append('xaxis tick major linewidth 2.5\n')
    lines_bat.append('xaxis tick minor linewidth 2.5\n')
    lines_bat.append('xaxis  bar linewidth 2.5\n')
    lines_bat.append('yaxis tick major linewidth 2.5\n')
    lines_bat.append('yaxis tick minor linewidth 2.5\n')
    lines_bat.append('yaxis  bar linewidth 2.5\n')
    lines_bat.append('yaxis ticklabel off\n')
    lines_bat.append('xaxis ticklabel off\n')
    lines_bat.append('world xmax ' + str(Emax) + '\n')
    lines_bat.append('world xmin ' + str(Emin) + '\n')
    lines_bat.append('yaxis label "\\f{Helvetica}EELS"\n')
    lines_bat.append('AUTOSCALE YAXES\n')
    lines_bat.append('AUTOTICKS\n')
    lines_bat.append('title "\\f{Helvetica}Core-loss Spectrum and PDOS for 3x1x3 MoO\s3\N"\n')
    lines_bat.append('subtitle "\\f{Helvetica}Calculated using LDA for excited O:1 atom"\n')

    # Plot the DOS and PDOS graph
    lines_bat.append('WITH G1\n')

    # Plot the total DOS if it is required
    first_graph = 0
    if DOS_filename != 0:
        lines_bat.append('READ "' + DOS_filename + '"\n')
        lines_bat.append('S0 LEGEND "\\f{Helvetica}DOS"\n')
        lines_bat.append('S0 LINE COLOR 7\n')
        lines_bat.append('S0 LINEWIDTH 2\n')
        first_graph = 1
    
    # Find out what projectors are in the PDOS file and colour and name the lines accordingly
    if PDOS_filename != 0:
        
        f = open( PDOS_filename, 'r')
        lines_f = f.readlines()
    
        projectors = []
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'Projector:' in line or 'Column:' in line:
                proj  = lines_f[num].split()[2]
                name  = lines_f[num+2].split()[1] + '(' + lines_f[num+2].split()[3] + ')'
                projectors.append(name)

        colour_table = {'S(s)':5,'S(p)':11,'S(d)':7,'O(s)':13,'O(p)':2,'O(d)':10,'O*(s)':15,'O*(p)':3,'Mo(s)':14,'Mo(p)':12,'Mo(d)':4} 

        n_projs = len(projectors)

        f.close()

        lines_bat.append('READ NXY "' + PDOS_filename + '"\n')

        for projector in projectors:
            colour     = str(colour_table[projector])
            legend     = projector
            line_index = str(projectors.index(projector) + first_graph)

            lines_bat.append('S' + line_index + ' LINE COLOR ' + colour + '\n')
            lines_bat.append('S' + line_index + ' LINEWIDTH 2\n')
            lines_bat.append('S' + line_index + ' LEGEND "\\f{Helvetica}' +  legend  + '"\n')
        if bands_filename != 0:
            lines_bat.append('view 0.090000, 0.250000, 1.090000, 0.550000\n')
            lines_bat.append('xaxis ticklabel off\n')
        else:
            lines_bat.append('view 0.090000, 0.15000, 1.090000, 0.495000\n')
            lines_bat.append('xaxis ticklabel on\n')
            lines_bat.append('xaxis label "\\f{Helvetica}Energy (eV)"\n')
        lines_bat.append('xaxis tick major linewidth 2.5\n')
        lines_bat.append('xaxis tick minor linewidth 2.5\n')
        lines_bat.append('xaxis  bar linewidth 2.5\n')
        lines_bat.append('yaxis tick major linewidth 2.5\n')
        lines_bat.append('yaxis tick minor linewidth 2.5\n')
        lines_bat.append('yaxis  bar linewidth 2.5\n')
        lines_bat.append('yaxis ticklabel off\n')
        lines_bat.append('world xmax ' + str(Emax) + '\n')
        lines_bat.append('world xmin ' + str(Emin) + '\n')
        lines_bat.append('yaxis label "\\f{Helvetica}PDOS"\n')
        lines_bat.append('AUTOSCALE YAXES\n')
        lines_bat.append('world ymin 0\n')
        lines_bat.append('AUTOTICKS\n')
        lines_bat.append('LEGEND 1.1,0.68\n')
        lines_bat.append('LEGEND fram linewidth 2\n')

    if bands_filename != 0:

        # PLot the graph of the real wavefunctions at the gamma point
        if PDOS_filename != 0:
            lines_bat.append('WITH G2\n')
        else:
            lines_bat.append('WITH G1\n')
        
        # Find the Fermi energy by which to shift the band energies
        get_Fermi_Energy(EELS_filename.replace('_core_edge.dat',Fermi_Energy_temp))
        #get_Fermi_Energy(Fermi_Energy_temp)
        Fermi_offset = float(config.Fermi_Energy)
        print 'Fermi offset is ' + str(Fermi_offset) + 'eV'

        f = open( bands_filename, 'r')
        lines_f = f.readlines()
        f.seek(0,0)
        
        for line in lines_f:
            if 'Number of eigenvalues' in line:
                n_bands = int(line.split()[3])

        print 'number of bands: ' + str(n_bands)
        
        l_k = 9
        for num, line in enumerate(f):
            if 'K-point' in line and '0.00000000  0.00000000  0.00000000' in line:
                l_k = num

        bands = []
    
        i = 0
        while i < n_bands:
            bands.append(27.21138386*float(lines_f[l_k + 2 + i].split()[0]) - Fermi_offset)
            i = i + 1

        f.close()

        spacing = (1.5/32)*(float(Emax)-float(Emin))
        
        gamma_bands = []
        old_band  = bands[0]-0.5*spacing
        last_band = old_band
        for band in bands:
            if band >= old_band + spacing:
                gamma_bands.append(str(band) + '\t0\t' + str(bands.index(band) + 1) + '\n')
                #print str(band) + '\t0\t' + str(bands.index(band) + 1) + '\n'
                last_band = band
            elif band >= last_band + 2*spacing:
                gamma_bands.append(str(band) + '\t0\t' + str(bands.index(band) + 1) + '\n')
                #print str(band) + '\t0\t' + str(bands.index(band) + 1) + '\n'
                last_band = band
            else:
                gamma_bands.append(str(band) + '\t0\t""\n')
                #print str(band) + '\t0\t""\n'
            old_band = band

        f = open('gamma_bands.dat','w')
        f.writelines(gamma_bands)
        f.close()

        lines_bat.append('READ BLOCK "gamma_bands.dat"\n')
        lines_bat.append('BLOCK XY "1:2:3"\n')
        lines_bat.append('view 0.090000, 0.090000, 1.090000, 0.240000\n')
        lines_bat.append('xaxis tick major linewidth 2.5\n')
        lines_bat.append('xaxis tick minor linewidth 2.5\n')
        lines_bat.append('xaxis  bar linewidth 2.5\n')
        lines_bat.append('yaxis tick major linewidth 2.5\n')
        lines_bat.append('yaxis tick minor linewidth 2.5\n')
        lines_bat.append('yaxis  bar linewidth 2.5\n')
        lines_bat.append('world xmax ' + str(Emax) + '\n')
        lines_bat.append('world xmin ' + str(Emin) + '\n')
        lines_bat.append('AUTOSCALE YAXES\n')
        lines_bat.append('AUTOTICKS\n')
        lines_bat.append('yaxis tick major 2\n')
        lines_bat.append('world ymax 1\n')
        lines_bat.append('world ymin -1\n')
        lines_bat.append('xaxis label "\\f{Helvetica}Energy (eV)"\n')
        lines_bat.append('S0 avalue on\n')
        lines_bat.append('S0 avalue type "string"\n')
        lines_bat.append('S0 avalue offset 0.0, 0.01\n')
        lines_bat.append('S0 linestyle 0\n')
        lines_bat.append('S0 symbol 9\n')
        lines_bat.append('yaxis tick spec type both\n')
        lines_bat.append('yaxis tick spec 1\n')
        lines_bat.append('yaxis tick major 0, 0\n')
        lines_bat.append('yaxis ticklabel 0, "\\xG"\n')
        lines_bat.append('S1 POINT ' + str(Emin) + ', 0\n')
        lines_bat.append('S1 POINT ' + str(Emax) + ', 0\n')
        lines_bat.append('S1 LINE COLOR 1\n')

    f = open('EELS_PDOS.bat','w')
    f.writelines(lines_bat)
    f.close()
    
    import os
    if output == 'xg':
        os.system("xmgrace -batch EELS_PDOS.bat")
    elif output == 'jpeg' or output == 'jpg':
        os.system("xmgrace -nosafe -hdevice JPEG -batch EELS_PDOS.bat")

    return

#****************************************************************************

# Plot Bandstructure of only interesting bands around the bandgap.... BE CAREFUL WITH THE ORDERING OF ARGUMENTS!!!!
def plot_BS_PDOS( BS_filename, PDOS_filename, bg_min_temp, bg_max_temp, output='xg', Fermi_Energy_temp='.odo', DOS_max=0, total_DOS_filename=0, spec_colour=1, set_colours=0, symmetry='hexagonal'):
    global bg_min
    global bg_max
    bg_min = bg_min_temp
    bg_max = bg_max_temp

    # Get Fermi Energy and calculate min and max Energy values
    # Since .odo files can have a number of possible endings e.g. .DOS.odo/.PDOS.odo then keep cycling through .odo files if the first does not exist until one does
    # If no .odo file can be found then use a .castep file
    if Fermi_Energy_temp == '.castep':
        Fermi_file = BS_filename.replace('.bands','.castep')
        get_Fermi_Energy(Fermi_file)
        Fermi_Energy = config.Fermi_Energy
    elif Fermi_Energy_temp == '.odo':
            Fermi_file = PDOS_filename.replace('.pdos.dat','.odo')
            finished = get_Fermi_Energy(Fermi_file)
            if finished == 0:
                Fermi_file = PDOS_filename.replace('.pdos.dat','.PDOS.odo')
                finished = get_Fermi_Energy(Fermi_file)
                if finished == 0:
                    Fermi_file = PDOS_filename.replace('.pdos.dat','.DOS.odo')
                    finished = get_Fermi_Energy(Fermi_file)
                    if finished == 0:
                        print 'Fermi Energy could not be found in any .odo file so taking Fermi energy from .castep file'
                        Fermi_file = BS_filename.replace('.bands','.castep')
                        get_Fermi_Energy(Fermi_file)
            Fermi_Energy = config.Fermi_Energy
    else:
        Fermi_Energy = Fermi_Energy_temp
    ymin = float(Fermi_Energy) - float(bg_min)
    ymax = float(Fermi_Energy) + float(bg_max)

    # Import and rewrite dispersion.pl file
    import os
    os.system("cp /home/ablitt/bin/dispersion_BG_DOS_coloured.pl dispersion_temp.pl")
    f = open('dispersion_temp.pl','r')
    lines_f  = f.readlines()
    # Replace bands ymin
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $ymin_bands ' in line:
            l = num
    lines_f[l]    = 'my $ymin_bands = ' + str(ymin) + ';\n'
    # Replace bands ymax
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $ymax_bands ' in line:
            l = num
    lines_f[l]    = 'my $ymax_bands = ' + str(ymax) + ';\n'
    # Replace DOS ymin
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $ymin_DOS ' in line:
            l = num
    lines_f[l]    = 'my $ymin_DOS = ' + str(-float(bg_min)) + ';\n'
    # Replace DOS ymax
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $ymax_DOS ' in line:
            l = num
    lines_f[l]    = 'my $ymax_DOS = ' + str(bg_max) + ';\n'
    # Replace .pdos.dat filename
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $file_PDOS ' in line:
            l = num
    lines_f[l]    = 'my $file_PDOS = "' + PDOS_filename + '";\n'
    # Replace DOS_max
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'my $DOS_max ' in line:
            l = num
    lines_f[l]    = 'my $DOS_max = ' + str(DOS_max) + ';\n'

    # Activate maximum DOS value if necessary
    if DOS_max == 0:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'S0 LEGEND' in line:
                l = num
                if '#' in lines_f[l-4]:
                    lines_f[l-4] = lines_f[l-4].replace('#','p')
                    lines_f[l-3] = lines_f[l-3].replace('p','#')
    else:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'S0 LEGEND' in line:
                l = num
                if '#' in lines_f[l-3]:
                    lines_f[l-3] = lines_f[l-3].replace('#','p')
                    lines_f[l-4] = lines_f[l-4].replace('p','#')

# Read indices from .pdos.dat file

    h = open( PDOS_filename, 'r')
    lines_h = h.readlines()
    
    projectors = []
    h.seek(0,0)
    for num, line in enumerate(h):
        if 'Projector:' in line:
            proj  = lines_h[num].split()[2]
            name  = lines_h[num+2].split()[1] + '(' + lines_h[num+2].split()[3] + ')'
            print 'projector ' + proj + ' is ' + name
            projectors.append(name)

# Ensure that correct number of pdos lines are imported from .pdos.dat file

    f.seek(0,0)
    for num, line in enumerate(f):
        if 'KILL BLOCK' in line:
            l_b = num + 1
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'WORLD YMIN' in line:
            l_e = num
    old_bands = l_e - l_b
        
    del lines_f[l_b+1:l_e]
    lines_to_insert = []
    lines_to_insert.append('    print   "\@BLOCK xy \\"2:1\\"\\n";\n')

    for projector in projectors:
        column = str(projectors.index(projector) + 2) + ':1'
        lines_to_insert.append('    print   "\@BLOCK xy \\"' +  column  + '\\"\\n";\n')

    lines_f[l_e-old_bands+1:l_e-old_bands+1] = lines_to_insert

# Since lines have been deleted, the document has changed length so need to close, rewrite and then reopen for further editing
    f.close()
    f = open('dispersion_temp.pl','w')
    f.writelines( lines_f )
    f.close()
    f = open('dispersion_temp.pl','r')
    lines_f  = f.readlines()
    f.seek(0,0)


    # If total_DOS are required, import data (i.e. the total_DOS_filename option is non zero and equal to a data file name)
    # Be careful here with altering the ordering of text in the dispersion_BG_DOS.pl file because the following arguments rely on lines within the chunck being inserted into the grace file being in a certain order
    if total_DOS_filename == 0:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'y $file_DOS' in line:
                l = num
                if 'm' in lines_f[l]:
                    lines_f[l] = lines_f[l].replace('m','#')
                f.seek(0,0)
                for num, line in enumerate(f):
                    if 'KILL BLOCK' in line:
                        l = num
                        if 'p' in lines_f[l]:
                            lines_f[l-1] = lines_f[l-1].replace('p','#')     # Hide import data for total_DOS from .dat
                            lines_f[l-2] = lines_f[l-2].replace('p','#')     # Hide read data for total_DOS from .dat
                            lines_f[l] = lines_f[l].replace('p','#')         # Hide 'KILL BLOCK' for total_DOS from .dat
                            lines_f[l+2] = lines_f[l+2].replace('#','p')     # Activate import extra S0 2:1 from .pdos.dat file
                            
                f.seek(0,0)
                for num, line in enumerate(f):
                    if 'S0 LEGEND' in line:
                        l = num
                        if 'p' in lines_f[l]:
                            lines_f[l] = lines_f[l].replace('p','#')         # Hide total_DOS legend
                f.seek(0,0)
                for num, line in enumerate(f):
                    if 'KILL G1.S0' in line:
                        l = num
                        if '#' in lines_f[l]:
                            lines_f[l] = lines_f[l].replace('#','p')         # Activate kill extra S0 2:1 from .pdos.dat file
    else:
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'y $file_DOS' in line:
                l = num
                lines_f[l] = 'my $file_DOS = "' + total_DOS_filename + '";\n'
                f.seek(0,0)
                for num, line in enumerate(f):
                    if 'KILL BLOCK' in line:
                        l = num
                        if '#' in lines_f[l]:
                            lines_f[l-1] = lines_f[l-1].replace('#','p')     # Activate import data for total_DOS from .dat
                            lines_f[l-2] = lines_f[l-2].replace('#','p')     # Activate read data for total_DOS from .dat
                            lines_f[l] = lines_f[l].replace('#','p')         # Activate 'KILL BLOCK' for total_DOS from .dat
                            lines_f[l+2] = lines_f[l+2].replace('p','#')     # Hide import extra S0 2:1 from .pdos.dat file
                            
                f.seek(0,0)
                for num, line in enumerate(f):
                    if 'S0 LEGEND' in line:
                        l = num
                        if '#' in lines_f[l]:
                            lines_f[l] = lines_f[l].replace('#','p')         # Activate total_DOS legend
                f.seek(0,0)
                for num, line in enumerate(f):
                    if 'KILL G1.S0' in line:
                        l = num
                        if 'p' in lines_f[l]:
                            lines_f[l] = lines_f[l].replace('p','#')         # Hide kill extra S0 2:1 from .pdos.dat file

# Insert lines between S0 entry (total DOS line) and kill S0 line, killing anything there before

    f.seek(0,0)
    for num, line in enumerate(f):
        if 'S0 LINESTYLE 3' in line:
            l_b = num
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'KILL G1.S0' in line:
            l_e = num
    old_bands = l_e - l_b
        
    del lines_f[l_b+1:l_e]


# Cycle through known dictionary of legends and colours and match to those present and Write lines to change the line colour and legend accordingly

    colour_table = {'S(s)':5,'S(p)':11,'S(d)':7,'O(s)':13,'O(p)':2,'O(d)':10,'Mo(s)':14,'Mo(p)':12,'Mo(d)':4} 

    for projector in projectors:
        colour     = str(colour_table[projector])
        legend     = projector
        if total_DOS_filename == 0:
            line_index = str(projectors.index(projector) + 1)
        elif total_DOS_filename != 0:
            line_index = str(projectors.index(projector) + 2)

        lines_f.insert(l_e-old_bands+1,'    print   "\@S' + line_index + ' LINE COLOR ' + colour + '\\n";\n')
        lines_f.insert(l_e-old_bands+1,'    print   "\@S' + line_index + ' LEGEND \\"' +  legend  + '\\"\\n";\n')

# Since lines have been deleted, the document has changed length so need to close, rewrite and then reopen for further editing
    f.close()
    f = open('dispersion_temp.pl','w')
    f.writelines( lines_f )
    f.close()
    f = open('dispersion_temp.pl','r')
    lines_f  = f.readlines()
    f.seek(0,0)

    #Fermi_offset = -0.22209075862861027
    Fermi_offset = -float(Fermi_Energy)
    print 'Fermi Offset = ' + str(Fermi_offset) + 'eV'

    # Colour bands to match DOS
    if spec_colour != 0:
        bands_colour = colour_bands(BS_filename, PDOS_filename, Fermi_offset, total_DOS_filename, set_colours)
        n_bands = len(bands_colour)
        bands_colour.append([n_bands, '1'])
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'begin_band_colours' in line:
                l_b = num
        f.seek(0,0)
        for num, line in enumerate(f):
            if 'end_band_colours' in line:
                l_e = num
        old_bands = l_e - l_b
        
        del lines_f[l_b+1:l_e]
        
        colours = []
        for band in bands_colour:
            if set_colours == 1:
                lines_f.insert(l_e-old_bands+1,'    print   "\@S' + str(band[0]) +' LINE COLOR ' + str(band[1]) + '\\n";\n')
            else:
                if band[1] == '1':
                    lines_f.insert(l_e-old_bands+1,'    print   "\@S' + str(band[0]) +' LINE COLOR ' + str(band[1]) + '\\n";\n')
                else:
                    
                    # If colour has already been used, no point creating a new colour, just use the old one
                    colour = str(band[1])
                    if colour in colours:
                        colour_number = str(colours.index(colour)+14)
                        lines_f.insert(l_e-old_bands+1,'    print   "\@S' + str(band[0]) +' LINE COLOR ' + colour_number + '\\n";\n')
                    elif colour == '(220, 220, 220)':
                        lines_f.insert(l_e-old_bands+1,'    print   "\@S' + str(band[0]) +' LINE COLOR 7\\n";\n')

                    # Only if colour has not already been used, create new colour and then continue as before
                    else:
                        colours.append(colour)
                        colour_number = str(colours.index(colour)+14)
                        lines_f.insert(l_e-old_bands+1,'    print   "\@S' + str(band[0]) +' LINE COLOR ' + colour_number + '\\n";\n')
                        lines_f.insert(l_e-old_bands+1,'    print   "\@MAP COLOR ' + colour_number + ' TO ' + str(band[1]) + ', \\"generic' + '_' + colour_number + '\\"\\n";\n')

    # Write the new information to file
    f.close()
    f = open('dispersion_temp.pl','w')
    f.writelines( lines_f )
    f.close()
    os.system("cp dispersion_temp.pl /home/ablitt/bin/dispersion_BG_DOS_coloured.pl")

    # Run dispersion.pl file
    if output == 'jpg':
        os.system("dispersion_BG_DOS_coloured.pl -jpg -bs -symmetry " + symmetry + " " + BS_filename )
    elif output == 'xg':
        os.system("dispersion_BG_DOS_coloured.pl -xg -bs -symmetry " + symmetry + " " + BS_filename )
        
    # Remove dispersion.pl file so as not to clutter/confuse directory
    os.system("rm dispersion_temp.pl")    
    
    return

#****************************************************************************

# The part of geom_opt which controls continuing calculations
def geom_continuation(chem, cores, test, mem, cl_queue, max_time, gpypid_temp, gc_cont=1):
    n = 1
    while n < restarts + 1:
        print 'Preparing to restart calculation due to timeout. Restart number : ' + str(n)
        file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_run_0.log')
        print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_run_0.log'
        os.system('rm ' + chem + '.sh.*')
        print 'Running calculation in parallel on ' + config.computer
        if gc_cont == 0:
            relaxed(chem + '.castep')
        out = castep_parallel( chem, cores, test, cont=gc_cont, mem_alloc=mem, queue=cl_queue, time_lim=max_time, pypid=pypid_temp)
        finished = out[0]
        procpid  = out[1]
        file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_run_' + str(n) + '.log')
        print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_run_' + str(n) + '.log'
        os.system('rm ' + chem + '.sh.*')
        if finished != 0.5:
            f = open(chem + '.castep','r')
            lines_f = f.readlines()
            f.seek(0,0)
            for line in lines_f:
                if 'BFGS : WARNING - Geometry optimization failed to converge' in line:
                    print line
                    finished == 0.5
                    n = n + 1
                else:
                    n = restarts + 2
        elif finished == 0.5:
            n = n + 1
        return finished

#****************************************************************************

# Run geometry optimisation and then update .cell file with new structure
def geom_opt(chem, cores, directory, tag, test=0, restarts=3, comp_temp='same machine', start_cont=0, mem='default', cl_queue='parallel.q', max_time='default'):
    ch_task(chem,'geometryoptimisation')
    import os
    n = 0
    pypid_temp = os.getpid()
    print 'geometry optimisation monitering script for ' + chem + ' has process pid ' +  str(pypid_temp)

    host_comp()
    if 'zener' in config.computer or 'kittel' in computer or 'ironman' in computer:
        os.system('rm ' + chem + '.sh.*')
    out = castep_parallel( chem, cores, test, cont=start_cont, mem_alloc=mem, queue=cl_queue, time_lim=max_time, pypid=pypid_temp)
    finished = out[0]
    procpid  = out[1]

    # Check that castep doesn't say that it has finished just because it has reached the maximum number of geom iterations
    if finished == 1:
        f = open(chem + '.castep','r')
        lines_f = f.readlines()
        f.close()
        for line in lines_f:
            if 'BFGS : WARNING - Geometry optimization failed to converge' in line:
                print line
                finished == 0.5

    # If the calculation has timed out then attempt to restart it and continue
    # Note that calculations may only time out on clusters which require a submission script
    if finished == 0.5:
        
        # Except this will only be possible if a .check file already exists
        try:
            g = open(chem + '.check','r')
            g.close()
            ch_continuation(chem, 'default')
            finished = geom_continuation(chem, cores, test, mem, cl_queue, max_time, pypid_temp, gc_cont=1)

        except IOError:
            # i.e the .check file does not exist

            h = open(chem + '.castep','r')
            lines_h = h.readlines()
            h.close()

            if 'BFGS: finished iteration' in f.read():
                # This means that the geometry optimisation has succeeded in completing at least one iteration and therefore may be resarted manually
                finished = geom_continuation(chem, cores, test, mem, cl_queue, max_time, pypid_temp, gc_cont=0)

            else:
                # The calculation has not been able to generate a .check file or a new structure and thefore has no checkpoint from which to continue
                print 'no .check file or checkpoint exists and therefore the calculation cannot be restarted'
                finished = 0

    if finished == 0.5:
        print 'Full geometry optimisation was unable to complete in ' + str(restarts) + ' restarts and therefore the calculation has been aborted'
        finished = 0

    if finished == 1:
        castep_copy(chem, directory, tag, comp=comp_temp)
        if 'zener' in config.computer or 'kittel' in config.computer or 'ironman' in computer:
            file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_run.log')
            print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_run.log'
            os.system('rm ' + chem + '.sh.*')
        if test == 0:
            get_cell_geom_complete('%s.castep' % chem)
            update_cell_complete(chem, config.real_lattice, config.cell_complete)
            get_BFGS_iterations('%s.castep' % chem)
            print 'Geometry optimisation complete after ' + str(config.BFGS_iterations) + ' BFGS_iterations and .cell file updated with optimised structure'
            if n!= 0:
                print 'Note that the above number refers to the total number of BFGS iterations in all restarts'

    elif finished == 0:
        castep_copy(chem, directory, tag + '_aborted', comp=comp_temp)
        if 'zener' in config.computer or 'kittel' in config.computer or 'ironman' in computer:
            file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_aborted' + '_run.log')
            print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_aborted' + '_run.log'
            os.system('rm ' + chem + '.sh.*')

    return

#****************************************************************************

# Since the processes involved in the castep calculation of any simulation based upon computing the DOS (e.g. bandstructure, DOS, PDOS, CORE EELS) are all essentially the same, might as well make them in a single function
def DOS_based_castep_calculation(chem, directory, tag, cores, test, restarts, start_cont, mem, comp_temp, cl_queue, DC, max_time):
    import os

    host_comp()
    if 'zener' in config.computer or 'kittel' in computer or 'ironman' in computer:
        os.system('rm ' + chem + '.sh.*')
    out = castep_parallel(chem, cores, test, cont=start_cont, mem_alloc=mem, queue=cl_queue, time_lim=max_time)
    finished = out[0]
    procpid  = out[1]

    # If the calculation has timed out then attempt to restart it and continue
    # Note that calculations may only time out on clusters which require a submission script
    if finished == 0.5:
        
        # Except this will only be possible if a .check file already exists
        try:
            f = open(chem + '.check','r')
            ch_continuation(chem, 'default')
            n = 1
            while n < restarts + 1:
                print 'Preparing to restart calculation due to timeout. Restart number : ' + str(n)
                file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_run_0.log')
                print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_run_0.log'
                out = castep_parallel( chem, cores, test, cont=1, mem_alloc=mem, queue=cl_queue, time_lim=max_time)
                finished = out[0]
                procpid  = out[1]
                file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_run_' + str(n) + '.log')
                print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_run_' + str(n) + '.log'
                os.system('rm ' + chem + '.sh.*')
                if finished != 0.5:
                    n = restarts + 2
                elif finished == 0.5:
                    n = n + 1

        except IOError:
            print 'no .check file exists and therefore the calculation cannot be restarted'
            finished = 0

    if finished == 0.5:
        print 'Full ' + config.task + ' calculation was unable to complete in ' + str(restarts) + ' restarts and therefore the calculation has been aborted'
        finished = 0

    # Save progress report files
    if finished == 1:
        castep_copy(chem, directory, tag, comp=comp_temp, DOS_calc=DC)
        if 'zener' in config.computer or 'kittel' in config.computer or 'ironman' in config.computer:
            file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_cas_run.log')
            print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_cas_run.log'
            os.system('rm ' + chem + '.sh.*')

    elif finished == 0:
        castep_copy(chem, directory, tag + '_aborted', comp=comp_temp, DOS_calc=DC)
        if 'zener' in config.computer or 'kittel' in config.computer or 'ironman' in config.computer:
            file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_aborted' + '_run.log')
            print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_aborted' + '_run.log'
            os.system('rm ' + chem + '.sh.*')
    
    return finished

#****************************************************************************

# Once input parameters are set up all optados calculations are basically the same
def standard_optados_calculation(chem, directory, tag, comp_temp, DC):
    import os
    
    # Run optados calculation on correct number of cores
    # Do this only if on Zener or Scarlet
    if 'zener' in config.computer:
        optados_zener(chem, 8)

    # Save progress report files
        file_transfer(chem + '.sh.o.*', comp_temp, directory, tag + '_opt_run.log')
        print 'copied ' + chem + '.sh file to ' + comp_temp + ':' + directory + '/' + tag
        os.system('rm ' + chem + '.sh.*')
    elif config.computer == 'scarlet':
        optados(chem,1)
        
    # Save .odo file in case further optados calculations to take place
    file_copy( chem + '.odo', '.', chem + '.core.odo' )
    file_remove( chem + '.odo' )
    optados_copy(chem, directory, tag, comp=comp_temp, DOS_calc=DC)
    print 'Optados ' + str(config.opt_task) + ' calculation complete'

    return

#****************************************************************************

# Run bandstructure calculation and then produce BS plot
def band_struct(chem, cores, directory, tag, test=0, restarts=3, comp_temp='same machine', start_cont=0, mem='default', cl_queue='parallel.q', bg_min=0, bg_max=0, max_time='default'):
    ch_task(chem,'bandstructure')
    if start_cont==0:
        ch_continuation(chem, 'none')
    else:
        ch_continuation(chem, 'default')

    # Run castep calculation
    finished = DOS_based_castep_calculation(chem, directory, tag, cores, test, restarts, start_cont, mem, comp_temp, cl_queue, '_BS', max_time)

    # Produce BS graph if required
    if finished == 1 and bg_min!=0 and bg_max!=0:
        if config.computer == 'scarlet':
            plot_BS(chem + '.bands', bg_min, bg_max)
            file_transfer(chem + '.jpg', directory, tag + '.jpg')
            file_remove(chem + '.jpg')
            print 'Bandstructure calculation complete with JPEG image of bandstructure produced'

    castep_cleanup(chem)
    return

#****************************************************************************

# Run spectral calculation and then run optados DOS calculation
def DOS(chem, cores, directory, tag, test=0, restarts=3, comp_temp='same machine', start_cont=0, mem='default', total_DOS=1, PDOS=1, cl_queue='parallel.q', max_time='default'):
    ch_task(chem,'spectral')
    # Don't yet need change spectral task since DOS is set to default
    if start_cont==0:
        ch_continuation(chem, 'none')
    else:
        ch_continuation(chem, 'default')

    # Run castep calculation
    finished = DOS_based_castep_calculation(chem, directory, tag, cores, test, restarts, start_cont, mem, comp_temp, cl_queue, '_DOS', max_time)

    # Run optados calculations as required (plot at a later date)
    if finished == 1:
        if total_DOS == 1:
            ch_opt_task(chem, 'DOS')
            standard_optados_calculation(chem, directory, tag, comp_temp, '_DOS')
    
        if PDOS == 1:
            ch_opt_task(chem, 'DOS')
            standard_optados_calculation(chem, directory, tag, comp_temp, '_PDOS')

    castep_cleanup(chem)
    return

#****************************************************************************

# Generate a CORE EELS spectra
def CORE_EELS(chem, cores, directory, tag, optados_cores=0, test=0, restarts=3, comp_temp='same machine', start_cont=0, methodology='corehole', mem='default', cl_queue='parallel.q', geom='polycrystalline',e_vector=[0,0,0], max_time='default'):
    ch_task(chem,'spectral')
    if start_cont==0:
        ch_continuation(chem, 'none')
    else:
        ch_continuation(chem, 'default')

    # Set general CORE EELS specific parameters
    ch_spectral_task(chem,'coreloss')
    ch_opt_task(chem,'CORE')
    ch_core_geom(chem,geom)
    ch_e_beam_vector(chem,e_vector)
    if methodology=='corehole':
        #ch_spin(chem,'true')  if the material is otherwise spin unpolarised then the spin change of creating a core hole will have no effect on greater spin 
        ch_charge(chem, 1)

    # Make sure that fix occupancy has been changed to false
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    if 'fix_occupancy : true' in f.read():
        ch_fix_occupancy(chem, 'false')
        print 'Fix occupancy had been set as true prior to CORE EELS calculation and therefore has been changed.'
        print 'WARNING: The default settings for n_extra_bands and n_spect_extra_bands are being used'
    
    # Run castep calculation
    finished = DOS_based_castep_calculation(chem, directory, tag, cores, test, restarts, start_cont, mem, comp_temp, cl_queue, '_EELS', max_time)

    # Run optados calculations
    if finished == 1:
        standard_optados_calculation(chem, directory, tag, comp_temp, '_EELS')
    
    castep_cleanup(chem)
    return
    
#****************************************************************************

# Run singlepoint castep calculation
def singlepoint(chem, cores, directory, tag, test=0, comp_temp='same machine', mem='default', cl_queue='parallel.q', max_time='default',start_cont=0):
    import os
    ch_task(chem,'singlepoint')
    ch_continuation(chem, 'none')
    host_comp()
    if 'zener' in config.computer or 'kittel' in computer or 'ironman' in computer:
        os.system('rm ' + chem + '.sh.*')
    out = castep_parallel(chem, cores, test, start_cont, mem_alloc=mem, queue=cl_queue, time_lim=max_time)
    finished = out[0]
    procpid  = out[1]

    if finished == 1:
        castep_copy(chem, directory, tag, comp=comp_temp)
        if 'zener' in config.computer or 'kittel' in config.computer or 'ironman' in config.computer:
            file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_cas_run.log')
            print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_cas_run.log'
            os.system('rm ' + chem + '.sh.*')

    elif finished == 0:
        castep_copy(chem, directory, tag + '_aborted', comp=comp_temp)
        if 'zener' in config.computer or 'kittel' in config.computer or 'ironman' in config.computer:
            file_transfer(chem + '.sh.o' + str(procpid), comp_temp, directory, tag + '_aborted' + '_run.log')
            print 'copied ' + chem + '.sh.o file to ' + comp_temp + ':' + directory + '/' + tag + '_aborted' + '_run.log'
            os.system('rm ' + chem + '.sh.*')

    castep_cleanup(chem)
    print 'singlepoint calculation complete'
    return

#****************************************************************************

# Change spectral task
def ch_spectral_task(chem, spectral_task_temp):
    global spectral_task
    spectral_task = spectral_task_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_task:' in line:
            l = num
    lines_f[l]    = 'spectral_task: ' + spectral_task_temp + ' \n'
    
    if spectral_task_temp == 'DOS':
        lines_f.insert(4, 'pdos_calculate_weights : TRUE\n')

    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'spectral_task changed to: ' +  spectral_task_temp
    config.spectral_task = spectral_task
    return

#****************************************************************************

# Change Charge
def ch_charge(chem, charge_temp):
    global charge
    charge = charge_temp
    f = open('%s.param' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'charge :' in line:
            l = num
    lines_f[l]    = 'charge : ' + str(charge_temp) + ' \n'
    f = open('%s.param' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'charge changed to: ' +  str(charge_temp)
    config.charge = charge
    return

#****************************************************************************

# Change pseudopotential
def ch_usp(chem, atom, usp='2|1.0|1.3|0.7|13|16|18|20:21{1s1.00}(qc=7)'):
    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)

    # Make sure referring to only the species section of the .cell file
    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK SPECIES_POT' in line:
            l_B = num
    
    # Edit the .cell file 
    f.seek(0,0)
    for num, line in enumerate(f):
        if atom in line and num > l_B - 1:
            l = num
    lines_f[l]   = atom + '\t' + usp + ' \n'
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    print 'Ultra Soft Pseudopotential used for ' + atom + ' changed to ' + usp
    f.close()

#****************************************************************************

# Plot PDOS of only interesting bands around the bandgap
def plot_PDOS( filename, chem, bg_min_temp=0, bg_max_temp=0, graph_type='xy', DOS_max=0):
    global bg_min
    global bg_max
    bg_min = bg_min_temp
    bg_max = bg_max_temp

    # Create the grace script
    if graph_type == 'xy':
        from graphscripts import PDOSplot_xy
        PDOSplot = PDOSplot_xy
        X = 'X'
        Y = 'Y'
    elif graph_type == 'yx':
        from graphscripts import PDOSplot_yx
        PDOSplot = PDOSplot_yx
        X = 'Y'
        Y = 'X'

    PDOSplot[0] = 'READ BLOCK "'+ filename + '"\n' 
    PDOSplot[6] = 'WORLD ' + X + 'MIN -' + str(bg_min) + '\n' 
    PDOSplot[7] = 'WORLD ' + X + 'MAX '  + str(bg_max) + '\n'
    if DOS_max == 0:
        PDOSplot[8] = 'AUTOSCALE ' + Y + 'AXES \n'
    else:
        PDOSplot[8] = 'WORLD ' + Y + 'MAX '  + str(DOS_max) + '\n'
    graphname = filename.replace('.dat','.jpg')
    PDOSplot[20] = 'PRINT TO "'  + graphname + '"\n'

    # Alter legend according to chemistry
    
    if chem == 'MoS2':

        f.seek(0,0)
        for num, line in enumerate(f):
            if 'S1 LEGEND' in line or 'S2 LEGEND' in line:
                l = num
                if 'S(s)' in line or 'S(p)' in lines_f[l]:
                     if '#' in lines_f[l]:
                        lines_f[l] = lines_f[l].replace('#','p')
                else:
                    if 'p' in lines_f[l]:
                        lines_f[l] = lines_f[l].replace('p','#')
        
    elif chem == 'MoO2':

        for num, line in enumerate(f):
            if 'S1 LEGEND' in line or 'S2 LEGEND' in line:
                l = num
                if 'O(s)' in line or 'O(p)' in lines_f[l]:
                     if '#' in lines_f[l]:
                        lines_f[l] = lines_f[l].replace('#','p')
                else:
                    if 'p' in lines_f[l]:
                        lines_f[l] = lines_f[l].replace('p','#')

    else:

        print 'Chemistry does not exist in legend library, please alter legend library in graphscipts module'
    
    # If no max and min energies are given then automatically scale energy axes

    if bg_min == 0 and bg_max == 0:
        del PDOSplot[6],PDOSplot[6]


    # Write the grace input file
    f = open('PDOSplot_temp','w')
    f.writelines( PDOSplot )
    f.close()

    # Generate graph
    import os
    os.system("grace -nosafe -hdevice JPEG -batch PDOSplot_temp")
    
    # Remove PDOSplot script in working directory
    os.system("rm PDOSplot_temp")

    return

#****************************************************************************

# Extract the number of BFGS iterations completed in a geometry optimisation
def get_BFGS_iterations(filename):
    h = open( filename,'r')
    lines_h  = h.readlines()
    runs = 0
    BFGS_tot = 0
    BFGS_iterations = 0
    for line in lines_h:
        if 'Welcome to Academic Release CASTEP version 6.11' in line:
            runs = runs + 1
            BFGS_tot = BFGS_tot + BFGS_iterations
            BFGS_iterations = 0

        if 'BFGS: finished iteration' in line:
            BFGS_iterations = int(line.split()[3])

    BFGS_tot = BFGS_tot + BFGS_iterations
    h.close()
    config.runs = runs
    config.BFGS_iterations = BFGS_tot
    return BFGS_tot

#****************************************************************************

# Change the entire .odi file specific to a particular optados task
def ch_opt_task(chem, opt_task):
    import os
    os.system('cp /home/ablitt/mypy/opt_tasks/%(a)s.odi %(b)s.odi' % {'a':opt_task,'b':chem})
    return

#****************************************************************************

# Change the projectors plotted in a PDOS calculation
def ch_projector(chem, projector):
    f = open('%s.odi' % chem,'r')
    lines_f  = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'PDOS :' in line:
            l = num
    lines_f[l]    = 'PDOS : ' + str(projector) + ' \n'
    f = open('%s.odi' % chem,'w')
    f.writelines( lines_f )
    f.close()
    return

#****************************************************************************

# Get host name
def host_comp():
    global computer
    import socket
    computer = socket.gethostname()
    config.computer = computer
    return

#****************************************************************************

# Get a time formatted in hours:mins:s all in seconds
def time_in_s( time_string ):
    global time_total
    time_split = time_string.replace(':',' ')
    time_h = float(time_split.split()[0])
    time_m = float(time_split.split()[1])
    time_s = float(time_split.split()[2])
    time_total = time_h*3600 + time_m*60 + time_s
    return time_total

#****************************************************************************

# Gives the local time as a string in a usful format
def print_time():
    import time
    t = time.localtime()
    time_string = str(t[3]) + ':' + str(t[4]) + ':' + str(t[5]) + ' on ' + str(t[2]) + '/' + str(t[1]) + '/' + str(t[0])
    return time_string

#****************************************************************************

# Calculate kpoint offset required to make grid gamma centred
def calc_offset(kpoints):
    global offset
    
    # Check if any kpoints in grid are even and if it is, calculate the required offset
    offset = []
    for k in kpoints:
        k = int(k)
        k_i = k/2
        k_f = float(k)/2
        if k_i - k_f == 0:
            off = float(1)/(2*k)
        else:
            off = 0
        offset.append(str(off))

    config.offset = offset
    return

#****************************************************************************

# Recalculate kpoint grid to fit a new supercell with new dimensions
def recalc_kpoints(k_old, factor):
    kpoints = {'a':int(k_old[0]),'b':int(k_old[1]),'c':int(k_old[2])}
    factors = {'a':factor[0], 'b':factor[1], 'c':factor[2]}

    k_new = {}
    for k in kpoints:
        k_a = int(kpoints[k]/factors[k])
        k_b = float(kpoints[k])/factors[k]
        if k_a - k_b == 0:
            k_new[k] = kpoints[k]/factors[k]
        else:
            k_new[k] = int(kpoints[k]/factors[k]) + 1

    new_kpoints = [k_new['a'],k_new['b'],k_new['c']]       
    return new_kpoints

#****************************************************************************

# Adjust all kpoint grids in a .cell file to fit a new supercell with new dimensions
def adjust_kpoints(chem, factor):
    f = open(chem+'.cell','r')
    cell = f.readlines()
    cell_new = cell
    
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'kpoint_mp_grid' in line and 'spectral' not in line and 'bs' not in line:
            l = num
            kpoints = [int(cell[l].split()[1]),int(cell[l].split()[2]),int(cell[l].split()[3])]
            k_new = recalc_kpoints(kpoints, factor)
            ch_kpoints(chem, k_new)
    
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'spectral_kpoint_mp_grid' in line:
            l = num
            kpoints = [int(cell[l].split()[1]),int(cell[l].split()[2]),int(cell[l].split()[3])]
            k_new = recalc_kpoints(kpoints, factor)
            ch_spectral_kpoints(chem, k_new)

    f.seek(0,0)
    for num, line in enumerate(f):
        if 'bs_kpoint_mp_grid' in line:
            l = num
            kpoints = [int(cell[l].split()[1]),int(cell[l].split()[2]),int(cell[l].split()[3])]
            k_new = recalc_kpoints(kpoints, factor)
            ch_bs_kpoints(chem, k_new)

    f.close()
    print 'All kpoint grids in enlarged supercell have been updated accordingly'
    return

#****************************************************************************

# Duplicate existing cell [l, n, m] times
def enlarge_cell(chem,tag,factor):
    f = open(chem+'.cell','r')
    cell = f.readlines()
    cell_new = cell
    factors = {'a':factor[0], 'b':factor[1], 'c':factor[2]}
           
    # Scale the x, y and z lattice parameters and write to cell_new
    a_x = float(cell[1].split()[0])
    b_x = float(cell[2].split()[0])
    b_y = float(cell[2].split()[1])
    c   = float(cell[3].split()[2])

    a_x = a_x*factors['a']
    b_x = b_x*factors['b']
    b_y = b_y*factors['b']
    c   = c*factors['c']

    cell_new[1] = str(a_x) + ' 0.00' + ' 0.00\n'
    cell_new[2] = str(b_x) + ' ' + str(b_y) + ' 0.00\n'
    cell_new[3] = '0.00' + ' 0.00 ' + str(c) + '\n'

    # Count number of atoms in the original cell file, n, delete the lines for the old atoms in cell_new
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1
    j = 1

    
    # Cycle through each old atom and replicate $factor^2 times in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos_x = float(cell[6 + i].split()[1])
        pos_y = float(cell[6 + i].split()[2])
        pos_z = float(cell[6 + i].split()[3])
        
        shrink = {}
        for d in factors:
            shrink[d] = float(1)/factors[d]   # scale factor by which to shrink fractional coordinates

        i_1    = 0                 # variable to cycle through a axis manipultations (occur $factor times)
        i_2    = 0                 # variable to cycle through b axis manipultations (occur $factor times)
        i_3    = 0
        
        while i_1 < factors['a']:
            while i_2 < factors['b']:
                while i_3 < factors['c']:
                
                    cell_new.insert(j+n+5, atom + '\t' + str(pos_x*shrink['a'] + i_1*shrink['a']) + '\t' + str(pos_y*shrink['b'] + i_2*shrink['b']) + '\t' + str(pos_z*shrink['c'] + i_3*shrink['c']) + '\n')

                    i_3 = i_3 +1
                    j = j + 1

                i_2 = i_2 +1
                i_3 = 0
                
            i_1 = i_1 + 1
            i_2 = 0
            
        i = i + 1

    del cell_new[7:6+n]
        
    # Write cell_new to a new .cell file
    g = open(tag + '.cell','w')
    g.writelines( cell_new )
    g.close
    print 'Supercell ' + str(factors) +' times the size of original cell has been formed'
    return

#****************************************************************************

# Append the outer edge of the cell with a border of pristine material NOTE: kpoint grid is NOT changed in an extension
# c parameter is included for completeness but DO NOT USE THIS FUNCTION TO EXTEND CELL IN C AXIS!!!!!!

def extend_cell(chem, pristine_chem, dim_old, tag, functional, dims_in=[1,1,0]):

    import structures
    atoms_pris = structures.prim_cell(pristine_chem, functional, 'atoms_pris')
    bond_length = structures.prim_cell(pristine_chem, functional, 'bondlength')

    f = open(chem+'.cell','r')
    cell = f.readlines()
    cell_new = cell
    dim_in   = {'a':int(dims_in[0]),'b':int(dims_in[1]),'c':int(dims_in[2])}
    dims_old = {'a':dim_old[0],'b':dim_old[1],'c':dim_old[2]}

    # Find the new dimensions in each dimension being extended
    dims_new = {}
    for d in dims_old:
        dims_new[d] = dims_old[d] + dim_in[d]
        
    # Scale the x, y and z lattice parameters and write to cell_new
    a_x = float(cell[1].split()[0])
    b_x = float(cell[2].split()[0])
    b_y = float(cell[2].split()[1])
    c   = float(cell[3].split()[2])

    factors = {}
    for d in dims_new:
        factors[d] = float(dims_new[d])/dims_old[d]

    a_pris = a_x/dims_old['a']

    a_x = a_x*factors['a']
    b_x = b_x*factors['b']
    b_y = b_y*factors['b']
    c   = c*factors['c']

    cell_new[1] = str(a_x) + ' 0.00' + ' 0.00\n'
    cell_new[2] = str(b_x) + ' ' + str(b_y) + ' 0.00\n'
    cell_new[3] = '0.00' + ' 0.00 ' + str(c) + '\n'

    # Be careful when calculating delta to use the UNIT cell NOT SUPERCELL value for b_y!
    b_y_unit = b_y/float(dims_new['b'])
    
    delta = ( float(bond_length)**2 - ( (2/float(3))*float(b_y_unit) )**2 )**0.5

    # Count number of atoms in the original cell file, n
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1
    j = 1
    
    # Cycle through each old atom and scale to new relative positions in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos_x = float(cell[6 + i].split()[1])
        pos_y = float(cell[6 + i].split()[2])
        pos_z = float(cell[6 + i].split()[3])
        
        shrink = {}
        for d in factors:
            shrink[d] = float(1)/factors[d]   # scale factor by which to shrink fractional coordinates
                      
        cell_new[6 + j] = atom + '\t' + str(pos_x*shrink['a']) + '\t' + str(pos_y*shrink['b']) + '\t' + str(pos_z*shrink['c']) + '\n'

        j = j + 1          
        i = i + 1

    # Now append the edges of the supercell with the new pristine material
  
    shrink_pris = {}                             # scale factor by which to shrink fractional coordinates
    for d in dims_new:
        shrink_pris[d] = float(1)/dims_new[d] 

    # Update pristine atom positions to new lattice parameter (specifially c coordinate)
    atom_pris_new = []
    for atom_pris in atoms_pris:

        if float(atom_pris[3]) < 0.5:
            new_atom_pris_3 = 0.5 - delta/float(c)
        elif float(atom_pris[3]) > 0.5:
            new_atom_pris_3 = 0.5 + delta/float(c)
        elif float(atom_pris[3]) == 0.5:
            new_atom_pris_3 = atom_pris[3]
        atom_pris_new.append(str(atom_pris[0]) + '  ' + str(atom_pris[1]) + '  ' + str(atom_pris[2]) + '  ' + str(new_atom_pris_3))
    
    atoms_pris = atom_pris_new
    combos     = [['a','b'],['b','a']]

    # For each atom in pristine unit cell, for each new row of pristine material cycle through all columns of origninal material inserting atom into additional unit cell
    for atom_pris in atoms_pris:
        for combo in combos:
            i = {'a':0,'b':0}                                          # variable to cycle through axis manipultations within each additonal layer
            m = {'a':0,'b':0}                                          # variable to cycle through each additonal layer
            while m[combo[0]] < dim_in[combo[0]]:
                while i[combo[1]] < int(dims_old[combo[1]]):
                    big   = float(dims_old[combo[0]]+m[combo[0]])
                    small = float(i[combo[1]])

                    if combo[0] == 'a':
                        extra_a = big
                        extra_b = small
                    else:
                        extra_b = big
                        extra_a = small

                    cell_new.insert(j+5, str(atom_pris.split()[0]) + '\t' + str((float(atom_pris.split()[1]) + extra_a)*shrink_pris['a']) + '\t' + str((float(atom_pris.split()[2]) + extra_b)*shrink_pris['b']) + '\t' + str(atom_pris.split()[3]) + '\n')
                    j = j + 1
                    i[combo[1]] = i[combo[1]] + 1
                i[combo[1]] = 0
                m[combo[0]] = m[combo[0]] + 1

    # Above procedure should leave a corner dim_in[a] x dim_in[b] in size which has not been filled in (obv will not happen if dim_in[a/b] = 0)
    for atom_pris in atoms_pris:
        m = {'a':0,'b':0}
        while m['a'] < dim_in['a']:
                while m['b'] < dim_in['b']:
                    cell_new.insert(j+5, str(atom_pris.split()[0]) + '\t' + str(float(atom_pris.split()[1])*shrink_pris['a'] + float(dims_old['a'] + m['a'])*shrink_pris['a']) + '\t' + str(float(atom_pris.split()[2])*shrink_pris['b'] + float(dims_old['b'] + m['b'])*shrink_pris['b']) + '\t' + str(atom_pris.split()[3]) + '\n')
                    j = j + 1
                    m['b'] = m['b'] + 1
                m['a'] = m['a'] + 1
                m['b'] = 0

    # Write cell_new to a new .cell file
    g = open(tag + '.cell','w')
    g.writelines( cell_new )
    g.close
    print 'Supercell ' + str(dim_in) + ' square unit(s) larger than original cell in a and b dimensions has been formed'
    return

#****************************************************************************

# Extends any cell by dumping blocks of pristine material at selected edges
# The appended material will be scaled to match the lattice parameters in each dimension of the existing material
# This method will not be efficient prior to geom opt since it does not preserve bondlengths in the pristine material
def extend_any_cell(chem, pristine_chem, dim_old, tag, functional, dims_in):

    import structures
    real_lattice_pris = structures.prim_cell(pristine_chem, functional, 'real_lattice')
    atoms_pris = structures.prim_cell(pristine_chem, functional, 'atoms_pris')

    f = open(chem + '.cell','r')
    cell = f.readlines()
    cell_new = cell
    dim_in   = {'a':int(dims_in[0]),'b':int(dims_in[1]),'c':int(dims_in[2])}
    dims_old = {'a':dim_old[0],'b':dim_old[1],'c':dim_old[2]}

    # Find the new dimensions in each dimension being extended
    dims_new = {}
    for d in dims_old:
        dims_new[d] = dims_old[d] + dim_in[d]
        
    # Get the old lattice
    real_lattice = []
    i = 1
    while i < 4:
        RL = [cell[i].split()[0], cell[i].split()[1], cell[i].split()[2]]  # line i of RL
        real_lattice.append(RL)
        i = i + 1

    factors = {}
    for d in dims_new:
        factors[d] = float(dims_new[d])/dims_old[d]

    # Extend all old lattice parameters to accomate for the new material being added
    new_lattice = []
    for RL in real_lattice:
        NL = [float(RL[0])*factors['a'], float(RL[1])*factors['b'], float(RL[2])*factors['c']]
        new_lattice.append(NL)

    # Update lattice parameters
    i = 1
    for line in new_lattice:
        cell_new[i]    = str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) + '\n'
        i = i + 1

    # Count number of atoms in the original cell file, n
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1
    j = 1
    
    # Cycle through each old atom and scale to new relative positions in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos_x = float(cell[6 + i].split()[1])
        pos_y = float(cell[6 + i].split()[2])
        pos_z = float(cell[6 + i].split()[3])
        
        shrink = {}
        for d in factors:
            shrink[d] = float(1)/factors[d]   # scale factor by which to shrink fractional coordinates
                      
        cell_new[6 + j] = atom + '\t' + str(pos_x*shrink['a']) + '\t' + str(pos_y*shrink['b']) + '\t' + str(pos_z*shrink['c']) + '\n'

        j = j + 1          
        i = i + 1

    # Now append the edges of the supercell with the new pristine material
  
    shrink_pris = {}                             # scale factor by which to shrink fractional coordinates
    for d in dims_new:
        shrink_pris[d] = float(1)/dims_new[d] 

    combos     = [['a','b','c'],['b','c','a'],['c','a','b']]

    # For each atom in pristine unit cell, for each new row of pristine material cycle through all columns of origninal material inserting atom into additional unit cell
    for atom_pris in atoms_pris:
        
        for combo in combos:
            i = {'a':0,'b':0,'c':0}                                          # variable to cycle through axis manipultations within each additonal layer
            m = {'a':0,'b':0,'c':0}                                          # variable to cycle through each additonal layer
            n = {'a':0,'b':0,'c':0}                                          # variable to cycle through each additonal layer

            # 1 of a, b and c are large
            while m[combo[0]] < dim_in[combo[0]]:
                while i[combo[1]] < int(dims_old[combo[1]]):
                    while n[combo[2]] < int(dims_old[combo[2]]):
                        big     = float(dims_old[combo[0]]+m[combo[0]])
                        small_i = float(i[combo[1]])
                        small_n = float(n[combo[2]])

                        if combo[0] == 'a':
                            extra_a = big
                            extra_b = small_i
                            extra_c = small_n
                        elif combo[0] == 'b':
                            extra_b = big
                            extra_c = small_i
                            extra_a = small_n
                        elif combo[0] == 'c':
                            extra_c = big
                            extra_a = small_i
                            extra_b = small_n

                        cell_new.insert(j+5, str(atom_pris[0]) + '\t' + str((float(atom_pris[1]) + extra_a)*shrink_pris['a']) + '\t' + str((float(atom_pris[2]) + extra_b)*shrink_pris['b']) + '\t' + str((float(atom_pris[3]) + extra_c)*shrink_pris['c']) + '\n')

                        j = j + 1
                        n[combo[2]] = n[combo[2]] + 1
                    i[combo[1]] = i[combo[1]] + 1
                    n[combo[2]] = 0
                i[combo[1]] = 0
                n[combo[2]] = 0
                m[combo[0]] = m[combo[0]] + 1
            
            # 2 of a, b and c are large
            i = {'a':0,'b':0,'c':0}
            m = {'a':0,'b':0,'c':0}
            n = {'a':0,'b':0,'c':0}

            while m[combo[0]] < dim_in[combo[0]]:
                while i[combo[1]] < dim_in[combo[1]]:
                    while n[combo[2]] < int(dims_old[combo[2]]):
                        big_m   = float(dims_old[combo[0]]+m[combo[0]])
                        big_i   = float(dims_old[combo[1]]+i[combo[1]])
                        small_n = float(n[combo[2]])
                        
                        if combo[0] == 'a':
                            extra_a = big_m
                            extra_b = big_i
                            extra_c = small_n
                        elif combo[0] == 'b':
                            extra_b = big_m
                            extra_c = big_i
                            extra_a = small_n
                        elif combo[0] == 'c':
                            extra_c = big_m
                            extra_a = big_i
                            extra_b = small_n

                        cell_new.insert(j+5, str(atom_pris[0]) + '\t' + str((float(atom_pris[1]) + extra_a)*shrink_pris['a']) + '\t' + str((float(atom_pris[2]) + extra_b)*shrink_pris['b']) + '\t' + str((float(atom_pris[3]) + extra_c)*shrink_pris['c']) + '\n')

                        j = j + 1
                        n[combo[2]] = n[combo[2]] + 1
                    i[combo[1]] = i[combo[1]] + 1
                    n[combo[2]] = 0
                i[combo[1]] = 0
                n[combo[2]] = 0
                m[combo[0]] = m[combo[0]] + 1
            
        # a, b and c are large
        m = 0
        i = 0
        n = 0
        while m < dim_in['a']:
            while i < dim_in['b']:
                while n < dim_in['c']:
                    extra_a = float(dims_old['a']+m)
                    extra_b = float(dims_old['b']+i)
                    extra_c = float(dims_old['c']+n)
                                           
                    cell_new.insert(j+5, str(atom_pris[0]) + '\t' + str((float(atom_pris[1]) + extra_a)*shrink_pris['a']) + '\t' + str((float(atom_pris[2]) + extra_b)*shrink_pris['b']) + '\t' + str((float(atom_pris[3]) + extra_c)*shrink_pris['c']) + '\n')

                    j = j + 1
                    n = n + 1
                i = i + 1
                n = 0
            i = 0
            n = 0
            m = m + 1

    # Write cell_new to a new .cell file
    g = open(tag + '.cell','w')
    g.writelines( cell_new )
    g.close
    print 'Supercell ' + str(dim_in) + ' square unit(s) larger than original cell in a and b dimensions has been formed'
    return

#****************************************************************************

# Increase the vacuum equally at both ends of a cell in a particular cell dimension by a given distance (in A)
def isolate_cell(chem, tag, axis, distance):
    import config
    f = open(chem+'.cell','r')
    cell = f.readlines()
    cell_new = cell
    
    # Update the lattice parameter
    axes = {'a':0,'b':1,'c':2}

    # Get the old lattice vector
    i = axes[axis] + 1
    RL = [float(cell[i].split()[0]), float(cell[i].split()[1]), float(cell[i].split()[2])]  # line i of RL
    lat_old = (RL[0]**2 + RL[1]**2 + RL[2]**2)**0.5
    lat_new = lat_old + float(distance)

    # Calculate the new lattice vector
    factor = float(lat_new)/lat_old
    j = 0
    while j < 3:
        RL[j] = RL[j]*factor
        j = j + 1
    cell_new[i] = str(RL[0]) + '\t' + str(RL[1]) + '\t' + str(RL[2]) + '\n'

    # Count number of atoms in the original cell file, n
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1
    
    # Cycle through each old atom and scale to new relative positions in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos = [float(cell[6 + i].split()[1]),float(cell[6 + i].split()[2]),float(cell[6 + i].split()[3])]

        # Shrink the fractional atomic positions to accomodate for the effective lattice parameter shrinkage
        # (as if you had shrank the cell from the old dimensions to 1/new dimensions)
        # Shift the atomic positions accordingly
        # (to allow for the increased vacuum at the start of the cell)
        
        shrink = float(1)/factor # scale factor by which to shrink fractional coordinates
        shift = float(distance)/(2*lat_new) # Fractional distance by which to shift fractional coordinates (half of the increase in vacuum)

        pos[axes[axis]] = pos[axes[axis]]*shrink + shift
                      
        cell_new[6 + i] = atom + '\t' + str(pos[0]) + '\t' + str(pos[1]) + '\t' + str(pos[2]) + '\n'

        i = i + 1

    # Write cell_new to a new .cell file
    g = open(tag + '.cell','w')
    g.writelines( cell_new )
    g.close
    print str(distance) + 'A vacuum added, split over both sides of ' + axis + ' lattice parameter in original cell'
    return

#****************************************************************************

# Create a new .cell file with all the atoms translated within the periodic cell by a vector v
def translate_cell(chem, tag, v):
    f = open(chem+'.cell','r')
    cell = f.readlines()
    cell_new = cell

    # Count number of atoms in the original cell file, n
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1

    # Cycle through each old atom and scale to new relative positions in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos_x = float(cell[6 + i].split()[1])
        pos_y = float(cell[6 + i].split()[2])
        pos_z = float(cell[6 + i].split()[3])

        pos_x = pos_x+float(v[0])
        pos_y = pos_y+float(v[1])
        pos_z = pos_z+float(v[2])
        
        pos_new = []
        
        pos = [pos_x, pos_y, pos_z]
        for pos_i in pos:
            if pos_i >= 0.995:
                pos_i_new = pos_i - 1
            elif pos_i < 0:
                pos_i_new = pos_i + 1
            else:
                pos_i_new = pos_i
            pos_new.append(pos_i_new)
                             
        cell_new[6 + i] = atom + '\t' + str(pos_new[0]) + '\t' + str(pos_new[1]) + '\t' + str(pos_new[2]) + '\n'
  
        i = i + 1

    # Write cell_new to a new .cell file
    g = open(tag + '.cell','w')
    g.writelines( cell_new )
    g.close
    print 'atoms in orignial .cell file translated by vector [' + str(v[0]) + ',' + str(v[1]) + ',' + str(v[2]) + ']'
    return

#****************************************************************************

# Adjusts atomic positions so that they all fit inside the unit cell
def fit_to_cell(chem):
    f = open(chem+'.cell','r')
    cell = f.readlines()
    cell_new = cell

    # Count number of atoms in the original cell file, n
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1

    # Cycle through each old atom and scale to new relative positions in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos_x = float(cell[6 + i].split()[1])
        pos_y = float(cell[6 + i].split()[2])
        pos_z = float(cell[6 + i].split()[3])

        pos_new = []

        pos = [pos_x, pos_y, pos_z]
        for pos_i in pos:
            if pos_i >= 0.995:
                pos_i_new = pos_i - 1
            elif pos_i < 0:
                pos_i_new = pos_i + 1
            else:
                pos_i_new = pos_i
            pos_new.append(pos_i_new)
                             
        cell_new[6 + i] = atom + '\t' + str(pos_new[0]) + '\t' + str(pos_new[1]) + '\t' + str(pos_new[2]) + '\n'
  
        i = i + 1

    # Write cell_new to a new .cell file
    g = open(chem + '.cell','w')
    g.writelines( cell_new )
    g.close
    print 'atoms in orignial .cell file translated such that they all fit within the unit cell'
    return

#****************************************************************************

# keep a float to a set number of decimal places
def dp(number, dp):
    no = float(number)
    host_comp()
    if 'zener' in config.computer:
        string = '%.' + str(dp) +'g'
        no = string % no
    else:
        string = "{0:." + str(dp) + "f}"
        no = string.format(no)
    return no

#****************************************************************************

# Tidy up the cell file so that all columns are the same size
def tidy_cell(chem, lat_digit=5, pos_digit=9):
    f = open(chem + '.cell','r')
    cell = f.readlines()
    cell_new = cell

    # Get the real lattice and the lattice parameters
    real_lattice = []
    i = 1
    while i < 4:
        RL = [float(cell[i].split()[0]), float(cell[i].split()[1]), float(cell[i].split()[2])]  # line i of RL
        real_lattice.append(RL)
        i = i + 1
    
    string = "{0:." + str(lat_digit) + "f}"

    cell_new[1] = str(string.format(real_lattice[0][0])) + '\t' + str(string.format(real_lattice[0][1])) + '\t' + str(string.format(real_lattice[0][2])) + '\n'
    cell_new[2] = str(string.format(real_lattice[1][0])) + '\t' + str(string.format(real_lattice[1][1])) + '\t' + str(string.format(real_lattice[1][2])) + '\n'
    cell_new[3] = str(string.format(real_lattice[2][0])) + '\t' + str(string.format(real_lattice[2][1])) + '\t' + str(string.format(real_lattice[2][2])) + '\n'

        # Count number of atoms in the original cell file, n
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1

    string = "{0:." + str(pos_digit) + "f}"

    # Cycle through each old atom and scale to new relative positions in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos_x = float(cell[6 + i].split()[1])
        if pos_x > 0.98:
            pos_x = pos_x - 1
        pos_y = float(cell[6 + i].split()[2])
        if pos_y > 0.98:
            pos_y = pos_y - 1
        pos_z = float(cell[6 + i].split()[3])
        if pos_z > 0.98:
            pos_z = pos_z - 1
                            
        cell_new[6 + i] = atom + '\t' + str(string.format(pos_x)) + '\t' + str(string.format(pos_y)) + '\t' + str(string.format(pos_z)) + '\n'
  
        i = i + 1

    # Write cell_new to a new .cell file
    g = open(chem + '.cell','w')
    g.writelines( cell_new )
    g.close
    print '.cell file tidied up so that all columns are the same width within each section'
    return

#****************************************************************************

# Cut the cell down to a smaller size and expand the fractional coordinates to fill the same space in real space
# Function assumes that all unit cells are approx 1/n the length of a supercell axis containing n unit cells (with a margin for error) 
def cut_cell(chem, dim_old, tag, dims_cut):
    f = open(chem+'.cell','r')
    cell = f.readlines()
    cell_new = cell

    dim_cut  = {'a':dims_cut[0],'b':dims_cut[1],'c':dims_cut[2]}
    dims_old = {'a':dim_old[0],'b':dim_old[1],'c':dim_old[2]}

    # Find the new dimensions in each dimension being extended
    dims_new = {}
    for d in dims_old:
        dims_new[d] = dims_old[d] - dim_cut[d]
        
    # Scale the x, y and z lattice parameters and write to cell_new
    a_x = float(cell[1].split()[0])
    b_x = float(cell[2].split()[0])
    b_y = float(cell[2].split()[1])
    c   = float(cell[3].split()[2])

    factors = {}
    for d in dims_new:
        factors[d] = float(dims_new[d])/dims_old[d]

    a_pris = a_x/dims_old['a']

    a_x = a_x*factors['a']
    b_x = b_x*factors['b']
    b_y = b_y*factors['b']
    c   = c*factors['c']

    cell_new[1] = str(a_x) + ' 0.00' + ' 0.00\n'
    cell_new[2] = str(b_x) + ' ' + str(b_y) + ' 0.00\n'
    cell_new[3] = '0.00' + ' 0.00 ' + str(c) + '\n'

    # Count number of atoms in the original cell file, n
    f.seek(0,0)
    
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_1 = num
            
    f.seek(0,0)

    for num, line in enumerate(f):
        if '%ENDBLOCK POSITIONS_FRAC' in line:
            l_2 = num
            
    n = l_2 - l_1
    
    i = 1

    shrink = {}
    for d in factors:
        shrink[d] = float(1)/factors[d]   # scale factor by which to shrink fractional coordinates

    del_list = []
    # Cycle through each old atom and scale to new relative positions in the new 2D cell
    while i < n:

        # Information on old atoms
        atom  = str(cell[6 + i].split()[0])
        pos_x = float(cell[6 + i].split()[1])
        pos_y = float(cell[6 + i].split()[2])
        pos_z = float(cell[6 + i].split()[3])

        deleted = 0
        posns   = {'a':pos_x,'b':pos_y,'c':pos_z}
        pos_new = {}
        for d in posns:
            pos_new[d] = str(posns[d]*shrink[d])
            if posns[d] > (0.95*float(dims_new[d]))/dims_old[d] and dims_new[d] != dims_old[d]:
                deleted = 1

        cell_new[6 + i] = atom + '\t' + str(pos_new['a']) + '\t' + str(pos_new['b']) + '\t' + str(pos_new['c']) + '\n'

        if deleted == 1:
            del_list.insert(0,6+i)

        i = i + 1

    for j in del_list:
        del cell_new[j]

    # Write cell_new to a new .cell file
    g = open(tag + '.cell','w')
    g.writelines( cell_new )
    g.close
    print 'excess atoms in orignial .cell file removed to shrink cell to [' + str(float(dims_new['a'])/dims_old['a']) + ',' + str(float(dims_new['b'])/dims_old['b']) + ',' + str(float(dims_new['c'])/dims_old['c']) + '] of original size'
    return
        

#****************************************************************************

# Check if a string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#****************************************************************************

# Attempt at colouring bands in BS according to PDOS
def colour_bands(BS_filename, PDOS_filename, Fermi_offset, total_DOS_filename=0, set_colours=1 ):
    f = open( BS_filename, 'r')
    lines_f = f.readlines()
    for line in lines_f:
        if 'Number of k-points' in line:
            n_kpoints = int(line.split()[3])
    for line in lines_f:
        if 'Number of eigenvalues' in line:
            n_bands = int(line.split()[3])
    for line in lines_f:
        if 'Number of spin components' in line:
            n_spins = int(line.split()[4])
    k = 0
    b = 0
    s = 0
    band = []
    bands = []
    while b < n_bands:
        while k < n_kpoints:
            while s < n_spins:
                band.append(27.21138386*float(lines_f[11+b+k*(n_spins*(n_bands+1)+1)+s*(n_bands+1)].split()[0])+Fermi_offset)
                s = s + 1
            k = k + 1
            s = 0
        bands.append(band)
        band = []
        k = 0
        b = b + 1

    bands_range = []
    for band in bands:
        E_min = min(band)-0.05
        E_max = max(band)+0.05
        bands_range.append([E_min, E_max])

    f.close()
    
    # For testing
    print 'analysis of .bands file complete'

    f = open( PDOS_filename, 'r')
    lines_f = f.readlines()
    
    projectors = []
    f.seek(0,0)
    for num, line in enumerate(f):
        if 'Projector:' in line:
            proj  = lines_f[num].split()[2]
            name  = lines_f[num+2].split()[1] + '(' + lines_f[num+2].split()[3] + ')'
            projectors.append(name)

    colour_table = {'S(s)':5,'S(p)':11,'S(d)':7,'O(s)':13,'O(p)':2,'O(d)':10,'Mo(s)':14,'Mo(p)':12,'Mo(d)':4} 
    colour_data = {'S(s)':'255 255 0', 'S(p)':'255 165 0', 'S(d)':'220 220 220', 'O(s)':'103 7 72', 'O(p)':'255 0 0', 'O(d)':'255 0 255', 'Mo(s)':'64 224 208','Mo(p)':'114 33 188','Mo(d)':' 0 0 255'}

    n_projs = len(projectors)
    i = 0
    bands_colour = []
    print 'calculating band colours'
    for band in bands_range:
        pdos = []
        i = 0
        while i < n_projs:
            pdos.append(0)
            i = i + 1
        for line in lines_f:
            if is_number(line.split()[0]) == True:
                E = float(line.split()[0])
                if E > band[0] and E < band[1]:
                    i = 0
                    while i < n_projs:
                        pdos[i] = pdos[i] + float(line.split()[i+1])
                        i = i + 1
                elif E > band[1]:
                    break
        print 'bands ' + str(band[0]) + ' - ' + str(band[1]) + ' with pdos ' + str(pdos).strip('[]')

        colour = str(colour_table[projectors[pdos.index(max(pdos))]])   # find the number of the colour associated with the orbital with the highest pdos
        if set_colours == 1:
            bands_colour.append([bands_range.index(band), colour, pdos])
        elif set_colours == 0:
            i = 0
            red = 0
            green = 0
            blue = 0
            pdos_tot = sum(pdos)
            if pdos_tot != 0:
                while i < n_projs:
                    red = (pdos[i]/pdos_tot)*int(colour_data[projectors[i]].split()[0]) + red
                    green = (pdos[i]/pdos_tot)*int(colour_data[projectors[i]].split()[1]) + green 
                    blue = (pdos[i]/pdos_tot)*int(colour_data[projectors[i]].split()[2]) + blue
                    i = i + 1
                if int(red) > 255:
                    red = 255
                elif int(red) < 0:
                    red = 0
                if int(blue) > 255:
                    blue = 255
                elif int(blue) < 0:
                    blue = 0
                if int(green) > 255:
                    green = 255
                elif int(green) < 0:
                    green = 0
                colour = '(' + str(int(red)) + ', ' + str(int(green)) + ', ' + str(int(blue)) + ')'
            else:
                colour = (220, 220, 220)
            bands_colour.append([bands_range.index(band), colour, pdos])
                
    f.close()

    # For testing
    print 'analysis of .pdos.dat file complete'
    return bands_colour

#****************************************************************************

# For a given total calculation memory, predicts how many processors are needed to parallise a job on Kittel
def calc_cores(total_mem, mem_max=2750, cores_per_node=8):      # on Kittel NEVER change the max memory allowance
    least_cores = int(total_mem/mem_max) + 1
    i = least_cores
    a = 0
    while a < 1:
        if float(i)/int(cores_per_node) - i/int(cores_per_node) == 0:
            a = 1
        else:
            i = i + 1
            cores = i

    return cores

#****************************************************************************

# Assesses the memory usage requirements for a running job as compared to the computer
def assess_mem(filename, cores, computer, node='default', queue='parallel.q'):
    h = open( filename,'r')
    lines_h  = h.readlines()
    h.seek(0,0)
    total_mem = 0
    for line in lines_h:
        if 'Approx. total storage required per node' in line:
            unit      = line.split()[8]
            if unit   == 'KB':
                power = -6
            elif unit == 'MB':
                power = -3
            elif unit == 'GB':
                power = 0
            total_mem = int(cores)*float(line.split()[7])*(10**power)

    # Note all memory values given in GB
    if 'rabi' in computer:
        max_core_mem = 5.3
    elif 'zener' in computer:
        if node != 'default':
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect('compute-0-' + str(node))
                (stdin, stdout, stderr) = ssh.exec_command('free -m')
                output = stdout.read()
                lines = output.split('\n')
                max_core_mem = float(lines[1].split()[1])/8000
            except:
                print 'Paramiko client failed taking available memory from previous records'
                if int(node) == 17 or  int(node) == 18 or int(node) == 19:
                    max_core_mem = 1.5
                elif int(node) == 20:
                    max_core_mem = 1.25
                else:
                    max_core_mem = 1
        elif node == 'default':
            max_core_mem = 1.5
    elif 'kittel' in computer:
        max_core_mem = 2.875
    elif 'ironman' in computer:
        if queue == 'parallel.q':
            max_core_mem = float(23)/8
        elif queue == 'newpara.q':
            max_core_mem = float(63)/12
    
    available_mem = max_core_mem * int(cores)

    config.total_mem     = total_mem
    config.available_mem = available_mem
    memory = [total_mem, available_mem]
    return memory

#****************************************************************************

# Send an email notification
def send_email(subject, message, attachment='none', address='c_ablitt@msn.com'):
    username = 'py.notifications.cja92'
    extension = '@gmail.com'
    email = username + extension
    password = 'DXfWkMvsbR'

    """The first step is to create an SMTP object, each object is used for connection 
with one server."""

    import smtplib

    #host_comp()
    #if 'scarlet' in config.computer or 'rabi' in config.computer:
    #from email.mime.multipart import MIMEMultipart
    #from email.mime.text import MIMEText
    #from email.mime.base import MIMEBase
    #from email import Encoders
    #elif 'zener' in config.computer:

    from email.MIMEText import MIMEText
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email import Encoders

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    #Next, log in to the server
    server.login(username, password)

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = address
    msg.attach(MIMEText(message))

    if attachment != 'none':
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="' + attachment + '"')
        msg.attach(part)

    #Send the mail
    server.sendmail(email, address, msg.as_string())
    return

#****************************************************************************

# Check whether a castep calculation has successfully completed
def check_complete(filename):
    global complete
    h = open( filename,'r')
    h.seek(0,0)
    if 'Total time' in h.read():
        h.seek(0,0)
        if 'Calculation time' in h.read():
            complete = 1
        else:
            complete = 0
    else:
        complete = 0
    return complete

#****************************************************************************

def update_O2(chem, a_temp, bondlength_temp,EELS=0):
    global a
    global bondlength
    a = a_temp
    bondlength = bondlength_temp

    f = open('%s.cell' % chem,'r')
    lines_f  = f.readlines()

    # Update lattice parameters
    lines_f[1]    = str(a) + ' 0.00 0.00\n'
    lines_f[2]    = '0.00 ' + str(a) + ' 0.00\n'
    lines_f[3]    = '0.00 0.00 ' + str(a) + '\n'

    f.seek(0,0)
    for num, line in enumerate(f):
        if '%BLOCK POSITIONS_FRAC' in line:
            l_B = num

    if EELS==0:
        lines_f[l_B+1]    = 'O ' + str(0.5 - float(bondlength)/(2*a)) + ' 0.5 0.5\n' 
    elif EELS==1:
        lines_f[l_B+1]    = 'O:1 ' + str(0.5 - float(bondlength)/(2*a)) + ' 0.5 0.5\n' 
    lines_f[l_B+2]    = 'O ' + str(0.5 + float(bondlength)/(2*a)) + ' 0.5 0.5\n'
    
    f = open('%s.cell' % chem,'w')
    f.writelines( lines_f )
    f.close()
    print 'Final lattice parameters a = b = c = ' + str(a) + ' and O - O bondlength is ' +  str(bondlength) + ' in .cell file'
    config.O2_cell_size = a
    return

#****************************************************************************

# Find O-O bondlength
def get_O2_bondlength( filename ):
    global bondlength
    h = open( filename,'r')
    lines_h  = h.readlines()
    for line in lines_h:
        if 'O 1 -- O 2' in line:
            bondlength = line.split()[6]
    h.close()
    return bondlength

#****************************************************************************

# Attempt to run a function and in the event of an error simply log the error and move on to the next stage of the script
# As long as the module is already imported then module should not be a string if referring to an external module
def attempt(function, inputs, script, module='local',logfile='email', cont=1, max_errors=3, keyword_inputs='none', final_act='none', final_act_inputs='none', final_act_module='none'):
    import traceback

    # Run the function
    try:
        if module=='local':
            import __main__
            if keyword_inputs=='none':
                getattr(__main__, function)(*inputs)
            else:
                getattr(__main__, function)(*inputs,**keyword_inputs)
        else:
            if keyword_inputs=='none':
                getattr(module, function)(*inputs)
            else:
                getattr(module, function)(*inputs,**keyword_inputs)

    # If the maximum number of errors reached in a sub-attempt-function (look at a script and it will make sense)
    except MaxError, e:
        print 'MaxError: ' + str(e)
        config.error_no = 0
        incident_time = print_time()
        if cont == 1:
            cont_string = '\nThe script has continued to run after this error.\n'
        elif cont == 0:
            cont_string = '\nThe script has been aborted after this error.\n'

        # Print error message to screen and send an email or append an error log file as required
        if logfile == 'email':
            host_comp
            send_email(script + ' Problem','The maximum number of allowed errors have been reached within the ' + str(function) + ' section of the script: ' + script + ' running on ' + config.computer + ' and therefore this section of the simulation had to be abandoned.\n\n' + cont_string)
        elif logfile == 'none':
            pass
        else:
            f = open(logfile,'a')
            f.write(incident_time + '\nMaximum number of allowed errors reached within the ' + function + ' section of the script and therefore this section of the simulation had to be abandoned\n' + cont_string + '\n\n')
        print incident_time

        # If instructed to do so, abort the script
        if cont == 0:
            import sys
            sys.exit('script ' + script + ' has been aborted')

        return

    # In the event of an error
    except:
        
        # Record the error traceback
        config.error_no = config.error_no + 1
        error = traceback.format_exc()
        incident_time = print_time()
        if cont == 1:
            cont_string = 'The script has continued to run after this error. This was error number ' + str(config.error_no)
        elif cont == 0:
            cont_string = 'The script has been aborted after this error.'

        # Print error message to screen and send an email or append an error log file as required
        if logfile == 'email':
            host_comp
            send_email(script + ' Problem','There has been an unexpected problem with the ' + script + ' script whilst running ' + str(function) + ' on ' + str(config.computer) + '.\n\nThe following traceback error was given:\n' + str(incident_time) + '\n' + str(error) + '\n\n' + str(cont_string))
        elif logfile == 'none':
            pass
        else:
            f = open(logfile,'a')
            f.write(incident_time + '\n' + error + '\n' + cont_string + '\n\n')
        print incident_time
        print 'An error has occured with the following traceback:'
        print error
        print cont_string

        # If the maximum number of errors have been reached, raise the max_error exception
        if config.error_no > max_errors:
            raise MaxError('The maximum number of allowed errors has been reached')

        if final_act != 'none':

            # Run the final_act function (note: unlike the finally statement, this ONLY happens after an error has occured)
            try:
                if final_act_module=='local':
                    import __main__
                    if final_act_keywords=='none':
                        getattr(__main__, final_act)(*final_act_inputs)
                    else:
                        getattr(__main__, final_act)(*final_act_inputs,**final_act_keywords)
                else:
                    if final_act_keywors=='none':
                        getattr(module, final_act)(*final_act_inputs)
                    else:
                        getattr(module, final_act)(*final_act_inputs,**final_act_keywords)
            except:
                print 'error processessing requested final act'
                error = traceback.format_exc()
                print error
                pass

        # If instructed to do so, abort the script
        if cont == 0:
            import sys
            sys.exit('script ' + script + ' has been aborted')
    return

#****************************************************************************

# In the event of calculation RAM exceeding that available on the processor, the plan of action
def memory_plan_B(chem, cores, computer, max_cores=128):

    # Zener
    if 'zener' in computer:

        # Request more memory if the maximum not already requested (or if mem_total for calc > 12GB)
        if config.mem_alloc == 'default' or config.mem_alloc < 10:
            if config.available_mem > 11.5:

                # Change opt strategy to 'default'
                if config.opt_strategy == 'speed':
                    ch_opt_strategy(chem, 'default')
                    try:
                        castep_parallel(chem, cores, cont=1, mem_alloc=11)
                    except CheckError, e:
                        castep_parallel(chem, cores, cont=0, mem_alloc=11)
            else:
                try:
                    castep_parallel(chem, cores, cont=1, mem_alloc=11)
                except CheckError, e:
                    castep_parallel(chem, cores, cont=0, mem_alloc=11)

        # Change opt strategy to 'default'
        elif config.mem_alloc >= 10:
            if config.opt_strategy == 'speed':
                ch_opt_strategy(chem, 'default')
                try:
                    castep_parallel(chem, cores, cont=1, mem_alloc=11)
                except CheckError, e:
                    castep_parallel(chem, cores, cont=0, mem_alloc=11)
            else:
                raise MemError('calculation is too large to be performed on ' + computer)

    # Kittel
    if 'kittel' in computer:

        # Request more cores up to a maximum allowance (user defined but with default) 
        if cores >= max_cores:
            raise MemError('calculation is too large to be performed on ' + computer)

        else:
            
            if config.mem_alloc != 'default':
                new_cores = calc_cores(config.mem_alloc*1.5)
            
            elif config.mem_alloc == 'default':
                new_cores = calc_cores(cores*2.2875*1.5)

            if new_cores <= max_cores:
                try:
                    castep_parallel(chem, new_cores, cont=1)
                except CheckError, e:
                    castep_parallel(chem, new_cores, cont=0)
            else:
                try:
                    castep_parallel(chem, max_cores, cont=1)
                except CheckError, e:
                    castep_parallel(chem, max_cores, cont=0)

    # Rabi
    if 'rabi' in computer:

        # Change opt strategy to 'default'
        if config.opt_strategy == 'speed':
            ch_opt_strategy(chem, 'default')
            try:
                castep_parallel(chem, cores, cont=1)
            except CheckError, e:
                castep_parallel(chem, cores, cont=0)
        else:
            raise MemError('calculation is too large to be performed on ' + computer)

    return

#****************************************************************************

# Calculates H atom positions at an edge given X-H and H-H bond distances and X positions
def calc_H_pos(XH, HH, X, b=35.4789757, c=16.0, places=6):
    XH = float(XH)
    HH = float(HH)
    X = [float(X[0]),float(X[1]),float(X[2])]
    H1_z = 0.5 + HH/(2*c)
    H2_z = 0.5 - HH/(2*c)
    Hz_abs = 0.5*HH
    Xz_abs = (((X[2]-0.5)*c)**2)**0.5
    if X[1] > 0.5:
        H_y = X[1] + ((XH**2 - (Xz_abs-Hz_abs)**2)**0.5)/b
    elif X[1] < 0.5:
        H_y = X[1] - ((XH**2 - (Xz_abs-Hz_abs)**2)**0.5)/b
    H1 = str(dp(float(X[0]),places)) + '\t' + str(dp(H_y,places)) + '\t' + str(dp(H1_z,places))
    H2 = str(dp(float(X[0]),places)) + '\t' + str(dp(H_y,places)) + '\t' + str(dp(H2_z,places))
    print H1
    print H2
    return H1, H2

#****************************************************************************

# Extract data as dictionary from EELS .dat file
def extract_EELS_data(filename, broadened=1, edge='O 1    K1'):
    print 'reading data from ' + filename
    f = open(filename,'r')
    lines_f = f.readlines()
    f.seek(0,0)
    for num, line in enumerate(f):
        if edge in line:
            l_0 = num
    A = {}
    if broadened==1:
        b = 2
    elif broadened==0:
        b = 1
    for line in lines_f:
        if lines_f.index(line) > l_0:
            try:
                A[float(line.split()[0])] = float(line.split()[b])
            except IndexError:
                pass
    return A

# Extract loss function data from loss_fn.dat file
def extract_loss_fn_data(filename, broadened=1):
    print 'reading data from ' + filename
    f = open(filename,'r')
    lines_f = f.readlines()
    f.seek(0,0)
    A = {}
    if broadened==1:
        b = 2
    elif broadened==0:
        b = 1
    for line in lines_f:
        if lines_f.index(line) > 15:
            try:
                A[float(line.split()[0])] = float(line.split()[b])
            except IndexError:
                pass
    return A

# Extract data as dictionary from _epsilon.dat file
def extract_ep_data(filename, ep=2):
    print 'reading data from ' + filename
    f = open(filename,'r')
    lines_f = f.readlines()
    f.seek(0,0)
    A = {}
    for line in lines_f:
        if lines_f.index(line) > 16:
            try:
                A[float(line.split()[0])] = float(line.split()[ep])
            except IndexError:
                pass
    return A

# for each x, find 1/y unless y=0 then leave y = 0 (or visa versa x/y)
def inverse_data(A,i=1,var='y'):
    B = {}
    i = float(i)
    if var == 'y':
        y_min = 0.01*(sum(A.values())/len(A)) 
        for x in A:
            y = A[x]
            if abs(y) > y_min:
                B[x] = float(i/y)
            else:
                B[x] = 0
    elif var == 'x':
        x_min = 0.01*(sum(A.keys())/len(A))
        for x in A:
            if abs(x) > x_min:
                B[float(i/x)] = A[x]
            else:
                pass
    return B

# Calculate full loss function
def calc_full_loss(ep1, ep2):
    B = {}
    y1_min = 0.01*(sum(ep1.values())/len(ep1))
    y2_min = 0.01*(sum(ep2.values())/len(ep2))
    y_min = min([y1_min,y2_min])
    for x in ep1:
        y1 = ep1[x]
        y2 = ep2[x]
        denom = y1**2 + y2**2
        if denom > y_min**2:
            loss = float(y2)/denom
        else:
            loss = 0
        B[x] = loss
    return B

# Read EELS from simple xy .dat file, output a dictionary
def read_data_xy(filename,x=0, y=1, block=0):
    f = open(filename,'r')
    lines_f = f.readlines()
    f.seek(0,0)
    A = {}
    b = 0
    check = 0
    for line in lines_f:
        try:
            if is_number(line.split()[0]) == True:
                A[float(line.split()[x])] = float(line.split()[y])
                check = 1
        except IndexError:
            if check == 0:
                pass
            elif check == 1:
                if b < block:
                    b = b + 1
                    A = {}
                    check = 0
                else:
                    break
    return A

# Find the ideal spacing between x values
def I(A):
    d = abs(sorted(A.keys())[1]-sorted(A.keys())[0])
    D_0 = round(1/d)
    d_x = 1.0/D_0
    return d_x

# Transform an x value to an ideal x value
def i(x, d_x):
    x_1 = float("%.6f" % (float(d_x*round(x/d_x))))
    return x_1

# Shift EELS to ideal EELS at transition energy
def Q(A, s=1, E_T=0):
    A_1 = {}
    d_x = I(A)
    for x in A:
        A_1[i((x + E_T), d_x)] = s*A[x]
    return A_1

# Find the maximum EELS in a set of spectra
def MAX(A_all):
    m = []
    for A in A_all:
       m.append(max(A))
    x_max = max(m)
    return x_max

# Find the minimum EELS in a set of spectra
def MIN(A_all):
    m = []
    for A in A_all:
       m.append(min(A))
    x_min = min(m)
    return x_min

# Find the intensity of EELS at a given energy
def mag(A, x, n_max=5):
    if x in A:
        y = A[x]
    else:
        d_x = I(A)
        n = 1
        while n <= n_max:
            try:
                x_1 = float("%.6f" % (x - n*d_x))
                y_1 = A[x_1]
            except KeyError:
                y_1 = 'empty'
            try:
                x_2 = float("%.6f" % (x + n*d_x))
                y_2 = A[x_2]
            except KeyError:
                y_2 = 'empty'
            if y_1 != 'empty' and y_2 != 'empty':
                y = 0.5*(y_1 + y_2)
                n = n_max + 1
            elif y_1 == 'empty' or y_2 == 'empty':
                n = n + 1
            else:
                y = 0
                n = n_max + 1
        try:
            y = float(y)
        except UnboundLocalError:
            y = 0
    return y

# Add different spectra at a given energy
def t(A_all, x):
    y_values = []
    for A in A_all:
        y_i = mag(A, x)
        y_values.append(y_i)
    y = sum(y_values)
    y_strings = []
    for value in y_values:
        y_strings.append(str(value))
    data = str(x) + '\t' + '\t'.join(y_strings) + '\t' + str(y)
    return y, data

# Add different spectra to form a total EELS
def T(A_all, d_x=0, freq=10):
    if d_x == 0:
        d_x = I(A_all[0])
    x = MIN(A_all)
    x_max = MAX(A_all)
    print 'summing spectra between ' + str(x) + ' and ' + str(x_max) + ' ...'
    F = {}
    ALL_DATA = [] 
    while x <= x_max:
        X = float("%.6f" % x)
        (F[X], data) = t(A_all, X)
        if freq != 0:
            if int(X)/freq - float(X)/freq == 0:
                print data
        ALL_DATA.append(data + '\n')
        x = x + d_x
    return F, ALL_DATA

# Print EELS to a data file
def print_data(data, filename):
    lines = []
    energies = sorted(data.keys())
    for entry in energies:
        lines.append(str(entry) + '\t' + str(data[entry]) + '\n')
    print 'writing data to ' + filename
    f = open(filename,'w')
    f.writelines( lines )
    f.close()
    return

# Produce output shifted EELS as datafile from input data file
def shift_EELS(input_file, supercell, shift, output_file):
    A = extract_EELS_data(input_fil)
    A_1 = Q(A, supercell, shift)
    print_data(A_1, output_file)
    return

# Produce output summation of EELS as datafile
def sum_EELS(A_all, output_file):
    (F, lines) = T(A_all)
    print 'writing data to ' + output_file
    f = open(output_file,'w')
    f.writelines( lines )
    f.close()
    return

# A lot simpiler than summing coreloss spectra - no need to account for shifts/supercells
def sum_nohole_EELS(spectra_files, output_file):
    # spectra_files is a list ['chem1_core_edge.dat', 'chem2_core_edge.dat', ... etc ]

    all_EELS = []

    for spectra in spectra_files:
        EELS = extract_EELS_data( spectra )
        all_EELS.append( Q(EELS, 1, 0) )

    sum_EELS( all_EELS, output_file )

    print '\nAll spectra have been shifted and summed to form a total spectra.\n'
    return

# From input EELS data files, shift and add a set of spectra (of the same supercell size) and export as a datafile
def read_and_sum_EELS(spectra_files, ground_file, supercell, output_file, functional='LDA'):
    # spectra_files is a dictionary of form {'chem1.castep','chem1_core_edge.dat', 'chem2.castep','chem2_core_edge.dat', ... etc }
    
    shifted_EELS = []

    for spectra in spectra_files:
        EELS = extract_EELS_data( spectra_files[spectra] )
        shift = calculate_shift( spectra, ground_file, supercell, functional )
        print spectra + ' gives a shift of ' + str(shift) + ' eV' 
        shifted_EELS.append( Q(EELS, supercell, shift) )

    sum_EELS( shifted_EELS, output_file )

    print '\nAll spectra have been shifted and summed to form a total spectra.\n'
    return

# Calculate value of gaussian at x2 arising from peak at x1
def g(x2, x1, width):
    from math import pi, exp
    g = (1/(width*(2*pi)**0.5))*exp(-0.5*(((x2 - x1)/width)**2))
    return g

def p(x2, x1, width):
    from math import pi, exp, log
    g = ((4*log(2))**0.5/(width*(pi)**0.5))*exp(-4*log(2)*(((x2 - x1)/width)**2))
    return g

# Apply Guassian broadening to dataset
def gauss(A, width, d_x=0, freq_p=10, freq_o=0, gaussian='g', x2_range=['default', 'default']):
    import time

    start_time = time.time()

    if d_x == 0:
        d_x = I(A)
    
    # Output frequency (i.e. spacing of points in output file)
    if freq_o == 0:
        freq_o = d_x

    x_min = min(A)
    x_max = max(A)

    if x2_range[0] == 'default':
        x2_min = x_min
    else:
        x2_min = x2_range[0]
    if x2_range[0] == 'default':
        x2_max = x_max
    else:
        x2_max = x2_range[1]

    print 'broadening spectra between ' + str(x_min) + ' and ' + str(x_max) + ' using Gaussian broadening with width ' + str(width) + ' with sampling d_x = ' + str(d_x)
    F = {}
    ALL_DATA = []
    x2 = x2_min
    while x2 <= x2_max:
        y = 0
        
        # Only cycle through x1 values +/- 4 peak widths of x2
        if x2 - 4*width > x_min:
            x1 = x2 - 4*width
        else:
            x1 = x_min
        if x2 - 4*width < x_max:
            x1_max = x2 + 4*width
        else:
            x1_max = x_max

        # cycle through x1 values
        while x1 <= x1_max:
            if gaussian == 'g':
                y = y + g(x2, x1, width)*mag(A,x1)*d_x
            elif gaussian == 'p':
                y = y + p(x2, x1, width)*mag(A,x1)*d_x
            x1 = x1 + d_x
            x1 = float("%.6f" % x1)

        X = float("%.6f" % x2)
        data = str(X) + '\t' + str(mag(A,x2)) + '\t' + str(y)
        ALL_DATA.append(data + '\n')
        F[X] = y

        # Print frequency (i.e. frequency to print results to terminal)
        if freq_p != 0:
            if int(x2)/freq_p - float(x2)/freq_p == 0:
                print data
        x2 = x2 + freq_o
        x2 = float("%.6f" % x2)

    total_time = time.time() - start_time

    print 'calculation completed in ' + str(total_time)  + 's'

    return F, ALL_DATA

# Used as a subprocess by gauss_parallel
# Note 'n' is the process number
def gauss_serial(A, width, n, x2_range, x_range, d_x, freq_p, freq_o, gaussian, queue):

    ALL_DATA = []
    x2 = x2_range[0]
    print 'subprocess ' + str(n) + ' broadening spectra in range ' + str(x2_range[0]) + ' to ' + str(x2_range[1])
    while x2 < x2_range[1]:
        y = 0
        
        # Only cycle through x1 values +/- 4 peak widths of x2
        if x2 - 4*width > x_range[0]:
            x1 = x2 - 4*width
        else:
            x1 = x_range[0]
        if x2 - 4*width < x_range[1]:
            x1_max = x2 + 4*width
        else:
            x1_max = x_range[1]

        # cycle through x1 values
        while x1 <= x1_max:
            if gaussian == 'g':
                y = y + g(x2, x1, width)*mag(A,x1)*d_x
            elif gaussian == 'p':
                y = y + p(x2, x1, width)*mag(A,x1)*d_x
            x1 = x1 + d_x
            x1 = float("%.6f" % x1)
        X = float("%.6f" % x2)
        data = str(X) + '\t' + str(mag(A,x2)) + '\t' + str(y)
        ALL_DATA.append(data + '\n')

        # Print frequency (i.e. frequency to print results to terminal)
        if freq_p != 0:
            if int(x2)/freq_p - float(x2)/freq_p == 0:
                print data
        x2 = x2 + freq_o
        x2 = float("%.6f" % x2)

    temp_file = 'tempbroadfile_' + str(n) + '.dat'
    f = open(temp_file,'w')
    f.writelines( ALL_DATA )
    f.close()

    # Put the result into a queue for safe keeping
    queue.put([temp_file,n])

    print 'subprocess ' + str(n) + ' complete!'
        

# Apply Guassian broadening to dataset ... IN PARALLEL
def gauss_parallel(A, width, cores, d_x=0, freq_p=10, freq_o=0, gaussian='p', x2_range=['default','default']):
    import multiprocessing as mp
    from operator import itemgetter
    import time

    start_time = time.time()

    if d_x == 0:
        d_x = I(A)
    
    # Output frequency (i.e. spacing of points in output file)
    if freq_o == 0:
        freq_o = d_x

    x_min = min(A)
    x_max = max(A)

    if x2_range[0] == 'default':
        x2_min = x_min
    else:
        x2_min = x2_range[0]
    if x2_range[0] == 'default':
        x2_max = x_max
    else:
        x2_max = x2_range[1]

    print 'broadening spectra between ' + str(x2_min) + ' and ' + str(x2_max) + ' using Gaussian broadening with width ' + str(width) + ' with sampling d_x = ' + str(d_x)
    F = {}
    ALL_DATA = []

    N = int((x2_max-x2_min)/d_x)
    points = N/cores       # How many points to compute per core
    extra = N%cores        # The number of points left over i.e. remainder

    n = 0                  # Process number

    x_range = [x_min, x_max]
    x_old = x2_min
    while n < cores:
        if n < extra:
            x_new = i(x_old + d_x*points + d_x,d_x)
        else:
            x_new = i(x_old + d_x*points,d_x)
        if x_new == x2_max:
            x_new = i(x2_max + d_x,d_x)
        vars()['x2_range_' + str(n)] = [x_old, x_new]
        n = n + 1
        x_old = x_new

    processes = []
    q = mp.Queue()

    for n in range(0,cores):
        proc = mp.Process(target=gauss_serial, args=(A, width, n, vars()['x2_range_' + str(n)], x_range, d_x, freq_p, freq_o, gaussian, q))
        processes.append(proc)
        
    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()
    
    print 'all subprocesses have completed!'

    results = []
    for proc in processes:
        results.append(q.get())
    
    results = sorted(results, key=itemgetter(1))

    print 'all results have been extracted'

    ALL_DATA = []

    for result in results:
        temp_file = open(result[0],'r')
        data_temp = temp_file.readlines()
        ALL_DATA = ALL_DATA + data_temp
        temp_file.close()

    print 'all results have been compiled'
    
    total_time = time.time() - start_time

    print 'calculation completed over ' + str(cores) + ' cores in ' + str(total_time)  + 's'

    file_remove('tempbroadfile_*.dat')

    return ALL_DATA

def read_and_broaden_data(filename, output, width, broadening='gaussian', xt=0, yt=2, blockt=0, d_xt=0, freq_pt=5, freq_ot=0, gaussiant='p', cores=4):
    B = read_data_xy(filename,x=xt, y=yt, block=blockt)

    A = Q(B, 1, 0)

    if broadening == 'gaussian':
        if cores == 1:
            ALL_DATA = gauss(A, width, d_x=d_xt, freq_p=freq_pt, freq_o=freq_ot, gaussian=gaussiant) 
        elif cores > 1:
            ALL_DATA = gauss_parallel(A, width, cores, d_x=d_xt, freq_p=freq_pt, freq_o=freq_ot, gaussian=gaussiant) 

    f = open(output,'w')
    f.writelines( ALL_DATA )
    f.close()
    print 'printed original and broadened data to ' + output
    return
    
