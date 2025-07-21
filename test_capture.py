from capture_intruder import capture_intruder_image

if __name__ == "__main__":
    image_path = capture_intruder_image("captured_images", show_preview=True)
    if image_path:
        print(f"Image saved: {image_path}")
    else:
        print("No image captured (maybe you were recognized?).")
