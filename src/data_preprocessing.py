"""Public data adapter added during cleanup; original merge code was not supplied."""
from pathlib import Path
import pandas as pd

def load_stations(path):
    df = pd.read_excel(Path(path), sheet_name='Sheet1')
    required = ['역명', '경도', '위도']
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    if df[required].isna().any().any():
        raise ValueError('Station names and coordinates must not be null')
    # Exact row deduplication only. Transfer station identity requires human review.
    return df.drop_duplicates(subset=required).reset_index(drop=True)
