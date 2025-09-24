# VoxCPM Gradio API client example
# Usage: python API_client_example.py

from gradio_client import Client
import shutil
from pathlib import Path

client = Client("http://localhost:7860/")
print("Connected to Gradio API")

result = client.predict(
    text_input="你好，这是一个测试消息",
    prompt_wav_path_input=None,
    prompt_text_input=None,
    cfg_value_input=2.0,
    inference_timesteps_input=10,
    do_normalize=False,
    denoise=False,
    api_name="/generate"
)

print("API raw result:", result)

if isinstance(result, str) and Path(result).exists():
    dest = Path("generated.wav")
    shutil.copy(result, dest)
    print("Generated audio saved to", dest.resolve())
else:
    print("Unexpected response type", type(result))
