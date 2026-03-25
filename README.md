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