from PIL import Image

with Image.open("minecwaft.jpg") as img:
    asd = img.rotate(90)
    asd.save("minecwaft-rot.jpg", "JPEG")