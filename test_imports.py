import sys
from pathlib import Path
root = Path(__file__).resolve().parent
sys.path.append(str(root))
print(f"Path added: {root}")

try:
    from pita.backend.config.settings import LOG_LEVEL
    print(f"Import success: LOG_LEVEL={LOG_LEVEL}")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
