function plots(datanamn)

sensor_vinkel = 30; %Anges inte detta i h5 filen?
height = 17.5;

dataset=h5read([datanamn '.h5'],'/data'); % Load dataset from H5-file


timestamp=h5read([datanamn '.h5'],'/timestamp'); % Time of measurement
session_info=h5read([datanamn '.h5'],'/session_info'); % Session info (e.g. length & ranges)
label=h5read([datanamn '.h5'],'/label'); % Label (Dry,snow,wet etc.)
sensor_config_dump=h5read([datanamn '.h5'],'/sensor_config_dump'); % Configuration paramters
% % % sensor_vinkel=h5read([datanamn '.h5'],'/angel'); % Angle of radar
% % % height=h5read([datanamn '.h5'],'/distance'); % Height of radar
temperature=h5read([datanamn '.h5'],'/temp'); % temp

%Extract information from datasets
all_info=split(session_info,',');
sensor_config_split=split(sensor_config_dump,',');

start=regexp(all_info(1),'[0-9].[0-9]','match');
distance_range=regexp(all_info(2),'[0-9].[0-9]','match');
data_length=regexp(all_info(3),'[0-9]','match');
step_length=regexp(all_info(5),'[0-9].[0-9][0-9]','match');
% % % sensor_vinkel=regexp(sensor_vinkel(1),'[0-9][0-9]','match');
% % % height=regexp(height(1),'[0-9][0-9].[0-9]','match');
temperature=regexp(temperature(1),'\d*','match');
update_rate=regexp(sensor_config_split(6),'[0-9][0-9][0-9].[0-9]','match');


step_length = str2double(cell2mat(step_length{1,1}));
data_length = str2double(cell2mat(data_length{1,1}));
range = str2double(cell2mat(distance_range{1,1}));
start = str2double(cell2mat(start{1,1}));
label=cell2mat(label);
% % % sensor_vinkel=str2double(cell2mat(sensor_vinkel{1,1}));
% % % height=str2double(cell2mat(height{1,1}));
temperature=str2double(cell2mat(temperature{1,1}));
update_rate=str2double(cell2mat(update_rate{1,1}));


time_temp=cell2mat(timestamp);
time_split=split(time_temp,'T');
date=cell2mat(time_split(1));
time=cell2mat(time_split(2));
clear time_temp time_split;


real=dataset.r;
im=dataset.i;
size_r=size(real); % (1) samples, (2) sensor, (3) Frames

% Display information
disp(['Dataname: ',datanamn]);
disp(['Surface type: ', label]);
disp(['-Date of measurement: ',date]);
disp(['-Time: ',time]);
disp(['-Samples in distance interval ',num2str(start),'-',num2str(start+range),' m']);
disp(['-Distance between samples: ',num2str(step_length),' m']);
disp(['-Angle ',num2str(sensor_vinkel),'°']);
disp(['-Height of radar ',num2str(height),' m']);
disp(['-Temperature ',num2str(temperature),'°C']);
disp(['-Update rate: ',num2str(update_rate),' Hz']);
disp(['-Number of frames: ',num2str(size_r(3))]);
disp(['-Samples per frame: ',num2str(size_r(1))]);


dist=linspace(start,range+start,data_length); % Vector with distance samples

% amplitude=@(d,array,sweep) sqrt(real(d,array,sweep).^2+im(d,array,sweep).^2); % sweep=sweep nr, d=dist index
amp=sqrt(real.^2+im.^2);


% Mean and variance of amplitude
mean_amplitude=mean(amp,3);
var_amplitude=var(amp,0,3);
sigma_amplitude=sqrt(var_amplitude); % Standardavvikelse

% Mean and variance of real part
mean_real=mean(real,3);
var_real=var(real,0,3);
sigma_real=sqrt(var_real); % Standardavvikelse

% Mean and variance of imaginary part
mean_im=mean(im,3);
var_im=var(im,0,3);
sigma_im=sqrt(var_im); % Standardavvikelse

figure('Name','Rectangular');

subplot(2,2,1)
% REAL part
hold on;
plot(dist,mean_real,'DisplayName','Mean'); % Medel
plot(dist,mean_real+sigma_real,'LineStyle','--','DisplayName','+1 STD'); % +1 standardavvikelse
plot(dist,mean_real-sigma_real,'LineStyle','--','DisplayName','-1 STD'); % -1 standardavvikelse
hold off;
title('Mean + STD of real part')
xlabel('Distance [m]') 
ylabel('Amplitude') 
legend('location','southeast')

subplot(2,2,2)
% IMAGINARY part
hold on;
plot(dist,mean_im,'DisplayName','Mean'); % Medel
plot(dist,mean_im+sigma_im,'LineStyle','--','DisplayName','+1 STD'); % +1 standardavvikelse
plot(dist,mean_im-sigma_im,'LineStyle','--','DisplayName','-1 STD'); % -1 standardavvikelse
hold off;
title('Mean + STD of imaginary part')
xlabel('Distance [m]') 
ylabel('Amplitude') 
legend('location','southeast')

subplot(2,2,3)
%histogram realdel första toppen?
subplot(2,2,4)
%histogram imaginärdel första toppen?


figure('Name','Polar');
subplot(2,2,1)
hold on;
plot(dist,mean_amplitude,'DisplayName','Mean'); % Medel
plot(dist,mean_amplitude+sigma_amplitude,'LineStyle','--','DisplayName','+1 STD'); % +1 standardavvikelse
plot(dist,mean_amplitude-sigma_amplitude,'LineStyle','--','DisplayName','-1 STD'); % -1 standardavvikelse
hold off;
title('Mean + STD  of "amplitude"')
xlabel('Distance [m]') 
ylabel('Amplitude') 
legend

subplot(2,2,2)
%Fasen (unwrap?)
subplot(2,2,3)
%histogram absolutvärdet för första toppen
subplot(2,2,4)
%histogram fasen första toppen

