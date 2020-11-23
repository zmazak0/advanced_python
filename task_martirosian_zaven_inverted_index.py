""""inverted index """
from collections import defaultdict
import struct


def compress_doc_ids(doc_ids: list):
    """ convert to int and sort list"""
    int_doc_ids = [int(x) for x in doc_ids]
    sorted_doc_ids = sorted(int_doc_ids)
    return sorted_doc_ids


class InvertedIndex:
    """inverted index"""
    def __init__(self, word_to_docs_mapping):
        self.word_to_docs_mapping = {
            word: doc_ids for word, doc_ids in word_to_docs_mapping.items()
        }

    def query(self, words: list) -> list:
        """Return the list of relevant documents for the given query"""
        relevant_documents = self.word_to_docs_mapping[words[0]]
        if len(words) > 1:
            for word in words:
                relevant_documents = relevant_documents & self.word_to_docs_mapping[word]
        return list(relevant_documents)

    def dump(self, file_path: str):
        """dump inverted index"""
        number_of_items = len(self.word_to_docs_mapping.items())

        with open(file_path, 'wb') as f_out:
            dump_temp = struct.pack('>i', number_of_items)  # запаковали количество элементов
            f_out.write(dump_temp)  # записали количество элементов
            for word, doc_ids in self.word_to_docs_mapping.items():
                compressed_ids = compress_doc_ids(doc_ids)  # уменьшили размер цифр
                length_of_word = len(word.encode('utf-8'))  # получили длину энкодированного слова
                dump_temp = struct.pack('>H', length_of_word)
                f_out.write(dump_temp)  # записали длину энкодированного слова
                bt_word = word.encode('utf-8')  # получили энкодированное слово
                dump_temp = struct.pack('>' + str(length_of_word) + 's', bt_word)
                f_out.write(dump_temp)  # записали закодированное энкодированное слово
                dump_temp = struct.pack('>H', len(compressed_ids))  # упаковали количество ids
                f_out.write(dump_temp)  # записали количество ids
                for item in compressed_ids:
                    dump_temp = struct.pack('>H', item)
                    f_out.write(dump_temp)

    @classmethod
    def load(cls, file_path: str):
        ''' load Inverted index'''
        loaded_documents = defaultdict(set)
        with open(file_path, 'rb') as fin:
            dump_temp = fin.read(4)  # считали количество элементов
            count = struct.unpack('>i', dump_temp)[0]  # преобразовали количество элементов
            real_count = 0  # прочитанное количсетво
            while real_count < count:
                dump_temp = fin.read(2)  # считали длину слова
                length = struct.unpack('>H', dump_temp)[0]  # распаковали длину слова
                string_format = '>' + str(length) + 's'  # сформировали вид строки
                dump_temp = fin.read(length)  # считали энкодированное слово
                string_bite = struct.unpack(string_format, dump_temp)[0]
                string_bite = string_bite.decode()  # раскодировали считанное слово
                list_len_bin = fin.read(2)  # считали количесво ids
                list_len = struct.unpack('>H', list_len_bin)[0]
                for _ in range(list_len):
                    id_bin = fin.read(2)
                    if id_bin:
                        new_id = struct.unpack('>H', id_bin)[0]
                        loaded_documents[string_bite].add(new_id)
                real_count = real_count + 1
            return InvertedIndex(loaded_documents)


def load_documents(file_path: str):
    """" load documents"""
    documents = {}
    with open(file_path, encoding='utf-8') as fin:
        for line in fin:
            line = line.rstrip("\n")
            if line:
                doc_id, content = line.split("\t", 1)
                documents[doc_id] = content
    return documents


def build_inverted_index(documents):
    """build inverted index"""
    word_to_docs_mapping = defaultdict(set)
    for doc_id, content in documents.items():
        words = content.split()
        for word in words:
            word_to_docs_mapping[word].add(int(doc_id))
    return InvertedIndex(word_to_docs_mapping)


def main():
    """main inverted index"""
    documents = load_documents("wikipedia_sample")
    inverted_index = build_inverted_index(documents)
    inverted_index.dump("inverted.index")
    document_ids = inverted_index.query(["two", "words"])
    print(document_ids)
    inverted_index = InvertedIndex.load("inverted.index")
    document_ids = inverted_index.query(["two", "words"])
    print(document_ids)


if __name__ == "__main__":
    main()
