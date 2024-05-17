from flask import Flask, jsonify, request
import mysql.connector

# MySQL configuration
config = {
    'host': 'localhost',
    'user': 'YOUR_USER_NAME',
    'password': 'YOUR_PASSWORD',  
    'database': 'DATABASE_NAME'
}
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/status', methods=['GET'])
def status():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            connection.close()
            return jsonify({ "status": "OK"})
        else:
            return jsonify({ "status": "Not OK"})
    except Exception as e:
        return jsonify({"status": "API is running but encountered an error: " + str(e)})
        
@app.route('/data', methods=['GET'])
def data():
    try:
        # Connection to MySQL database
        connection = mysql.connector.connect(**config)
    
        if connection.is_connected():
            # Create cursor object to execute queries
            cursor = connection.cursor()
        
            # Execute SQL query to select all data from the "project" table
            cursor.execute("SELECT * FROM project")
        
            # Fetch all rows from the result set
            rows = cursor.fetchall()
        
            # Close cursor and connection
            cursor.close()
            connection.close()
            
             # Convert the fetched data to a list of dictionaries
            data = [{'id': row[0], 'name': row[1], 'email': row[2], 'status': row[3]} for row in rows]

            # Return the data as JSON response
            return jsonify(data)
        else:
            print('Failed to connect to MySQL database')
    except Exception as e:
        print('Error connecting to MySQL database:', e)
        
@app.route('/update_data/<int:id>', methods=['PUT'])
def update_data(id):
    try:
        # Get the updated data from the request body
        updated_data = request.json
        
        # Connection to MySQL database
        connection = mysql.connector.connect(**config)
    
        if connection.is_connected():
            # Create cursor object to execute queries
            cursor = connection.cursor()
        
            # Construct the SQL query to update data in the project table
            update_query = "UPDATE project SET name = %s, email = %s, status = %s WHERE id = %s"
            
            # Execute the update query with the provided data
            cursor.execute(update_query, (updated_data['name'], updated_data['email'], updated_data['status'], id))
            
            # Commit the transaction
            connection.commit()
        
            # Close cursor and connection
            cursor.close()
            connection.close()
            
            # Return success message
            return jsonify({"message": "Data updated successfully"})
        else:
            return jsonify({"error": "Failed to connect to MySQL database"})
    except Exception as e:
        return jsonify({"error": "Error updating data: " + str(e)})
    
@app.route('/delete_data/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:   
        # Connection to MySQL database
        connection = mysql.connector.connect(**config)
    
        if connection.is_connected():
            # Create cursor object to execute queries
            cursor = connection.cursor()
        
            # Construct the SQL query to update data in the project table
            delete_query = "DELETE FROM project WHERE id = %s"
            
            # Execute the update query with the provided data
            cursor.execute(delete_query, (id,))
            
            # Commit the transaction
            connection.commit()
        
            # Close cursor and connection
            cursor.close()
            connection.close()
            
            # Return success message
            return jsonify({"message": "Data deleted successfully"})
        else:
            return jsonify({"error": "Failed to connect to MySQL database"})
    except Exception as e:
        return jsonify({"error": "Error delete data: " + str(e)})
    
@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        insert_data = request.json
        
        connection = mysql.connector.connect(**config)
    
        if connection.is_connected():
            
            cursor = connection.cursor()
        
            cursor.execute("SELECT MAX(id) FROM project")
            result = cursor.fetchone()
            if result[0] is not None:
                new_id = result[0] + 1
            else:
                new_id = 1
            
            insert_query = "INSERT INTO project (id, name, email, status) VALUES (%s, %s, %s, %s)"
            
            cursor.execute(insert_query, (new_id, insert_data['name'], insert_data['email'], insert_data['status']))
            
            connection.commit()
        
            cursor.close()
            connection.close()
            
            return jsonify({"message": "Data inserted successfully"})
        else:
            return jsonify({"error": "Failed to connect to MySQL database"})
    except Exception as e:
        return jsonify({"error": "Error inserting data: " + str(e)})
    
if __name__ == '__main__':
    app.run()