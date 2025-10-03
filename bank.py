import os
import sqlite3
from flask import Blueprint, request, jsonify

# Allow tests to override the DB path via environment variable
DB_PATH = os.environ.get("TEST_BANK_DB") or os.path.join(os.path.dirname(__file__), "banking.db")

def init_bank_db():
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bank (
                username TEXT PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                last_gain INTEGER DEFAULT 0,
                last_loss INTEGER DEFAULT 0,
                total_gained INTEGER DEFAULT 0,
                total_lost INTEGER DEFAULT 0
            )
        """)
init_bank_db()

def get_user_bank(username):
    with sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10) as conn:
        row = conn.execute("SELECT * FROM bank WHERE username=?", (username,)).fetchone()
        if row:
            keys = ["username", "balance", "last_gain", "last_loss", "total_gained", "total_lost"]
            return dict(zip(keys, row))
        else:
            conn.execute("INSERT INTO bank (username) VALUES (?)", (username,))
            # Fetch the newly created user in the same connection
            row = conn.execute("SELECT * FROM bank WHERE username=?", (username,)).fetchone()
            keys = ["username", "balance", "last_gain", "last_loss", "total_gained", "total_lost"]
            return dict(zip(keys, row))

def update_bank(username, amount):
    user = get_user_bank(username)
    gain = loss = 0
    if amount > 0:
        gain = amount
    elif amount < 0:
        loss = -amount
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            UPDATE bank
            SET balance = balance + ?,
                last_gain = ?,
                last_loss = ?,
                total_gained = total_gained + ?,
                total_lost = total_lost + ?
            WHERE username = ?
        """, (amount, gain, loss, gain, loss, username))
    return get_user_bank(username)

bank_bp = Blueprint("bank", __name__, url_prefix="/api/bank")

@bank_bp.route("/<username>", methods=["GET"])
def bank_status(username):
    return jsonify(get_user_bank(username))

@bank_bp.route("/<username>/add", methods=["POST"])
def bank_add(username):
    data = request.get_json(force=True)
    amount = int(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    user = update_bank(username, amount)
    return jsonify(user)

@bank_bp.route("/<username>/remove", methods=["POST"])
def bank_remove(username):
    data = request.get_json(force=True)
    amount = int(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    user = get_user_bank(username)
    if user["balance"] < amount:
        return jsonify({"error": "Insufficient funds"}), 400
    user = update_bank(username, -amount)
    return jsonify(user)


def list_all_banks():
    """Return a list of all users in the bank as dicts."""
    with sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10) as conn:
        rows = conn.execute("SELECT username, balance, last_gain, last_loss, total_gained, total_lost FROM bank ORDER BY username").fetchall()
        keys = ["username", "balance", "last_gain", "last_loss", "total_gained", "total_lost"]
        return [dict(zip(keys, row)) for row in rows]


@bank_bp.route("/all", methods=["GET"])
def bank_list_all():
    """API endpoint that returns all bank users."""
    return jsonify(list_all_banks())