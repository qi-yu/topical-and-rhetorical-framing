import os, re
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list
from tqdm import tqdm


print("Annotating concessive connectors...")

inputRoot = os.path.join(os.getcwd(), "annotated")
for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                lexemeList = get_sentence_as_lexeme_list(s)

                index = 0
                for lexeme in lexemeList:
                    currentLemma = lexeme.get("lemma")
                    currentPos = lexeme.get("pos")

                    # ----- 1. dennoch -----
                    if currentLemma == "dennoch":
                        lexeme.set("concessive", "dennoch")

                    # ----- 2. obwohl -----
                    if currentLemma == "obwohl":
                        lexeme.set("concessive", "obwohl")

                    # ----- 3. wobei -----
                    if currentLemma == "wobei" and index < len(lexemeList)-1 and re.fullmatch("[,.-]", lexemeList[index+1].text):
                        lexeme.set("concessive", "wobei")

                    # ----- 4. trotzdem -----
                    if currentLemma == "trotzdem":
                        lexeme.set("concessive", "trotzdem")

                    # ----- 5. trotz -----
                    if currentLemma == "trotz":
                        lexeme.set("concessive", "trotz")

                    # ----- 6. ungeachtet / ungeachtet dessen / dessen ungeachtet -----
                    if currentLemma == "ungeachtet":
                        lexeme.set("concessive", "ungeachtet")

                    # ----- 7. zwar -----
                    # Exclude "zwar" in "und zwar":
                    if currentLemma == "zwar" and index > 0 and lexemeList[index-1].get("lemma") != "und":
                        lexeme.set("concessive", "zwar")

                    # ----- 8. gleichwohl -----
                    if currentLemma == "gleichwohl":
                        lexeme.set("concessive", "gleichwohl")

                    # ----- 9. wenngleich -----
                    if currentLemma == "wenngleich":
                        lexeme.set("concessive", "wenngleich")

                    # ----- 10. obschon -----
                    if currentLemma == "obschon":
                        lexeme.set("concessive", "obschon")

                    # ----- 11. nichtsdestotrotz -----
                    if currentLemma == "nichtsdestotrotz":
                        lexeme.set("concessive", "nichtsdestotrotz")

                    # ----- 12. nichtsdestoweniger -----
                    if currentLemma == "nichtsdestoweniger":
                        lexeme.set("concessive", "nichtsdestoweniger")

                    # ----- 13. unbeschadet dessen -----
                    if currentLemma == "unbeschadet" and index < len(lexemeList)-1 and lexemeList[index+1].text == "dessen":
                        lexeme.set("concessive", "unbeschadet_dessen")
                        lexemeList[index+1].set("concessive_2", "dessen")

                    index += 1

            tree.write(os.path.join(r, filename), encoding="utf-8")