dictionary-model
----------------

To use, first create CharPredictor object::

    >>> predictor = CharPredictor()

This may take a while as model is being downloaded and loaded.

Then, to track utterance context, use::

    >>> letter_index = 1    # 1 -> a,   letters should be indexed in order: ' abcdefghijklmnopqrstuvwxyz' (0 -> space)
    >>> predictor.add_to_context(letter_index)

or::

    >>> letter = 'a'
    >>> predictor.add_to_context(letter)

And finally - you can predict probabilities of each letter coming next after text stored in context. (Letters are indexed in order shown below)::

    >>> predictor.transform()

Letters order::

     ' abcdefghijklmnopqrstuvwxyz' # space character comes at index 0, then alphabetical order for indices from 1 to 26

