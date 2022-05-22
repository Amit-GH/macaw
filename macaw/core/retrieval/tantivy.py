"""
The Indri search engine.

Authors: Hamed Zamani (hazamani@microsoft.com)
"""

import os
import subprocess

import tantivy

from macaw.core.retrieval.doc import get_trec_doc
from macaw.core.retrieval.search_engine import Retrieval


class Tantivy(Retrieval):
    def __init__(self, params):
        if not os.path.exists(params['path']):
            os.mkdir(params['path'])
        schema_builder = tantivy.SchemaBuilder()
        schema_builder.add_text_field("body", stored=False)
        schema_builder.add_unsigned_field("doc_id", stored=True)
        schema = schema_builder.build()
        self.index = tantivy.Index(schema, path=params['path'], reuse=params['load'])
        self.searcher = self.index.searcher()

    def retrieve(self, query):
        results = []
        docs = []
        try:
            query = self.index.parse_query(query, ["body"])
            scores = self.searcher.search(query, 100).hits
            docs = [(self.searcher.doc(doc_id)['doc_id'][0], score)
                    for score, doc_id in scores]
        except:
            pass
        results.append(docs)

        return results

    def get_doc_from_index(self, doc_id):
        pass
