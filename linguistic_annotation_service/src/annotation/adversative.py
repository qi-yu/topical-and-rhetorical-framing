import os, re
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list
from tqdm import tqdm


print("Annotating adversative connectors...")

inputRoot = os.path.join(os.getcwd(), "annotated")
for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                lexemeList = get_sentence_as_lexeme_list(s)

                # ----- variables used for disambiguing "sondern" -----
                findNichtNur = False

                index = 0
                for lexeme in lexemeList:
                    currentLemma = lexeme.get("lemma")
                    currentPos = lexeme.get("pos")

                    # ----- 1. allerdings -----
                    ### TODO: difficulties with disambiguating "allerdings" as adversative connector from "allerdings" as adverb for affirmation
                    if currentLemma == "allerdings":
                        lexeme.set("adversative", "allerdings")


                    # ----- 2. sondern -----
                    # Exclude "sondern" in "nicht nur..., sondern (auch)...":
                    if currentLemma == "nicht" and index < len(lexemeList)-1 and lexemeList[index+1].get("lemma") == "nur":
                        findNichtNur = True

                    if currentLemma == "sondern":
                        if findNichtNur != True:
                            lexeme.set("adversative", "sondern")

                        if index < len(lexemeList)-1 and lexemeList[index+1].get("lemma") == "auch":
                            lexeme.attrib.pop("adversative", None)


                    # ----- 3. jedoch -----
                    if currentLemma == "jedoch":
                        lexeme.set("adversative", "jedoch")

                    # ----- 4. einerseits -----
                    if currentLemma == "einerseits":
                       lexeme.set("adversative", "einerseits")


                    # ----- 5. andererseits -----
                    if currentLemma == "andererseits":
                        lexeme.set("adversative_2", "andererseits")


                    # ----- 6. zum einen -----
                    if re.fullmatch("[Zz]u", lexeme.text) and index < len(lexemeList)-2 and re.fullmatch("dem", lexemeList[index+1].text) and re.fullmatch("einen", lexemeList[index+2].text):
                       lexeme.set("adversative", "zum_einen")
                       lexemeList[index+1].set("adversative_2", "dem")
                       lexemeList[index+2].set("adversative_3", "einen")


                    # ----- 7. zum anderen -----
                    if re.fullmatch("[Zz]u", lexeme.text) and index < len(lexemeList)-2 and re.fullmatch("dem", lexemeList[index+1].text) and re.fullmatch("anderen", lexemeList[index+2].text):
                        lexeme.set("adversative_4", "zu")
                        lexemeList[index + 1].set("adversative_5", "dem")
                        lexemeList[index + 2].set("adversative_6", "anderen")

                    # ----- 8. statt -----
                    if currentLemma == "statt" and currentPos != "PTKVZ":
                        lexeme.set("adversative", "statt")

                    # ----- 9. anstatt -----
                    if currentLemma == "anstatt":
                        lexeme.set("adversative", "anstatt")

                    # ----- 11. vielmehr -----
                    if currentLemma == "vielmehr":
                        lexeme.set("adversative", "vielmehr")

                    # ----- 12. andernfalls / anderenfalls -----
                    if currentLemma == "andernfalls" or currentLemma == "anderenfalls":
                        lexeme.set("adversative", "andernfalls")

                    index += 1

            tree.write(os.path.join(r, filename), encoding="utf-8")