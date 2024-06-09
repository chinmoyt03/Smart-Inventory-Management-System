from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import spacy
from word2number import w2n

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'           # MySQL username
app.config['MYSQL_PASSWORD'] = '1122'       # MySQL password
app.config['MYSQL_DB'] = 'shopping_list'

mysql = MySQL(app)

# Load Spacy model
nlp = spacy.load('en_core_web_sm')

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    text = data['text']

    # Process text using Spacy NLP
    doc = nlp(text)

    # Extract relevant information from the text
    action = None
    item = None
    quantity = None

    for token in doc:
        if token.text.lower() == 'add':
            action = 'add'
        elif token.text.lower() == 'update':
            action = 'update'
        elif token.dep_ == 'dobj':
            item = token.text.lower()
        elif token.dep_ == 'pobj' and token.head.text.lower() == 'to':
            quantity = w2n.word_to_num(token.text)

    # Store or update the shopping list in the database
    if action == 'add':
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO shopping_items (item, quantity) VALUES (%s, %s)", (item, quantity))
        mysql.connection.commit()
        cur.close()
    elif action == 'update':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE shopping_items SET quantity = %s WHERE item = %s", (quantity, item))
        mysql.connection.commit()
        cur.close()

    return jsonify({'message': 'Successfull'})

@app.route('/get_shopping_list', methods=['GET'])
def get_shopping_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT item, quantity FROM shopping_items")
    items = cur.fetchall()
    cur.close()

    shopping_list = [{'item': item, 'quantity': quantity} for item, quantity in items]
    return jsonify(shopping_list)

if __name__ == '__main__':
    app.run(debug=True)
