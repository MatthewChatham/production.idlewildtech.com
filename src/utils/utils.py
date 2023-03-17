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
    return read_from_s3('production.idlewildtech.com', 'data/dd.csv').set_index('colname').to_dict()['coltype']


def get_filter_mask(
        df,
        dd,
        ctrl_values,
        ctrl_idx,
        null_values,
        apply_filters
):

    ctrl_cols = [i['column'] for i in ctrl_idx]
    print('ctrl_cols:')
    print(ctrl_cols)

    mask = [True]*len(df)

    if not ctrl_values or not apply_filters:
        return mask

    for i, c in enumerate(ctrl_cols):
        if dd[c] == 'numeric':
            m = df[c].between(*ctrl_values[i])
            if null_values[i]:
                m = m | df[c].isnull()
        else:
            m = df[c].isin(ctrl_values[i])
            if null_values[i]:
                m = m | df[c].isnull()

        mask = mask & m

    return mask
