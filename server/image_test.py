from core.storage import get_image
from core.embedding_generation import convert_image_to_text
content_key = "content/dereference/f679fafc-d068-475a-a281-a3ba2f207219.jpeg"
# image = get_image(content_key)

print(convert_image_to_text(content_key))
