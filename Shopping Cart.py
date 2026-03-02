products = [{
    'Serial no.' : 1,
    'Item' : 'Biscuits',
    'Quantity' : 5,
    'Cost/Item' : 20.5
},
{
    'Serial no.' : 2,
    'Item' : 'Cereals',
    'Quantity' : 10,
    'Cost/Item' : 90
},
{
    'Serial no.' : 3,
    'Item' : 'Chicken',
    'Quantity' : 20,
    'Cost/Item' : 100
}
]
 
cart = []
 
def print_menu():
    print(f'Sr.no    Item      Quantity      Cost/Item')
    print('-------- -------   -----------   ------------')
    for x in products:
        print(f'{x['Serial no.']}        {x['Item']}   {x['Quantity']}            {x['Cost/Item']}')
 
 
def take_order():
   
    while True:
        try:
            serial = int(input('What would you like to purchase?: '))
        except:
            print('Please input a valid numerical value!')
            continue
        if 1 <= serial <= len(products):
            break
        else:
            print('Invalid Serial number. Try again.')
 
    product_item = products[serial - 1]['Item']
    product_quantity = products[serial - 1]['Quantity']
    product_cost = products[serial - 1]['Cost/Item']
 
 
    while True:
        try:
            quantity = int(input(f'How many {product_item} would you like?: '))
        except:
            print('Please input a valid numerical value!')
            continue
        else:
            break
   
   
    if quantity > product_quantity :
        print(f'Available quantity of {product_item} is {product_quantity}:')
        return
    elif quantity <= 0:
        print('Invalid')
        return
    else:
        products[serial - 1]['Quantity'] -= quantity
        cart.append({product_item :
                     {'qty' : quantity,
                      'cost' : product_cost}})
 
 
 
def collect_details():
    delivery_charge = 0
    name = input('Enter your name: ')
    address = input('Enter your address: ')
    distance = int(input('Enter the distance from store 5/10/25/30: '))
    if distance <= 15:
        print("Delivery charge: 50Rs will be added to bill for distance less than 15km")
        delivery_charge = 50
    elif 15 < distance <= 30:
        print("Delivery charge: 100Rs will be added to bill for distance between 15 to 30km")
        delivery_charge = 100
    else:
        print('No delivery is available')
    return delivery_charge, name, address, distance
       
 
 
def print_bill(delivery_charge, name, address, distance):
    print('----------------Bill-----------------')
    print(f'Customer: {name}')
    print(f'Address: {address}')
    print(f'Distance: {distance} km')
    print('-------------------------------------')
    print(f'S.No       Item        Qty         TotalCost')
 
    grand_total = 0
    s_no = 1
 
    for purchase in cart:
        for item_name, details in purchase.items():
            qty = details['qty']
            cost = details['cost']
            line_total = qty * cost
            grand_total += line_total
            print(f'{s_no}   {item_name}   {qty}    {line_total}')
            s_no += 1
   
    print('-------------------------------------')
    print(f'Delivery Charge: {delivery_charge}')
    print(f'Grand Total: {grand_total + delivery_charge}')
    print('-------------------------------------')
 
 
 
shopping = True
while shopping:
    print_menu()
    take_order()
    choice = input("Do you want to continue shopping? Y/N: ")
    if choice.lower() == 'n':
        shopping = False
        delivery_charge, name, address, distance = collect_details()
        print_bill(delivery_charge, name, address, distance)
        print('----------------- Remaining Quantity In Store ---------------------')
        print_menu()