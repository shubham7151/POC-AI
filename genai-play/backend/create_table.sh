#!/bin/bash
# Script to create 'users' table in PostgreSQL database

DB_NAME="$1"
DB_USER="$2"
DB_PASSWORD="$3"
DB_HOST="${4:-localhost}"
DB_PORT="${5:-5432}"

export PGPASSWORD="$DB_PASSWORD"

# Drop tables if they exist
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "DROP TABLE IF EXISTS portfolio;"
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "DROP TABLE IF EXISTS users;"

psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "\
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10)
);"

# Insert users
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "\
INSERT INTO users (name, age, gender) VALUES
    ('Alice', 30, 'Female'),
    ('Bob', 25, 'Male');"

# Fetch user IDs
alice_id=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -t -c "SELECT id FROM users WHERE name='Alice';" | xargs)
bob_id=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -t -c "SELECT id FROM users WHERE name='Bob';" | xargs)

psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "\
CREATE TABLE IF NOT EXISTS portfolio (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    total_money NUMERIC,
    invested NUMERIC,
    isa_life_time NUMERIC,
    pension NUMERIC,
    cash_isa NUMERIC,
    stocks NUMERIC,
    GIA NUMERIC,
    balance NUMERIC
);"

# Insert portfolio records using fetched user IDs
if [ -n "$alice_id" ]; then
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "\
INSERT INTO portfolio (user_id, total_money, invested, isa_life_time, pension, cash_isa, stocks, GIA, balance) VALUES
    ($alice_id, 10000, 5000, 0, 1500, 8500, 0, 0, 5000)
;"
fi
if [ -n "$bob_id" ]; then
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "\
INSERT INTO portfolio (user_id, total_money, invested, isa_life_time, pension, cash_isa, stocks, GIA, balance) VALUES
    ($bob_id, 15000, 7000, 0, 2000, 2000, 500, 2500, 8000)
;"
fi

# Drop resources table if it exists
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "DROP TABLE IF EXISTS resources;"

# Create resources table
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "\
CREATE TABLE IF NOT EXISTS resources (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    available_content JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

# Define JSON content (unchanged)
building_portfolio='[
  {
    "title": "How to build an investment portfolio",
    "description": "In our penultimate chapter of '\''Investing for beginners'\'', Dan Coatsworth breaks down how you might construct an investment portfolio",
    "content": null,
    "type": "video",
    "link": "https://www.ajbell.co.uk/investment/videos/how-build-investment-portfolio"
  },
  {
    "title": "How to build an investment portfolio",
    "description": "On this episode we are going back to basics on investing. Lots of women say they don'\''t how to invest, there'\''s too much jargon or they are embarrassed to ask questions – but we'\''re aiming to solve that...",
    "content": null,
    "type": "podcast",
    "link": "https://www.ajbellmoneymatters.co.uk/podcasts/how-build-investment-portfolio"
  },
  {
    "title": "How to invest for income",
    "description": "Income investing isn'\''t just for retired savers – younger investors could also use as part of a balanced return strategy. Learn more about investing for income.",
    "content": "Investing for income in the UK is often seen as the preserve of retired savers...",
    "type": "article",
    "link": "https://www.ajbell.co.uk/learn/income-investing"
  }
]'

isas='[
  {
    "title": "What is a Cash ISA?",
    "description": "The Cash ISA is a type of individual savings account with tax-free interest and withdrawals.",
    "content": "A Cash ISA is a UK savings account offering tax-free interest...",
    "type": "article",
    "link": "https://www.ajbell.co.uk/isa/what-is-cash-isa"
  },
  {
    "title": "Which ISA is best?",
    "description": "Stocks and shares, Lifetime, Junior, Cash – the list goes on but what is the best ISA?",
    "content": "Individual Savings Accounts (ISAs) have helped millions save and invest...",
    "type": "article",
    "link": "https://www.ajbell.co.uk/isa/which-isa-is-best"
  }
]'

# Escape and compact using jq
building_json=$(echo "$building_portfolio" | jq -c .)
isas_json=$(echo "$isas" | jq -c .)

# Insert using heredoc to support variable substitution
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" \
  --set=building="$building_json" \
  --set=isas="$isas_json" <<EOF
INSERT INTO resources (category, available_content) VALUES
    ('Building your portfolio', :'building'::jsonb),
    ('ISAs', :'isas'::jsonb);
EOF