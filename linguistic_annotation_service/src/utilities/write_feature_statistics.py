import os, datetime, shutil
import pandas as pd
from src.utilities.annotation_utils import parse_xml_tree, get_sentence_as_lexeme_list, get_feature_list, get_flag_arguments


print("Writing out feature statistics...")

inputRoot = os.path.join(os.getcwd(), "annotated")
output_root = os.path.join(os.getcwd(), "results")

if os.path.exists(output_root):
    shutil.rmtree(output_root)
os.makedirs(output_root)

file_path, text_column, separator = get_flag_arguments()
df_original = pd.read_csv(file_path, sep=separator, encoding="utf-8")

feature_names = get_feature_list()
all_feature_stats = {feature: [] for feature in feature_names}
all_feature_match = {feature: [] for feature in feature_names}
all_total_token_counts = []

exclude_quotation = ["common_ground", "resigned_acceptance", "hedging", "question", "exclamation"]
score_based = ["arousal", "concreteness", "imageability", "valence"]

for r, d, f in os.walk(inputRoot):
    for filename in sorted(f):
        tree, root = parse_xml_tree(os.path.join(r, filename))

        total_token_count = 0
        current_feature_stats = {feature: 0 for feature in feature_names}
        current_feature_match = {feature: [] for feature in feature_names}

        # ----- Start calculation -----
        for s in root.iter("sentence"):
            lexemeList = get_sentence_as_lexeme_list(s)

            for lexeme in lexemeList:
                total_token_count += 1
                for feature in current_feature_stats:
                    if lexeme.get(feature):

                        ## ----- 1. Deal with scrore-based features: -----
                        if feature in score_based:
                            current_feature_stats[feature] += float(lexeme.get(feature))

                        ## ----- 2. Deal with count-based features: -----
                        else:
                            ### If the usage within quotation should be excluded from the final statistics:
                            if feature in exclude_quotation:
                                if lexeme.get("within_direct_speech") is None and lexeme.get("within_indirect_speech") is None:
                                    current_feature_stats[feature] += 1
                                    current_feature_match[feature].append(lexeme.get(feature))
                            ### If not:
                            else:
                                current_feature_stats[feature] += 1
                                current_feature_match[feature].append(lexeme.get(feature))

        current_feature_stats = {k: v / total_token_count for k, v in current_feature_stats.items()}
        for k, v in current_feature_stats.items():
            all_feature_stats[k].append(v)

        for k, v in current_feature_match.items():
            all_feature_match[k].append(v)

df_stats = pd.concat([df_original, pd.DataFrame(all_feature_stats)], axis=1)

df_match = pd.DataFrame(all_feature_match)
df_match.drop(["question", "exclamation", "arousal", "valence"], axis=1, inplace=True)
df_match = pd.concat([df_original, df_match], axis=1)

df_stats.to_csv(os.path.join(output_root, "feature_statistics_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".tsv"), sep="\t", encoding="utf-8", index=False)
df_match.to_pickle(os.path.join(output_root, "matched_items_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".pkl"))