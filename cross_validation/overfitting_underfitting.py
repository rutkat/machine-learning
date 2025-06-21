# Import necessary libraries for numerical computations, plotting, and machine learning
import numpy as np  # For numerical operations and array manipulations
import matplotlib.pyplot as plt  # For creating plots and visualizations
from sklearn.pipeline import Pipeline  # For creating machine learning pipelines
from sklearn.preprocessing import PolynomialFeatures  # For creating polynomial features
from sklearn.linear_model import LinearRegression  # For linear regression model
from sklearn.metrics import mean_squared_error  # For calculating mean squared error
from sklearn.model_selection import train_test_split  # For splitting data into train/test sets
import seaborn as sns  # For enhanced plotting styles and color palettes

# Set matplotlib style to use seaborn for better-looking plots
plt.style.use('seaborn-v0_8')
# Set color palette for consistent and attractive colors across plots
sns.set_palette("husl")

def generate_data(n_samples=100, noise=0.1):
    """
    Generate synthetic data with a known underlying function plus noise.
    
    Parameters:
    n_samples (int): Number of data points to generate
    noise (float): Standard deviation of Gaussian noise to add
    
    Returns:
    X: Feature array (1D array reshaped to 2D for sklearn compatibility)
    y: Target values with noise
    y_true: True target values without noise
    """
    # Set random seed for reproducible results
    np.random.seed(42)
    # Create evenly spaced feature values from 0 to 10
    X = np.linspace(0, 10, n_samples).reshape(-1, 1)
    # Define the true underlying function: y = 2*x + 0.5*x^2
    y_true = 2 * X.flatten() + 0.5 * X.flatten()**2
    # Add Gaussian noise to create realistic data
    y = y_true + noise * np.random.randn(n_samples)
    return X, y, y_true

def fit_polynomial_model(X, y, degree):
    """
    Fit a polynomial regression model of specified degree.
    
    Parameters:
    X: Feature array
    y: Target values
    degree (int): Degree of polynomial (1=linear, 2=quadratic, etc.)
    
    Returns:
    model: Fitted sklearn Pipeline object
    """
    # Create a pipeline that first creates polynomial features, then fits linear regression
    model = Pipeline([
        ('poly', PolynomialFeatures(degree=degree, include_bias=False)),  # Create polynomial features
        ('linear', LinearRegression())  # Fit linear regression on polynomial features
    ])
    # Fit the model to the training data
    model.fit(X, y)
    return model

def plot_overfitting_underfitting_demo():
    """
    Create comprehensive visualization showing underfitting, good fit, and overfitting.
    This function creates a 2x3 subplot showing three different polynomial degrees
    and their corresponding residual plots.
    """
    
    # Generate synthetic data with moderate noise for clear demonstration
    X, y, y_true = generate_data(n_samples=50, noise=0.5)
    # Split data into training (70%) and test (30%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Create a figure with 2 rows and 3 columns of subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    # Add main title to the entire figure
    fig.suptitle('Overfitting vs Underfitting Demonstration', fontsize=16, fontweight='bold')
    
    # Define polynomial degrees to test: 1 (underfitting), 2 (good fit), 15 (overfitting)
    degrees = [1, 2, 15]
    # Define descriptive titles for each subplot
    titles = ['Underfitting (Degree 1)', 'Good Fit (Degree 2)', 'Overfitting (Degree 15)']
    
    # Loop through each polynomial degree and create visualizations
    for i, (degree, title) in enumerate(zip(degrees, titles)):
        # Fit polynomial model of current degree to training data
        model = fit_polynomial_model(X_train, y_train, degree)
        
        # Create fine-grained x values for smooth plotting
        X_plot = np.linspace(0, 10, 1000).reshape(-1, 1)
        # Generate predictions for plotting (smooth curve)
        y_pred_plot = model.predict(X_plot)
        # Generate predictions for training data
        y_pred_train = model.predict(X_train)
        # Generate predictions for test data
        y_pred_test = model.predict(X_test)
        
        # Calculate mean squared error for training data
        train_error = mean_squared_error(y_train, y_pred_train)
        # Calculate mean squared error for test data
        test_error = mean_squared_error(y_test, y_pred_test)
        
        # Plot training data points (blue dots)
        axes[0, i].scatter(X_train, y_train, color='blue', alpha=0.6, label='Training Data', s=50)
        # Plot test data points (red dots)
        axes[0, i].scatter(X_test, y_test, color='red', alpha=0.6, label='Test Data', s=50)
        
        # Plot the true underlying function (green dashed line)
        axes[0, i].plot(X_plot, 2 * X_plot.flatten() + 0.5 * X_plot.flatten()**2, 
                       'g--', linewidth=2, label='True Function', alpha=0.8)
        
        # Plot model predictions (orange solid line)
        axes[0, i].plot(X_plot, y_pred_plot, 'orange', linewidth=3, label='Model Prediction')
        
        # Set subplot title with error metrics
        axes[0, i].set_title(f'{title}\nTrain MSE: {train_error:.3f}, Test MSE: {test_error:.3f}', 
                            fontsize=12, fontweight='bold')
        # Set x-axis label
        axes[0, i].set_xlabel('X')
        # Set y-axis label
        axes[0, i].set_ylabel('y')
        # Add legend to subplot
        axes[0, i].legend()
        # Add grid for better readability
        axes[0, i].grid(True, alpha=0.3)
        
        # Calculate residuals (actual - predicted) for training data
        residuals_train = y_train - y_pred_train
        # Calculate residuals for test data
        residuals_test = y_test - y_pred_test
        
        # Plot training residuals vs predicted values (blue dots)
        axes[1, i].scatter(y_pred_train, residuals_train, color='blue', alpha=0.6, 
                          label='Training Residuals', s=50)
        # Plot test residuals vs predicted values (red dots)
        axes[1, i].scatter(y_pred_test, residuals_test, color='red', alpha=0.6, 
                          label='Test Residuals', s=50)
        # Add horizontal line at y=0 for reference
        axes[1, i].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        # Set x-axis label for residual plot
        axes[1, i].set_xlabel('Predicted Values')
        # Set y-axis label for residual plot
        axes[1, i].set_ylabel('Residuals')
        # Set title for residual subplot
        axes[1, i].set_title('Residual Plot')
        # Add legend to residual subplot
        axes[1, i].legend()
        # Add grid to residual subplot
        axes[1, i].grid(True, alpha=0.3)
    
    # Adjust layout to prevent overlap between subplots
    plt.tight_layout()
    # Save the figure as a high-resolution PNG file
    plt.savefig('overfitting_underfitting_demo.png', dpi=300, bbox_inches='tight')
    # Display the plot
    plt.show()

def plot_learning_curves():
    """
    Plot learning curves to demonstrate bias-variance tradeoff.
    Learning curves show how training and test errors change with training set size.
    """
    
    # Generate larger dataset for learning curve analysis
    X, y, _ = generate_data(n_samples=200, noise=0.3)
    
    # Test different polynomial degrees to show varying complexity
    degrees = [1, 2, 5, 10]
    # Create array of training set sizes from 10% to 100% of data
    train_sizes = np.linspace(0.1, 1.0, 20)
    
    # Create 2x2 subplot grid for learning curves
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    # Add main title
    fig.suptitle('Learning Curves: Bias-Variance Tradeoff', fontsize=16, fontweight='bold')
    
    # Loop through each polynomial degree
    for i, degree in enumerate(degrees):
        # Calculate row and column indices for subplot positioning
        row, col = i // 2, i % 2
        
        # Initialize lists to store error scores
        train_scores = []
        test_scores = []
        
        # Loop through different training set sizes
        for train_size in train_sizes:
            # Calculate number of samples for current training size
            n_samples = int(len(X) * train_size)
            # Split data into training and test sets
            X_train, X_test, y_train, y_test = train_test_split(
                X[:n_samples], y[:n_samples], test_size=0.3, random_state=42
            )
            
            # Fit polynomial model to current training set
            model = fit_polynomial_model(X_train, y_train, degree)
            
            # Generate predictions for training data
            train_pred = model.predict(X_train)
            # Generate predictions for test data
            test_pred = model.predict(X_test)
            
            # Calculate mean squared error for training predictions
            train_mse = mean_squared_error(y_train, train_pred)
            # Calculate mean squared error for test predictions
            test_mse = mean_squared_error(y_test, test_pred)
            
            # Store errors for plotting
            train_scores.append(train_mse)
            test_scores.append(test_mse)
        
        # Plot training error curve (blue line with markers)
        axes[row, col].plot(train_sizes * len(X), train_scores, 'o-', color='blue', 
                           label='Training Error', linewidth=2, markersize=6)
        # Plot test error curve (red line with markers)
        axes[row, col].plot(train_sizes * len(X), test_scores, 'o-', color='red', 
                           label='Test Error', linewidth=2, markersize=6)
        
        # Set subplot title
        axes[row, col].set_title(f'Polynomial Degree {degree}')
        # Set x-axis label
        axes[row, col].set_xlabel('Training Set Size')
        # Set y-axis label
        axes[row, col].set_ylabel('Mean Squared Error')
        # Add legend
        axes[row, col].legend()
        # Add grid
        axes[row, col].grid(True, alpha=0.3)
        # Set y-axis limits for consistent scaling
        axes[row, col].set_ylim(0, max(max(train_scores), max(test_scores)) * 1.1)
    
    # Adjust layout
    plt.tight_layout()
    # Save figure
    plt.savefig('learning_curves.png', dpi=300, bbox_inches='tight')
    # Display plot
    plt.show()

def plot_model_complexity_analysis():
    """
    Plot model complexity vs error to find the optimal model complexity.
    This visualization shows the U-shaped curve of test error and helps identify
    the sweet spot between underfitting and overfitting.
    """
    
    # Generate data for complexity analysis
    X, y, _ = generate_data(n_samples=100, noise=0.4)
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Test polynomial degrees from 1 to 15
    degrees = range(1, 16)
    # Initialize lists to store errors
    train_errors = []
    test_errors = []
    
    # Loop through each polynomial degree
    for degree in degrees:
        # Fit polynomial model of current degree
        model = fit_polynomial_model(X_train, y_train, degree)
        
        # Generate predictions for training data
        train_pred = model.predict(X_train)
        # Generate predictions for test data
        test_pred = model.predict(X_test)
        
        # Calculate training mean squared error
        train_mse = mean_squared_error(y_train, train_pred)
        # Calculate test mean squared error
        test_mse = mean_squared_error(y_test, test_pred)
        
        # Store errors for plotting
        train_errors.append(train_mse)
        test_errors.append(test_mse)
    
    # Create single figure for complexity analysis
    plt.figure(figsize=(12, 8))
    # Plot training error curve (blue line with markers)
    plt.plot(degrees, train_errors, 'o-', color='blue', linewidth=3, markersize=8, 
             label='Training Error', alpha=0.8)
    # Plot test error curve (red line with markers)
    plt.plot(degrees, test_errors, 'o-', color='red', linewidth=3, markersize=8, 
             label='Test Error', alpha=0.8)
    
    # Find the optimal degree (minimum test error)
    optimal_degree = degrees[np.argmin(test_errors)]
    # Add vertical line at optimal degree
    plt.axvline(x=optimal_degree, color='green', linestyle='--', linewidth=2, 
                label=f'Optimal Degree: {optimal_degree}')
    
    # Fill area between training and test curves to show generalization gap
    plt.fill_between(degrees, train_errors, test_errors, alpha=0.2, color='gray', 
                     label='Generalization Gap')
    
    # Set main title
    plt.title('Model Complexity vs Error: Finding the Sweet Spot', fontsize=16, fontweight='bold')
    # Set x-axis label
    plt.xlabel('Polynomial Degree (Model Complexity)')
    # Set y-axis label
    plt.ylabel('Mean Squared Error')
    # Add legend
    plt.legend()
    # Add grid
    plt.grid(True, alpha=0.3)
    # Set x-axis ticks to show all degrees
    plt.xticks(degrees)
    
    # Add annotation for underfitting region
    plt.annotate('Underfitting\n(High Bias)', xy=(2, train_errors[1]), xytext=(4, train_errors[1] + 0.5),
                arrowprops=dict(arrowstyle='->', color='black'), fontsize=10)
    # Add annotation for overfitting region
    plt.annotate('Overfitting\n(High Variance)', xy=(12, test_errors[11]), xytext=(10, test_errors[11] + 0.5),
                arrowprops=dict(arrowstyle='->', color='black'), fontsize=10)
    # Add annotation for sweet spot
    plt.annotate('Sweet Spot\n(Optimal Complexity)', xy=(optimal_degree, test_errors[optimal_degree-1]), 
                xytext=(optimal_degree+2, test_errors[optimal_degree-1] - 0.3),
                arrowprops=dict(arrowstyle='->', color='green'), fontsize=10, color='green')
    
    # Adjust layout
    plt.tight_layout()
    # Save figure
    plt.savefig('model_complexity_analysis.png', dpi=300, bbox_inches='tight')
    # Display plot
    plt.show()

# Main execution block - only runs if script is executed directly
if __name__ == "__main__":
    # Print status message
    print("Creating overfitting and underfitting visualizations...")
    
    # Create all three visualizations
    plot_overfitting_underfitting_demo()  # Main demonstration plots
    plot_learning_curves()  # Learning curve analysis
    plot_model_complexity_analysis()  # Complexity vs error analysis
    
    # Print completion message with file names
    print("Visualizations completed! Check the generated PNG files:")
    print("- overfitting_underfitting_demo.png")
    print("- learning_curves.png") 
    print("- model_complexity_analysis.png") 


