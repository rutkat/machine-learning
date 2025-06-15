# A model that categorizes an article into one of the selected topics
#
import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

categories = [
    "comp.graphics",
    "talk.religion.misc",
    "comp.sys.mac.hardware",
    "sci.med",
]
newsgroups_training = fetch_20newsgroups(
    subset="train", categories=categories, random_state=0
)
print("Newsgroups_training:\n", newsgroups_training.data[0])

newsgroups_testing = fetch_20newsgroups(
    subset="test", categories=categories, random_state=0
)

model = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB(),
)

model.fit(newsgroups_training.data, newsgroups_training.target)

predicted_targets = model.predict(newsgroups_testing.data)

accuracy = accuracy_score(newsgroups_testing.target, predicted_targets)
print(accuracy)

confusion = confusion_matrix(newsgroups_testing.target, predicted_targets)
confusion_df = pd.DataFrame(
    confusion,
    index=pd.Index(newsgroups_testing.target_names, name="True"),
    columns=pd.Index(newsgroups_testing.target_names, name="Predicted"),
)

print(confusion_df)


