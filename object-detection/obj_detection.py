import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import YolosForObjectDetection, YolosImageProcessor

# set jpg image
picture_path = "./cafe.jpg"
image = Image.open(picture_path)

# use huggingface model yolos-tiny
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

inputs = image_processor(images=image, return_tensors="pt")
outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(
    outputs, target_sizes=target_sizes
)[0]

draw = ImageDraw.Draw(image)
font_path = "OpenSans-ExtraBold.ttf"
font = ImageFont.truetype(str(font_path), 24)

# generate labels and outlines to image
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
  if score > 0.7:
    box_values = box.tolist()
    label = model.config.id2label[label.item()]
    draw.rectangle(box_values, outline="red", width=5)
    draw.text(box_values[0:2], label, fill="red", font=font)
# render image
image.show()

