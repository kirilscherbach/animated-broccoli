"""
NOTE: Scratchpad blocks are used only for experimentation and testing out code.
The code written here will not be executed as part of the pipeline.
"""
from mage_ai.data_preparation.variable_manager import get_variable

df = get_variable("data_inspection", "broken_sunset", "output_0")
# df.columns
len(df)
