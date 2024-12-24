# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "gliner==0.2.13",
# ]
# ///
from gliner import GLiNER

model = GLiNER.from_pretrained('urchade/gliner_small-v2.1')