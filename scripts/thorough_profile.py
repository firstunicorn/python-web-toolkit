"""Pytest plugin that globally registers Hypothesis profiles.

If the environment variable `THOROUGH_TESTS` is set to ``1``, the plugin
activates the ``thorough`` profile (1000 examples). Otherwise the default
profile (100 examples) is used.
"""
from os import getenv

from hypothesis import settings

# Always register profiles so they are available for loading later
settings.register_profile("default", max_examples=100)
settings.register_profile("thorough", max_examples=1000)

# Activate profile based on environment variable (set by test script)
if getenv("THOROUGH_TESTS") == "1":
    settings.load_profile("thorough")
else:
    settings.load_profile("default")

