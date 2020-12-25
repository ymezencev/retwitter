# Technical requirement 

### Technologies:
    backend: Django-rest-framework API
    frontend: Vue.js

### PAGES
1) Registration/authorization
2) Home page
    - create tweet
    - see feed

3) Profile
    - see all my posts
    - profile description
    - edit header, avatar, main info (name, bio, location, site)

4) Settings
    - edit profile information
    - edit password

5) Bookmarks
    - see all posts added to bookmarks list

6) Notification
    - see main info about user actions

7) Messages
    - chat with users

---------
- Tweet
    - text, image, time_created, user_created
    - smiles should be available in tweets
    Actions:
        - like/dislike
        - add to bookmarks
        - retweet
        - comment
            - reply to comment
            - like/dislike
            - time_created
        - search tweets

- User 
    - name (any), username (unique)
    - login/logout
    - account information (phone, email, is_verified, date_created, country, gender, birth date, age)
    - profile information (header img, avatar img, bio description, site, location, following, followers)

    Actions:
        - follow/unfollow
        - see other users tweets
        - see all my tweets
        - see all my replies
        - see all my likes
        - see all my media

### Add script to create first 20 users with tweets like real people




