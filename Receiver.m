function [Tgot] = Receiver(varargin)
% Algorithm receiver uses to get its message 
%       Receiver(Xp, M, A)
%
%
%
Xp = varargin{1};
M = varargin{2};
A = varargin{3};
[n,m] = size(M);
[~,len] = size(Xp);
if m > len
    Xp(n) = 0;
    X = Xp;
else
    X = Xp;
end
[U, D, V] = svd(M);
%Mt = U*X;
Tgot = [];
for count = 1:1:n
    a = (A(count, :))';
    f = U(count, :);
    d = D*V'*a;
    if isrow(X)
        X = X';
    end
    in = X - d;
    Tgot(count) = f*(in);
end
