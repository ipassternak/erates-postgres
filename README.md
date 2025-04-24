# E-Rates

The **E-Rates** information system is designed to automate currency exchange processes in a financial institution.

## License

This project is licensed under the [MIT License](LICENSE).

## Requirements

- docker-compose 

**or:**
  - Python 3.12
  - Node.js 20
  - PostgreSQL >=15

## Local Startup

### Using Docker:
1. Clone the repository from GitHub.
    ```bash
    git clone https://github.com/ipassternak/erates.git
    ```
2. Create the database file:  
   ```bash
   touch app/db/app.db
   ```
3. Start the application:  
   ```bash
   docker-compose up -d
   ```

### Without Docker:
1. Clone the repository from GitHub.
    ```sh
    git clone https://github.com/ipassternak/erates.git
    ```
2. Create `.env` file from `.env.sample` and change `DATABASE_URL` variable
   ```bash
   cp .env.sample .env
   ```
3. Build the client:  
   ```bash
   cd client
   npm i
   npm run build:static
   cd ..
   ```
4. Set up the Python environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
7. Apply all env variables from `.env` file
6. Start the application:  
   ```bash
   make start-dev
   ```

## Creating an Admin User

### If Running in Docker:
1. Connect to the Docker instance:  
   ```bash
   docker exec -it erates_app /bin/sh
   ```
2. Run the following command:  
   ```bash
   python -m app.cmd.create_admin_user <email> <password> <full_name>
   ```

### If Running Locally:
Run the same command locally:  
```bash
python -m app.cmd.create_admin_user <email> <password> <full_name>
```

## Running the Client as a Separate App

1. Navigate to the client directory:  
   ```bash
   cd client
   ```
2. Install dependencies:  
   ```bash
   npm i
   ```
3. Start the development server:  
   ```bash
   npm run dev
   ```