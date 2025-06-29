import numpy as np
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

df = pandas.read_csv("faqs.csv")
df.dropna(inplace=True)

print(df)
vectorizer = TfidfVectorizer()
vectorizer.fit(np.concatenate((df.Question,df.Answer)))

vectorized_questions = vectorizer.transform(df.Question)
print(vectorized_questions)

while True:
    user_input = input()
    vectorized_user_input = vectorizer.transform([user_input])
    similarities = cosine_similarity(vectorized_user_input,
                                       vectorized_questions)
    closest_question = np.argmax(similarities,
                                 axis=1)
    print(similarities)
    print(closest_question)

    answer = df.Answer.iloc[closest_question].values[0]
    print("Answer: ", answer)
    break    