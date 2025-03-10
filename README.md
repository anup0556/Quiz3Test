# Quiz API Documentation

## Setup
1. Configure database in settings.py
2. Run migrations: `python manage.py migrate`
3. Start server: `python manage.py runserver`

## API Endpoints
1. GET /api/leaderboard/
   - Returns top 10 performers
   - Supports large datasets (30k+ users)
   - Cached for performance
   
## Database Configuration
- Supports any SQL database (PostgreSQL, MySQL, etc.)
- Includes database indexes for performance
- Optimized for large datasets