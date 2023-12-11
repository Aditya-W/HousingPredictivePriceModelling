# -*- coding: utf-8 -*-
"""437FinalProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EkAkQjTNfvkUPSOOVga1vnlz1OkxDwGy

# **Importing Libraries**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

"""#**Initializing DataFrame**#"""

df = pd.read_csv('/content/AmsterdamHousing.csv')

"""#**Exploratory Data Analysis**#

This helps us identify obvious errors and understand patterns within the data.
"""

# EDA Section
# Summary statistics
print(df.describe())

# Correlation heatmap
# helps identify which variables can include faults in the analysis
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

# Pairplot to visualize relationships between features and the target variable
# Helps identify obvious errors and understand patterns within the data
sns.pairplot(df[['Area', 'Room', 'Lon', 'Lat', 'Price']])
plt.title("Relationships Between Features and Target Variables")
plt.show()

"""#**Handle Missing Values**#"""

# Check for missing values in the target variable
print(df['Price'].isnull().sum())  # Check if there are missing values in the 'Price' column

# If there are missing values, handle them before splitting the data
df = df.dropna(subset=['Price'])  # Drop rows with missing 'Price' values

# Separate features and target variable
# Price is chosen as a target variable because it allows for the most accurate analysis
X = df[['Area', 'Room', 'Lon', 'Lat']]
y = df['Price']

"""#**Feature Engineering:**#


*   Polynomial Features: Generate polynomial features to capture potential nonlinear relationships between features and the target variable.
*   Interaction Terms: Create interaction terms by multiplying different features together to capture combined effects.




"""

# Enhances the model's ability to represent complex interactions between variables.
# Add Polynomial Features and Interaction Terms
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
X_train_poly, X_test_poly, y_train_poly, y_test_poly = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Standardize Polynomial Features
scaler_poly = StandardScaler()
X_train_poly_scaled = scaler_poly.fit_transform(X_train_poly)
X_test_poly_scaled = scaler_poly.transform(X_test_poly)

# Ridge Regression with Polynomial Features
ridge_reg_poly = Ridge(alpha=1.0)
ridge_reg_poly.fit(X_train_poly_scaled, y_train_poly)
ridge_pred_poly = ridge_reg_poly.predict(X_test_poly_scaled)
ridge_rmse_poly = mean_squared_error(y_test_poly, ridge_pred_poly, squared=False)
print("Ridge Regression with Polynomial Features RMSE:", ridge_rmse_poly)

# Split the data into training and testing sets for original features
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize original features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""#**Regression Models**#"""

# Linear Regression
# Establishes a fundamental understanding of the relationship
# between independent variables (features like area, rooms, location) and the target variable (price).
linear_reg = LinearRegression()
linear_reg.fit(X_train_scaled, y_train)
linear_pred = linear_reg.predict(X_test_scaled)
linear_rmse = mean_squared_error(y_test, linear_pred, squared=False)
linear_r2 = r2_score(y_test, linear_pred)
print("Linear Regression RMSE:", linear_rmse)
print("Linear Regression R-squared:", linear_r2)

#Both of these introduce regularization to prevent model overfitting and improve generalization
# by penalizing large coefficients.
# Ridge Regression
ridge_reg = Ridge(alpha=1.0)
ridge_reg.fit(X_train_scaled, y_train)
ridge_pred = ridge_reg.predict(X_test_scaled)
ridge_rmse = mean_squared_error(y_test, ridge_pred, squared=False)
ridge_r2 = r2_score(y_test, ridge_pred)
print("Ridge Regression RMSE:", ridge_rmse)
print("Ridge Regression R-squared:", ridge_r2)

# Lasso Regression
lasso_reg = Lasso(alpha=0.1)
lasso_reg.fit(X_train_scaled, y_train)
lasso_pred = lasso_reg.predict(X_test_scaled)
lasso_rmse = mean_squared_error(y_test, lasso_pred, squared=False)
lasso_r2 = r2_score(y_test, lasso_pred)
print("Lasso Regression RMSE:", lasso_rmse)
print("Lasso Regression R-squared:", lasso_r2)

# Cross-validation
cv_scores = cross_val_score(ridge_reg, X_train_scaled, y_train, cv=5, scoring='neg_mean_squared_error')
cv_rmse = (-cv_scores.mean()) ** 0.5
print("Cross-Validation RMSE (Ridge):", cv_rmse)

"""#**Hyper Parameter Tuning**#"""

# Hyperparameter tuning for Ridge Regression
params = {'alpha': [0.1, 1.0, 10.0]}
ridge_grid = GridSearchCV(Ridge(), params, cv=5)
ridge_grid.fit(X_train_scaled, y_train)
best_alpha = ridge_grid.best_params_['alpha']
print("Best alpha for Ridge Regression:", best_alpha)

# Feature Importance for Ridge Regression
plt.figure(figsize=(8, 6))
coef = ridge_reg.coef_
feature_names = ['Area', 'Room', 'Lon', 'Lat']
sns.barplot(x=coef, y=feature_names)
plt.title("Feature Importance (Ridge Regression)")
plt.xlabel("Coefficient")
plt.ylabel("Feature")
plt.show()

# Residuals Plot
plt.figure(figsize=(8, 6))
residuals = y_test - ridge_pred
sns.scatterplot(x=y_test, y=residuals)  # Specify x and y-axis variables separately
plt.axhline(y=0, color='r', linestyle='--')
plt.title("Residuals Plot (Ridge Regression)")
plt.xlabel("Actual Price")
plt.ylabel("Residuals")
plt.show()

"""#**Regulariztion Techniques**#"""

from sklearn.linear_model import ElasticNet
from sklearn.model_selection import RandomizedSearchCV

# ElasticNet Regression
# Controls for multicollinearity while encouraging sparse feature selection, contributing to model interpretability and performance
elastic_net = ElasticNet(alpha=1.0, l1_ratio=0.5)  # You can tune alpha and l1_ratio
elastic_net.fit(X_train_scaled, y_train)
elastic_pred = elastic_net.predict(X_test_scaled)
elastic_rmse = mean_squared_error(y_test, elastic_pred, squared=False)
elastic_r2 = r2_score(y_test, elastic_pred)
print("ElasticNet Regression RMSE:", elastic_rmse)
print("ElasticNet Regression R-squared:", elastic_r2)

# Early Stopping (example with SGDRegressor)
from sklearn.linear_model import SGDRegressor
from sklearn.base import clone
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils._testing import ignore_warnings

sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1, warm_start=True)

minimum_val_error = float("inf")
best_epoch = None
best_model = None

for epoch in range(1000):
    sgd_reg.fit(X_train_scaled, y_train)  # Continues where it left off
    y_val_predict = sgd_reg.predict(X_test_scaled)
    val_error = mean_squared_error(y_test, y_val_predict)
    if val_error < minimum_val_error:
        minimum_val_error = val_error
        best_epoch = epoch
        best_model = clone(sgd_reg)
        # You can add early stopping criteria here
        # For example, if the validation error does not decrease for several iterations, break the loop

print("Best Epoch:", best_epoch)

"""#**Model Ensemble Techniques:**#


*   Random Forest or Gradient Boosting: Use ensemble methods to combine multiple models for improved predictions.
*   Stacking: Combine predictions of multiple models to create a meta-model.




"""

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_predict

#Offer higher predictive accuracy by combining multiple weak learners (trees) and reducing bias and variance.
# Random Forest Regression
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train_scaled, y_train)
rf_pred = rf_reg.predict(X_test_scaled)
rf_rmse = mean_squared_error(y_test, rf_pred, squared=False)
rf_r2 = r2_score(y_test, rf_pred)
print("Random Forest Regression RMSE:", rf_rmse)
print("Random Forest Regression R-squared:", rf_r2)

# Gradient Boosting Regression
gb_reg = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
gb_reg.fit(X_train_scaled, y_train)
gb_pred = gb_reg.predict(X_test_scaled)
gb_rmse = mean_squared_error(y_test, gb_pred, squared=False)
gb_r2 = r2_score(y_test, gb_pred)
print("Gradient Boosting Regression RMSE:", gb_rmse)
print("Gradient Boosting Regression R-squared:", gb_r2)

# Stacking (combining predictions of multiple models)
# Improves prediction accuracy by leveraging the strengths of various models, reducing the impact of individual model weaknesses.
models = [linear_reg, ridge_reg, lasso_reg, elastic_net, rf_reg, gb_reg]
predictions = []
for model in models:
    pred = cross_val_predict(model, X_train_scaled, y_train, cv=5)
    predictions.append(pred)

stacked_predictions = np.mean(np.array(predictions), axis=0)
stacked_rmse = mean_squared_error(y_train, stacked_predictions, squared=False)
print("Stacked Models RMSE:", stacked_rmse)