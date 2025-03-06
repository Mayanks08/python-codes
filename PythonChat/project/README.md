# Chatbot for Python Tutorials (Class 6-8)

## Overview
This is an AI-powered chatbot designed to provide Python tutorials and solve programming-related queries for students of classes 6 to 8. The chatbot is built with a **React** frontend and a **Node.js** backend, leveraging **Google API** to generate responses.

## Features
- Interactive chatbot interface for easy communication
- Python tutorials tailored for students from class 6 to 8
- Answers Python-related queries in real-time
- Engaging and easy-to-understand responses
- Responsive design for both desktop and mobile users

## Tech Stack
- **Frontend:** React.js
- **Backend:** Node.js (Express.js)
- **API Integration:** Google API
- **Styling:** Tailwind CSS (Optional)
- **Database:** MongoDB (Optional, for storing conversations and user interactions)

## Installation & Setup
### Prerequisites
Make sure you have the following installed:
- Node.js (latest version)
- npm or yarn
- MongoDB (if using a database)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/chatbot-python-tutorials.git
   cd chatbot-python-tutorials
   ```

2. Install dependencies for both frontend and backend:
   ```sh
   cd frontend
   npm install  # or yarn install
   ```
   ```sh
   cd ../backend
   npm install  # or yarn install
   ```

3. Configure environment variables:
   - Create a `.env` file in the backend folder and set up required credentials for Google API.
   
4. Start the development servers:
   ```sh
   cd frontend
   npm start  # Runs React frontend
   ```
   ```sh
   cd ../backend
   node server.js  # Runs Node.js backend
   ```

## Usage
- Open the chatbot in the browser.
- Ask Python-related questions or select tutorials.
- The chatbot will provide responses using the Google API.

## Future Improvements
- Support for more programming languages
- Voice-based interactions
- Personalized learning recommendations

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License.

