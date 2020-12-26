
### Пользователь
auth.User
- id
- username
- first_name
- last_name
- email
- password
- is_superuser
- is_active
- is_staff
- date_joined
- last_login

### Профиль пользователя
Profile
- id
- name
- user_id FK
- avatar
- header
- description
- phone_number
- date_of_birth
- gender
- country_id FK
- location
- site

### Контакты пользователя
Follower
- user_from_id FK User
- user_to_id FK User
- created_at

---------------------
### Действия пользоваеля
Action
- user_id FK
- action_type_id FK
- created_at
- target_id FK
- tatget_ct_id FK (ContentType)

### Типы действий пользователя
ActionType
    id
    verb
---------------------

### Твиты
Tweet
- id
- user_id FK
- image
- text
- created_at    
- total_likes
- total_comments

### Данные по просмотру твитов пользователем
TweetViewer
- user_id FK
- tweet_id FK
- is_liked
- is_in_bookmarks

### Комментарий
Comment
- id
- tweet_id FK
- user_id FK
- text
- created_at
- parent_id FK

---------------------
### Чаты пользователей
Chat
- id
- created_at

### Пользователи в чатах
UserChat
- chat_id FK
- user_id FK

### Сообщения пользователей
ChatMessage
- id
- text
- chat_id FK
- user_id FK
- created_at    


## Методы:
### Accounts app
- Registration, Login, Change password
- Get, Edit main profile settings (avatar, header, description, location, site)
- Get, Edit account settings (all other profile data)

- Follow/Unfollow user
- Get all followers
- Get who follows user


### Tweets
- Get feed
- Get user's tweets for profile page
- Get posts that the user liked
- Get user's media
- Get tweets where the user replied
