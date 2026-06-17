import csv
import random
import uuid
from datetime import datetime, timedelta

def generate_transactions_csv(filename="transactions_data.csv", num_rows=50000):
    # set columns:
    headers = [
        "transaction_id",
        "user_id",
        "timestamp",
        "product_category",
        "amount",
        "payment_method",
        "status"
    ]

    # generate base data 
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Toys", "Books"]
    payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Crypto"]
    statuses = ["Completed", "Completed", "Completed", "Pending", "Failed", "Refunded"] 

    start_date = datetime(2025, 1, 1)

    print(f"Starting to generate {num_rows} rows into {filename}...")

    # write directly to the file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for _ in range(num_rows):
            transaction_id = str(uuid.uuid4())
            user_id = random.randint(1000, 99999)
            
            # generate random date
            random_days = random.randint(0, 365)
            random_seconds = random.randint(0, 86400)
            tx_date = start_date + timedelta(days=random_days, seconds=random_seconds)
            timestamp = tx_date.strftime("%Y-%m-%d %H:%M:%S")

            product_category = random.choice(categories)
            amount = round(random.uniform(5.0, 2500.0), 2)
            payment_method = random.choice(payment_methods)
            status = random.choice(statuses)

            writer.writerow([
                transaction_id,
                user_id,
                timestamp,
                product_category,
                amount,
                payment_method,
                status
            ])

    print("Data generation finished successfully! The file is ready.")

if __name__ == "__main__":
    generate_transactions_csv()