from googletrans import Translator
x = Translator()
text1 = input ("enter any sentence:")
text2 = input ("enter the target:")
result = x.translate(text1, dest=text2)
print("the orginal test:",text1)
print("translategoogle: ",result)