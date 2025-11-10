class Phone:
    def __init__(self):
        self.brand = "Infinix"
        self.name = "Note 8 I"
        self.colour = "Green"
        self.year = "2022"
        self.charger = "Type-C"
        #self.person = person

    def transport(self):
        country = "Nigeria"
        location = "Abuja"

        print(f"We at {self.brand} headquaters will now distribute our new phone, produced {self.year}, the {self.name} for sale in {country} beginning in {location}")

    def sale(self):
        price = 130000
        quantity = 5000

        print(f"The phones will be sold at a price of {price} Naira and over {quantity} phones with a {self.colour} phone pouch have been dispersed around Abuja for sale.")

    def warning(self):
        print(f"please note that our phones only use {self.charger} chargers and any other type is prohibited \nThank you for choosing {self.brand} phones and you have a lovely day.")

print(Phone.transport())
print(Phone.warning())
print(Phone.sale())