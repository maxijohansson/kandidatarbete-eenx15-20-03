function pick_and_plot(timelags, plot_sample,divide_frames,line_color)
%PICK_AND_PLOT Summary of this function goes here
%   Detailed explanation goes here

% timelags= number of lags
% plot_sample= välj för vilken fasttime sample som ska plottas
% frames_divide= hur många frames som ska vara med för varje AC
% line_color= färg på linje t.ex. 'r','b','k'

% Vill man plotta flera platser kan man köra funktionen flera gånger utan
% att stänga plotfönstret

% Ex. pick_and_plot(10,300,5000,'r'), 10 lags, sample 300, 5000 frames( 10
% mätningar*500 frames ger en linje) och röd linje

filelist=uigetfile('*.h5','Select the INPUT DATA FILE(s)','MultiSelect','on');

if isequal(filelist,0)
    disp('No file picked');
    return;
end

if ischar(filelist)
    data=ReadData_h5_Env(filelist);
    name=filelist;
    
else
    data=[];
    name=filelist{1};
    for k=1:size(filelist,2)
%         temp=ReadData_h5_IQ(filelist{k}); % IQ
        temp=ReadData_h5_Env(filelist{k}); % Envelope
        data=[data temp];
    end
end    
    [samples,frames]=size(data);
    AC=[];
    
    for i=1:divide_frames:frames
       temp=ACF(data(:,i:i+divide_frames-1),timelags);
       AC=[AC temp];
    end
    disp(size(AC));
   name=regexp(name,'_\d','split');
    lags=1:timelags;
    hold on;
    for plots=1:frames/divide_frames
%%% ej normalized
        if plots==1
            plot(lags,AC(plot_sample,timelags*(plots-1)+1:timelags*(plots-1)+timelags),'DisplayName',name{1},'Marker','o','Color',line_color);
        else
            plot(lags,AC(plot_sample,timelags*(plots-1)+1:timelags*(plots-1)+timelags),'Marker','o','Color',line_color);
        end
%%% Normalized
%         if plots==1
%             plot(lags,AC(plot_sample,timelags*(plots-1)+1:timelags*(plots-1)+timelags)/AC(plot_sample,(plots-1)*timelags+1),'DisplayName',name{1},'Marker','o','Color',line_color);
%         else
%             plot(lags,AC(plot_sample,timelags*(plots-1)+1:timelags*(plots-1)+timelags)/AC(plot_sample,(plots-1)*timelags+1),'Marker','o','Color',line_color);
%         end
    end
    title(['AC at sample ' num2str(plot_sample)]);
    xlabel('Timelags')
    legend('location','northeast','Interpreter', 'none')
    grid on;
end


