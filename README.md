# Socilal Network API
This is an introduction to my social network API implementation. It was written using Django REST framework, and provides some basic social network functionality.

### Models
There are two main models, __User__ and __Post__, representing network users and posts respectively. User is a simple Django `AbstractUser` model, and Post is custom, however yet pretty simple. It only contains _text_ and refers to it's _author_. Also, posts can be liked and unliked, for what another model __Like__ was made. It contains referenses to both User that made this like and Post that was liked.

### User authentication
For this purpose, a JWT token is used. This is a `SlidingToken` provided by __rest_framework_simplejwt__. It is being returned after user login, and expires after 10 minutes of user inactivity on the website. To get a new token, user has to log in again.

### Endpoints
There is a number of endpoints allowing to interact with the network. Let's see what they are and what you can do with them.

Note: all of them are prefixed with `api/v1/`

##### Signup/Login

__url:__ `signup/`

| method | body | return value |
|---|---|---|
| post | {"username":"yourusername", "password":"yourpassword"} | serialized data with created user representation

__url:__ `login/`

| method | body | return value |
|---|---|---|
| post | {"username":"yourusername", "password":"yourpassword"} | jwt token for further authorization

Note: those are the only two endpoints that don't require authorization. __For all of the following endpoints, you need to include__ `Authorization: Bearer [your_jwt_token]` __to request headers__.

##### Users

__url:__ `users/`

| method | body | return value |
|---|---|---|
| get | - | all existing users representation

##### User activity

__url:__ `users/<user_id>/activity/`

| method | body | return value |
|---|---|---|
| get | - | date and time of when user was last logged in and made his last request to the service

##### Posts

__url:__ `posts/`

| method | body | return value |
|---|---|---|
| get | - | all existing posts representation
| post | {"text":"textofyourpost"} | representation of newly created post |

__url:__ `users/<user_id>/posts/`

| method | body | return value |
|---|---|---|
| get | - | representation of posts, aggregated by user

##### Like/Unlike

__url:__ `posts/<post_id>/like`

| method | body | return value |
|---|---|---|
| post | - | representation of post with updated likes count

__url:__ `posts/<post_id>/unlike`

| method | body | return value |
|---|---|---|
| post | - | representation of post with updated likes count

Note: if a user tries to like the same post twice, or unlike the post that he haven't liked, nothing happens.

##### Like analytics

__url:__ `analytics/`

| method | body | optional parameters | return value |
|---|---|---|---|
| get | - | date_from=dd-mm-yyyy, date_to=dd-mm-yyyy | analytics of likes aggregated by date range

### Automation bot

The last thing to introuce is an automation bot. It's a python script that takes a config file at the following format:
```
number_of_users max_posts_per_user max_likes_per_user
```
and does the following:
* signs up `number_of_users` new users with random usernames and passwords
* for each newly created user, creates some number of posts (from one up to `max_posts_per_user`)
* after that, from each user likes random amount (from one up to `max_likes_per_user`) of randomly picked posts

It's placed at __network_app/bot.py__ and should be runned as regular python script. To configure it, you can whether edit the __config.txt__ file (placed at the same directory), or create your own file and pass a path to it as a command-line argument. Another optional argument that you might want to use is `-v` flag (or `--verbose`), that enables logging of bot actions to console.

That's it, now you can go ahead and test this API yourself.