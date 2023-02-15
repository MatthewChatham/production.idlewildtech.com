import pandas as pd
from sqlalchemy import create_engine
from utils.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_dd(engine=engine):
    with engine.connect() as conn:
        dd = pd.read_sql_table(
            'dd',
            con=conn
        )
        
    return dd
        
def get_df(engine=engine):
    with engine.connect() as conn:
        df = pd.read_sql_table(
            'df',
            con=conn
        )
    
    return df