# Topical and Rhetorical Framing Strategies in German Newspapers 

## About

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

## Scripts

- Folder ```linguistic_annotation_service```: 
  Pipeline for annotating all linguistic features used in our study. Section 4 of the paper gives a comprehensive description of them. 
  See also Section 5.1 for further details on the pipeline creation.
- Folder ```logistic_regression```: 
  Scripts for the logistic regression analysis presented in Section 5.2 of the paper.
  
## Acknowledgement
This project is funded by the Deutsche Forschungsgemeinschaft (DFG – German Research Foundation) under Germany‘s Excellence Strategy – EXC-2035/1 – 390681379.