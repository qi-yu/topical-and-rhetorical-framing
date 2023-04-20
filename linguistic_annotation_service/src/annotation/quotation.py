import os, re
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list
from tqdm import tqdm


print("Annotating quotation...")

inputRoot = os.path.join(os.getcwd(), "annotated")
for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            all_lexeme_list = []
            first_quotation_idx = None
            second_quotation_idx = None

            for s in root.iter("sentence"):
                current_lexeme_list = get_sentence_as_lexeme_list(s)
                all_lexeme_list += current_lexeme_list
                has_konjunktiv_1 = False

                # ----- 1. Check Konjunktiv I ------
                for idx, lexeme in enumerate(current_lexeme_list):
                    if re.search("Mood=Sub", lexeme.get("feats")):
                        currentLemma = lexeme.get("lemma")
                        currentText = lexeme.text

                        ### ----- Third person singular -----
                        if re.search("Number=Sing\|Person=3", lexeme.get("feats")):
                            if currentLemma[-2:] == "en" and currentText == currentLemma[:-2] + "e":
                                has_konjunktiv_1 = True

                            if currentLemma[-2:] != "en" and currentText == currentLemma[:-1] + "e":
                                has_konjunktiv_1 = True

                        ### ----- Verb "sein" -----
                        if re.fullmatch("(seie?st|seien|seiet|sei)", currentText):
                            has_konjunktiv_1 = True

                if has_konjunktiv_1 == True:
                    for lexeme in current_lexeme_list:
                        lexeme.set("within_indirect_speech", "y")

            for idx, lexeme in enumerate(all_lexeme_list):
                if lexeme.text == '"':
                    if first_quotation_idx is None:
                        first_quotation_idx = idx
                    else:
                        second_quotation_idx = idx

                        for i in all_lexeme_list[first_quotation_idx+1:second_quotation_idx]:
                            i.set("within_direct_speech", "y")

                        first_quotation_idx = None
                        second_quotation_idx = None

            tree.write(os.path.join(r, filename), encoding="utf-8")