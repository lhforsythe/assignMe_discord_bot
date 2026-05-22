## Just a Discord bot that displays upcomming school assignments
<img width="859" height="195" alt="image" src="https://github.com/user-attachments/assets/634778ab-575e-4e94-93e3-dd2dfcf04eeb" />

### How to use it:
* Install the bot to your server at this link -> https://discord.com/oauth2/authorize?client_id=1496980757548236800
* Run the bot command `/set-token` in the server in which it was added to
* Supply your assignMe API key within the command
* Watch as the bot DMs you of any assignments that are due within a specified period of time (right now, this is one day, but I'll probably change it to be user-configurable.
### How it works:
It basically just uses the API I set up within my assignMe app to gather information on a certain user via their private API key. More specifically, after a user runs the bot command with their token, a tuple is created with their discord user-id and API key, which is then stored in a mySQL database. Then, the main python script periodically checks (~once a day) whether there are any assignments due (so, `due < 2` in API json) for any user, and if so, sends DMs to the appropriate user via their discord user-id.
