import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []


    for i, (X, lengths) in test_set.get_all_Xlengths().items():

        probs = {}
        for model_name, hmm_model in models.items():
            try:
                logL = hmm_model.score(X, lengths)
            except:
                logL = float('-inf')

            probs[model_name] = logL

        best_guess = max(probs.items(), key=lambda x: x[1])[0]
        guesses.append(best_guess)
        probabilities.append(probs)

    return probabilities, guesses
