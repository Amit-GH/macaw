import os
from typing import List

import tantivy
import argparse

from macaw.core.retrieval.doc import get_trec_doc
from macaw.util import logging


def get_trec_docs(documents_path: str) -> List[str]:
    # can be optimized
    doc_list = []
    for trec_files in os.listdir(documents_path):
        with open(os.path.join(documents_path, trec_files), 'r') as fobj:
            doc_list.append(get_trec_doc(fobj.read()))
    return doc_list


def main(index_path, documents_path):
    # build the schema
    schema_builder = tantivy.SchemaBuilder()
    schema_builder.add_text_field("body", stored=False)
    schema_builder.add_unsigned_field("doc_id", stored=True)
    schema = schema_builder.build()
    # create index
    index = tantivy.Index(schema, path=index_path)
    # read all trec doc
    documents = get_trec_doc(documents_path)
    # add documents
    logging.info('Building sparse index of {} docs...'.format(len(documents)))
    writer = index.writer()
    for i, doc in enumerate(documents):
        writer.add_document(tantivy.Document(
            body=[doc.text],
            doc_id=i
        ))
        if (i + 1) % 100000 == 0:
            writer.commit()
            logging.info('Indexed {} docs'.format(i + 1))
    writer.commit()
    logging.info('Built sparse index')
    index.reload()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Index documents')
    parser.add_argument('--index_path', type=str, help='path to store the index')
    parser.add_argument('--document_path', type=str, help='path for documents to index')
    args = parser.parse_args()

    main(args.index_path, args.document_path)
