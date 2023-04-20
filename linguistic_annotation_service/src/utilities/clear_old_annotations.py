import os
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list, get_feature_list
from tqdm import tqdm

print("Clear old annotations...")

inputRoot = os.path.join(os.getcwd(), "annotated")
feature_names = get_feature_list()

for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for s in root.iter("sentence"):
                lexemeList = get_sentence_as_lexeme_list(s)

                for lexeme in lexemeList:
                    for feature in feature_names:
                        lexeme.attrib.pop(feature, None)

            tree.write(os.path.join(r, filename), encoding="utf-8")