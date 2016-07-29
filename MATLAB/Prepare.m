function [UpM, T]=Prepare(varargin)
%Finds matrix with receiver that need information along with their side
%information
%     
%     [UpM]=Prepare(M)
%
UpM = varargin{1};
T = varargin{2};
M = UpM;
[n,~] = size(M);
%if matrix is empty return
if n == 0
    return
else
    delete = 0;
    %look at every row to determine if receiver has message (a 1 in the NxN
    %spot
    for count=1:1:n
            % If a zero in NxN spot, delete row and column N
            if M(count,count)
               UpM(count - delete,:) = [];
               UpM(:,count - delete)=[];
               T(count - delete) = [];
               delete = delete + 1;
            end
    end    
end
