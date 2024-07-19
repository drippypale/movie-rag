import re

def meta_data(row,exclude=["idf","summary_tiny","summary_kio","summary_digi","summary_uptv","stroy",'total_summary']):
    dic = row.to_dict()
    result = {}
    for key, value in dic.items():
        if key not in exclude:
            if str(value) != 'nan':
                result[key] = value if not isinstance(value, str) else re.sub(r"\['|\']", '', value)

    return result

def extrac_id(row):
    return str(row["idf"])

def extract_id_from_search(search_dic):
  return search_dic['ids'][0]

def search_querY_chroma(collection,query_text:str,where_meta_data = [],where_document = [], n_results = 5):
  where = {} if len(where_meta_data) == 0 else         (where_meta_data[0] if len(where_meta_data) == 1 else { "$or": where_meta_data })
  where_document = {} if len(where_document) == 0 else (where_document[0]  if len(where_document)  == 1 else { "$or": where_document })
  search_result =  collection.query(
    query_texts=[query_text],
    n_results=n_results,
    where = where,
    where_document=where_document)
  
  search_ids = extract_id_from_search(search_result)
  if (len(search_ids) > 0):
    return search_ids

  ## if we did not find any result
  ## serach without any condition
  search_result =  collection.query(
  query_texts=[query_text],
  n_results=n_results)

  return extract_id_from_search(search_result)