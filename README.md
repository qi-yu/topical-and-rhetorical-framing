# Topical and Rhetorical Framing Strategies in German Newspapers 

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## 1. About

This repository contains the source code of the following paper:

*Qi Yu. 2023. Towards a More In-Depth Detection of Political Framing. 
In Proceedings of the 6th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature.*

### Overview of the paper:

This paper aims to investigate the *linguistic properties of framing in political discourse*.
Whereas most NLP studies on automated framing detection focus heavily on framing effect arising from topic coverage, 
framing effect arising from subtle semantic and pragmatic devices remains understudied. 
Such devices include, but are not limited to: 

- **presupposition triggers** (e.g., *Refugees rioted at the train station <ins>again and again</ins>.*),
- **scalar particles** (e.g., *The infrastructure is overcrowded. <ins>Even</ins> tents were set up.*)
- **modal particles** (e.g., *There are further death cases at the mediterranean sea – because there is <ins>just</ins> no legal route to Europe for refugees.*).

Focusing on a dataset of German newspaper articles on the event "European Refugee Crisis" published between 2014-2018, 
we demonstrate the crucial role of these linguistic devices in framing.  

## 2. Content of the Repository

- Folder ```linguistic_annotation_service```: 
  Pipeline for annotating all linguistic features used in our study. Section 4 of the paper gives a comprehensive description of them. 
  See also Section 5.1 for further details on the pipeline creation.
- Folder ```analyses```: 
  Scripts for the analyses of German newspaper articles on "European Refugee Crisis" as presented in Section 5-6 of the original paper.

## 3. Use Our Linguistic Annotation Service

We provide our Linguistic Annotation Service (*LiAnS*; under the folder ```linguistic_annotation_service```) as an open-source tool. 
LiAnS conducts automated annotation of in-depth semantic and pragmatic features in German that are relevant to framing. 
It currently supports the following features: 

<table>
    <thead>
        <tr>
            <th>Dimension</th>
            <th>Feature</th>
            <th>Example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=1>emotion intensity</td>
            <td rowspan=1>arousal</td>
            <td><i>schlecht</i> 'bad' (lower emotion intensity) vs. <i>dreist</i> 'brazen-faced' (higher emotion intensity)</td>
        </tr>
        <tr>
            <td rowspan=2>presupposition</td>
            <td>scalar particles </td>
            <td><i>sogar</i> 'even', <i>wenigstens</i> 'at least' </td>
        </tr>
        <tr>
            <td>adverbs for iteration/continuation </td>
            <td><i>wieder</i> 'again', <i>andauernd</i> 'continuously'</td>
        </tr>
        <tr>
            <td rowspan=3>modal particle</td>
            <td>modal particles for common ground</td>
            <td><i>ja</i> 'as we all know'</td>
        </tr>
        <tr>
            <td>modal particles for resigned acceptance</td>
            <td><i>eben</i> / <i>halt</i>  'that’s just the way it is'</td>
        </tr>
        <tr>
            <td>modal particles for weakened commitment</td>
            <td><i>wohl</i> 'I assume'</td>
        </tr>
        <tr>
            <td rowspan=2>sentence type</td>
            <td>question</td>
        </tr>
        <tr>
            <td>exclamation</td>
        </tr>
        <tr>
            <td rowspan=4>information structure</td>
            <td>causal connectives</td>
            <td><i>weil</i> 'because', <i>deshalb</i> 'therefore'</td>
        </tr>
        <tr>
            <td>adversative connectives</td>
            <td><i>jedoch</i> 'but', <i>Einerseits...Andereseits...</i> 'On the one hand...On the other hand...'</td>
        </tr>
        <tr>
            <td>concessive connectives</td>
            <td><i>obwohl</i> 'although', <i>trotzdem</i> 'despite'</td>
        </tr>
        <tr>
            <td>conditional connectives</td>
            <td><i>wenn</i> 'if', <i>falls</i> 'in case'</td>
        </tr>
    </tbody>
</table>

### 3.1 Usage
**LiAnS accepts .csv or .tsv files as input.** 
For ease of annotation storage, LiAnS converts each raw text in the input file to an XML file and stores all annotations as XML attributes. 
Once the annotation has run successfully, all feature statistics will be written out as a separate .csv/.tsv file. 
See [Section "Ouput"](#32-output) below for details. 

To use LiAnS, please run the following commands in the terminal:
1. Install all requested packages: <br> ```pip install -r requirements.txt```
2. Redirect to the directory of LiAnS: <br> ```cd linguistic_annotation_service```
3. Start annotation: <br> ```sh annotate.sh --path <path_of_input_file> --column <text_column> --separator <separator_of_input_file>``` 
  <br> where:
   1. ```<path_of_input_file>``` should be replaced by the path of your input .csv/.tsv file 
   2. ```<text_column>``` should be replaced by the name of the column in your .csv/.tsv file where the texts to be annotated are stored
   3. ```<separator_of_input_file>``` should be replaced by the separator of your input file. <br> It accepts the following options: ```comma```,  ```tab```, ```semicolon```


### 3.2 Output
After successfully running LiAnS, you can find all feature statistics in the folder ```results```. See Section 4 of the original paper for details of the feature calculation.

The annotated texts can be found in the folder ```annotation```. 
All files have the name format ```doc_x_annotated.xml```, 
where ```x``` stands for the corresponding row number of the text of the input .csv/.tsv file.

> [!WARNING]
> LiAnS uses [Stanza](https://stanfordnlp.github.io/stanza/) for preprocessing. 
As the model server of Stanza is slow, the runtime can be long for large amount of documents.

## 4. Cite the paper
```
@inproceedings{yu-2023-towards,
    title = "Towards a More In-Depth Detection of Political Framing",
    author = "Yu, Qi",
    booktitle = "Proceedings of the 7th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.latechclfl-1.18",
    pages = "162--174"
}
```

## 5. Acknowledgment

This project is funded by the Deutsche Forschungsgemeinschaft (DFG – German Research Foundation) under Germany‘s Excellence Strategy – EXC-2035/1 – 390681379.

The tool *LiAnS* adapted the wordlists and disambiguation rules the linguistic feature annotation pipeline of the project [VisArgue](https://visargue.lingvis.io).
