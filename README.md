## FORTUNA FLOW
[![GitHub top language](https://img.shields.io/github/languages/top/Shiyinq/fortuna-flow)](https://github.com/Shiyinq/fortuna-flow)
![GitHub repo size](https://img.shields.io/github/repo-size/Shiyinq/fortuna-flow)
![GitHub last commit](https://img.shields.io/github/last-commit/Shiyinq/fortuna-flow)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Shiyinq/fortuna-flow)


<div style="display: flex; justify-content: space-between; gap: 5px; max-width: 100%; overflow-x: auto; margin-bottom: 20px">
  <img src="docs/images/home.png" alt="Gambar 1" style="width: 24.5%; height: auto; object-fit: cover; border-radius: 8px;">
  <img src="docs/images/transactions.png" alt="Gambar 2" style="width: 24.5%; height: auto; object-fit: cover; border-radius: 8px;">
  <img src="docs/images/report.png" alt="Gambar 3" style="width: 24.5%; height: auto; object-fit: cover; border-radius: 8px;">
  <img src="docs/images/profile.png" alt="Gambar 4" style="width: 24.5%; height: auto; object-fit: cover; border-radius: 8px;">
</div>

**Track Your Finances, Unleash Your Fortune**

FortunaFlow is a personal finance management application that empowers you to take control of your money and unlock the path to financial prosperity. By meticulously tracking your income and expenses, you gain valuable insights into your spending habits and uncover opportunities to optimize your financial well-being.

## Features
* **Comprehensive User Management**
  * Seamlessly register and log in using your preferred method: email, GitHub, or Google.
  * Maintain a comprehensive profile to keep your personal information up-to-date.

* **Robust Wallet Management**
  * Create and manage multiple wallets to effortlessly track various accounts or budgets.
  * Gain a holistic view of your financial standing by consolidating data from all your wallets.

* **Granular Transaction Tracking**
  * Add, update, or delete transactions with ease, ensuring accuracy and completeness.
  * View transactions filtered by wallet or across all wallets for a comprehensive overview.

* **Customizable Transaction Categorization**
  * Create and manage your own transaction categories to tailor the app to your unique needs.
  * Gain insights into your spending patterns by grouping transactions into meaningful categories.

* **Insightful Data Analytics**
  * Access a suite of reports and analytics to gain deeper understanding of your financial data.
  * Identify trends, patterns, and anomalies in your spending to make informed financial decisions.

Embark on a journey toward financial freedom with FortunaFlow as your trusted guide. Let the power of data illuminate your path to a prosperous future.

## Development

### **How to Run the Back end**

This application is built using Python and MongoDB. To run this application, you will need to have Python and MongoDB installed on your computer.

#### **Step 1: Clone the Repository**

Clone the application repository from GitHub using the following command:

```
git clone https://github.com/Shiyinq/fortuna-flow.git
```

#### **Step 2: Create a Virtual Environment (venv)**

Create a virtual environment (venv) using conda with the following command:

```
conda create -n [venv-name] python=3.10
```

Activate the venv with the following command:

```
conda activate [venv-name]
```

#### **Step 3: Create the .env File**

Copy the `.env.example` file to the `.env` file.

```
cp .env.example .env
```

#### **Step 4: Update the .env File**

Update the `.env` file with the following information:

**FastAPI**

* `ORIGINS`: The allowed origins for CORS requests.

* `PORT`: The port on which the server will listen for requests.

**MongoDB**

* `MONGODB_URI`: The connection string for the MongoDB database.

* `DB_NAME`: The name of the database to use.

**JWT**

* `SECRET_KEY`: The secret key used to sign JWT tokens.

* `ALGORITHM`: The algorithm used to sign JWT tokens.

* `TOKEN_EXPIRE`: The expiration time for JWT tokens, in seconds.

#### **Step 5: Run the Server**

Run the server with the following command:

```
sh script/start-dev.sh
```

#### **Step 6: Open the API Documentation**

The API documentation can be opened in a browser at the following address:

```
http://localhost:8000/docs
```

**Example**

Here is an example of commands to run the application:

```
git clone https://github.com/Shiyinq/fortuna-flow.git
conda create -n my-app python=3.10
conda activate my-app
cp .env.example .env
vim .env
# Update information on .env
sh script/start-dev.sh
```

After running the above commands, the application will be running on port 8000. You can open the API documentation in a browser at the address http://localhost:8000/docs.

**Short Explanation**

* Step 1: Clone the application repository from GitHub.
* Step 2: Create a virtual environment (venv) using conda.
* Step 3: Create the `.env` file.
* Step 4: Update the `.env` file with the MongoDB and PORT information.
* Step 5: Run the server with the `sh script/start-dev.sh` command.
* Step 6: Open the API documentation in a browser.