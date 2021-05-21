"""
intro to pystan
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import stan

def sim_legs(n):
    """simulate leg lengths"""
    np.random.seed(0)
    height = np.random.normal(10, 2, size=n)
    leg_prop = np.random.uniform(0.4, 0.5, n)
    leg_left = leg_prop * height + np.random.normal(0, 0.02, n)
    left_right = leg_prop * height + np.random.normal(0, 0.02, n)
    legs = {"N": n,
            "height": height,
            "leg_left": leg_left,
            "leg_right": left_right}
    return legs

stan_code = """
data{
    int<lower=0> N;  
    vector[N] height;
    vector[N] leg_right;
    vector[N] leg_left;
}
parameters{
    real a;
    real bl;
    real br;
    real<lower=0> sigma;
}
model{
    vector[N] mu;
    sigma ~ exponential( 1 );
    br ~ normal( 2 , 10 );
    bl ~ normal( 2 , 10 );
    a ~ normal( 10 , 100 );
    for ( i in 1:N ) {
        mu[i] = a + bl * leg_left[i] + br * leg_right[i];
    }
    height ~ normal( mu , sigma );
}
"""
# generated quantities{
#     vector[N] log_lik;
#     vector[N] mu;
#     for ( i in 1:N ) {
#         mu[i] = a + bl * leg_left[i] + br * leg_right[i];
#     }
#     for ( i in 1:N ) log_lik[i] = normal_lpdf( height[i] | mu[i] , sigma );
# }

# simulate
legs_data = sim_legs(n=100)
# print(legs_data)

# fit
posterior = stan.build(stan_code, data=legs_data)
fit = posterior.sample(num_chains=4, num_samples=1000)
df = fit.to_frame()  # pandas `DataFrame, requires pandas
print(df)

# plot
df_params = df[['bl', 'br', 'a']]
g = sns.pairplot(df_params)
plt.savefig('./ch10.png')