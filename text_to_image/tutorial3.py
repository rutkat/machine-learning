#
# pip install diffusers transformers accelerate
#
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
 
model = "./path/realisticVisionV60B1_v60B1VAE.safetensors"
pipe = StableDiffusionPipeline.from_single_file(model)
# Mac silicon
pipe.to("mps") 
# pipe.to("cuda")
print("Enter prompt to generate image:")
prompt = input()
scheduler = EulerDiscreteScheduler(beta_start=0.00085, beta_end=0.012,
                                   beta_schedule="scaled_linear")
image = pipe(
    prompt,
    scheduler=scheduler,
    num_inference_steps=30,
    guidance_scale=7.5,
).images[0]
image.save("tutorial3.png")


