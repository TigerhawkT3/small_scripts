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
        self.TAX = 0.08
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
        self.time_label.grid(row=0, column=1, columnspan=4, sticky='E')
        for idx,item in enumerate(self.items.values(), start=1):
            item.button.grid(row=idx, column=0, sticky='W')
        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=1, sticky='W', rowspan=idx+1, columnspan=4)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.box = tk.Listbox(self.frame,
                              yscrollcommand=self.scrollbar.set,
                              width=self.MAX_NAME_WIDTH + self.MAX_PRICE_WIDTH + 10,
                              font=self.font)
        self.scrollbar.config(command=self.box.yview)
        self.box.grid(row=0, column=1, sticky='NS')
        self.scrollbar.grid(row=0, column=2, sticky='NS')
        self.box.bind("<Double-Button-1>", self.modify_item)
        self.checkout_button = tk.Button(root, text='Checkout', command=self.checkout)
        self.checkout_button.grid(row=idx+2, column=1, sticky='W')
        self.till_button = tk.Button(root, text='Till', command=self.check_till)
        self.till_button.grid(row=idx+2, column=2, sticky='W')
        self.new_order_button = tk.Button(root, text='New order', command=self.new_order)
        self.new_order_button.grid(row=idx+2, column=3, sticky='W')
        self.total_label = tk.Label(root, text='', font=self.font)
        self.total_label.grid(row=idx+2, column=4, sticky='E')
        self.new_order()
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
        self.subtotal = sum(self.items[key].price * value for key,value in self.current_order.items())
        self.tax = round(self.subtotal * self.TAX)
        self.total = self.subtotal + self.tax
        self.total_label.config(text=f'{self.format_money(self.subtotal):>25}\n{self.format_money(self.total):>25}')
    def scan(self, code):
        self.current_order[code] += 1
        self.current_codes.append(code)
        name = self.items[code].name
        price = self.format_money(self.items[code].price)
        self.box.insert(tk.END, f'{name:<{self.MAX_NAME_WIDTH}}' + f'{price:>{self.MAX_PRICE_WIDTH+10}}')
        self.box.see(self.box.size()-1)
        self.update_totals()
    def format_money(self, cents):
        d,c = divmod(cents, 100)
        return f'${d}.{c:0>2}'
    def checkout(self):
        self.total_label.config(text=f'TOTAL: {self.format_money(self.total)}\n')
        for item in self.items.values():
            item.button.config(state=tk.DISABLED)
        top = tk.Toplevel()
        label = tk.Label(top, text='Input money: ')
        label.grid(row=0, column=0)
        text = tk.Entry(top)
        text.grid(row=0, column=1)
        text.focus_set()
        def pay(event=None):
            # tender is integer of pennies
            tender = int(text.get().replace('.', ''))
            change = tender - self.total
            label.config(text=f'Change: {self.format_money(change)}. Have a nice day!')
            self.till += self.total
            self.new_order()
            text.config(state=tk.DISABLED)
            go.config(text='Close', command=top.destroy)
        go = tk.Button(top, text='Pay', command=pay)
        go.grid(row=0, column=2)
    def check_till(self, event=None):
        top = tk.Toplevel()
        b = tk.Button(top, text=self.format_money(self.till), command=top.destroy)
        b.pack()
        b.focus_set()
    def new_order(self, event=None):
        self.subtotal = self.tax = self.total = 0
        for item in self.items.values():
            item.button.config(state=tk.NORMAL)
        self.box.delete(0, tk.END)
        self.current_order = count()
        self.current_codes = []
        self.update_totals()
    def tick(self):
        self.time_label.config(text=str(datetime.datetime.now()).rpartition('.')[0])
        self.parent.after(1000, self.tick)
root = tk.Tk()
app = Register(root)
root.mainloop()