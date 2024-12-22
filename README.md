# Script News for Discord Scraper

## Create a Webhook in Discord

A Webhook is a URL that you can use to send messages to a Discord channel. To create a Webhook, follow these steps:

1. Go to your Discord server.
2. Right-click on the text channel where you want the messages to be posted.
3. Click on "Channel Settings" (gear icon).
4. In the left menu, select "Integrations".
5. Then, select "Webhooks".
6. Click the "Create Webhook" button.
7. Configure the Webhook:
   - Give it a name.
   - Make sure to select the correct channel where the messages will be posted.
   - Copy the Webhook URL, which will be something like `https://discord.com/api/webhooks/ID/TOKEN`.
8. Click Save.

## Create the table in `Supabase`

1. Go to the Supabase dashboard.
2. Open the project.
3. Go to the SQL Editor section and run a query to create the table. Use the following SQL:

```sql
CREATE TABLE IF NOT EXISTS scraped_data (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL
);
```

> This will create the `scraped_data` table with an `id` column as the primary key and a `url` column, unique, to store the URLs.
