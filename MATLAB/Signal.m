function [M, T] = Signal(varargin)
%   Generates random signal based on probabilty and matrix size
%   Returns NxN sized matrix, M, and message vector, T
%   [M, T] = Signal(N, P)
%
%
K = varargin{1};
cntP = varargin{2};
M = rand(K,K);
for i=1:K
    for j=1:K
        if M(i,j) < (1-cntP)
            M(i,j) = 0;
        else
            M(i,j) = NaN;
        end
        % Set the diagonal to 1
        if i == j
            if M(i,j) < (1-cntP)
                M(i,j) = 0;
            else
                M(i,j) = 1;
            end
        end
    end
end
T = randi([0,1000],1,K);


        
