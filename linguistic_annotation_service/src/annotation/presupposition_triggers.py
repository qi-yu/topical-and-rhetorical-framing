import os, re
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list, get_wordlist_from_txt
from tqdm import tqdm

print("Annotating presupposition triggers...")

# ----- Get word list -----
iter_cont_list = get_wordlist_from_txt(os.path.join(os.getcwd(), "wordlists/iteratives_and_continuation.txt"))
scalar_particle_list = get_wordlist_from_txt(os.path.join(os.getcwd(), "wordlists/scalar_particles.txt"))

# ----- Start processing -----
inputRoot = os.path.join(os.getcwd(), "annotated")
for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                lexemeList = get_sentence_as_lexeme_list(s)

                for idx, lexeme in enumerate(lexemeList):

                    # ----- 1. Items that do not need disambiguation -----
                    if lexeme.get("lemma") in iter_cont_list:
                        lexeme.set("adv_iter_cont", lexeme.get("lemma"))

                    if lexeme.get("lemma") in scalar_particle_list:
                        lexeme.set("scalar_particle", lexeme.get("lemma"))

                    # ----- 2. N-grams -----
                    # 2.1 immer mehr
                    if idx < len(lexemeList)-1 and lexeme.get("lemma") == "immer" and lexemeList[idx+1].get("lemma") == "mehr":
                        lexeme.set("adv_iter_cont", "immer_mehr")
                        lexemeList[idx+1].set("adv_iter_cont_2", "mehr")

                    # 2.2 immer noch
                    if idx < len(lexemeList)-1 and lexeme.get("lemma") == "immer" and lexemeList[idx+1].get("lemma") == "noch":
                        lexeme.set("adv_iter_cont", "immer_noch")
                        lexemeList[idx+1].set("adv_iter_cont_2", "noch")

                    # 2.3 nicht einmal
                    if idx < len(lexemeList)-1 and lexeme.get("lemma") == "nicht" and lexemeList[idx+1].get("lemma") == "einmal":
                        lexeme.set("scalar_particle", "nicht_einmal")
                        lexemeList[idx+1].set("scalar_particle_2", "einmal")

                    # 2.3 nicht mal
                    if idx < len(lexemeList) - 1 and lexeme.get("lemma") == "nicht" and lexemeList[idx+1].get("lemma") == "mal":
                        lexeme.set("scalar_particle", "nicht_mal")
                        lexemeList[idx + 1].set("scalar_particle_2", "mal")

                    # 2.3 geschweige denn
                    if idx < len(lexemeList)-1 and re.fullmatch("geschweigen?", lexeme.get("lemma")) and lexemeList[idx+1].get("lemma") == "denn":
                        lexeme.set("scalar_particle", "geschweige_denn")
                        lexemeList[idx+1].set("scalar_particle_2", "denn")

                    #TODO: Items that are difficult to disambiguate: wiederum, selbst, allein, auch nur

            tree.write(os.path.join(r, filename), encoding="utf-8")