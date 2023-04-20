#!/bin/bash

export PYTHONPATH="$PWD"

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

## ----- 1. Preprocessing -----
python src/preprocessing/df2xml.py "$@"
python src/preprocessing/preprocessing_stanza.py
rm -r ./interim

# ----- 2. Clear old annotation -----
python src/utilities/clear_old_annotations.py

# ----- 3. Annotation -----
# Annotate negation and quotation (They should be done first, because some other scripts depend on them)
python src/annotation/negation.py
python src/annotation/quotation.py

# Annotate sentence type
python src/annotation/sentence_type.py

# Annotate discourse connectives
python src/annotation/causal.py
python src/annotation/adversative.py
python src/annotation/conditional.py
python src/annotation/concessive.py

# Annotate modal particles
python src/annotation/modal_particles.py

# Annotate affectiveness (arousal, valence, abstractness, imageability)
python src/annotation/affectiveness.py

# Annotate presupposition triggers
python src/annotation/presupposition_triggers.py

# Annotate Refugees and Migration Framing Vocabulary
python src/annotation/rmfv.py

# ----- 4. Write out feature statistics -----
python src/utilities/write_feature_statistics.py "$@"


echo "\033[32mDone with annotation./results\033[m"
echo "\033[32mAll annotated articles can be found at: /annotated\033[m"
echo "\033[32mStatistics of all features can be found at: /results\033[m"