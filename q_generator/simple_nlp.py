import spacy
from scraping import clean_srt_nlp
import pandas as pd
import re



def get_top_entities(srt_input):
    nlp = spacy.load("en_core_web_sm")

    cleaned = clean_srt_nlp.remove_time_stamps(srt_input)
    cn = nlp(cleaned)
    print([(word, word.ent_type_) for word in cn if word.ent_type_])
    named_entities = []
    for sentence in cleaned:
        temp_entity_name = ""
        temp_named_entity = None
        sentence = nlp(sentence)
        for word in sentence:
            term = word.text
            tag = word.ent_type_
            if tag:
                temp_entity_name = " ".join([temp_entity_name, term]).strip()
                temp_named_entity = (temp_entity_name, tag)
            else:
                if temp_named_entity:
                    named_entities.append(temp_named_entity)
                    temp_entity_name = ""
                    temp_named_entity = None

    entity_frame = pd.DataFrame(named_entities, columns=["Entity Name", "Entity Type"])

    # get the top named entities
    top_entities = (
        entity_frame.groupby(by=["Entity Name", "Entity Type"])
        .size()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={0: "Frequency"})
    )
    print(top_entities.T.iloc[:, :15])


def remove_markup(srt_str: str) -> str:
    result = srt_str
    result = re.sub(r'(\[[^\[\]]*\])|(\*.*\*)','', result)
    return result
