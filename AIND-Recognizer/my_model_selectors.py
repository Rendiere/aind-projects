import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3, min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        results = {}
        for n in range(self.min_n_components, self.max_n_components + 1):
            # Train the model
            try:
                model = GaussianHMM(n_components=n, n_iter=1000).fit(self.X, self.lengths)
            except:
                continue
            try:
                logL = model.score(self.X, self.lengths)

                bic = -2 * logL + n * np.log(len(self.X))
                results[n] = bic
            except:
                pass

        if results:
            # Get the number of hidden states that gave the best log loss
            best_n_components = min(results.items(), key=lambda x: x[1])[0]
            # Now train a model on the entire training set
            return GaussianHMM(n_components=best_n_components, n_iter=1000).fit(self.X, self.lengths)

        else:
            return None


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf


    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def train_model(self, n):
        try:
            return GaussianHMM(n_components=n, n_iter=1000).fit(self.X, self.lengths)
        except:
            return None

    def get_log_likelihood(self, model, word):
        X, lengths = self.hwords[word]
        try:
            logL = model.score(X, lengths)
            return logL

        except:
            return None

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        dic_results = {}

        for n in range(self.min_n_components, self.max_n_components + 1):

            hmm_model = self.train_model(n)

            if hmm_model:
                # log(P(X(i))
                log_likelihood = self.get_log_likelihood(hmm_model, self.this_word)

                # log(P(X(all but i)
                anti_log_likelihoods = [self.get_log_likelihood(hmm_model, word) for word in self.words
                                        if word != self.this_word]

                # Filter out Nones
                anti_log_likelihoods = [l for l in anti_log_likelihoods if l is not None]

                if log_likelihood and anti_log_likelihoods:
                    dic_results[n] = log_likelihood - (1 / (len(self.words) - 1)) * sum(anti_log_likelihoods)

        if dic_results:
            best_n = max(dic_results.items(), key=lambda x: x[1])[0]
            return GaussianHMM(n_components=best_n, n_iter=1000).fit(self.X, self.lengths)
        else:
            return None


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        if len(self.sequences) < 2:
            return None

        kf = KFold(n_splits=2)

        cv_results = {}
        for n in range(self.min_n_components, self.max_n_components + 1):

            log_likelihoods = []

            # For each fold
            for cv_train_idx, cv_val_idx in kf.split(self.sequences):

                # Get the training and validation sets
                X_tr, lengths_tr = combine_sequences(cv_train_idx, self.sequences)
                X_val, lengths_val = combine_sequences(cv_val_idx, self.sequences)

                # Train the model
                try:
                    model = GaussianHMM(n_components=n, n_iter=1000).fit(X_tr, lengths_tr)
                except:
                    pass

                # Evaluate model on the validation set
                try:
                    logL = model.score(X_val, lengths_val)
                    log_likelihoods.append(logL)
                except:
                    continue

            # Save the average log loss over all folds
            cv_results[n] = np.average(log_likelihoods)

        # Get the number of hidden states that gave the best log loss
        best_n_components = max(cv_results.items(), key=lambda x: x[1])[0]

        # Now train a model on the entire training set
        model = GaussianHMM(n_components=best_n_components, n_iter=1000).fit(self.X, self.lengths)

        return model
