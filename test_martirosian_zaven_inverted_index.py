from textwrap import dedent
import pytest


from task_martirosian_zaven_inverted_index import ArrayStoragePolicy, InvertedIndex, build_inverted_index, \
    load_documents


def test_can_load_documents(tmpdir):
    dataset_fio = tmpdir.join("dataset.txt")
    dataset_fio.write(dedent("""\
        <define your dataset here>
    """))
    documents = load_documents(dataset_fio)
    etalon_documents = {
        # define your dataset here
    }
    assert etalon_documents == documents, (
        "load_documents incorrectly loaded dataset"
    )


def test_can_load_wikipedia_sample():
    documents = load_documents("../resources/wikipedia.sample")
    assert len(documents) == 4100, (
        "you incorrectly loaded Wikipedia sample"
    )


@pytest.fixture
def wikipedia_documents():
    documents = load_documents("../resources/wikipedia.sample")
    return documents


@pytest.fixture
def small_sample_wikipedia_documents():
    documents = load_documents("../resources/small_wikipedia.sample")
    return documents


def test_can_build_and_query_inverted_index(wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(wikipedia_documents)
    doc_ids = wikipedia_inverted_index.query(["wikipedia"])
    assert isinstance(doc_ids, list), "inverted index query should return list"


@pytest.fixture
def wikipedia_inverted_index(wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(wikipedia_documents)
    return wikipedia_inverted_index


@pytest.fixture
def small_wikipedia_inverted_index(small_sample_wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(small_sample_wikipedia_documents)
    return wikipedia_inverted_index


def test_can_dump_and_load_inverted_index(tmpdir, wikipedia_inverted_index):
    index_fio = tmpdir.join("index.dump")
    wikipedia_inverted_index.dump(index_fio)
    loaded_inverted_index = InvertedIndex.load(index_fio)
    assert wikipedia_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


@pytest.mark.xfail
def test_can_dump_and_load_inverted_index_with_array_policy(tmpdir, small_wikipedia_inverted_index):
    # do some magic here
    pass


@pytest.mark.skip
def test_can_dump_and_load_big_inverted_index_with_array_policy(tmpdir, wikipedia_inverted_index):
    # do some magic here
    pass


@pytest.mark.parametrize(
    ("filepath",),
    [
        ("../resources/wikipedia.sample",),
        ("../resources/small_wikipedia.sample",),
    ],
    ids=["small dataset", "big dataset"],
)
def test_can_dump_and_load_inverted_index_with_array_policy_parametrized(filepath, tmpdir):
    # some code here

    inverted_index.dump(index_fio, storage_policy=ArrayStoragePolicy)
    InvertedIndex.load(index_fio, storage_policy=ArrayStoragePolicy)

    assert etalon_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )
