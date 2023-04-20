'''
Source of the lexicon:
Yu & Fliethmann. 2021. Frame Detection in German Political Discourses: How Far Can We Go Without Large-Scale Manual Corpus Annotation?
https://github.com/qi-yu/refugees-and-migration-framing-vocabulary
'''

import os, re
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list, get_wordlist_from_txt
from tqdm import tqdm

print("Annotating Refugees and Migration Framing Vocabulary...")

# ----- Get wordlist -----
wordlistsRoot = os.path.join(os.getcwd(), "wordlists/rmfv")
wordlistDict = {}

for filename in os.listdir(wordlistsRoot):
    if filename.endswith(".txt"):
        currentAnnotationLabel = filename.split(".")[0]
        currentWordList = get_wordlist_from_txt(os.path.join(wordlistsRoot, filename))

        for w in currentWordList:
            if w not in wordlistDict:
                wordlistDict[w] = [currentAnnotationLabel]
            else:
                wordlistDict[w].append(currentAnnotationLabel)

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

                # ----- Start annotation -----
                for idx, lexeme in enumerate(lexemeList):
                    currentLemma = lexeme.get("lemma")

                    if currentLemma in wordlistDict:
                        for label in wordlistDict[currentLemma]:
                            lexeme.set(label, currentLemma)

                    # ----- 1. Deal with particle verbs -----
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
                            if currentPV in wordlistDict:
                                for label in wordlistDict[currentPV]:
                                    stemLexeme.set(label, currentPV)
                                    particleLexeme.set(label + "_PTKVZ", currentPV)

                    # ----- 2. Deal with multi-word expressions and ambiguous words -----
                    # ----- 2.1 legal.txt: "Burka-Verbot" -----
                    if lexeme.text == "Burka" and idx < len(lexemeList) - 2 and lexemeList[idx+1].text == "-" and lexemeList[idx+2].text == "Verbot":
                        lexeme.set("legal", "Burka-Verbot")
                        lexeme.set("policy", "Burka-Verbot")
                        lexemeList[idx + 1].set("legal_2", "-")
                        lexemeList[idx + 1].set("policy_2", "-")
                        lexemeList[idx + 2].set("legal_3", "Verbot")
                        lexemeList[idx + 2].set("policy_3", "Verbot")

                    # ----- 2.2 policy.txt: "Genfer Flüchtlingskonvention" -----
                    if lexeme.text == "Genfer" and idx < len(lexemeList) - 1 \
                            and re.fullmatch("(Flüchtlingskonvention|Flüchtlingskonventionen|Konventionen|Abkommen)", lexemeList[idx+1].text):
                        lexeme.set("policy", "Genfer_Fluechtlingskonvention")
                        lexemeList[idx+1].set("policy_2", "Fluechtlingskonvention")

                    # ----- 2.3 security.txt: "U-Haft", "unbegleitete minderjährige *" -----
                    if lexeme.text == "U-" and idx < len(lexemeList) - 1 and lexemeList[idx+1].text == "Haft":
                        lexeme.set("security", "U-Haft")
                        lexemeList[idx+1].set("security_2", "Haft")

                    if re.fullmatch("unbegleitet[enr]*", currentLemma) and idx < len(lexemeList) - 1 and re.fullmatch("minderjährig[enr]*", lexemeList[idx+1].get("lemma")):
                        lexeme.set("security", "unbegleitete_minderjaehrige")
                        lexemeList[idx+1].set("security_2", "minderjaehrige")

                    # ----- 2.4 welfare.txt: "finanzielle Unterstützung", "Soziale Sicherung"
                    if currentLemma == "finanziell" and idx < len(lexemeList) - 1 and lexemeList[idx + 1].get("lemma") == "Unterstützung":
                        lexeme.set("welfare", "finanzielle_Unterstuetzung")
                        lexemeList[idx+1].set("welfare_2", "Unterstuetzung")

                    if lexeme.get("lemma") == "sozial" and idx < len(lexemeList) - 1 and lexemeList[idx + 1].get("lemma") == "Sicherung":
                        lexeme.set("welfare", "soziale_Sicherung")
                        lexemeList[idx+1].set("welfare_2", "Sicherung")

                    # ----- 2.5 identity.txt: "Christin" -----
                    if lexeme.text == "Christin" and lexeme.get("pos") != "NE":
                        lexeme.set("identity", "Christin")

                    # ----- 2.6 public_opinion.txt: "Öffentlich* Eindruck/Gefühl/Interesse" -----
                    if currentLemma == "öffentlich" and idx < len(lexemeList) - 1 and lexemeList[idx+1].get("lemma") == "Eindruck":
                        lexeme.set("public_opinion", "oeffentlicher_Eindruck")
                        lexemeList[idx+1].set("public_opinion_2", "Eindruck")

                    if currentLemma == "öffentlich" and idx < len(lexemeList) - 1 and lexemeList[idx+1].get("lemma") == "Gefühl":
                        lexeme.set("public_opinion", "oeffentliches_Gefuehl")
                        lexemeList[idx+1].set("public_opinion_2", "Gefuehl")

                    if currentLemma == "öffentlich" and idx < len(lexemeList) - 1 and lexemeList[idx+1].get("lemma") == "Interesse":
                        lexeme.set("public_opinion", "oeffentliches_Interesse")
                        lexemeList[idx+1].set("public_opinion_2", "Interesse")

            tree.write(os.path.join(r, filename), encoding="utf-8")