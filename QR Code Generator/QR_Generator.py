import qrcode
import os
import os


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

createFolder('./QR Codes/')


qr = qrcode.QRCode(version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=1)
choice = str(input("Text or URL: "))
choice = choice.upper()
if choice == "URL":
    data = str(input("Enter a URL: "))
elif choice == "TEXT":
    data = str(input("Enter a text: "))

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

name = str(input(f"Enter a name for the image: "))
img.save(f'./QR Codes/{name}.png')

