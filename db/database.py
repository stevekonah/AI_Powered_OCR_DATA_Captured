import random
# ... (rest of your imports and models)

def get_random_validated(sample_size=5):
    session = Session()
    all_validated = session.query(ValidatedForm).all()
    samples = random.sample(all_validated, min(sample_size, len(all_validated)))
    session.close()
    return samples