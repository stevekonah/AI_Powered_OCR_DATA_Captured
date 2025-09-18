import pandas as pd
import matplotlib.pyplot as plt
from db.database import Session, StagingForm, ValidatedForm

def generate_validation_report():
    session = Session()
    total = session.query(StagingForm).count()
    approved = session.query(StagingForm).filter_by(status="approved").count()
    rejected = session.query(StagingForm).filter_by(status="rejected").count()
    pending = session.query(StagingForm).filter_by(status="pending").count()
    session.close()
    data = {
        "Total": total,
        "Approved": approved,
        "Rejected": rejected,
        "Pending": pending
    }
    df = pd.DataFrame([data])
    print(df)
    df.plot(kind="bar")
    plt.title("Batch Validation Summary")
    plt.xticks(rotation=0)
    plt.show()