# YouTV
 [Video Demo](https://youtu.be/G9ITSwskh94) for a live demonstration of the application.
 </br>
YouTV is a YouTube clone where users can upload videos, subscribe to each other, like and dislike videos, post comments, search for videos, and change their profile picture. All pages are mobile responsive.

## Description
YouTV stands out due to its modern and mobile-responsive design. It manages files and posts them to different directories in the Django project. Users can customize their profiles by changing their profile pictures and uploading videos, fostering a strong community around their uploads.

Key features include:
- A modern, responsive UI inspired by YouTube Dark Theme with a custom logo and color scheme.
- Description hide and show feature.
- Like and dislike functionality with mutual exclusivity.
- Custom CSS with minimal reliance on Bootstrap.
- Separate JavaScript files for better visibility and page-specific inclusion.
- Secure data validation using Django models.

## Files and Directories
- `app` - Main application directory
    - `static` - Contains all static content
        - `icon.svg` - Main icon for the website
        - `comment.js` - Script to post comments to the server
        - `expand-description.js` - Script to expand and hide video descriptions
        - `get-cookie.js` - Script to get the session cookie for forms
        - `like.js` - Script for liking and disliking videos without page refresh
        - `profile-redirect.js` - Script to link profile pictures and usernames to user profiles
        - `recommended-vid-redirect.js` - Script to link recommended videos to their watch page
        - `search.js` - Script to search for videos
        - `subscribe.js` - Script for subscribing and unsubscribing to users
        - `vid-redirect.js` - Script to redirect home page videos to their watch page
        - `style.css` - Main CSS file for styling
    - `templates` - Contains all HTML templates
        - `change.html` - Page for changing avatar
        - `error.html` - Page for displaying errors
        - `index.html` - Home page
        - `layout.html` - Main layout for all pages
        - `login.html` - Login form
        - `profile.html` - Page for displaying user profiles
        - `register.html` - Registration form
        - `search.html` - Page for searching videos
        - `subscribed.html` - Page for videos from subscribed users
        - `upload.html` - Form for uploading videos
        - `watch.html` - Page for viewing videos
    - `forms.py` - Contains all Django forms for the application
    - `models.py` - Contains all models for the application (User, Video, Comment, Like, Dislike, Subscription)
    - `signals.py` - Contains signal for pre-deleting videos to remove the video file from the application folder
    - `urls.py` - Contains all URLs for the application
    - `views.py` - Contains all views for the application
- `youtv` - Project directory
    - `settings.py` - Modified to include the MEDIA_URL for uploading videos and avatars
- `media` - Media directory
    - `avatars` - Location of all user avatars, with 'default-avatar.png' as the default avatar
    - `videos` - Location of all user videos
    - `videos/thumbnails` - Location of all thumbnails for all videos

## Updates

- Implemented video compression to reduce file size.
- Added automatic thumbnail generation for uploaded videos.


## Setup

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


## Licence
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 
