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
        parent.title('Point of Sale')
        self.font = ('Courier New', 12)
        self.till = 0
        self.TAX = 1.08
        self.items = {'lemonade':Item('Lemonade', 50,
                                      tk.Button(root,
                                      text='Lemonade',
                                      command=lambda: self.scan('lemonade'),
                                      font=self.font)),
                      'grapefruit_juice':Item('Grapefruit Juice', 75,
                                              tk.Button(root,
                                              text='Grapefruit Juice',
                                              command=lambda: self.scan('grapefruit_juice'),
                                              font=self.font)),
                       'cookie':Item('Cookie', 100,
                                     tk.Button(root,
                                     text='Cookie',
                                     command=lambda: self.scan('cookie'),
                                     font=self.font))}
        self.MAX_NAME_WIDTH = max(map(len, (item.name for item in self.items.values()))) + 3
        self.MAX_PRICE_WIDTH = 10
        self.server_label = tk.Label(root, text='Cashier: Bob', font=self.font)
        self.server_label.grid(row=0, column=0, sticky='W')
        self.time_label = tk.Label(root, text='', font=self.font)
        self.time_label.grid(row=0, column=1, sticky='E')
        for idx,item in enumerate(self.items.values(), start=1):
            item.button.grid(row=idx, column=0, sticky='W')
        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=1, rowspan=3)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.box = tk.Listbox(self.frame,
                              yscrollcommand=self.scrollbar.set,
                              width=self.MAX_NAME_WIDTH + self.MAX_PRICE_WIDTH,
                              font=self.font)
        self.scrollbar.config(command=self.box.yview)
        self.box.grid(row=0, column=1, sticky='NS')
        self.scrollbar.grid(row=0, column=2, sticky='NS')
        self.box.bind("<Double-Button-1>", self.modify_item)
        self.total_label = tk.Label(root, text='', font=self.font)
        self.total_label.grid(row=4, column=1, sticky='E')
        self.current_order = count()
        self.current_codes = []
        self.update_totals()
        self.tick()
    def modify_item(self, event=None):
        top = tk.Toplevel()
        entry = tk.Entry(top, font=self.font)
        entry.pack()
        entry.focus_set()
        def set_new_quantity():
            new_value = int(entry.get())
            idx = self.box.index(tk.ACTIVE)
            self.box.delete(idx)
            code = self.current_codes.pop(idx)
            self.current_order[code] -= 1
            for i in range(new_value):
                self.scan(code)
            top.destroy()
            self.update_totals()
        confirm = tk.Button(top, text='OK', command=set_new_quantity, font=self.font)
        confirm.pack()
    def update_totals(self):
        subtotal = sum(self.items[key].price * value for key,value in self.current_order.items())
        total = self.format_money(round(subtotal * self.TAX))
        subtotal = self.format_money(subtotal)
        self.total_label.config(text=f'{subtotal:>25}\n{total:>25}')
    def scan(self, code):
        self.current_order[code] += 1
        self.current_codes.append(code)
        name = self.items[code].name
        price = self.format_money(self.items[code].price)
        self.box.insert(tk.END, f'{name:<{self.MAX_NAME_WIDTH}}' + f'{price:>{self.MAX_PRICE_WIDTH}}')
        self.box.see(self.box.size()-1)
        self.update_totals()
    def format_money(self, cents):
        d,c = divmod(cents, 100)
        return f'${d}.{c:0>2}'
    def checkout(self):
        pass
    def tick(self):
        self.time_label.config(text=str(datetime.datetime.now()).rpartition('.')[0])
        self.parent.after(1000, self.tick)
# TODO:
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