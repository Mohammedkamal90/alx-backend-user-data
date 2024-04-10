#!/usr/bin/env python3
"""
module for filtering sensitive data in log messages
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in log message

    Args:
        fields (List[str]):list of strings representing fields to obfuscate
        redaction (str): string representing replacement for obfuscated fields
        message (str): log message to filter.
        separator (str): string representing separator character between fields

    Returns:
        str: filtered log message with specified fields obfuscated
    """
    pattern = '|'.join(map(re.escape, fields))
    return re.sub(pattern, redaction, message)
