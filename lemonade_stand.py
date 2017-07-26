def get_order():
    item = input()
    if not item:
        return '00'
    if item == 'Q':
        return 'QQ'
    quantity = int(input('How many? '))
    return item, quantity
    
register = 0
order = ''
prices = 50, 75, 100

print('Lemonade Stand starting up...')
print('Ready to take orders!')

while 1:
    print('What would you like to order (1-3)? One at a time, please.')
    print('1. Glass of lemonade - $0.50\n'
          '2. Glass of grapefruit juice - $0.75\n'
          '3. Cookie - $1.00')
    item, quantity = get_order()
    if item == 'Q':
        break
    if item == '0':
        quantities = list(order.count(obj) for obj in '123')
        for name,number,price in zip(('Glasses of lemonade', 'Glasses of grapefruit juice', 'Cookies'),
                                       quantities,
                                       prices):
            if number:
                print('{}: {}. ${:.02f}'.format(name, number, number*price/100))
        total = sum(name*number for name,number in zip(quantities, prices))
        register += total
        print('Total: ${:.02f}'.format(total/100))
        tendered = int(input('Input cash (n.nn): ').replace('.', '').lstrip('0'))
        change = tendered - total
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
        if any(user_denominations.values()):
            print('Your change:')
            for denomination in denominations:
                quant = user_denominations[denomination]
                if quant:
                    print('{}: {}'.format(denomination, quant))
        order = ''
    else:
        order += item*quantity

print("Today's total: ${:.02f}".format(register/100))