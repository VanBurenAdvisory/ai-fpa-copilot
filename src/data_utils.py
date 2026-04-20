from __future__ import annotations

from io import StringIO

import pandas as pd


def load_dataframe_from_upload(uploaded_file) -> pd.DataFrame:
    """Load a CSV from Streamlit uploader or a StringIO object."""
    if hasattr(uploaded_file, "read"):
        content = uploaded_file.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        return pd.read_csv(StringIO(content))
    raise ValueError("Unsupported uploaded file type")
