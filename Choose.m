function [Xp, M]=Choose(varargin)
%Takes IC,MinRank, and message(T) and chooses the rows to send using SVD
%     
%     [Mess]=Choose(M, Rmin, T)
%
M = varargin{1};
R = varargin{2};
T = varargin{3};
[~,D,V] = svd(M);
%error checking, if Rmin and non-zero diag do not equal
[lim, ~] = size(D);
non = 0;
for int= 1:1:lim
    if abs(D(int, int))  > .001
        non = non + 1;
    end
end
if non ~= R
     warning('Rank does not match non-zero singular values')
end
X = D*(V')*T';
[ma, ~] = size(X);
Xp = X;
delete = 0;
for index=1:1:ma
    if abs(X(index)) < .001
        Xp(index - delete) = [];
        delete = delete + 1; %#ok<NASGU>
    end
end