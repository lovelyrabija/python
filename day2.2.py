import qrcode
x = qrcode.QRCode()
msg = ("you are so sweet ")
x.add_data(msg)
x.make(fit=True)
result=x.make_image(fill_color="black",back_color="white")
result.save("ak.png")
