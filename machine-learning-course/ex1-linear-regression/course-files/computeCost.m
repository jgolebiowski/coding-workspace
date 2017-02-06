function J = computeCost(X, y, theta)
%COMPUTECOST Compute cost for linear regression
%   J = COMPUTECOST(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;


% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta
%               You should set J to the cost.

% The hypothesis is given as h(x) = X * theta
% As a result h(x) - y is given as 
% (X * theta - y)
% ANs the cost fuctions as 1/2m * (X * theta -y).T * (X * theta - y)

errValue = (X * theta - y);
J = ( 1/(2*m) ) * errValue' * errValue;



% =========================================================================

end
