from diffusers import StableDiffusionPipeline
import torch
from pathlib import Path

# cargar modelo
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
)

pipe = pipe.to("cpu")  # o "cuda" si tienes GPU

# prompt
prompt = "Un paisaje hermoso"

# generar imagen
image = pipe(prompt).images[0]

# guardar imagen
folder = Path.home() / "Pictures" / "Fondos"
folder.mkdir(parents=True, exist_ok=True)

file_path = folder / "fondo.png"
image.save(file_path)

print("Imagen guardada en:", file_path)