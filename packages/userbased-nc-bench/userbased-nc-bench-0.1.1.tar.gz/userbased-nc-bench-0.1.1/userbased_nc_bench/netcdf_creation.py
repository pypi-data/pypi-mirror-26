#!/usr/bin/env python2.7

import numpy as np
from netCDF4 import Dataset
import sys

def create_netcdf(size, path):
    # Calculate dim size
    
    fid = path+'test_2d_chunkC.nc'
    f = Dataset(fid,'w',format='NETCDF4')
    dim1 = f.createDimension('dim1',size[0])
    dim2 = f.createDimension('dim2',size[1])
    var = f.createVariable('var','f8',('dim1','dim2'))#,chunksizes=(430,430))#,chunksizes=(11584,46336))

    for i in range(size[0]):
        var[i,:] = np.random.random(size[1])

    f.close()

def create_netcdf_4d(size, path):
    # Calculate dim size
    
    fid = path+'test_4d_chunkF.nc'
    f = Dataset(fid,'w',format='NETCDF4')
    dim1 = f.createDimension('dim1',size[0])
    dim2 = f.createDimension('dim2',size[1])
    dim2 = f.createDimension('dim3',size[2])
    dim2 = f.createDimension('dim4',size[3])
    var = f.createVariable('var','f8',('dim1','dim2','dim3','dim4'),chunksizes=(430,1,1,430))#,chunksizes=(430,1,430,430)

    for i in range(size[1]):
        for j in range(size[2]):
            var[:,i,j,:] = np.random.random((size[0],size[3]))

    f.close()



def create_netcdf_1d(size, path, fname, buffersize, mpirank):
    # Calculate dim size
    dimsize = long(size/8.)
    bsize = long(buffersize/8.)
    fid = path+fname+str(mpirank)+'.nc'
    f = Dataset(fid,'w',format='NETCDF4')
    dim1 = f.createDimension('dim1',dimsize)
    var = f.createVariable('var','f8',('dim1'))

    for i in xrange(0,dimsize,bsize):
        slice_ind0 = i
        slice_ind1 = i+bsize
        var[slice_ind0:slice_ind1] = np.random.random(bsize)



    f.close()



if __name__ == '__main__':
    
    '''size = long(sys.argv[3]) # in bytes
    path = sys.argv[1]
    fname = sys.argv[2]
    create_netcdf_1d(size, path, fname, buffersize)
    #create_netcdf((184900,184900), path)
    #create_netcdf_4d((430,430,430,430), path)
    print 'Finished'
    '''
