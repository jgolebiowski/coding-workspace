data = load('ex1data1.txt');
X = data(:, 1); 
y = data(:, 2);
m = length(y); % number of training examples

fprintf('Computing cost ...\n')

X = [ones(m, 1), data(:,1)]; % Add a column of ones to x
theta = zeros(2, 1); % initialize fitting parameters

% Some gradient descent settings
iterations = 1500;
alpha = 0.01;

% compute and display initial cost
computeCost(X, y, theta)

fprintf('Running Gradient Descent ...\n')

% run gradient descent
theta = gradientDescent(X, y, theta, alpha, iterations);

% print theta to screen
fprintf('Theta found by gradient descent: ');
fprintf('%f %f \n', theta(1), theta(2));

% % % Plot the linear fit
% % hold on; % keep previous plot visible
% % plot(X(:,2), X*theta, '-')
% % legend('Training data', 'Linear regression')
% % hold off % don't overlay any more plots on this figure

% % Predict values for population sizes of 35,000 and 70,000
% predict1 = [1, 3.5] *theta;
% fprintf('For population = 35,000, we predict a profit of %f\n',...
%     predict1*10000);
% predict2 = [1, 7] * theta;
% fprintf('For population = 70,000, we predict a profit of %f\n',...
%     predict2*10000);