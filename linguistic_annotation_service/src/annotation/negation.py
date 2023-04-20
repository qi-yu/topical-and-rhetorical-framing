import os, re
from src.utilities.annotation_utils import parse_xml_tree
from tqdm import tqdm


print("Annotating negation...")

inputRoot = os.path.join(os.getcwd(), "annotated")
for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                wederIndex = None

                index = 0
                for lexeme in s.findall("lexeme"):
                    currentLemma = lexeme.get("lemma")

                    # ----- Group 1: Relative negation -----
                    if re.fullmatch("kaum", currentLemma) is not None:
                        lexeme.set("negation", "relative")

                    # ----- Group 2: Absolute negation -----
                    if re.fullmatch("nein", currentLemma) is not None:
                        lexeme.set("negation", "absolute")

                    if re.fullmatch("kein\w*", currentLemma) is not None:
                        lexeme.set("negation", "absolute")

                    if re.fullmatch("nicht\w*", currentLemma) is not None:
                        lexeme.set("negation", "absolute")

                    if re.fullmatch("nirgend\w*", currentLemma) is not None:
                        lexeme.set("negation", "absolute")

                    if re.fullmatch("nie(mand|mals)?", currentLemma) is not None:
                        lexeme.set("negation", "absolute")

                    if re.fullmatch("ohne", currentLemma) is not None:
                        lexeme.set("negation", "absolute")

                    if re.fullmatch("weder", currentLemma) is not None:
                        lexeme.set("negation", "absolute")
                        wederIndex = index

                    # Only when preceded with a "weder": annotate "noch" as negation
                    if re.fullmatch("noch", currentLemma) is not None and wederIndex is not None and wederIndex < index:
                        lexeme.set("negation_2", "absolute")

                    index += 1

            tree.write(os.path.join(r, filename), encoding="utf-8")