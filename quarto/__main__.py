from quarto import Quarto

TARGET = 'target'

site = Quarto()
print(site)

print('Write to',TARGET)
site.write(TARGET)
