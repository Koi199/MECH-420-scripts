## Curve fitting
# Script to fit a curve on a given data 

## Import libraries
# Data Manipulation
import pandas as pd  # For data manipulation and analysis
import numpy as np   # For numerical operations

# Data Visualization
import matplotlib.pyplot as plt  # For creating static, interactive, and animated visualizations
import seaborn as sns            # For statistical data visualization
from scipy.optimize import curve_fit

#import dataset, skipping the first row 
dataset = pd.read_csv("Lab1_prelab_curve_fitting.csv", skiprows = 1)
print(dataset)

#define the model function to fit
def model_function(x, a, b, c):
    #S = a + be^(cx)
    return  a + b* np.exp(c*x)

#Initial guess
initial_guess = [1, 1, 1]

# Use curve_fit to fit the model to the data
popt, pcov = curve_fit(model_function, dataset['distance (mm)'], dataset['Signal (V)'], p0=initial_guess)

# Get the fitted parameters
a, b, c = popt

# Formatted to 2 decimal places
a_formatted = f'{a:.2f}'
b_formatted = f'{b:.2f}'
c_formatted = f'{c:.2f}'
# Calculate the fitted values using the original x-values
y_fit = model_function(dataset['distance (mm)'], *popt)

# Calculate R^2 score manually
def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

r2 = r2_score(dataset['Signal (V)'], y_fit)
r2_formatted = f'{r2:.2f}'

# Print fitted parameters and R^2 score
print(f"Fitted parameters: a = {a}, b = {b}, c = {c}")
print(f"R^2 score: {r2_formatted}")

# Create the figure and axis
fig, ax = plt.subplots()

# Plot the data points and fitted curve
ax.plot(dataset['distance (mm)'], dataset['Signal (V)'], marker='o', label='Data Points')
ax.plot(dataset['distance (mm)'], y_fit, label=rf'Fitted Line: $S = {a_formatted} + {b_formatted} e^{{({c_formatted} x)}}$', color='red')

# Move the x-axis and y-axis to intersect at zero
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')

# Hide the top and right spines
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Set limits to ensure visibility
ax.set_xlim(min(dataset['distance (mm)']) - 0.05, max(dataset['distance (mm)']) + 0.2)
ax.set_ylim(min(dataset['Signal (V)']) - 2, max(dataset['Signal (V)']) + 1)

# Set labels and title
ax.set_xlabel('Distance (mm)')
ax.set_ylabel('Signal (V)')
ax.set_title(rf'Curve Fitting: $S = a + b e^{{(c x)}}$')

# Show the grid
ax.grid(True)

# Add the R^2 score as text annotation
ax.text(0.05, 0.9, f'$R^2 = {r2_formatted}$', transform=ax.transAxes, fontsize=12, verticalalignment='top')

# Display the legend
ax.legend(loc = 'lower right')

# Show the plot
plt.show()
