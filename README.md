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

# Indexes

## (Result.competition_id, Result.time)
- Speeds up filtering by competition
- Speeds up filtering by cutoff time

## Result.competitor_id
- Speeds up deletion of competitor's times