import warnings

# Suppress specific warnings
# This is a generic suppression for all warnings. You can customize it to suppress specific warnings if needed.
# For example, to suppress DeprecationWarning and FutureWarning:
def suppress_warnings():
  warnings.filterwarnings("ignore", category=DeprecationWarning)
  warnings.filterwarnings("ignore", category=FutureWarning)
  warnings.filterwarnings("ignore", category=UserWarning)
  return