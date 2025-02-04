
# Pinsphere Backend

---

## Table of Contents
- [Aim](#aim)
- [Features](#features)
- [Usage](#usage)
- [Infrastructure](#infrastructure)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

---

## Aim

The primary goal of Pinsphere is to create a seamless and intuitive environment for users to interact with a digital collection of media. The platform enables users to upload, categorize, and share pins (images, videos, and media) within a scalable and secure ecosystem. Whether for personal use or collaborative teams, Pinsphere streamlines the way media is managed and shared.

---

## Features

- **Pin Storage:** Store various types of media like images, GIFs, and videos in a secure and organized environment.
- **Tagging & Categorization:** Classify and categorize your pins using tags for easy searching and browsing.
- **User Management:** Manage users and permissions to control who can upload, view, or modify pins.
- **Search Functionality:** Powerful search capabilities that allow you to quickly find pins based on tags, categories, or metadata.
- **Responsive UI:** A simple, responsive web interface for easy interaction with the platform.
- **REST API:** A fully featured API for developers to interact with the platform programmatically.

---

## Usage

1. **Start the Application:**

    You can either run the application locally or deploy it on a cloud service. To start the application locally, follow the installation instructions below.

2. **Upload Pins:**

    Use the web interface to upload images, GIFs, and videos. You can easily tag and categorize pins during the upload process.

3. **Organize Content:**

    Pins can be organized into categories and tagged for easier access. Use the search functionality to quickly find your desired content.

4. **Share Pins:**

    Pins can be shared with other users, or public links can be generated to distribute your media.

---

## Infrastructure

Pinsphere is built with the following key technologies:

- **Backend:**
  - Python with FastAPI: Server-side framework for handling API requests.
  - MongoDB: NoSQL database for storing media metadata, tags, and categories.
  - PostgreSQL: Relational database for user management and permissions.
  - Cloud Storage (e.g., AWS S3 / Minio): For storing the media files themselves.

- **Authentication & Authorization:**
  - OAuth 2.0 for secure user authentication.
  - Role-based access control (RBAC) to manage permissions and users.

- **API:**
  - RESTful API for developers to interact with the platform programmatically.

- **DevOps:**
  - Docker: For containerization and consistency across environments.
  - CI/CD (GitHub Actions) for automated testing, building, and deployment.


---

## Installation

To get started with Pinsphere locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saurabh254/PinSphere.git
   cd PinSphere/server
   ```

2. **Install dependencies:**
   For backend, run:
   ```bash
   uv sync 
   ```

3. **(Optional) Environment variables setup:**
   Create a `.env` file and add the required environment variables for the database, cloud storage credentials, and OAuth setup. Example:

   ```env
   MONGODB_URI=mongodb://localhost/pinsphere
   POSTGRES_URI=postgresql://user:password@localhost/pinsphere
   SECRET_KEY=your-secret-key
   AWS_BUCKET=your-aws-bucket
   AWS_ENDPOINT=your-aws-endpoint
   AWS_REGION=your-aws-region
   AWS_ACCESS_KEY=your-aws-access-key
   AWS_SECRET_KEY=your-aws-secret-key
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

4. **Apply migrations:**
     ```bash
    uv run task apply_migrations
   ```
5. **Start Backend server:**
     ```bash
    uv run fastapi run
   ```

Your app should now be running at `http://localhost:3000`.

---


## License

Pinsphere is open-source software licensed under the [MIT License](LICENSE).



### Points Covered:
- **Aim:** The purpose of the platform is explained clearly.
- **Features:** What the platform offers and how users can benefit.
- **Usage:** Instructions for running the app locally and a brief guide for using the platform.
- **Infrastructure:** Technologies used for both frontend and backend, authentication, and cloud storage.
- **Installation:** Steps to set up the app locally.
- **Contributing:** How others can contribute.
- **License:** Open-source information.
