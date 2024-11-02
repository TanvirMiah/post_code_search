from flask import Flask, render_template, request, jsonify
import duckdb

app = Flask(__name__)
conn = duckdb.connect('.\\db\\postcodes.duckdb')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup_postcode():
    postcode = request.form['postcode'].strip().upper()
    try:
        result = conn.execute("""
                    SELECT p.postcode, c.Constituency, c.Party, c.MP, p.ward
                    FROM postcodes.postcodes_list AS p
                    JOIN postcodes.constituency AS c ON p.code = c.Code
                    WHERE p.postcode LIKE ?
                              """, [f'%{postcode}%']).fetchall()
        # Fixed column names
        columns = ['postcode', 'constituency', 'party', 'mp', 'ward']
        
        # Fetch all matching rows
        rows = result
        
        if rows:
            # Convert rows to list of dictionaries
            formatted_result = []
            for row in rows:
                row_dict = {}
                for col, val in zip(columns, row):
                    row_dict[col] = str(val) if val is not None else ''
                formatted_result.append(row_dict)
            
            return jsonify({
                'columns': columns,
                'data': formatted_result
            })
        
        return jsonify({'error': 'Postcode not found'}), 404
        
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({'error': str(e)}), 500