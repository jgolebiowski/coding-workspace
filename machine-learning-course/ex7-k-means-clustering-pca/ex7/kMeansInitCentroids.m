function centroids = kMeansInitCentroids(X, K)
%KMEANSINITCENTROIDS This function initializes K centroids that are to be 
%used in K-Means on the dataset X
%   centroids = KMEANSINITCENTROIDS(X, K) returns K initial centroids to be
%   used with the K-Means on the dataset X
%

% You should return this values correctly
centroids = zeros(K, size(X, 2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should set centroids to randomly chosen examples from
%               the dataset X
%

%Randomly permute a vector from 1:K
% Randomly reorder the indices of examples
idxrand = randperm(size(X, 1));

%Select the first examples from the list of randomized indices
% Take the first K examples as centroids
centroids = X(idxrand(1:K), :);

% =============================================================

end

