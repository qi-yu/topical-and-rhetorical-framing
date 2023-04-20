import argparse
import xml.etree.ElementTree as ET


def parse_xml_tree(filepath):
    """
    Parse an XML-file using xml.etree.ElementTree.

    :param filepath: The path of the file to be parsed.
    :return:
        mytree: The parsed XML-tree.
        myroot: The root of the parsed XML-tree.
    """

    # print("Process file:", filepath, "...")
    mytree = ET.parse(filepath)
    myroot = mytree.getroot()
    return mytree, myroot


def get_sentence_as_lexeme_list(sentence):
    """
    Get sentence as a list of lexemes.

    :param sentence: The sentence to be converted to lexeme list.
    :return: The sentence as a list of lexemes.
    """
    lexemeList = []
    for lexeme in sentence.findall("lexeme"):
        lexemeList.append(lexeme)

    return lexemeList


def get_sentence_as_text(sentence):
    """
    Get sentence as text.

    :param sentence: The sentence to be converted to text.
    :return: The sentence as text.
    """
    sentenceAsText = ""
    for lexeme in sentence.findall("lexeme"):
        sentenceAsText += lexeme.text + " "

    return sentenceAsText


def get_wordlist_from_txt(source):
    """
    Create a list of keywords from .txt files.

    :param source: the path of the source lexicon.
    :return: A list of keywords.
    """
    keywordList = []
    with open(source) as f:
        for line in f.readlines():
            if line.startswith("#") is False:
                keywordList.append(line.strip())
    return keywordList


def get_feature_list():
    """
    Get all feature names.

    :return: A list of all features.
    """
    feature_list = ["question", "exclamation",
                    "causal", "consecutive", "adversative", "concessive", "conditional",
                    "common_ground", "resigned_acceptance", "hedging",
                    "iter_cont_item", "scalar_particle",
                    "economy", "identity", "legal", "morality", "policy", "politics", "public_opinion", "security", "welfare",
                    "arousal", "valence"
                    ]

    return feature_list


def get_flag_arguments():
    """Get all flag arguments from CLI.

    :return:
        file_path (str):  path of the .csv/.tsv file to be processed
        text_column (str): name of the column for the texts to be annotated
        separator (str): separator of the .csv/.tsv file to be processed
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True, help="path of the .csv/.tsv file to be processed")
    parser.add_argument("-c", "--column", required=True, help="name of the column for the texts to be annotated")
    parser.add_argument("-s", "--separator", required=True,
                        help="separator of the .csv/.tsv file to be processed. Available options: comma, tab, semicolon")
    args = vars(parser.parse_args())

    file_path = args["path"]
    text_column = args["column"]
    separator = None

    if args["separator"] == "comma":
        separator = ","
    if args["separator"] == "tab":
        separator= "\t"
    if args["separator"] == "semicolon":
        separator = ";"

    return file_path, text_column, separator