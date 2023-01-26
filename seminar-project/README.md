# Neologism Detection: Exclusion Lists
###### Author: Pavels Ivanovs pi19003

---

## Goal
This repo's goal is to showcase the implementation of the first layer of 
automatic neologism detection: **exclusion lists**.

## Description

The method of exclusion lists is based on constructing a list of words and use
this list for filtering out possible neologism candidates from the working corpus by
filtering out words which are not in the exclusion list.

This method is pretty much straightforward due to the simplicity of its 
implementation, though it helps out to reduce the amount of words which would
be a subject for neologism classification - the next layer of neologism detection.

Taking into account that Latvian is strongly flexive language, i.e., its words 
change the form according to the meaning (word is a subject of an action, word is an object of an action, etc.),
it is a necessity to get the lemma of the word we are looking up in exclusion lists.

In order to reach this goal, morphological analyzer of 
Latvian language is used: **LVTagger** (https://github.com/PeterisP/LVTagger).

After getting the lemma of the word the lemma is looked up in the database table of entries of thesaurus of 
Latvian language Tēzaurs.lv (link for download: https://wordnet.ailab.lv/data/).

If an attempt to look up the lemma ends up unsuccessful, then the word is being added to the list of 
possible neologism candidates.

The corpus on which this method has been tested is the thesaurus itself. Definitions of the thesaurus entries
have been analyzed for the search of possible neologisms.

## Technical Part

- Local installation of Java is required (detailed: https://github.com/PeterisP/LVTagger/blob/master/README.txt)
- It is possible to work with Tēzaurs.lv data in two ways:
  - XML file describing all the entries.
    - The file is not a valid XML. Thus it is required to process it by removing the conflicting (see [here](get_candidates_from_xml.py))
  - PostgreSQL database dump. 
    - Docker container is created for working with PostgreSQL. For starting run: `docker-compose up`
- Python is used for the rest part of the project.

## Results

Due to the simplicity of this method, it is not doing very well at filtering out false positives: typos, 
words with a lacking space symbol, punctuation, numbers. These statements have been observed in this project as well.

As it has been observed after running the Python script, a lot of toponyms are filtered out, which are proper
words of Latvian language. Besides that, the definitions have words from other languages and are 
being filtered out as well.

## What is next?

After implementation of exclusion lists next stop is to proceed to implementing a machine learning model
goal of which is to classify words which were left after using exclusion lists.

## Papers used for research
- A. Abel un E. W. Stemle, «On the Detection of Neologism Candidates as Basis for Language Observation and Lexicographic Endeavours: The STyrLogism Project,»  Proceedings of the XVIII EURALEX International Congress: Lexicography in Global Contexts, 2018, pp. 535-544. 
- I. Falk, D. Bernhard un G. Christophe, «From Non Word to New Word: Automatically Identifying Neologisms in French Newspapers,»  LREC - The 9th edition of the Language Resources and Evaluation Conference, Rejkjavika, 2014. 


