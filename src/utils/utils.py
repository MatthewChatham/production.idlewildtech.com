import pandas as pd

def get_dd(engine):
    with engine.connect() as conn:
        dd = pd.read_sql_table(
            'dd',
            con=conn
        )
        
    return dd
        
def get_df(engine):
    with engine.connect() as conn:
        df = pd.read_sql_table(
            'df',
            con=conn
        )
    
    return df