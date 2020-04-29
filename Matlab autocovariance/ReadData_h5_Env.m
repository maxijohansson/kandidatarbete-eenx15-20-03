function [data_matrix] = ReadData_h5_Env(filename)
%READDATA Summary of this function goes here
%   Detailed explanation goes here
%
% Input: 
% Output: 


% data_matrix=squeeze(h5read([filename '.h5'],'/data')); % Load dataset from H5-file
data_matrix=squeeze(h5read([filename],'/data')); % Load dataset from H5-file


end

