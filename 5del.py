# -*- coding: utf-8 -*-

import re
import os
import fasttext
import webbrowser
import numpy as np
import lime.lime_text
from pathlib import Path

# This function regularizes a piece of text so it's in the same format
# that we used when training the FastText classifier.
def strip_formatting(string):
    string = string.lower()
    string = re.sub(r"([.!?,'/()])", r" \1 ", string)
    return string

# LIME needs to be able to mimic how the classifier splits
# the string into words. So we'll provide a function that
# mimics how FastText works.
def tokenize_string(string):
    return string.split()

# Load our trained FastText classifier model (created in Part 2)
classifier = fasttext.load_model("/home/peterr/macocu/taskB/data/models/ftmodel_3.bin")

# Create a LimeTextExplainer. This object knows how to explain a text-based
# prediction by dropping words randomly.
explainer = lime.lime_text.LimeTextExplainer(
    # We need to tell LIME how to split the string into words. We can do this
    # by giving it a function to call to split a string up the same way FastText does it.
    split_expression=tokenize_string,
    # Our FastText classifer uses bigrams (two-word pairs) to classify text. Setting
    # bow=False tells LIME to not assume that our classifier is based on single words only.
    bow=False,
    # To make the output pretty, tell LIME what to call each possible prediction from our model.
    class_names=["__label__hr", "__label__bs", "__label__sr"]
)

# LIME is designed to work with classifiers that generate predictions
# in the same format as Scikit-Learn. It expects every prediction to have
# a probability value for every possible label.
# The default FastText python wrapper generates predictions in a different
# format where it only returns the top N highest likelihood results. This
# code just calls the FastText predict function and then massages it into
# the format that LIME expects (so that LIME will work).
def fasttext_prediction_in_sklearn_format(classifier, texts):
    res = []
    # Ask FastText for the top 10 most likely labels for each piece of text.
    # This ensures we always get a probability score for every possible label in our model.
    labels, probabilities = classifier.predict(texts, 10)

    # For each prediction, sort the probabaility scores into the same order
    # (I.e. no_stars, 1_star, 2_star, etc). This is needed because FastText
    # returns predicitons sorted by most likely instead of in a fixed order.
    for label, probs, text in zip(labels, probabilities, texts):
        order = np.argsort(np.array(label))
        res.append(probs[order])

    return np.array(res)

# Review to explain
review = """Na pitanje koja mu je njegova fotografija od velikog značaja,autor fotografije, Paul Hansen,odgovorio je:“Bilo je to u Sarajevu.Čovjek po imenu Izet Grebović bacao je buket cvijeća na grob svoje preminule supruge jer nije mogao prići od snajperske vatre.Bila je to raketa ljubavi”"""

# Pre-process the text of the review so it matches the training format
preprocessed_review = strip_formatting(review)

# Make a prediction and explain it!
exp = explainer.explain_instance(
    # The review to explain
    preprocessed_review,
    # The wrapper function that returns FastText predictions in scikit-learn format
    classifier_fn=lambda x: fasttext_prediction_in_sklearn_format(classifier, x),
    # How many labels to explain. We just want to explain the single most likely label.
    top_labels=1,
    # How many words in our sentence to include in the explanation. You can try different values.
    num_features=300,
)

# Save the explanation to an HTML file so it's easy to view.
# You can also get it to other formats: as_list(), as_map(), etc.
# See https://lime-ml.readthedocs.io/en/latest/lime.html#lime.explanation.Explanation
output_filename = Path(__file__).parent / "explanation.html"
# output_filename = os.path.join("/home/peterr/macocu/taskB/task4", "explanation.html")
exp.save_to_file(output_filename)

# Open the explanation html in our web browser.
webbrowser.open(output_filename.as_uri())
