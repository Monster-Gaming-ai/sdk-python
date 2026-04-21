# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Luxedeum, LLC d/b/a Monster Gaming

"""
Monster Gaming SDK for Python

Official Python client for Monster Gaming — AI-powered game development platform.
https://monstergaming.ai
"""

from .client import MonsterGaming, MonsterGamingError

__version__ = "0.1.0"
__all__ = ["MonsterGaming", "MonsterGamingError"]