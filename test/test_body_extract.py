import pytest
from helpers.prpar import _extractLinkFromBody, _getRallyArtifactUrls, _getRallyArtifactRefs
from helpers.dbconn import getConnection, _query

DATABASE_URL = "postgresql://pairing:pairing@localhost:5432/installs"
INSTALL_ID   = 575440

def connect_to_db():
    return getConnection(DATABASE_URL)

single_ref_body = """
zigby shuuzle went to town where nobody knew his old sick cow
https://rally1.rallydev.com/#detail/userstory/233499351572 but his old sick cow named 12345 is too well known and he
sold his cow and got drunk
"""

multi_ref_body = """
zigby shuuzle went to town where nobody knew his old sick cow
https://rally1.rallydev.com/#detail/userstory/233499351572 but his old sick cow named 12345 is too well known and he
https://rally1.rallydev.com/#detail/portfolioitem/feature/253303082732
sold his cow and got drunk
"""

no_ref_body = """
zigby shuuzle went to town where nobody knew his old sick cow
https://rally1.rallydev.com/#/userstory/233beta9 but his old sick cow named 12345 is too well known and he
sold his cow and got drunk
"""

def test_extract_single_ref():
    links = _extractLinkFromBody(single_ref_body)
    assert len(links) == 1
    assert 'rally1.rallydev.com/#detail/userstory/233' in links[0]


def test_extract_multiple_ref():
    links = _extractLinkFromBody(multi_ref_body)
    assert len(links) == 2

def test_extract_no_ref():
    links = _extractLinkFromBody(no_ref_body)
    assert len(links) == 0

def test_getArtUrls():
    short_refs = _getRallyArtifactUrls(single_ref_body)
    assert len(short_refs) == 1
    assert 'userstory' in short_refs[0]
    result = _query(connect_to_db(), INSTALL_ID)
    api_key = result[1]
    art_refs = _getRallyArtifactRefs(short_refs, api_key)
    assert len(art_refs) == 1
    assert "hierarchicalrequirement/233499351572" in art_refs[0]

def test_getArtUrlsWithMultipleRefs():
    short_refs = _getRallyArtifactUrls(multi_ref_body)
    assert len(short_refs) == 2
    assert 'userstory' in short_refs[0]
    result = _query(connect_to_db(), INSTALL_ID)
    api_key = result[1]
    art_refs = _getRallyArtifactRefs(short_refs, api_key)
    assert len(art_refs) == 2
    assert "hierarchicalrequirement/233499351572" in art_refs[0]
    assert "portfolioitem/feature/253303082732"   in art_refs[1]