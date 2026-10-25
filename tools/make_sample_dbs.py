"""Write the sample Postgres databases used by the in-browser SQL runner.

Output: docs/assets/sql/shop.sql, events.sql, warehouse.sql
Deterministic (random.Random(42)), standard library only.
Run:  py tools/make_sample_dbs.py
"""
import random
from datetime import date, datetime, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets" / "sql"
rng = random.Random(42)

# province code -> (tax type, rate, [cities])
PROVINCES = {
    "ON": ("HST", 0.13, ["Toronto", "Ottawa", "Hamilton", "London", "Waterloo", "Kingston", "Sudbury"]),
    "QC": ("GST+QST", 0.14975, ["Montreal", "Quebec City", "Laval", "Gatineau"]),
    "BC": ("GST+PST", 0.12, ["Vancouver", "Victoria", "Kelowna", "Burnaby"]),
    "AB": ("GST", 0.05, ["Calgary", "Edmonton", "Red Deer"]),
    "MB": ("GST+PST", 0.12, ["Winnipeg", "Brandon"]),
    "SK": ("GST+PST", 0.11, ["Saskatoon", "Regina"]),
    "NS": ("HST", 0.15, ["Halifax", "Sydney"]),
    "NB": ("HST", 0.15, ["Moncton", "Fredericton"]),
    "NL": ("HST", 0.15, ["St. John's"]),
    "PE": ("HST", 0.15, ["Charlottetown"]),
}
PROV_WEIGHTS = {"ON": 38, "QC": 22, "BC": 14, "AB": 11, "MB": 4, "SK": 3, "NS": 3, "NB": 2, "NL": 2, "PE": 1}

FIRST = ["Aiden", "Amara", "Ben", "Chloe", "Daniel", "Elena", "Farid", "Grace", "Hassan", "Isabelle",
         "Jacob", "Kavya", "Liam", "Maya", "Noah", "Olivia", "Priya", "Quinn", "Ravi", "Sofia",
         "Tariq", "Uma", "Victor", "Wendy", "Xavier", "Yara", "Zoe", "Marc", "Sophie", "Jean",
         "Emily", "Ethan", "Fatima", "Gabriel", "Hannah", "Ivan", "Jasmine", "Kenji", "Lucas", "Nadia"]
LAST = ["Tremblay", "Roy", "Gagnon", "Smith", "Brown", "Singh", "Patel", "Chen", "Wong", "Nguyen",
        "MacDonald", "Campbell", "Wilson", "Khan", "Ahmed", "Lavoie", "Bouchard", "Fraser", "Murray", "Kim",
        "Lee", "Martin", "Clarke", "Hussain", "Sharma", "Gill", "Morin", "Cote", "Leblanc", "Scott"]


def q(v):
    """SQL literal."""
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, datetime):
        return "'" + v.strftime("%Y-%m-%d %H:%M:%S") + "'"
    if isinstance(v, date):
        return "'" + v.isoformat() + "'"
    return "'" + str(v).replace("'", "''") + "'"


def inserts(table, cols, rows, per=100):
    out = []
    for i in range(0, len(rows), per):
        chunk = rows[i:i + per]
        vals = ",\n".join("(" + ", ".join(q(v) for v in r) + ")" for r in chunk)
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n{vals};\n")
    return "\n".join(out)


def money(x):
    return f"{x:.2f}"


def pick_province():
    return rng.choices(list(PROV_WEIGHTS), weights=list(PROV_WEIGHTS.values()))[0]


def write(name, text):
    path = OUT / f"{name}.sql"
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"{path.name}: {len(text.encode()) / 1024:.0f} KB")


# ---------------------------------------------------------------- shop
def make_shop():
    tax_rows = [(p, t, r) for p, (t, r, _) in PROVINCES.items()]

    customers = []
    for cid in range(1, 201):
        prov = pick_province()
        city = rng.choice(PROVINCES[prov][2])
        fn, ln = rng.choice(FIRST), rng.choice(LAST)
        email = None if rng.random() < 0.12 else f"{fn}.{ln}{cid}@example.ca".lower()
        phone = None if rng.random() < 0.25 else f"{rng.choice([416, 647, 514, 604, 403, 613, 905, 780])}-555-{rng.randint(0, 9999):04d}"
        signed_up = date(2024, 6, 1) + timedelta(days=rng.randint(0, 600))
        customers.append((cid, fn, ln, email, phone, city, prov, signed_up))
    # 40 customers never order
    no_orders = set(rng.sample(range(1, 201), 40))

    catalog = {
        "Electronics": [("USB-C Cable 2m", 14.99), ("Wireless Mouse", 29.99), ("Mechanical Keyboard", 119.00),
                        ("Bluetooth Speaker", 59.95), ("27in Monitor", 329.00), ("Webcam 1080p", 64.50),
                        ("Noise-Cancelling Headphones", 249.99), ("Phone Charger 30W", 24.99),
                        ("Portable SSD 1TB", 139.00), ("Smart Plug", 17.49)],
        "Home": [("Cast Iron Skillet", 44.99), ("Wool Blanket", 79.00), ("LED Desk Lamp", 34.99),
                 ("French Press", 32.00), ("Maple Cutting Board", 38.50), ("Kettle 1.7L", 49.99),
                 ("Storage Bins (3 pack)", 27.99), ("Candle Set", 19.99)],
        "Outdoors": [("Rain Jacket", 139.00), ("Hiking Socks (2 pack)", 21.99), ("Camping Mug", 12.50),
                     ("Headlamp", 29.99), ("Trekking Poles", 89.00), ("Dry Bag 20L", 24.99),
                     ("Toque", 22.00), ("Insulated Bottle", 34.95)],
        "Books": [("Intro to Statistics", 69.99), ("Canadian Cookbook", 32.95), ("Python Crash Course", 44.99),
                  ("Atlas of Canada", 49.95), ("Personal Finance Basics", 24.99), ("Linear Algebra Notes", 54.00)],
        "Stationery": [("Notebook A5", 6.99), ("Gel Pens (10 pack)", 9.49), ("Sticky Notes", 4.99),
                       ("Desk Organizer", 18.99), ("Whiteboard 24x36", 36.00), ("Highlighters", 7.25)],
    }
    products = []
    pid = 0
    for cat, items in catalog.items():
        for name, price in items:
            pid += 1
            products.append((pid, name, cat, money(price), rng.randint(0, 250)))
    # 6 products are never ordered
    never = set(rng.sample(range(1, pid + 1), 6))
    orderable = [p for p in products if p[0] not in never]

    orders, items = [], []
    oid = oiid = 0
    start, end = datetime(2025, 1, 1), datetime(2026, 8, 31, 23, 59)
    span = int((end - start).total_seconds())
    buyers = [c for c in customers if c[0] not in no_orders]
    for _ in range(900):
        oid += 1
        c = rng.choice(buyers)
        ts = start + timedelta(seconds=rng.randint(0, span))
        age_days = (end - ts).days
        if age_days < 5:
            status = rng.choice(["pending", "paid", "shipped"])
        else:
            status = rng.choices(["delivered", "cancelled", "refunded", "shipped"], weights=[80, 8, 6, 6])[0]
        orders.append((oid, c[0], status, ts, c[6]))
        for p in rng.sample(orderable, rng.choices([1, 2, 3, 4], weights=[45, 30, 17, 8])[0]):
            oiid += 1
            items.append((oiid, oid, p[0], rng.choices([1, 2, 3, 5], weights=[70, 20, 7, 3])[0], p[3]))

    ddl = """-- Sample database "shop": a small Canadian online store.
-- Customers, products, orders and order items, plus tax rates by province.
DROP TABLE IF EXISTS order_items, orders, products, customers, tax_rates CASCADE;

CREATE TABLE tax_rates (
  province   char(2) PRIMARY KEY,
  tax_type   text NOT NULL,
  rate       numeric(6,5) NOT NULL
);

CREATE TABLE customers (
  customer_id integer PRIMARY KEY,
  first_name  text NOT NULL,
  last_name   text NOT NULL,
  email       text,
  phone       text,
  city        text NOT NULL,
  province    char(2) NOT NULL REFERENCES tax_rates (province),
  signed_up   date NOT NULL
);

CREATE TABLE products (
  product_id  integer PRIMARY KEY,
  name        text NOT NULL,
  category    text NOT NULL,
  price       numeric(10,2) NOT NULL CHECK (price >= 0),
  stock       integer NOT NULL
);

CREATE TABLE orders (
  order_id      integer PRIMARY KEY,
  customer_id   integer NOT NULL REFERENCES customers (customer_id),
  status        text NOT NULL CHECK (status IN ('pending','paid','shipped','delivered','cancelled','refunded')),
  created_at    timestamp NOT NULL,
  ship_province char(2) NOT NULL REFERENCES tax_rates (province)
);

CREATE TABLE order_items (
  order_item_id integer PRIMARY KEY,
  order_id      integer NOT NULL REFERENCES orders (order_id),
  product_id    integer NOT NULL REFERENCES products (product_id),
  quantity      integer NOT NULL CHECK (quantity > 0),
  unit_price    numeric(10,2) NOT NULL
);

"""
    body = "\n".join([
        inserts("tax_rates", ["province", "tax_type", "rate"], tax_rows),
        inserts("customers", ["customer_id", "first_name", "last_name", "email", "phone", "city", "province", "signed_up"], customers),
        inserts("products", ["product_id", "name", "category", "price", "stock"], products),
        inserts("orders", ["order_id", "customer_id", "status", "created_at", "ship_province"], orders),
        inserts("order_items", ["order_item_id", "order_id", "product_id", "quantity", "unit_price"], items, 200),
    ])
    write("shop", ddl + body)


# ---------------------------------------------------------------- events
def make_events():
    users, events = [], []
    start = date(2025, 1, 1)
    plans = ["free", "free", "free", "basic", "pro"]
    cap = datetime(2026, 9, 30, 23, 59, 59)
    for uid in range(1, 301):
        prov = pick_province()
        signup = start + timedelta(days=min(int(rng.expovariate(1 / 140)), 560))
        users.append((uid, signup, rng.choice(plans), "CA", prov))
        t0 = datetime(signup.year, signup.month, signup.day, rng.randint(7, 22), rng.randint(0, 59), rng.randint(0, 59))
        events.append((uid, "signup", t0))
        # active for a decaying number of weeks after signup
        weeks_active = min(int(rng.expovariate(1 / 4)), 30)
        for w in range(weeks_active + 1):
            if rng.random() < 0.35:
                continue
            for _ in range(rng.choice([1, 1, 2, 3])):
                ts = t0 + timedelta(days=7 * w + rng.randint(0, 6), hours=rng.randint(0, 10),
                                    minutes=rng.randint(0, 59), seconds=rng.randint(0, 59))
                events.append((uid, "page_view", ts))
                if rng.random() < 0.30:
                    ts2 = ts + timedelta(minutes=rng.randint(1, 20))
                    events.append((uid, "add_to_cart", ts2))
                    if rng.random() < 0.45:
                        events.append((uid, "purchase", ts2 + timedelta(minutes=rng.randint(1, 30))))
    events = [e for e in events if e[2] <= cap]
    events.sort(key=lambda e: (e[2], e[0]))
    ev_rows = [(i + 1, u, t, ts) for i, (u, t, ts) in enumerate(events)]

    ddl = """-- Sample database "events": product analytics for a small Canadian web app.
-- Good for window functions, cohorts, funnels and retention.
DROP TABLE IF EXISTS events, users CASCADE;

CREATE TABLE users (
  user_id     integer PRIMARY KEY,
  signup_date date NOT NULL,
  plan        text NOT NULL CHECK (plan IN ('free','basic','pro')),
  country     char(2) NOT NULL,
  province    char(2) NOT NULL
);

CREATE TABLE events (
  event_id    integer PRIMARY KEY,
  user_id     integer NOT NULL REFERENCES users (user_id),
  event_type  text NOT NULL CHECK (event_type IN ('signup','page_view','add_to_cart','purchase')),
  occurred_at timestamp NOT NULL
);
CREATE INDEX events_user_time ON events (user_id, occurred_at);

"""
    body = "\n".join([
        inserts("users", ["user_id", "signup_date", "plan", "country", "province"], users),
        inserts("events", ["event_id", "user_id", "event_type", "occurred_at"], ev_rows, 150),
    ])
    write("events", ddl + body)


# ---------------------------------------------------------------- warehouse
def make_warehouse():
    d0, d1 = date(2025, 1, 1), date(2026, 6, 30)
    dates = []
    d = d0
    while d <= d1:
        dates.append((int(d.strftime("%Y%m%d")), d, d.year, (d.month - 1) // 3 + 1, d.month,
                      d.strftime("%B"), d.strftime("%A"), d.weekday() >= 5))
        d += timedelta(days=1)

    cats = {
        "Electronics": [("Wireless Mouse", 29.99), ("Mechanical Keyboard", 119.00), ("27in Monitor", 329.00),
                        ("Webcam 1080p", 64.50), ("Portable SSD 1TB", 139.00)],
        "Home": [("Cast Iron Skillet", 44.99), ("Wool Blanket", 79.00), ("LED Desk Lamp", 34.99), ("Kettle 1.7L", 49.99)],
        "Outdoors": [("Rain Jacket", 139.00), ("Trekking Poles", 89.00), ("Toque", 22.00), ("Insulated Bottle", 34.95)],
        "Books": [("Python Crash Course", 44.99), ("Atlas of Canada", 49.95), ("Personal Finance Basics", 24.99)],
        "Stationery": [("Notebook A5", 6.99), ("Gel Pens (10 pack)", 9.49), ("Whiteboard 24x36", 36.00)],
    }
    products = []
    k = 0
    for cat, items in cats.items():
        for name, price in items:
            k += 1
            products.append((k, name, cat, "Own brand" if k % 3 == 0 else "Name brand", money(price)))

    store_defs = [("Toronto Eaton", "Toronto", "ON", "Mall"), ("Ottawa Rideau", "Ottawa", "ON", "Mall"),
                  ("Montreal Plateau", "Montreal", "QC", "Street"), ("Quebec Old Town", "Quebec City", "QC", "Street"),
                  ("Vancouver Robson", "Vancouver", "BC", "Street"), ("Calgary Chinook", "Calgary", "AB", "Mall"),
                  ("Edmonton West", "Edmonton", "AB", "Mall"), ("Halifax Waterfront", "Halifax", "NS", "Street"),
                  ("Winnipeg Portage", "Winnipeg", "MB", "Street"), ("Online", "Toronto", "ON", "Online")]
    stores = [(i + 1, *s) for i, s in enumerate(store_defs)]

    customers = []
    segs = ["Consumer", "Consumer", "Consumer", "Small business", "Student"]
    for cid in range(1, 151):
        prov = pick_province()
        customers.append((cid, rng.choice(FIRST) + " " + rng.choice(LAST), rng.choice(segs),
                          rng.choice(PROVINCES[prov][2]), prov))

    facts = []
    for sid in range(1, 1501):
        dt = rng.choice(dates)
        # weekdays outside Nov/Dec are sometimes re-rolled, so weekends and the holiday season are a bit busier
        if not dt[7] and dt[4] not in (11, 12) and rng.random() < 0.25:
            dt = rng.choice([x for x in dates if x[7] or x[4] in (11, 12)])
        p = rng.choice(products)
        st = rng.choice(stores)
        c = rng.choice(customers)
        qty = rng.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
        unit = float(p[4])
        disc = rng.choice([0, 0, 0, 0.05, 0.10, 0.20])
        net = round(qty * unit * (1 - disc), 2)
        facts.append((sid, dt[0], p[0], st[0], c[0], qty, money(unit), money(net)))

    ddl = """-- Sample database "warehouse": a star schema for sales analysis.
-- One fact table (fact_sales) surrounded by four dimension tables.
DROP TABLE IF EXISTS fact_sales, dim_date, dim_product, dim_store, dim_customer CASCADE;

CREATE TABLE dim_date (
  date_key     integer PRIMARY KEY,      -- yyyymmdd
  full_date    date NOT NULL,
  year         integer NOT NULL,
  quarter      integer NOT NULL,
  month        integer NOT NULL,
  month_name   text NOT NULL,
  day_name     text NOT NULL,
  is_weekend   boolean NOT NULL
);

CREATE TABLE dim_product (
  product_key  integer PRIMARY KEY,
  product_name text NOT NULL,
  category     text NOT NULL,
  brand_type   text NOT NULL,
  list_price   numeric(10,2) NOT NULL
);

CREATE TABLE dim_store (
  store_key    integer PRIMARY KEY,
  store_name   text NOT NULL,
  city         text NOT NULL,
  province     char(2) NOT NULL,
  store_type   text NOT NULL
);

CREATE TABLE dim_customer (
  customer_key integer PRIMARY KEY,
  full_name    text NOT NULL,
  segment      text NOT NULL,
  city         text NOT NULL,
  province     char(2) NOT NULL
);

CREATE TABLE fact_sales (
  sale_id      integer PRIMARY KEY,
  date_key     integer NOT NULL REFERENCES dim_date (date_key),
  product_key  integer NOT NULL REFERENCES dim_product (product_key),
  store_key    integer NOT NULL REFERENCES dim_store (store_key),
  customer_key integer NOT NULL REFERENCES dim_customer (customer_key),
  quantity     integer NOT NULL,
  unit_price   numeric(10,2) NOT NULL,   -- CAD, before discount and tax
  net_amount   numeric(10,2) NOT NULL    -- CAD, after discount, before tax
);

"""
    body = "\n".join([
        inserts("dim_date", ["date_key", "full_date", "year", "quarter", "month", "month_name", "day_name", "is_weekend"], dates, 200),
        inserts("dim_product", ["product_key", "product_name", "category", "brand_type", "list_price"], products),
        inserts("dim_store", ["store_key", "store_name", "city", "province", "store_type"], stores),
        inserts("dim_customer", ["customer_key", "full_name", "segment", "city", "province"], customers),
        inserts("fact_sales", ["sale_id", "date_key", "product_key", "store_key", "customer_key", "quantity", "unit_price", "net_amount"], facts, 200),
    ])
    write("warehouse", ddl + body)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    make_shop()
    make_events()
    make_warehouse()
