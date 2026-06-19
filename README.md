# Full-Stack Social Network Single-Page Application

A dynamic, single-page social networking platform engineered with a robust asynchronous frontend and a custom backend data API. The application supports user interactions, real-time profile updates, and network connections without any full-page reloads.

## 📺 Live Video Demonstration

[![Watch the Social Network Demo](https://img.youtube.com/vi/h07DAETR0UQ/0.jpg)](https://youtu.be/h07DAETR0UQ)

*Click the image thumbnail above to watch the unlisted video walkthrough demonstrating the asynchronous post feed, live liking mechanisms, dynamic follow system, and direct inline editing.*

## 🚀 Key Features Implemented
- **Asynchronous Global Feed:** Features an interactive social timeline where users can publish text posts that render instantly to the feed without a page refresh.
- **Dynamic Follow Engine:** Interactive user profile cards displaying real-time follower/following counts with toggle buttons that update connection states asynchronously via background API requests.
- **Customized Sub-Feeds:** A dedicated "Following" dashboard that filters and serves a personalized stream of content containing only posts from a user's direct connections.
- **Client-Side Pagination:** Implements a sleek, database-friendly pagination mechanic to cleanly divide long timelines into 10-post views with fluid navigation.
- **Inline Post Editing:** Empowers authors to instantly swap post content text into a pre-populated textarea box, saving updates directly to the database via `PUT` requests without disrupting the UI layout.
- **Asynchronous Like/Unlike System:** Toggleable heart buttons that communicate instantly with backend server models, dynamically incrementing or decrementing counts on the fly.

## 🛠️ Technical Stack
- **Frontend Core:** JavaScript (Vanilla asynchronous UI architecture), HTML5, CSS3, Bootstrap
- **Backend Architecture:** Python, Django
- **Database:** SQLite
