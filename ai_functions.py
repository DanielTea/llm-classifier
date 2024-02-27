import requests
import os
from openai import OpenAI

def classify_txt(txt: str, 
                 example_classes: list,
                 max_words_per_class: int,
                 openai_client: OpenAI
                 ):


    # Prepare the classification prompt with the classes from the CSV
    class_prompt = f"""
    
    Classify this text:\n\n
    
    '{txt}'\n\n
    
    Given classes are {', '.join(example_classes)}.\n\n
    
    If none of these classes are applicable create a new class, don't use none as a class\n\n

    Use only up to {max_words_per_class} words as class.\n\n

    Be very specific in naming the classes. Try not to give genaral classes like "Sports", or "Technology".\n\n

    Return a valid dictionary nothing else. Dont use ```json to mark if its a json\n\n

    keys of the dict: \n\n
    
    "class": "string"

    """

    # Classify the GitHub project
    classification_completion = openai_client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "You are a text classifier you find the best fitting class for the given text or create new class."},
            {"role": "user", "content": class_prompt}
        ]
    )
    classification = classification_completion.choices[0].message.content

    # print(classification)

    return classification

def merge_classes(overflow_class: str, 
                 example_classes: list, 
                 fixed_classes: list, 
                 max_classes: int, 
                 max_words_per_class: int,
                 openai_client: OpenAI
                 ):
    
    class_overflow_prompt = f"""
    
    
    There is a maximum amount of {max_classes} classes we have currently {len(example_classes)} classes already set. 

    Given classes are {', '.join(example_classes)}.\n\n
    
    Use only up to {max_words_per_class} words as class.\n\n
    
    The class which does not fit is: {overflow_class}\n\n

    I need to merge only 2 classes to not get over the maximum amount of {max_classes} classes. Do not merge more than 2 classes.\n\n

    Return a new class in  which other classes can merge into. \n\n

    Be very specific in naming the classes. Try not to give genaral classes like "Sports", or "Technology".\n\n

    Prefer using a given class before creating a new class.\n\n

    Return a valid dictionary nothing else. Dont use ```json to mark if its a json.\n\n

    keys of the dict: \n\n
    
    "new_class": "string"
    "classes_to_merge": stringlist

    """

    if fixed_classes and len(fixed_classes)!=0:
        fixed_prompt = f"""
            Don't use {', '.join(fixed_classes)} to merge. These Classes must persist. dont return it in classes_to_merge\n\n
        """

        class_overflow_prompt = class_overflow_prompt+fixed_prompt

      # Classify the GitHub project
    classification_completion = openai_client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": class_overflow_prompt}
        ]
    )
    classification = classification_completion.choices[0].message.content

    # print(classification)

    return classification

