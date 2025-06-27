from diffusers import StableDiffusionPipeline, DDPMScheduler
import torch

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4",
                                               variant="fp16", torch_dtype=torch.float16)
pipe.to("mps")
# pipe.to("cuda")
print("Enter prompt to generate image:")
prompt = input()
scheduler = DDPMScheduler(beta_start=0.00085, beta_end=0.012,
                          beta_schedule="scaled_linear")
image = pipe(
    prompt,
    scheduler=scheduler,
    num_inference_steps=30,
    guidance_scale=7.5,
).images[0]
image.save("tutorial1.png")

