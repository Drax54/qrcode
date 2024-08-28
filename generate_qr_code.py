import qrcode

# Data to be encoded in the QR code
data = "Kavita"

# Create an instance of QRCode
qr = qrcode.QRCode(
    version=1,  # Version of the QR code, controls the size of the QR code matrix
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each box in the QR code
    border=4,  # Border size (minimum is 4 for QR codes)
)

# Add data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill='black', back_color='white')

# Save the image to a file
img.save('code.png')

print("QR Code generated and saved as 'sample_qr_code.png'.")
