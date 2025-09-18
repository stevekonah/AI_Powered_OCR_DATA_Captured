from db.database import get_random_validated, ValidatedForm, Session, Base, engine
import pytest

def setup_module(module):
    Base.metadata.create_all(engine)
    # Add some dummy forms
    session = Session()
    for i in range(10):
        form = ValidatedForm(form_type="FormA", field_data={"field": i})
        session.add(form)
    session.commit()
    session.close()

def teardown_module(module):
    Base.metadata.drop_all(engine)

def test_get_random_validated():
    samples = get_random_validated(sample_size=5)
    assert len(samples) == 5
    # Each sample is a ValidatedForm
    for sample in samples:
        assert hasattr(sample, "form_type")
        assert hasattr(sample, "field_data")