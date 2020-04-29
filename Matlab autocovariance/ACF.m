function [ACF_matrix] = ACF(x, maxlag)
%ACF Summary of this function goes here
%   Detailed explanation goes here
% Input: 
% Output: 

[samples,frames]=size(x);
x_mean=mean(x,2);
% ACF_matrix=zeros(maxlag,samples);
ACF_matrix=zeros(samples,maxlag);
for lag=1:maxlag
    for n=1:samples
        sum=0;
            for t=lag+1:frames
                sum =sum + (x(n,t)-x_mean(n))*(x(n,t-lag)-x_mean(n))';
            end
%         ACF_matrix(lag,n)=sum/(frames-lag);
            ACF_matrix(n,lag)=sum/(frames-lag);
    end
end
