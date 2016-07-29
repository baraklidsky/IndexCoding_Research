function [A] = Known(varargin)
%   Makes Matrix A with what each receiver knows of others messages
%       [A] = Known(M,T)
%   M is original matrix and T is each receivers wanted message
%
% EX:   M = [0 NaN 0;0 0 NaN; NaN 0 0]
%       T = [1 , 2 , 3]
%       [A] = Known(M, T);
%       A = [0 2 0;0 0 3;1 0 0]
M = varargin{1};
T = varargin{2};
[siz, ~] = size(M);
A(siz,siz) = 0;
for int=1:1:siz
    for ant=1:1:siz
        if isnan(M(int,ant))
            A(int,ant) = T(ant);
        end
    end
end
