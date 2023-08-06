dictionary-model
----------------

To use, first create CharPredictor object::

    >>> predictor = CharPredictor()

This may take a while as model is being downloaded and loaded.

Then, to track utterance context, you can add letter index to context::

    >>> letter_index = 1    # 1 -> a,   letters should be indexed in order: ' abcdefghijklmnopqrstuvwxyz' (0 -> space)
    >>> predictor.add_to_context(letter_index)

or you can add letter as string of length 1 (make sure it is one of AsciiEncoder.AVAILABLE_CHARS)::

    >>> letter = 'a'
    >>> predictor.add_to_context(letter)

or you can add probability distribution for all AsciiEncoder.AVAILABLE_CHARS letters::

    >>> import numpy as np
    >>> import AsciiEncoder as AE
    >>>
    >>> num_chars = len(AE.AVAILABLE_CHARS)
    >>> letter_distr = np.random.random((1, num_chars)) # random proba distribution
    >>> predictor.add_to_context(letter_distr)

And finally - you can predict probabilities of each letter coming next after text stored in context. (Letters are indexed in order shown below)::

    >>> predictor.transform()

Letters order::

     ' abcdefghijklmnopqrstuvwxyz' # space character comes at index 0, then alphabetical order for indices from 1 to 26

