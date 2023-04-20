import os, shutil, argparse
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
from src.utilities.annotation_utils import get_flag_arguments


print("Convert files to XML...")

outputRoot = os.path.join(os.getcwd(), "interim")
if os.path.exists(outputRoot):
   shutil.rmtree(outputRoot)
os.makedirs(outputRoot)

file_path, text_column, separator = get_flag_arguments()
df = pd.read_csv(file_path, sep=separator, encoding="utf-8")

for idx, row in tqdm(df.iterrows(), total=len(df), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
    section = ET.Element("section")
    topic = ET.SubElement(section, "topic")
    utterance = ET.SubElement(topic, "utterance")
    utterance.text = row[text_column]

    currentFileName = "doc_" + str(idx+1) + ".xml"
    ET.ElementTree(section).write(os.path.join(outputRoot, currentFileName), encoding="utf-8", xml_declaration=True)

print("DONE.")