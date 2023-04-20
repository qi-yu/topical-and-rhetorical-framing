import os, re
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list, get_sentence_as_text
from tqdm import tqdm


print("Annotating modal particles...")

inputRoot = os.path.join(os.getcwd(), "annotated")
for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                lexemeList = get_sentence_as_lexeme_list(s)
                lexemeList_toString = get_sentence_as_text(s)

                # ----- variables used for disambiguing "wohl" -----
                wohlGov = None
                wohlIndex = None
                fuehlenIndex = None
                reflexGov = None

                # ----- Start disambiguation -----
                for idx, lexeme in enumerate(lexemeList):
                    currentLemma = lexeme.get("lemma")
                    currentPos = lexeme.get("pos")

                    # ----- 1. ja -----
                    if currentLemma == "ja":
                        lexeme.set("common_ground", "ja")

                        # Exclude cases like "Oh ja", "Ach ja", "Und ja" etc.:
                        if idx == 1 and re.fullmatch("(ADV|KON)", lexemeList[0].get("pos")):
                            lexeme.attrib.pop("common_ground", None)

                        # Exclude "Na ja"
                        if idx > 0 and lexemeList[idx-1].get("lemma") == "na":
                            lexeme.attrib.pop("common_ground", None)

                        # Exclude "wenn ja (,|:) ....."
                        if idx > 0 and idx < len(lexemeList)-1 and lexemeList[idx - 1].get("lemma") == "wenn" and re.fullmatch("[,:]", lexemeList[idx+1].text):
                            lexeme.attrib.pop("common_ground", None)

                        # Exclude "ja" surrounded by punctuations
                        if idx > 0 and idx < len(lexemeList)-1 and (re.fullmatch("\$[,.(]",lexemeList[idx-1].get("pos")) or re.fullmatch("\$[,.(]", lexemeList[idx+1].get("pos"))):
                            lexeme.attrib.pop("common_ground", None)

                        # Exclude "ja" in "..., ja genau, ..."
                        if idx < len(lexemeList) - 2 and lexemeList[idx+1].get("lemma") == "genau" and re.fullmatch("[,.!-]", lexemeList[idx+2].text):
                            lexeme.attrib.pop("common_ground", None)

                    # ----- 2. doch -----
                    ### TODO: annotation of "doch" is urrently excluded - difficult to disambiguate with rule-based approach

                    # ----- 3. eben -----
                    if currentLemma == "eben":
                        lexeme.set("resigned_acceptance", "eben")

                        # Exclude "eben" in "gerade eben":
                        if idx > 0 and lexemeList[idx-1].get("lemma") == "gerade":
                            lexeme.attrib.pop("resigned_acceptance", None)

                        # Exclude "eben" in "Ja eben, ..."
                        if idx > 0 and lexemeList[idx-1].text == "Ja":
                            lexeme.attrib.pop("resigned_acceptance", None)

                    # ----- 4. halt -----
                    if currentLemma == "halt" and re.match("(ADV|ADJD)", currentPos):
                        lexeme.set("resigned_acceptance", "halt")

                    # ----- 5. wohl -----
                    if currentLemma == "wohl" and currentPos == "ADV":
                        wohlGov = lexeme.get("governor")
                        wohlIndex = idx
                        lexeme.set("hedging", "wohl")

                        # Exclude "wohl" in "sehr wohl":
                        if idx > 0 and lexemeList[idx-1].get("lemma") == "sehr":
                            lexeme.attrib.pop("hedging", None)

                    # Exclude "wohl" in "sich wohl fühlen":
                    if currentLemma == "fühlen":
                        fuehlenIndex = lexeme.get("index")

                    if re.search("Reflex=Yes", lexeme.get("feats")):
                        reflexGov = lexeme.get("governor")

                    if wohlGov is not None and fuehlenIndex is not None and reflexGov is not None:
                        if wohlGov == fuehlenIndex and reflexGov == fuehlenIndex:
                            lexemeList[wohlIndex].attrib.pop("hedging", None)

            tree.write(os.path.join(r, filename), encoding="utf-8")