# pymc3 model in development
with pm.Model() as twitter_model:
    # global model parameters
    # Time-related hyperparameters
    alpha = pm.Normal('alpha', mu=0, sd=100)
    sigma_squared_delta = pm.InverseGamma('sigma_squared_delta', alpha=2, beta=2)
    log_a_tau = pm.Normal('log_a_tau', mu=0, sd=10)
    b_tau = pm.Gamma('b_tau', alpha=1, beta=.002)
    
    # Graph-related hyperparameters
    # binom model for graph structure
    sigma_squared_b = pm.InverseGamma('sigma_squared_b', alpha=0.5, beta=0.5, testval=10000)
    beta_0 = pm.Normal('beta_0', mu=0, sd=100)
    beta_F = pm.Normal('beta_F', mu=0, sd=100)
    beta_d = pm.Normal('beta_d', mu=0, sd=100)
    
    # log-normal model for reaction times, nonrecursive...
    a_tau = pm.Deterministic('a_tau', pm.math.exp(log_a_tau))
    for i in range(num_root_tweets):
        t_x = pm.InverseGamma('tau_x_squared_' + str(i), alpha=a_tau, beta=b_tau)
        a_x = pm.Normal('alpha_x_' + str(i), mu=alpha, tau=1/sigma_squared_delta)        
        l_x = pm.Normal('log_s_j_x_' + str(i), mu=a_x, tau=t_x**0.5, observed=log_s_j_x[i])
        
        # binom model for user
        for j, row in tweet_dfs[i].iterrows():
            f_j_x = row['FollowerCount']
            d_j_x = row['DistanceFromRoot']
            b_j_x = beta_0 + beta_F*math.log(f_j_x + 1) + beta_d*math.log(d_j_x + 1)
            mu_j = beta_0 + beta_f*