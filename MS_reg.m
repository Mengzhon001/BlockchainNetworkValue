

addpath('/Users/andyma/Desktop/Projects/NFT project/matlab coding/MS_Regime Switchng/MS_Regress-Matlab-master/m_Files'); % add 'm_Files' folder to the search path

dau_used=dau_usd_100;
dau_trend=dau_usd_100_trend;

dep=log(Market_cap);                    % Defining dependent variable from .mat file
constVec=ones(length(dep),1);       % Defining a constant vector in mean equation (just an example of how to do it)
indep=[constVec log(dau_used)];     % Defining some explanatory variables
k=2;                                % Number of States
S=[0 1 0];                        % Defining which parts of the equation will switch states (column 1 and variance only)
advOpt.distrib='Normal';            % The Distribution assumption ('Normal', 't' or 'GED')
advOpt.std_method=1;                % Defining the method for calculation of standard errors. See pdf file for more details

[MS_results]=MS_Regress_Fit(dep,indep,k,S,advOpt); % Estimating the model
AIC=2*MS_results.Number_Parameters-2*MS_results.LL

% rmpath('m_Files');
%%%%%%%%%%%%%%%%%%%%%%% fit
%%% for state 1
predict_state1=[MS_results.Coeff.nS_Param{1}(1) , MS_results.Coeff.S_Param{1}(1)]*[constVec log(dau_trend)]';
State1=zeros(1,length(Market_cap));
State1(1,MS_results.smoothProb(:,1)>=0.5)=1;
predict_state1(1,State1==0)=nan;
predict_state1=exp(predict_state1)';
%%% for state 2
predict_state2=[MS_results.Coeff.nS_Param{1}(1) , MS_results.Coeff.S_Param{1}(2)]*[constVec log(dau_trend)]';
predict_state2(1,State1==1)=nan;
predict_state2=exp(predict_state2)';

%%%%%%%%%%%%%%%%%%%%%%% plot
% Date_unique=datenum(day1);
% Shadow=zeros(1,length(Date_unique));
% Shadow(1,MS_results.smoothProb(:,1)>=0.5)=1;
% 
% 
% patch([Date_unique',flip(Date_unique')], [6*10^(12)*Shadow,flip(-10000*Shadow)],[0.8 0.8 0.8],'facealpha',0.4,'edgealpha',0,'edgecolor',[0 0 0])
% 
% hold on
% plot(Date_unique,Market_cap,'-', 'Color', [0.53 0.81 0.92],'linewidth',1.5)
% hold on
% plot(Date_unique,predict_state1,'linewidth',2)
% hold on
% plot(Date_unique,predict_state2,'linewidth',2)

%%%%% reversed
Date_unique=datenum(day1);
Shadow=zeros(1,length(Date_unique));
Shadow(1,MS_results.smoothProb(:,2)>=0.5)=1;

patch([Date_unique',flip(Date_unique')], [6*10^(12)*Shadow,flip(-10000*Shadow)],[0.8 0.8 0.8],'facealpha',0.4,'edgealpha',0,'edgecolor',[0 0 0])

hold on
plot(Date_unique,Market_cap,'-', 'Color', [0.53 0.81 0.92],'linewidth',1.5)
hold on
plot(Date_unique,predict_state2,'linewidth',2)
hold on
plot(Date_unique,predict_state1,'linewidth',2)

%%%%% reversed end

ylabel('Market Cap',"FontName","Times New Roman","FontSize",17);
ylim([min(Market_cap) max(Market_cap)*1.1])
xlim([min(Date_unique),max(Date_unique)])

set(gca,"FontName","Times New Roman","FontSize",15,"LineWidth",1.5)
xlabel("Time","FontName","Times New Roman","FontSize",17);

set(gcf,'unit','normalized','position',[0.2,0.2,0.44,0.22]);

datetick('x','yyyy-mm')

% legend('State 1','Market Cap','Fitted Market Cap (State1)','Fitted Market Cap (State2)','Location', 'northwest')
legend('State 1','Market Cap','Fitted Market Cap (State1)','Fitted Market Cap (State2)')
% set(gcf,'unit','normalized','position',[0.2,0.2,0.7,0.4]);
