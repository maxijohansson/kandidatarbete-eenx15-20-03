function [data_matrix] = ReadData_h5_IQ(filename)
%READDATA Summary of this function goes here
%   Detailed explanation goes here
%
% Input: filename exlusive '.h5', Ex: ReadData('maskingrand_move_30_1') 
% Output: Datamatrix dimension (samples x frames) or (fasttime x slowtime)


dataset=h5read([filename],'/data');
real=dataset.r;
im=dataset.i;

data_matrix=squeeze(sqrt(real.^2+im.^2));

end

