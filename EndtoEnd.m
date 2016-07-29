function EndtoEnd(varargin)
%   End to End system of Index Coding Model
%   Calls Sigal to generate a random  NxN matrix and messages
%   Calls Prepare to remove unneccesary signals from matrix
%   Calls APIndex Coding to rank reduce M
%   Calls Choose to select which independent rows to send
%   Calls Receiver to have receivers decode their messages
%       EndtoEnd(N); N = size of wanted sqaure matrix

N = varargin{1};
expRound = 100;
lstAvgRMin= [];
%AvgError = [];
for cntP=0.1:0.05:0.7
    sumRMin=0;
    cntP
    sumErr = 0;    
    for cnt=1:expRound
        [G, t] = Signal(N, cntP);
        [UpM, T]=Prepare(G, t);
        [rMin, M] = APIndexCoding(G);
        sumRMin=sumRMin+rMin;
        [len, ~] = size(M);
        if rMin < len
            [Xp, Ma]=Choose(M, rMin, t);
            [A] = Known(G, t);
            [Tgot] = Receiver(Xp, Ma, A);
            [Error] = Check(Tgot, t);
            sumErr = sumErr + Error;
        end
        
    end
    %avgErr = sumErr/expRound;
    avgRMin=sumRMin/expRound;
    lstAvgRMin=[lstAvgRMin avgRMin]; %#ok<AGROW>
    %AvgError = [AvgError avgErr]; %#ok<AGROW>
end
x = (.1:.05:.7);
%plot (x, AvgError)
%figure;
plot(x, lstAvgRMin)
lstAvgRMin


