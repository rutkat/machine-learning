from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

digits = load_digits()

data = digits.data
targets = digits.target

# Split training data
training_data, testing_data, training_targets, testing_targets = \
 train_test_split( data, targets, random_state=0)

print("Training Data:")
print(training_data)
print("Test Data:\n", testing_data)

# Train model
model = GaussianNB()
model.fit(training_data, training_targets)
predicted_targets = model.predict(testing_data)

accuracy = accuracy_score(testing_targets, predicted_targets)
print("Accuracy:\n", accuracy)


