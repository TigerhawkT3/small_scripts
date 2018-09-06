import tkinter as tk
from collections import Counter as count
import datetime

class Item:
    def __init__(self, name, price, button):
        self.name = name
        self.price = price
        self.button = button

class Register:
    def __init__(self, parent):
        self.parent = parent
        self.till = 0
        self.items = {'lemonade':Item('Lemonade', 50,
                                      tk.Button(root,
                                      text='Lemonade',
                                      command=lambda: self.scan('lemonade'))),
                      'grapefruit_juice':Item('Grapefruit Juice', 75,
                                              tk.Button(root,
                                              text='Grapefruit Juice',
                                              command=lambda: self.scan('grapefruit_juice'))),
                       'cookie':Item('Cookie', 100,
                                     tk.Button(root,
                                     text='Cookie',
                                     command=lambda: self.scan('cookie')))}
        self.MAX_NAME_WIDTH = max(map(len, (item.name for item in self.items.values()))) + 3
        self.MAX_PRICE_WIDTH = 10
        self.server_label = tk.Label(root, text='Cashier: Bob')
        self.server_label.grid(row=0, column=0, sticky='W')
        self.time_label = tk.Label(root, text='')
        self.time_label.grid(row=0, column=1, sticky='E')
        for idx,item in enumerate(self.items.values(), start=1):
            item.button.grid(row=idx, column=0, sticky='W')
        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=1, rowspan=3)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.box = tk.Listbox(self.frame,
                              yscrollcommand=self.scrollbar.set,
                              width=self.MAX_NAME_WIDTH + self.MAX_PRICE_WIDTH,
                              font=('Courier New', 12))
        self.scrollbar.config(command=self.box.yview)
        self.box.grid(row=0, column=1, sticky='NS')
        self.scrollbar.grid(row=0, column=2, sticky='NS')
        self.current_order = count()
        self.tick()
    def scan(self, code):
        self.current_order[code] += 1
        dollars, cents = divmod(self.items[code].price, 100)
        self.box.insert(tk.END, self.items[code].name.ljust(self.MAX_NAME_WIDTH) + f'${dollars}.{cents:0>2}'.rjust(self.MAX_PRICE_WIDTH))
        self.box.see(self.box.size()-1)
    def checkout(self):
        pass
    def tick(self):
        self.time_label.config(text=str(datetime.datetime.now()).rpartition('.')[0])
        self.parent.after(1000, self.tick)
# TODO:
# display subtotal
# add multiples of item
# remove item
# end order and calculate total, tax, change
# clear order and reset
# track till total
'''
        denominations = ('Fifties', 'Twenties', 'Tens', 'Fives', 'Ones',
                         'Quarters', 'Dimes', 'Nickels', 'Pennies')
        user_denominations = {}
        dollars, cents = divmod(change, 100)
        user_denominations['Fifties'], dollars = divmod(dollars, 50)
        user_denominations['Twenties'], dollars = divmod(dollars, 20)
        user_denominations['Tens'], dollars = divmod(dollars, 10)
        user_denominations['Fives'], user_denominations['Ones'] = divmod(dollars, 5)
        user_denominations['Quarters'], cents = divmod(cents, 25)
        user_denominations['Dimes'], cents = divmod(cents, 10)
        user_denominations['Nickels'], user_denominations['Pennies'] = divmod(cents, 5)
'''
root = tk.Tk()
app = Register(root)
root.mainloop()