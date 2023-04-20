'''
Source of the lexicon:
Köper & Schulte im Walde. 2016. Automatically Generated Affective Norms of Abstractness, Arousal, Imageability and Valence for 350 000 German Lemmas
https://www.ims.uni-stuttgart.de/forschung/ressourcen/experiment-daten/affective-norms/
'''


import os, re
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list, get_wordlist_from_txt
from nltk.corpus import stopwords
from tqdm import tqdm


print("Annotating affectiveness scores...")

# ----- Get word list -----
affectiveWords_raw = get_wordlist_from_txt(os.path.join(os.getcwd(), "wordlists/affectiveness.txt"))
stopwords = stopwords.words("german")

affectiveWordsDict = {}
for i in affectiveWords_raw:
    currentWord = re.split("\s", i)[0]
    if currentWord.startswith("#") is False and currentWord not in stopwords:
        currentValueList = [re.split("\s", i)[1], re.split("\s", i)[2], re.split("\s", i)[3], re.split("\s", i)[4]]
        affectiveWordsDict[currentWord] = currentValueList

# ----- Start processing -----
inputRoot = os.path.join(os.getcwd(), "annotated")

for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                lexemeList = get_sentence_as_lexeme_list(s)

                # ----- Variables used for particle verbs with stems and particles separated -----
                stemIndex = None
                stemListIndex = None
                particleGov = None
                particleListIndex = None

                for idx, lexeme in enumerate(lexemeList):
                    currentLemma = lexeme.get("lemma")

                    if re.fullmatch("(NE|PTKVZ)", lexeme.get("pos")) is None and currentLemma in affectiveWordsDict:
                        lexeme.set("concreteness", affectiveWordsDict[currentLemma][0])
                        lexeme.set("arousal", affectiveWordsDict[currentLemma][1])
                        lexeme.set("imageability", affectiveWordsDict[currentLemma][2])
                        lexeme.set("valence", affectiveWordsDict[currentLemma][3])

                    # ----- Deal with particle verbs -----
                    if lexeme.get("pos") == "VVFIN":
                        stemIndex = lexeme.get("index")
                        stemListIndex = idx

                    if re.fullmatch("(PTKVZ|ADV)", lexeme.get("pos")):
                        particleGov = lexeme.get("governor")
                        particleListIndex = idx

                    if stemIndex and particleGov and particleGov == stemIndex:
                        particleLexeme = lexemeList[particleListIndex]
                        particleLemma = particleLexeme.get("lemma")
                        stemLexeme = lexemeList[stemListIndex]
                        stemLemma = stemLexeme.get("lemma")

                        stemOptionList = stemLemma.split("|")
                        for stem in stemOptionList:
                            currentPV = particleLemma + stem
                            if currentPV in affectiveWordsDict:
                                stemLexeme.set("concreteness", affectiveWordsDict[currentPV][0])
                                stemLexeme.set("arousal", affectiveWordsDict[currentPV][1])
                                stemLexeme.set("imageability", affectiveWordsDict[currentPV][2])
                                stemLexeme.set("valence", affectiveWordsDict[currentPV][3])

                                particleLexeme.set("concreteness_PTKVZ", affectiveWordsDict[currentPV][0])
                                particleLexeme.set("arousal_PTKVZ", affectiveWordsDict[currentPV][1])
                                particleLexeme.set("imageability_PTKVZ", affectiveWordsDict[currentPV][2])
                                particleLexeme.set("valence_PTKVZ", affectiveWordsDict[currentPV][3])

            tree.write(os.path.join(r, filename), encoding="utf-8")