from flask import Flask, request, jsonify
import pandas as pd
from pathlib import Path
from utils import read_customers, write_customers, assign_new_id
from decorators import log_action

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / "data" / "customers.csv"

# Ensure CSV file exists
if not DATA_FILE.exists():
    pd.DataFrame(columns=["id", "name", "phone", "email", "address", "due_amount"]).to_csv(DATA_FILE, index=False)

@app.route("/customers", methods=["GET"])
@log_action("View all customers")
def get_customers():
    customers = read_customers(DATA_FILE)
    return jsonify(customers)

@app.route("/customers", methods=["POST"])
@log_action("Add new customer")
def add_customer():
    data = request.json
    df = pd.read_csv(DATA_FILE)

    # Assign ID (reuse smallest available)
    new_id = assign_new_id(df)
    data["id"] = new_id

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return jsonify({"message": "Customer added successfully", "customer": data})

@app.route("/customers/<int:customer_id>", methods=["PUT"])
@log_action("Update customer")
def update_customer(customer_id):
    data = request.json
    df = pd.read_csv(DATA_FILE)

    if customer_id not in df["id"].values:
        return jsonify({"error": "Customer not found"}), 404

    for key, value in data.items():
        df.loc[df["id"] == customer_id, key] = value

    df.to_csv(DATA_FILE, index=False)
    return jsonify({"message": f"Customer {customer_id} updated", "updated_data": data})

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
@log_action("Delete customer")
def delete_customer(customer_id):
    df = pd.read_csv(DATA_FILE)

    if customer_id not in df["id"].values:
        return jsonify({"error": "Customer not found"}), 404

    df = df[df["id"] != customer_id]
    df.to_csv(DATA_FILE, index=False)
    return jsonify({"message": f"Customer {customer_id} deleted"})

@app.route("/customers", methods=["DELETE"])
@log_action("Delete all customers")
def delete_all_customers():
    pd.DataFrame(columns=["id", "name", "phone", "email", "address", "due_amount"]).to_csv(DATA_FILE, index=False)
    return jsonify({"message": "All customers deleted"})

@app.route("/customers/sorted", methods=["GET"])
@log_action("Sort customers by due amount")
def get_sorted_customers():
    df = pd.read_csv(DATA_FILE)
    df_sorted = df.sort_values(by="due_amount", ascending=True)
    return jsonify(df_sorted.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
