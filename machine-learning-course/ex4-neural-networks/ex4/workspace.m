
%% Initialization
clear ; close all; clc


input_layer_size  = 3;  % 20x20 Input Images of Digits
hidden_layer_size = 4;   % 25 hidden units
num_labels = 2;          % 10 labels, from 1 to 10   
                          % (note that we have mapped "0" to label 10)

X = [1 2 3; 4 5 6]
y = [1 2]
Theta1 = [1 1 2 3; 2 4 5 6; 3 7 8 9;4 10 11 12] 
Theta2 = [1 1 2 3 4; 2 5 6 7 8]
nn_params = [Theta1(:) ; Theta2(:)];

lambda = 1;

J = nnCostFunction_vectorized(nn_params, input_layer_size, hidden_layer_size, ...
                   num_labels, X, y, lambda)