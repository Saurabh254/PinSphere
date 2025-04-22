# type: ignore
import io
import logging

import ollama
from sentence_transformers import SentenceTransformer

from config import settings
from .prompts import PROMPT_V1

from .storage import get_image


def convert_image_to_text(key: str) -> str:
    image = get_image(key)
    # Convert image to bytes for Ollama
    img_bytes_io = io.BytesIO()
    image.save(img_bytes_io, format=image.format)
    img_bytes = img_bytes_io.getvalue()

    response = ollama.chat(  # type: ignore
        model="gemma3:4b",
        messages=[
            {"role": "system",
             "content": PROMPT_V1.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": PROMPT_V1.USER_PROMPT,
                "images": [img_bytes],
            }
        ],
    )
    logging.info("Generated the text: {}".format(response))
    return response["message"]["content"]


def generate_embeddings(query: str) -> list[float]:
    model = SentenceTransformer(settings.SBERT_MODEL_NAME)  # type: ignore

    return model.encode(query).tolist()  # type: ignore
