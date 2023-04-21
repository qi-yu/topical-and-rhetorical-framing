# Topical and Rhetorical Framing Strategies in German Newspapers 

## 1. About

This repository contains the source code of the paper to appear in:

*Qi Yu. 2023. Towards a More In-Depth Detection of Political Framing. 
In Proceedings of the 6th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature.*

### Overview of the paper:

This paper aims to investigate the *linguistic properties of framing in political discourse*:
whereas most NLP studies on automated framing detection focus heavily on framing effect arising from topic coverage, 
framing effect arising from subtle semantic and pragmatic devices remains understudied. 
Such devices include, but are not limited to: 

- **presupposition triggers** (e.g., *Refugees rioted at the train station <ins>again and again</ins>.*),
- **scalar particles** (e.g., *The infrastructure is overcrowded. <ins>Even</ins> tents were set up.*)
- **modal particles** (e.g., *There are further death cases at the mediterranean sea – because there is <ins>just</ins> no legal route to Europe for refugees.*).

Focusing on a dataset of German newspaper articles on the event "European Refugee Crisis" published between 2014-2018, 
we demonstrate the crucial role of these linguistic devices in framing.  

## 2. Code

- Folder ```linguistic_annotation_service```: 
  Pipeline for annotating all linguistic features used in our study. Section 4 of the paper gives a comprehensive description of them. 
  See also Section 5.1 for further details on the pipeline creation.
- Folder ```logistic_regression```: 
  Scripts for the logistic regression analysis presented in Section 5.2 of the paper.

## 3. Use Our Linguistic Annotation Service (LiAnS)

We provide our Linguistic Annotation Service (folder ```linguistic_annotation_service```) as an open-source tool. 

**LiAnS accepts .csv or .tsv files as input.** To use LiAnS, please run the following commands in your terminal:
1. Redirect to the directory of LiAnS: ```cd linguistic_annotation_service```
2. Install all requested packages: ```pip install -r requirements.txt```
3. Start annotation: ```sh annotate.sh --path <path_of_input_file> --column <text_column> --separator <separator_of_input_file>```, where:
   1. ```<path_of_input_file>``` should be replaced by the path of your input .csv/.tsv file 
   2. ```<text_column>``` should be replaced by the name of the column in your .csv/.tsv file where the texts to be annotated are stored
   3. ```<separator_of_input_file>``` should be replaced by the separator of your input file. It accepts the following options: ```comma```,  ```tab```, ```semicolon```

  
Once the annotation has run successfully, you can find all feature statistics in the folder ```results```. The annotated files can be found in the folder ```annotation``` 

### NOTE:
LiAnS uses [Stanza](https://stanfordnlp.github.io/stanza/) for preprocessing. 
As the model server of Stanza is slow, the runtime can be long for large amount of documents.

## 4. Acknowledgement

This project is funded by the Deutsche Forschungsgemeinschaft (DFG – German Research Foundation) under Germany‘s Excellence Strategy – EXC-2035/1 – 390681379.

The tool *LiAnS* adapted the wordlists and disambiguation rules the linguistic feature annotation pipeline of the project [VisArgue](https://visargue.lingvis.io).