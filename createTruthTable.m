%Create a dictionary of cities and serial numbers, 
%the serial numbers are used to index the matrix later
dic=containers.Map;
[num,txt,raw]=xlsread('Tables for storing dictionaries');
[ro,co]=size(raw);

for a=2:ro
    dic(char(raw(a,1)))=cell2mat(raw(a,2));
end
 
% Create the truth table
for yea=2016:2018
    filename=['data in folders'];
    [num,txt,raw]=xlsread(filename,1);
    [ro2,co]=size(raw);
    adja=zeros(ro2,ro-1);
    
    % Read adjacent records row by row
    for r=1:ro2
        str1=char(raw(r,2));
        ss=strsplit(str1);
        [~,cos]=size(ss);
        
        for cc=1:cos
            % corresponds to the index value according to the city name
            no=dic(char(ss(1,cc)));            
            adja(r,no)=1;                     
        end        
    end
    
    filename=['Save Location'];
    xlswrite(filename,adja);
    disp(yea)
end