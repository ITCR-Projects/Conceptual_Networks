from StructureStemming import StructureStemming

def test_one():
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 1}, 1]}

def test_two():
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educa')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 2, 'educa': 1}, 3]}

def test_three():
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educa')
    handleStemming.add('corr', 'correr')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 2, 'educa': 1}, 3], 'corr': [{'correr': 1}, 1]}

def test_four():
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educa', 'educacionando')
    handleStemming.merge('educ','educa')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 1, 'educacionando': 1}, 2]}

