import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
from ai_functions import *
import util
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def llm_classify(dataframe: pd.DataFrame, 
                 class_column_name: str, 
                 data_column_name: str, 
                 example_classes: list, 
                 fixed_classes: list, 
                 max_classes: int, 
                 max_words_per_class: int,
                 openai_client: OpenAI
                 ) -> pd.DataFrame:
    


    classes_df = util.get_values_as_list(dataframe, column_name=class_column_name)
    print(classes_df)
    example_classes = list(set(example_classes + classes_df + fixed_classes))

    while len(example_classes) > max_classes:
        class_classified=""
        merge_dict = json.loads(merge_classes(class_classified, example_classes, fixed_classes, max_classes, max_words_per_class, openai_client))
        print(merge_dict)
        for class_ in merge_dict["classes_to_merge"]:
             dataframe = util.replace_values_in_column(dataframe, class_column_name, match_string=class_, replace_string=merge_dict["new_class"])

        example_classes = [merge_dict["new_class"]] + [class_ for class_ in example_classes if class_ not in merge_dict["classes_to_merge"]]

        print(example_classes)

        
    for index, row in dataframe[dataframe[class_column_name].isnull()].iterrows():
        text = row[data_column_name]
        class_classified = classify_txt(text, example_classes, max_words_per_class, openai_client)
        class_classified_json = json.loads(class_classified)
        class_ = class_classified_json["class"]
        print(class_)
        dataframe.at[index, class_column_name] = class_

        if class_ not in example_classes and len(example_classes) < max_classes:
            example_classes.append(class_)
            print(example_classes)

        elif class_ not in example_classes and len(example_classes) == max_classes:
            print("DOING A MERGE")
            merge_dict = json.loads(merge_classes(class_classified, example_classes, fixed_classes, max_classes, max_words_per_class, openai_client))
            print(merge_dict)
            for class_ in merge_dict["classes_to_merge"]:
                dataframe = util.replace_values_in_column(dataframe, class_column_name, match_string=class_, replace_string=merge_dict["new_class"])

            example_classes = [merge_dict["new_class"]] + [class_ for class_ in example_classes if class_ not in merge_dict["classes_to_merge"]]

    return dataframe


dataframe = pd.read_csv("/Users/danieltremer/Documents/llm-classifier/trending_repositories_summary.csv")
openai_client = OpenAI(api_key=api_key)
class_column_name="Classification"
data_column_name = "Summary"
example_classes = []
max_classes = 10
max_words_per_class = 4
fixed_classes = []


new_df = llm_classify(dataframe, 
             class_column_name, 
             data_column_name, 
             example_classes, 
             fixed_classes, 
             max_classes, 
             max_words_per_class, 
             openai_client)

new_df.to_csv("output.csv", index=False)