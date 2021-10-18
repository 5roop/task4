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
review = """'Rumunski predsednik Trajan Bašesku sastao se u ponedeljak (31. januara) u Londonu sa britanskim premijerom Tonijem Blerom. [AFP] Rumunski predsednik Trajan Bašesku sastao se u ponedeljak (31. januara) sa britanskim premijerom Tonijem Blerom, tokom prve posete jednoj zapadnoj zemlji od kada je u decembru preuzeo funkciju. Cilj odluke o odlasku u London bio je da se uputi promišljen «politički signal», izjavio je Bašesku, a prenosi AP. Tokom svoje kampanje on je obećao da će dati visok prioritet odnosima sa Sjedinjenim Državama i Britanijom. Posle sastanka Bašesku i Bler potvrdili su svoju posvećenost razvijanju strateškog partnerstva -- koje postoji od 2003. godine -- između dve zemlje. «Dvojica lidera odlučili su da rade na uspešnoj integraciji Rumunije u EU 1. januara 2007. godine, na osnovu implementacije obaveza Rumunije preuzetih u pregovorima. Premijer Bler izrazio je snažnu kontinuiranu podršku Velike Britanije», navodi se u saopštenju izdatom posle sastanka. Bler je bio jedan od najvažnijih pristalica integracije Rumunije u EU. On je odigrao vitalnu ulogu 1999. godine, kada je Evropski savet u Helsinkiju doneo odluku da počne pregovore o pridruživanju sa Bukureštom. Dvojica lidera «naglasili su značaj unapređivanja poslovne klime u Rumuniji, posebno putem dalekosežne i nepristrasne kampanje za borbu protiv korupcije na svim nivoima». Britanija je ponudila da pomogne u borbi protiv korupcije upućivanjem savetnika britanske vlade u Rumuniju koji bi radili zajedno sa tamošnjim vlastima. Kada je u pitanju spoljna politika, oni su razmotrili strateški značaj Rumunije na istočnoj granici NATO-a i složili se da «blisko sarađuju na uključivanju pitanja šireg regiona Crnog mora u evroatlantski program». Bašesku je više puta rekao da je razvoj strategije za integraciju regiona jedan od njegovih političkih prioriteta, uprkos kritikama političkih protivnika koji kažu da to predstavlja skretanje pažnje sa glavnog spoljnopolitičkog cilja Rumunije, pridruživanja EU. Bašesku i Bler saglasili su se oko potrebe proširenja demokratije, stabilnosti, bezbednosti i prosperiteta nevezano za budućnost EU i ukazali da će udružiti napore sa sadašnjim i potencijalnim članicama EU da pomognu implementaciju akcionih planova EU za Moldaviju i Ukrajinu. Oni su obećali pomoć u unapređivanju stabilnosti, bezbednosti i dalje evropske integracije na zapadnom Balkanu. Rumunski predsednik je takođe ponovo potvrdio da će njegova zemlja zadržati svojih 730 vojnika u Iraku «dok nove iračke institucije ne budu u mogućnosti da efikasno vladaju zemljom i osiguraju miroljubivu klimu kako bi počeo zdrav proces obnove». Euro 2010: Hrvatska i Grčka se takmiče za poziciju Veze između igrača i navijačkih naklonosti imaju dugu istoriju. H.K.  """

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
