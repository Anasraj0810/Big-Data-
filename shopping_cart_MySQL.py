import mysql.connector
from mysql.connector import Error
from decimal import Decimal

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Withi123!",
    "database": "shopping_cart_db",
}

cart = []


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_valid_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")


def print_menu() -> None:
    query = "SELECT serial, item, quantity, price FROM products ORDER BY serial"

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        products = cursor.fetchall()

        print("\nAvailable Products")
        print("-" * 55)
        print(f"{'Sr.No':<8}{'Item':<15}{'Quantity':<12}{'Cost/Item':<10}")
        print("-" * 55)

        for product in products:
            print(
                f"{product['serial']:<8}{product['item']:<15}"
                f"{product['quantity']:<12}{product['price']:<10}"
            )
        print("-" * 55)

    except Error as e:
        print(f"Error fetching products: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def find_product_by_serial(serial: int):
    query = "SELECT serial, item, quantity, price FROM products WHERE serial = %s"

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (serial,))
        return cursor.fetchone()

    except Error as e:
        print(f"Error finding product: {e}")
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def update_product_quantity(serial: int, new_quantity: int) -> None:
    query = "UPDATE products SET quantity = %s WHERE serial = %s"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (new_quantity, serial))
        conn.commit()

    except Error as e:
        print(f"Error updating quantity: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def add_to_cart() -> None:
    while True:
        serial = get_valid_int("What would you like to purchase? Enter serial number: ")
        product = find_product_by_serial(serial)

        if product is None:
            print("Invalid serial number. Try again.")
            continue
        break

    if product["quantity"] == 0:
        print(f"Sorry, {product['item']} is out of stock.")
        return

    quantity = get_valid_int(f"How many {product['item']} would you like? ")

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    if quantity > product["quantity"]:
        print(f"Available quantity of {product['item']} is only {product['quantity']}.")
        return

    new_quantity = product["quantity"] - quantity
    update_product_quantity(product["serial"], new_quantity)

    for cart_item in cart:
        if cart_item["serial"] == product["serial"]:
            cart_item["qty"] += quantity
            return

    cart.append({
        "serial": product["serial"],
        "item": product["item"],
        "qty": quantity,
        "price": Decimal(str(product["price"]))
    })


def collect_details():
    name = input("Enter your name: ").strip()
    address = input("Enter your address: ").strip()
    distance = get_valid_int("Enter distance from store (in km): ")

    if distance <= 15:
        delivery_charge = Decimal("50.00")
        print("Delivery charge: Rs 50")
    elif distance <= 30:
        delivery_charge = Decimal("100.00")
        print("Delivery charge: Rs 100")
    else:
        delivery_charge = Decimal("0.00")
        print("No delivery available beyond 30 km. Delivery charge set to Rs 0.")

    return delivery_charge, name, address, distance


def save_order(name: str, address: str, distance: int, delivery_charge: Decimal):
    items_total = sum(item["qty"] * item["price"] for item in cart)
    grand_total = items_total + delivery_charge

    order_query = """
        INSERT INTO orders (customer_name, address, distance, delivery_charge, grand_total)
        VALUES (%s, %s, %s, %s, %s)
    """

    item_query = """
        INSERT INTO order_items (order_id, product_serial, item_name, qty, price, line_total)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(order_query, (name, address, distance, delivery_charge, grand_total))
        order_id = cursor.lastrowid

        item_rows = []
        for item in cart:
            line_total = item["qty"] * item["price"]
            item_rows.append((
                order_id,
                item["serial"],
                item["item"],
                item["qty"],
                item["price"],
                line_total
            ))

        cursor.executemany(item_query, item_rows)
        conn.commit()
        return order_id

    except Error as e:
        print(f"Error saving order: {e}")
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def fetch_bill(order_id: int):
    order_query = """
        SELECT order_id, customer_name, address, distance, delivery_charge, grand_total, created_at
        FROM orders
        WHERE order_id = %s
    """

    items_query = """
        SELECT item_name, qty, price, line_total
        FROM order_items
        WHERE order_id = %s
        ORDER BY id
    """

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(order_query, (order_id,))
        order_data = cursor.fetchone()

        cursor.execute(items_query, (order_id,))
        items_data = cursor.fetchall()

        return order_data, items_data

    except Error as e:
        print(f"Error fetching bill: {e}")
        return None, []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def print_bill(order_id: int) -> None:
    order_data, items_data = fetch_bill(order_id)

    if not order_data:
        print("Unable to retrieve bill.")
        return

    print("\n" + "=" * 60)
    print("BILL")
    print("=" * 60)
    print(f"Order ID : {order_data['order_id']}")
    print(f"Customer : {order_data['customer_name']}")
    print(f"Address  : {order_data['address']}")
    print(f"Distance : {order_data['distance']} km")
    print(f"Date     : {order_data['created_at']}")
    print("-" * 60)
    print(f"{'S.No':<6}{'Item':<15}{'Qty':<8}{'Price':<10}{'Total':<10}")
    print("-" * 60)

    items_total = Decimal("0.00")

    for index, item in enumerate(items_data, start=1):
        line_total = Decimal(str(item["line_total"]))
        items_total += line_total
        print(
            f"{index:<6}{item['item_name']:<15}{item['qty']:<8}"
            f"{item['price']:<10}{item['line_total']:<10}"
        )

    print("-" * 60)
    print(f"{'Items Total:':<40}Rs {items_total}")
    print(f"{'Delivery Charge:':<40}Rs {order_data['delivery_charge']}")
    print(f"{'Grand Total:':<40}Rs {order_data['grand_total']}")
    print("=" * 60)


def main() -> None:
    while True:
        print_menu()
        add_to_cart()

        choice = input("Do you want to continue shopping? (Y/N): ").strip().lower()
        if choice == "n":
            break

    if not cart:
        print("Your cart is empty.")
    else:
        delivery_charge, name, address, distance = collect_details()
        order_id = save_order(name, address, distance, delivery_charge)

        if order_id is not None:
            print_bill(order_id)

    print("\nRemaining Quantity In Store")
    print_menu()


if __name__ == "__main__":
    main()