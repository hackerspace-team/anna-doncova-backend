import os

import replicate

from AnnaDoncovaBackend import settings

os.environ["REPLICATE_API_TOKEN"] = settings.REPLICATE_API_TOKEN


def get_face_swap_image(width: int, height: int, target_image: str, source_image: str):
    model_ref = "yan-ops/face_swap:1c128bbaa2b685bcee5378b39d079a2c52de358a54d6e432f5dc3d61689e9de3"
    input_parameters = {
        "width": width,
        "height": height,
        "prompt": "Please perform a high-quality face swap ensuring sharp and clear edges around the face. "
                  "The swapped face should blend seamlessly with the target image without any blurring or pixelation. "
                  "Adjust the lighting and texture to match the original image for a natural and realistic look. "
                  "The face should be correctly aligned and proportionate to the body in the target image. "
                  "Aim for a result where the face swap is not noticeable and "
                  "appears as a natural part of the original photo.",
        "cache_days": 10,
        "det_thresh": 0.1,
        "target_image": target_image,
        "source_image": source_image,
        "num_inference_steps": 5,
        "num_images_per_prompt": 1
    }

    output = replicate.run(
        ref=model_ref,
        input=input_parameters
    )

    return output['image']
