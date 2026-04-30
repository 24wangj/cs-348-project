# Database Design

## Competition
- `id` (Primary Key)
- `name`
- `city`
- `state`
- `date`

## Competitor
- `id` (Primary Key)
- `name`
- `city`
- `state`

## Result
- `competition_id` (Primary Key, Foreign Key -> `Competition.id`)
- `competitor_id` (Primary Key, Foreign Key -> `Competitor.id`)
- `time`

# SQL Injection Protection
- SQLAlchemy ORM prevents SQL injection by separating the query from its parameters into prepared statements

# Indexes

## (Result.competition_id, Result.time)
- Speeds up filtering by competition
- Speeds up filtering by cutoff time

## Result.competitor_id
- Speeds up deletion of competitor's times

# Transactions and Isolation

- Atomicity is guaranteed by committing to the database only at the end of each transaction
- Designed for a single user
- If multi-user, use a READ COMMITTED isolation level to prevent dirty reads or serializable to address concurrent updates

# AI Usage

- Used Copilot
- Assisted with frontend component styling
- Verified output by ensuring that it maintained the structure of the html file. Modified frontend to interact with backend