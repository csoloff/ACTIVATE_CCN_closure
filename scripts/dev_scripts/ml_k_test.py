import pandas as pd
import numpy as np
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor  # ML model
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load and preprocess data
d = pd.read_csv('./tables/merged_observed.csv')
d = d[np.logical_not((d['Ice_Flag_2DS']==1) | (d['ED-liquid_2DS']>=60E-6) | (d['LWC_FCDP']>0.005) | (d['ams_tot'] < 0.04) | (d['N_CCN_stdPT'] < 50))].reset_index(drop=True)
d = d[(d['Org_Ave_IsoK_STP']>=0) & (d['SO4_Ave_IsoK_STP']>=0) & (d['NO3_Ave_IsoK_STP']>=0) & (d['NH4_Ave_IsoK_STP']>=0) & (d['Chl_Ave_IsoK_STP']>=0)].reset_index(drop=True)
d = d.dropna(subset=['k_obs'])

d = d[(d['k_obs']>0.0)&(d['k_obs']<.05)]

# Define the function to calculate 'k' values based on given kappas
def calc_k(data, org_k, so4_k, no3_k, nh4_k, chl_k):
    d = data.copy()
    d['Org_vc'] = d['Org_Ave_IsoK_STP'] / 1000
    d['SO4_vc'] = d['SO4_Ave_IsoK_STP'] / 1770
    d['NO3_vc'] = d['NO3_Ave_IsoK_STP'] / 1770
    d['NH4_vc'] = d['NH4_Ave_IsoK_STP'] / 1770
    d['Chl_vc'] = d['Chl_Ave_IsoK_STP'] / 2200
    d['ams_tot_vc'] = d['Org_vc'] + d['SO4_vc'] + d['NO3_vc'] + d['NH4_vc'] + d['Chl_vc']
    d['k'] = (
        org_k * d['Org_vc'] / d['ams_tot_vc'] +
        so4_k * d['SO4_vc'] / d['ams_tot_vc'] +
        no3_k * d['NO3_vc'] / d['ams_tot_vc'] +
        nh4_k * d['NH4_vc'] / d['ams_tot_vc'] +
        chl_k * d['Chl_vc'] / d['ams_tot_vc']
    )
    return d

# Objective function for optimization
def objective(params, d):
    org_k, so4_k, no3_k, nh4_k, chl_k = params
    k_predicted = calc_k(d, org_k, so4_k, no3_k, nh4_k, chl_k)['k']
    return np.sum((d['k_obs'] - k_predicted)**2)

# Initial guesses for kappas
initial_guess = [0.1, 0.1, 0.1, 0.1, 0.1]

# Optimization to fit 'k_obs' using defined function
result = minimize(objective, initial_guess, args=(d,), method='Nelder-Mead')
org_k_opt, so4_k_opt, no3_k_opt, nh4_k_opt, chl_k_opt = result.x
print("Optimized kappa values:")
print("org_k:", org_k_opt)
print("so4_k:", so4_k_opt)
print("no3_k:", no3_k_opt)
print("nh4_k:", nh4_k_opt)
print("chl_k:", chl_k_opt)

# Adding calculated 'k' to the DataFrame
d = calc_k(d, *result.x)
plt.scatter(d['k_obs'], d['k'], s=0.5)
plt.xlabel('Observed k')
plt.ylabel('Predicted k (optimized)')
#plt.xlim([0, 0.18])
plt.show()

# Machine Learning Component - Predicting 'k_obs' with Gradient Boosting Regressor
# Define feature columns
feature_cols = ['Org_Ave_IsoK_STP', 'SO4_Ave_IsoK_STP', 'NO3_Ave_IsoK_STP', 'NH4_Ave_IsoK_STP', 'Chl_Ave_IsoK_STP']
X = d[feature_cols]
y = d['k_obs']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor()#GradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error (ML model):", mse)

# Compare predictions with observed values
plt.scatter(y_test, y_pred, s=0.5)
plt.xlabel('Observed k_obs')
plt.ylabel('Predicted k_obs (ML model)')
plt.xlim([y_test.min(), y_test.max()])
plt.ylim([y_test.min(), y_pred.max()])
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_pred.max()], 'r--')  # 1:1 line
plt.show()
