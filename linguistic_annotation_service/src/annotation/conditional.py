import os
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list
from tqdm import tqdm


print("Annotating conditional connectors...")

# ----- List of conditional connectors that don't need disambiguation -----
conditionalConnectorsList = ["wenn", "falls", "sofern"]

# ----- Start processing -----
inputRoot = os.path.join(os.getcwd(), "annotated")
for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                lexemeList = get_sentence_as_lexeme_list(s)

                # ----- Start annotation -----
                index = 0
                for lexeme in lexemeList:
                    currentLemma = lexeme.get("lemma")
                    currentPos = lexeme.get("pos")
                    currentWord = lexeme.text
                    depRelation = lexeme.get("dependency_relation")

                    # ----- 1. Items that do not need disambiguation -----
                    if currentLemma in conditionalConnectorsList:
                        lexeme.set("conditional", currentLemma)


                    # ----- 2. Items that need disambiguation -----
                    # ----- 2.1 "gesetzt" -----
                    if currentWord == "Gesetzt" or currentWord == "gesetzt" and index == 0:
                        # "gesetzt den Fall"
                        if len(lexemeList) > 2 and lexemeList[index+1].get("lemma") == "der" and lexemeList[index+2].get("lemma") == "Fall":
                            lexemeList[index].set("conditional", "gesetzt_den_Fall")
                            lexemeList[index+1].set("conditional_2", "den")
                            lexemeList[index+2].set("conditional_3", "Fall")
                        # "gesetzt"
                        if depRelation == "conj":
                            lexeme.set("conditional", "gesetzt")

                    index += 1

            tree.write(os.path.join(r, filename), encoding="utf-8")