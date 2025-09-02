# 📝 WordPress Publishing Agent

 An AI-powered publishing agent that automatically posts Markdown content to your WordPress blog via the REST API. 

## ✨ Features
```
 ✔ Publish Markdown blog posts to WordPress
 ✔ Add SEO metadata (title, tags, status)
 ✔ Works with WordPress Application Passwords
 ✔ Returns the live post URL after publishing
 ✔ Simple fallback when publishing fails
```
## 🗂️ Folder Structure
```
research-blog-agent/
├─ main.py 
├─ agents/
│ ├─ __init__.py
│ ├─ researcher.py 
│ ├─ writer.py 
│ ├─ seo.py 
│ └─ publisher.py 
├─ utils/
│ ├─ __init__.py
│ └─ io.py 
├─ requirements.txt
├─ .env.example
└─ README.md
```

## 📦 Installation
```
 Clone the repo and install dependencies:
 git clone https://github.com/your-username/wordpress-publishing-agent.git
 cd wordpress-publishing-agent
 pip install -r requirements.txt
```
## ⚙️ Setup

 Enable REST API
 WordPress REST API is available by default at:

 https://your-blog.com/wp-json/wp/v2/


### Generate Application Password
```
 Go to WordPress Dashboard → Users → Profile → Application Passwords
 Create a new password (e.g., Agent-Token)
 Save username and the application password
 Environment Variables
```
### Create a .env file in the project root:
```
 GOOGLE_API_KEY="Enter your Google API key here"
 WORDPRESS_BASE_URL=https://your-blog.com/wp-json/wp/v2
 WORDPRESS_USERNAME=your_username
 WORDPRESS_APP_PASSWORD=your_generated_app_password
 WORDPRESS_PUBLISH_STATUS=publish   # or 'draft'
```
### 🚀 Usage

### Example:
```
python main.py "Enter the name of your Research here" --save

```

### Output:

{'published_url': 'https://your-blog.com/2025/08/28/hello-world/'}


## 🛡 License

This project is licensed under the MIT License.
