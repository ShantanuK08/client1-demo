import sqlite3

# Connect to the database (or create it if it doesn't exist)
con = sqlite3.connect('example.db')

# Create a cursor object
cur = con.cursor()

# Create a table
cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Insert data into the table
cur.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
cur.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")

# Commit the transaction
con.commit()

# Query the database
cur.execute("SELECT * FROM users")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the connection
con.close()