function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

% vector of hypothesis values for each training example and the lambda vector
h = sigmoid(X * theta);
lambdaVec = ones(length(theta), 1) * lambda;
lambdaVec(1) = 0;

% Evaluate the cost
J = (1/m) * ( -y' * log(h) - (1-y)' * log(1-h) ) + (1/ (2 * m)) * (lambdaVec .* theta)' * theta;

%Evaluate gradient
grad = (1/m) * X' * (h - y) + (1/m) * lambdaVec .* theta;




% =============================================================

end
