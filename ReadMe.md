# HeY!! [PlEaSe ReAdMe]


## 🚀 Project Objective:
Our primary goal with this project is to develop a web-based dashboard application that caters to the needs of a startup in the finance sector. This startup has generously provided 10 stock traders with an initial capital of $100 each. Our project's central mission is to create a user-friendly platform that empowers both the traders and administrators to comprehensively monitor trading performance over time.

## 📊 User Interaction and Navigation:

1. **Homepage (`/home/`):**
   - Traders and administrators can access the homepage to obtain an overview of all the traders.
   - A well-structured table provides detailed information about each trader, enhancing visibility and transparency.

2. **Login (`/login/`):**
   - We offer a straightforward login page, ensuring a smooth and secure entry into the system.

3. **Trader Dashboard:**
   - For administrators, an additional feature is accessible. They can click on a trader's name in the homepage table to access that trader's personalized dashboard.

4. **Non-Admin Dashboard:**
   - For traders who are not administrators, a dedicated dashboard is readily available. This can be reached by simply clicking on 'dashboard' in the navigation bar, providing a seamless user experience.

5. **Loging in**
   - All users automatically created have same password which is : 'password' i.e one user is email=trader1@gmail.com, password = 'password',

   - And an admin usewr is automatically created i.e (email = 'admin@ftnja.com', password = 'admin')
   please note: username has been replaced with email throughout this app
   

## 📈 User Dashboard Features:

1. **Date Filtering:**
   - To enhance the analytical capabilities of traders, we've introduced a date filtering option. This empowers users to focus on specific time intervals and gain deeper insights into their trading history.

2. **Mixed Graph:**
   - Our dashboard employs a mixed graph representation that combines bars and lines. This dynamic visual approach effectively showcases a trader's trading journey and their transaction growth.

## 🌱Data Seeding and Initialization:

1. **Docker Setup:**
   - To ensure the accessibility and ease of running the application, we've implemented Docker containers. To get started, one can execute the following command: `docker-compose up --build`. This simple step allows the application to be accessed at `http://localhost:8000/`.

2. **Command Line Scripts:**
   - In an effort to provide a seamless and efficient starting point for our users, we've developed custom command line scripts. These scripts play a pivotal role in seeding the database with essential data.

3. **Initialization Scripts:**
   - For users starting with an empty database volume, or for those who prefer not to use data from a `db.json` file, a sequence of commands is made available:
     - **For Windows:** Simply execute `spinup` or `spinup.bat`.
     - **For Linux:** Ensure the script is executable by running `chmod +x spinup.sh`. Alternatively, these commands can be run sequentially:
       - `docker-compose exec web python manage.py flush`
       - `docker-compose exec web python manage.py migrate`
       - `docker-compose exec web python manage.py makeadmin`
       - `docker-compose exec web python manage.py seed_traders`
       - `docker-compose exec web python manage.py simulate_profit_loss`
   - It's important to note that these commands may take some time to complete due to the inclusion of delays in the `seed_traders` script, allowing us to simulate real-world scenarios.

## 🧰Code Structure:

- Our project maintains a structured and organized codebase with comprehensive test coverage. All tests are stored in the `test` folder, ensuring that edge cases are well-covered.
- The `utils` folder contains utility scripts that are crucial to the application's functionality.

## ⚙️ How It Works:

1. **Data Capture:**
   - The heart of our application is the `Transaction` model, responsible for capturing critical details of financial transactions. These details encompass the type of transaction, the associated trader, transaction date, description, amount, and balance.

2. **Validation:**
   - The validation process is rigorously implemented to ensure data integrity. The `amount_validation` method within subclasses (e.g., `Credit` and `Debit`) enforces specific rules for transaction amounts. For example, `Credit` only permits positive amounts.

3. **Balance Update:**
   - Whenever a `Credit` or `Debit` transaction is saved, the application intelligently adjusts the trader's balance and records the updated balance. This ensures that the balance accurately reflects the impact of each transaction.

4. **Subclass Specifics:**
   - Our model is designed to cater to various transaction types, and this is where subclasses such as `Credit` and `Debit` come into play. These subclasses are tailored to handle specific transaction types and implement the `amount_validation` method to enforce transaction amount rules.

5. **User Access:**
   - The user's role is a pivotal aspect of our application. Transactions are intricately associated with users through a foreign key relationship with the `Trader` model. This allows for a highly personalized experience, with individual transaction histories and balance tracking.

6. **Reporting (Incomplete):**
   - Our application has provision for generating detailed reports, yet it's important to note that the specific implementation details for report generation are not covered in this code snippet.

In conclusion, our project centers around the `Transaction` model and its subclasses, which serve as the backbone for tracking financial transactions and maintaining balance records for traders. Our structured approach, meticulous validation, and data visualization via mixed graphs create an efficient and user-friendly financial tracking system that has been designed with extensibility in mind.