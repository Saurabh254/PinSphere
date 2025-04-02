import logging
from typing import List

from sentence_transformers import SentenceTransformer

import ollama
from PIL import Image
import io

from config import settings
from .storage import get_image



def convert_image_to_text(key: str) -> str:
    image = get_image(key)
    # Convert image to bytes for Ollama
    img_bytes_io = io.BytesIO()
    image.save(img_bytes_io, format=image.format)
    img_bytes = img_bytes_io.getvalue()

    # Use Ollama LLaMA 3.2 Vision model to analyze the image
    model_name = "gemma3:4b"
    response = ollama.chat(
        model='gemma3:4b',
        messages=[{
            'role': 'user',
            'content': 'What is in this image? in max 20 words. in simple words so that I can implement vector search on this texts and strictly speaking only reply with the resulting sentence nothing else. ',
            'images': [img_bytes]
        }]
    )
    logging.info("Generated the text: {}".format(response))
    return response['message']['content']

def generate_embeddings(query: str) -> List[float]:
    model = SentenceTransformer(settings.SBERT_MODEL_NAME)  # light & fast model, you can use any SBERT model

    return model.encode(query).tolist()
