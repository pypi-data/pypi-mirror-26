
Lightweight library which implements `Markov
algorithm <https://en.wikipedia.org/wiki/Markov_algorithm>`__ (cycle of
replacements) for text strings.

--------------

Usage:
~~~~~~

*creating rules*

::

    from markalgo import rules
    from markalgo import processing

    # from text
    replacement = rules.create_rules([("Norwegian blue", "parrot"), ("alive", "dead"), ("dead", "no more")])

    # or from csv files
    with open("notes/cicero.csv") as argumentation:
        replacement = rules.read_all_rules_from_csv_file(argumentation)

*processing text…*

::

    processing.process_text("This Norwegian blue is alive", replacement)

     *"This parrot is no more"*

*…or plain-text files*

::

    with open("notes/note.txt") as argumentation:
        processing.process_file()



