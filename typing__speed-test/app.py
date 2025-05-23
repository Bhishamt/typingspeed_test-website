from flask import Flask, jsonify, render_template, request
import json
import sqlite3
import os

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('typing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                 (user_id TEXT, wpm INTEGER, accuracy INTEGER, errors INTEGER, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS quotes
                 (quote TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Load initial quotes
quotes_file = 'quotes.json'
if not os.path.exists(quotes_file):
    with open(quotes_file, 'w') as f:
        json.dump([
            "The quick brown fox jumps over the lazy dog.",
            "Life is what happens when you're busy making other plans.",
            "To be or not to be, that is the question.",
            "All that glitters is not gold.",
            "The only way to do great work is to love what you do.",
            "Success is not final, failure is not fatal.",
            "The journey of a thousand miles begins with a single step.",
            "Be the change you wish to see in the world.",
            "Stay hungry, stay foolish.",
            "Dream big, work hard, stay focused.",
            "The future belongs to those who believe in their dreams.",
            "Do not wait to strike till the iron is hot; but make it hot by striking.",
            "It does not matter how slowly you go as long as you do not stop.",
            "You miss 100% of the shots you don’t take.",
            "The only limit to our realization of tomorrow will be our doubts of today.",
            "What you get by achieving your goals is not as important as what you become by achieving your goals.",
            "The best way to predict the future is to create it.",
            "Life is 10% what happens to you and 90% how you react to it.",
            "The only way to do great work is to love what you do.",
            "You are never too old to set another goal or to dream a new dream.",
            "The greatest glory in living lies not in never falling, but in rising every time we fall.",
            "The way to get started is to quit talking and begin doing.",
            "Your time is limited, so don’t waste it living someone else’s life.",
            "If life were predictable it would cease to be life, and be without flavor.",
            "If you look at what you have in life, you’ll always have more.",
            "If you set your goals ridiculously high and it’s a failure, you will fail above everyone else’s success.",
            "Life is what we make it, always has been, always will be.",
            "The only impossible journey is the one you never begin.",
            "In the end, it’s not the years in your life that count. It’s the life in your years.",
            "You only live once, but if you do it right, once is enough.",
            "Many of life’s failures are people who did not realize how close they were to success when they gave up.",
            "If you want to live a happy life, tie it to a goal, not to people or things.",
            "Never let the fear of striking out keep you from playing the game.",
            "Money and success don’t change people; they merely amplify what is already there.",
            "Your time is limited, don’t waste it living someone else’s life.",
            "Not how long, but how well you have lived is the main thing.",
            "If life were predictable it would cease to be life, and be without flavor.",
            "The whole secret of a successful life is to find out what is one’s destiny to do, and then do it.",
            "In order to write about life first you must live it.",
            "The big lesson in life is never be scared of anyone or anything.",
            "Sing like no one’s listening, love like you’ve never been hurt, dance like nobody’s watching.",
            "Curiosity about life in all of its aspects, I think, is still the secret of great creative people.",
            "Life is not a problem to be solved, but a reality to be experienced.",
            "The unexamined life is not worth living.",
            "Turn your wounds into wisdom.",
            "The way I see it, if you want the rainbow, you gotta put up with the rain.",
            "Do all the good you can, for all the people you can, in all the ways you can, as long as you can.",
            "Don’t settle for what life gives you; make life better and build something.",
            "Everything negative – pressure, challenges – is all an opportunity for me to rise.",
            "I like criticism. It makes you strong.",
            "You never really learn much from hearing yourself speak."
        ], f)

with open(quotes_file, 'r') as f:
    quotes = json.load(f)

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    return render_template('index.html', lang=lang)

@app.route('/quotes')
def get_quotes():
    conn = sqlite3.connect('typing.db')
    c = conn.cursor()
    c.execute('SELECT quote FROM quotes')
    db_quotes = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify(quotes + db_quotes)

@app.route('/save_stats', methods=['POST'])
def save_stats():
    data = request.json
    conn = sqlite3.connect('typing.db')
    c = conn.cursor()
    c.execute('INSERT INTO stats (user_id, wpm, accuracy, errors, timestamp) VALUES (?, ?, ?, ?, ?)',
              (data['user_id'], data['wpm'], data['accuracy'], data['errors'], data['timestamp']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/add_quote', methods=['POST'])
def add_quote():
    data = request.json
    quote = data['quote']
    conn = sqlite3.connect('typing.db')
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote) VALUES (?)', (quote,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)