import os
from pathlib import Path
import shutil

p = Path.cwd()
shutil.copy(p / "readme.md", p / "automated")
