Variational Bayesian Inference Toolbox

--------------------------------------


This module is inspired by the paper 'Black Box Variational Inference'
by Rajesh Ranganath et al. It attempts to make nearly trivial the task
of fitting a variational distribution to a user-specified log-likelihood
function without derivatives. Currently it only uses a
mean field variational distribution, but the main class 
VariationalInferenceMF is flexible enough for simple subclassing in the
future. This module also contains a number of implementations of
stochastic gradient descent algorithms to be used for optimization.


