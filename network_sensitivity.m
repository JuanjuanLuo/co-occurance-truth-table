yangmin=0;
[Exist]=xlsread('truth talbe');

[ro,co]=size(Exist);
influ=zeros(1,co);
    
for a=1:ro
    for b=1:co
        Tem=Exist;
       if Tem(a,b)==1
            Tem(a,b)=0;
        %If a co-occurrence pattern exists after flipping a node, 
        %the result matrix of the unique function will be reduced by one row
            if size(Tem,1)==size(unique(Tem,'rows'),1)
                 yangmin=yangmin+1;
                 influ(1,b)=influ(1,b)+1;
            end
       end
    end
end

zongmin=yangmin/ro;
fprintf('network sesitivity:%d\n',zongmin);
            
