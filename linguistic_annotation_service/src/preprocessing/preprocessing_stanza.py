import os, shutil, stanza
import xml.etree.ElementTree as ET
from xml.dom import minidom
from src.utilities.annotation_utils import parse_xml_tree
from tqdm import tqdm


def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.

    :param elem: The XML element to be prettified.
    :return: prettified XML string.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

print("Preprocessing files with Stanza...")

stanza.download(lang="de", verbose=False)
nlp = stanza.Pipeline(lang="de", verbose=False)

# ----- Define the paths of input and output files -----
inputRoot = os.path.join(os.getcwd(), "interim")

outputRoot = os.path.join(os.getcwd(), "annotated")
if os.path.exists(outputRoot):
   shutil.rmtree(outputRoot)
os.makedirs(outputRoot)

# -----Start processsing -----

for r, d, f in os.walk(inputRoot):
    for file_index, filename in tqdm(enumerate(f), total=len(f), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        if filename.endswith(".xml"):
            tree, root = parse_xml_tree(os.path.join(r, filename))

            for utr in root.iter('utterance'):
                currentUtr = nlp(utr.text)

                for s in currentUtr.sentences:
                    sentenceLabel = ET.SubElement(utr, "sentence")
                    for w in s.words:
                        lexemeLabel = ET.SubElement(sentenceLabel, "lexeme")
                        lexemeLabel.text = w.text
                        lexemeLabel.set("index", str(w.id))
                        lexemeLabel.set("lemma", str(w.lemma))
                        lexemeLabel.set("pos", str(w.xpos))
                        lexemeLabel.set("feats", str(w.feats))
                        lexemeLabel.set("governor", str(w.head))
                        lexemeLabel.set("dependency_relation", str(w.deprel))

                        if w.parent.ner != "O":
                            lexemeLabel.set("ner", w.parent.ner)

                utr.text = None

            output = prettify(root)
            with open(os.path.join(outputRoot, filename.split(".xml")[0] + "_annotated.xml"), mode="w", encoding="utf-8") as outputfile:
                outputfile.write(output)

print("DONE.")