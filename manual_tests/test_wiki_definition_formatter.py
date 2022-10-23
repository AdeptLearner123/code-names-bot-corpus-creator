import sys

from code_names_bot_dictionary_compiler.wiki_utils.definition_formatter import (
    format_definition,
)
from code_names_bot_dictionary_compiler.utils.spacy_utils import split_sentences
from code_names_bot_dictionary_compiler.download.caches import (
    WikiSummariesCache,
)


def main():
    title = sys.argv[1]

    summaries_cache = WikiSummariesCache()

    summary = summaries_cache.get_cached_value(title).strip()
    sentences = split_sentences(summary)
    definition = sentences[0]
    formatted_def = format_definition(definition)
    print(formatted_def)


if __name__ == "__main__":
    main()
