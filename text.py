import numpy as np
import matplotlib.pyplot as plt

# Sample data points (replace with your actual data)
x_data = np.array([0,300,400,450,500])
y_data = np.array([0,0.1,0.15,0.5,0.95])

# Log-transform the y-values
log_y_data = np.log(y_data)

# Perform linear regression on the log-transformed data
coeffs = np.polyfit(x_data, log_y_data, 1)
b = coeffs[0]
ln_a = coeffs[1]
a = np.exp(ln_a)

# Generate points to plot the fitted curve
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = a * np.exp(b * x_fit)

# Plot the original data and the fitted curve
plt.scatter(x_data, y_data, label='Data Points')
plt.plot(x_fit, y_fit, color='red', label=f'Fitted: $y = {a:.2f}e^{{{b:.2f}x}}$')
plt.title('Exponential Fit')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

# Print the fitted parameters
print(f"Fitted parameters: a = {a:.2f}, b = {b:.2f}")
