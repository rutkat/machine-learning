
import joblib
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load some categories of newsgroups dataset
categories = [
    "soc.religion.christian",
    "talk.religion.misc",
    "comp.sys.mac.hardware",
    "sci.crypt",
]
newsgroups_training = fetch_20newsgroups(
    subset="train", categories=categories, random_state=0
)
print("Newsgroups_training:\n")

newsgroups_testing = fetch_20newsgroups(
    subset="test", categories=categories, random_state=0
)

model = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB(),
)

# Train model
model.fit(newsgroups_training.data, newsgroups_training.target)

# Serialize the model and the target names
model_file = "newsgroups_model.joblib"
model_targets_tuple = (model, newsgroups_training.target_names)

print("Model_targets_tuple: ", model_targets_tuple)

joblib.dump(model_targets_tuple, model_file)


