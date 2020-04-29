clc;
close all;
clear;

%% Detta script skapar csv matriser med autocovariance

filelist=uigetfile('*.h5','Select the INPUT DATA FILE(s)','MultiSelect','on');

data=[];
    for k=1:size(filelist,2)
        temp=ReadData_h5_Env(filelist{k});
        data=[data temp];
    end

    [samples,frames]=size(data);
    step=16; % Downsampling
    data_downsampled=data(1:step:samples-25,:); % ful lösning
    [samples_ds,frames_ds]=size(data_downsampled)
    lags=5;
    T=50;
    
    AC=[];
    for i=1:T:frames_ds
       temp=ACF(data_downsampled(:,i:i+T-1),lags);
       temp=reshape(temp,1,[]);
       AC=[AC;temp];
    end
    size(AC)
    
    prompt={'Ange namn på .csv fil:'};
    namn=inputdlg(prompt,'Input');
    namn=cell2mat(namn);
    writematrix(AC,['AC_' namn '.csv']);



