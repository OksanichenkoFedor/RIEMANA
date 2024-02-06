import numpy as np

def generate_particles(num, xsize):
    x = np.random.random((num,1))*xsize
    angle = np.random.random((num,1))*np.pi - np.pi*0.5
    angle = np.where(angle<0,angle+2*np.pi,angle)
    #angle = np.random.random() * np.pi + np.pi * 0.5
    #angle = np.random.random() * np.pi*2.0
    is_add = (np.random.random((num,1))>1.1).astype(float)
    return np.concatenate((x,angle,is_add),axis=1)#[x, angle, is_add]