# Film_DB
Collection xv

🎬Film Recommendation System is an application using Python and PostgreSQL to generate recommendations for films and stores based on actual rental data. The system employs SQL queries and machine learning models to recommend movies, predict the most rented films, and suggest the stores where these films are most readily available.

# Objectives 🎯
- **Build a movie recommendation engine using data from a PostgreSQL database.**
- Predict **highly rented films** with machine learning models.  
- Recommend **stores** based on selected films.  
- Demonstrate practical integration of **SQL** and **Python** for data-driven insights.
- **Project base** A Random Forest model identifies “highly rented” films based on historical rental data.  

# Features 🖌️
- **Keyword-based movie recommendation:**  
  Customers can search by title or description to find top-rented films.  
- **Store recommendations:**  
  Suggests stores where a selected film is most frequently rented.  
- **Configurable PostgreSQL connection:**  
  Database settings are stored in `config.py` for easy customization.  
- **Extensible design:**  
  Modular code organization (`db.py`, `recommendation.py`, `models.py`, `app.py`) for future expansion into a web or API service.  

# Technical Stack ⚙️
 Layer | Technology 
-------|-------------
**Programming Language**| Python 3
**Database** | PostgreSQL 
**Libraries**| psycopg2, pandas, scikit-learn, numpy 
**Model**| Random Forest classifier
**Environment**| Windows, macOS, or Linux
**Additional Extensions**| Flask/FastAPI for API integration 

# Database Schema 🏗️
The restored database from the tar file contains the following tables:
- **actor** (`actor_id`, `first_name`, `last_name`, `last_update`)  
- **film** (`film_id`, `title`, `description`, `release_year`, `rental_duration`, `rental_rate`, `length`, `replacement_cost`)  
- **inventory** (`inventory_id`, `film_id`, `store_id`)  
- **rental** (`rental_id`, `inventory_id`, `staff_id`, `rental_date`, `return_date`)  
- **payment** (`payment_id`, `staff_id`, `payment_date`, `rental_id`, `amount`)  
- **store** (`store_id`, `manager_staff_id`, `address_id`)

# Getting Started 📦
- PostgreSQL installed and running  
- pg_restore utility available in your PATH  

### 1. Restore the Database
- cd ~/file directory
**pg_restore -U postgres -W -C -d postgres filename.tar**
  
- Or create and load manually:
createdb -U postgres movie
**pg_restore -U postgres -W -d movie filename.tar**

### 2. Set up Configuration
Edit `config.py`

### 3. Install Dependencies
pip install psycopg2-binary pandas scikit-learn numpy

### 4. Run the Application
python application.py

### 5. Workflow
1. Enter a keyword/title (e.g., “matrix”, “love”).  
2. Get top 10 most-rented films related to the keyword.  
3. Choose a film ID to:  
   - Get the probability of being highly rented.
   - Display suggested stores for the movie rent. 
