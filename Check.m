function [Error] = Check(varargin)
%Checks to see how close received messaged was to original
%   [Error] = Check(Tgot, T);
%   returns average error margin
%
Tgot = varargin{1};
%Tgot = round(Tgot, 5);
T = varargin{2};
[~, len] = size(Tgot);
[~, len2] = size(T);
error = [];
if len == len2
    for i=1:1:len
        error(i) = abs(T(i) - Tgot(i)); %#ok<AGROW>
    end
else
    warning('Message sizes do not match')
end
Error = mean(error);

