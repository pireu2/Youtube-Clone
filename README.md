# CS50W Final Project
 [Video Demo](https://youtu.be/G9ITSwskh94)
 </br>
This is my final project for CS50’s Web Programming with Python and JavaScript. </br>
My final project is a youtube clone where users cand upload videos, subscribe to eachother, like and dislike videos, post comments, search for videos and change their profile picture. </br>
All my pages are mobile responsive. </br>

# Distinctiveness and Complexity
My project is different from all the other projects in this course, because I put a lot of effort in making the website look modern and mobile responsive, also my project is the only one to manage files and to post the to different directories in the django project.</br>
Another unique thing about my project is the customization that each user has. Every user can change their profile picture and upload any videos they want. In his way, they can build a strong community around their uploads. </br>
A major part of my project developement was put in the responsivity of the website and the ui design. I chose to inspire myself from the Youtube Dark Theme but I made my own logo and color scheme. For the reactive part, I implemented a very cool description hide and show feature that looks very good. Also, I added features like you can like and dislike the same video, if you like a video and then press dislike, the like gets remove. </br>
Another important point about my project was the usage of custom css. In my project I used a few bootstrap components like the navbar and some input groups and buttons, but i added my own css on top of that to achieve my design and everything else uses my own css for every component. </br>
I chose to make separete javascript files for every script I made for better visibility and to only include the scripts I need for every page. </br>
For almost any Model I used I tried to use the built-it django models for using their good validation of the data, but when that wasn't possible with the comments especially I put a lot of effort in making everything secure for the users of the application. </br>

# Files and Directories
- `app` - main application directiory
    - `static` - contains all static content
        - `icon.svg` - main icon for the website
        - `comment.js` - js script to post comments to the server
        - `expand-description.js` - js script to expand and hide description of a video
        - `get-cookie.js` - js script to get the cookie of the current session to use in the forms for the server
        - `like.js` - js script for liking and dislinking videos without refreshin the page
        - `profile-redirect.js` - js script to link all profile pictures and usernames to a user's profile
        - `recommended-vid-redirect.js` - js script to link all recommended videos to their watch page
        - `search.js` - js script to search for videos 
        - `subscribe.js` - js script for subscribing and unsubscribing to users 
        - `vid-redirect.js` - js script to redirect home page videos to their wath page
        - `style.css` - main css file used for styling
    - `templates` - contains all html templates
        - `change.html` - page for changing avatar
        - `error.html` - page for displaying errors
        - `index.html` - home page
        - `layout.html` - main layout for all pages
        - `login.html` - login form
        - `profile.html` - page for displaying user profiles
        - `register.html` - register form
        - `search.html` - page for searching videos
        - `subscribed.html` - page for all videos from users you subscribed to
        - `upload.html` - form for uploading vidoes
        - `watch.html` - page for viewing videos
    - `forms.py` - contains all django forms for the application
    - `models.py` - contains all forms for the application(user, video, comment, like, dislike, subscription)
    - `signals.py` - contains signal for pre deleting videos to remove the video from the application folder as well
    - `urls.py` - contains all urls for the application
    - `views.py` - contains all views for the application
- `youtv` - project directory
    - `settings.py` - modified to include the MEDIA_URL for the models to upload the videos and avatars
- `media` - media directory
    - `avatars` - location of all user avatars, 'default-avatar.png' is the default avatar when creating a account
    - `videos` - location of all user videos


# Setup

```shell script
git clone https://github.com/pireu2/Youtube-Clone.git
pip install -r requirements.txt
```

Run those following commands to migrate database.

```shell script
python manage.py makemigrations
python manage.py migrate
```

When the dependent packages are installed, you can run this command to run your server.
```shell script
python manage.py runserver
```

### Special thanks for the CS50W team for making this amazing course possible.
