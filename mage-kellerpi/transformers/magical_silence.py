from collections import defaultdict
from typing import Dict, List

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(messages: List[Dict], *args, **kwargs):
    """
    Template code for a transformer block.

    Args:
        messages: List of messages in the stream.

    Returns:
        Transformed messages
    """
    # for message in messages:
    #    print(message)

    product_count = defaultdict(int)

    for purchase in messages:
        product_count[purchase["product"]] += 1

    print(f"Wewt! I can see the purchases: {dict(product_count)}")
    return product_count
