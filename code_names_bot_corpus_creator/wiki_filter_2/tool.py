import json
from code_names_bot_corpus_creator.download.caches import WikiRedirectsCategoriesCache

cache = WikiRedirectsCategoriesCache()

title_to_json = cache.get_key_to_value()
for title in title_to_json:
    result_json = json.loads(title_to_json[title])
    
    if "query" not in result_json:
        print("Removing", title)
        cache.delete_key(title)

cache.commit()