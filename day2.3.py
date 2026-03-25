import qrcode
x= qrcode.QRCode()
upi_id= "jakeke233-3@oksbi"
name= "jackrose"
notes = "kasu kududa pun**"
anount = "100"
link = f"upi://pay?pa={upi_id}&pn={name}&tn={notes}&an={anount}&cu=INR"
x.add_data(link)
x.make(fit=True)
result= x.make_image(fill_color = "black",back_color="white")
result.save("TVK.png")