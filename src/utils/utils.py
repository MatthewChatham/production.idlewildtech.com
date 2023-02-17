import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET = os.environ['AWS_SECRET']

def read_from_s3(bucket, filename, access_key=AWS_ACCESS_KEY, secret=AWS_SECRET):
    pth = f"s3://{bucket}/{filename}"
    print(pth)
    df = pd.read_csv(
        pth,
        storage_options={
            "key": access_key,
            "secret": secret
        }
    )

    return df

def get_df():
    return read_from_s3('production.idlewildtech.com', 'data/df_latest.csv')
        
def get_dd():
    return read_from_s3('production.idlewildtech.com', 'data/dd.csv')