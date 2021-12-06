yangmin=0;
yang=0;
[Exist]=xlsread('F:\\小论文\\真值表.xlsx',2,'B2:AB247');
%[time]=xlsread('F:\data\设阈值的真值表\无阈值-高铁.xlsx',11,'AG2:AG274');
%disp(Exist);
%xlswrite('F:\try.xlsx',Exist);
% Exist(:,1)=[];
[ro,co]=size(Exist);
influ=zeros(1,co);
    
for a=1:ro
    for b=1:co
        Tem=Exist;
%         Tem(a,b)=1-Tem(a,b);%翻转节点
%         Tem(a,b)=xor(Exist(a,b),1);%翻转节点
        if Tem(a,b)==1
            Tem(a,b)=0;
        %假如翻转某个节点后的共现模式存在，unique函数的结果矩阵将减少一行
            if size(Tem,1)==size(unique(Tem,'rows'),1)
                 yangmin=yangmin+1;
                 influ(1,b)=influ(1,b)+1;
            end
       end
    end   
end
% end

% influ=influ/ro;
% influ=influ/2^co;
% zongmin=yangmin*2;
% fprintf('阳性敏感度为:%d\n',yangmin/ro);
% fprintf('%d\n',yangmin/ro);
% fprintf('阴性敏感度为:%d\n',yangmin/(2^co-ro));
% fprintf('%d\n',yangmin/(2^co-ro));
% fprintf('平均敏感度为:%d\n',zongmin/2^co);
% fprintf('%d\n',zongmin/2^co);
% fprintf('总敏感度为:%d\n',zongmin);
% fprintf('%d\n',zongmin);
fprintf('%d ',influ);
            
