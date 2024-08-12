CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

INSERT INTO stocks (symbol, price, quantity)
VALUES
	('IREDA', 238.90, 1000),
	('IRFC', 182.90, 1000),
	('ITC', 495.05, 1000)
	on conflict (symbol) do nothing;

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL REFERENCES users(username),
    stock_symbol VARCHAR(10) NOT NULL REFERENCES stocks(symbol),
    quantity INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_type VARCHAR(4) NOT NULL CHECK (transaction_type IN ('BUY', 'SELL'))
);

CREATE TABLE IF NOT EXISTS stock_price_history (
    id SERIAL PRIMARY KEY,
    stock_symbol VARCHAR(10) NOT NULL REFERENCES stocks(symbol),
    price DECIMAL(10, 2) NOT NULL,
    year INT NOT NULL
);
