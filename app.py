from flask import Flask, render_template, request, redirect, url_for
import json
import os
import webbrowser
from threading import Timer

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entry_id = request.form.get('id')
        plant_name = request.form.get('plant_name')
        country = request.form.get('country')
        pincode = request.form.get('pincode')
        
        if plant_name and country and pincode:
            data = load_data()
            
            if entry_id:  # Update
                entry_id = int(entry_id)
                for entry in data:
                    if entry['id'] == entry_id:
                        entry.update({
                            'Plant Name': plant_name, 
                            'Country': country, 
                            'Pincode': int(pincode)
                        })
                        break
            else:  # Create
                new_id = max([e['id'] for e in data] + [0]) + 1
                data.append({
                    'id': new_id, 
                    'Plant Name': plant_name, 
                    'Country': country, 
                    'Pincode': int(pincode)
                })
            
            save_data(data)
            return redirect(url_for('index'))
    
    entries = load_data()
    entry_id = request.args.get('id')
    entry = None
    if entry_id and entry_id.isdigit():
        entry_id = int(entry_id)
        entry = next((e for e in entries if e['id'] == entry_id), None)
    
    return render_template(
        'index.html',
        entries=entries,
        show_form=request.args.get('show_form') == 'true',
        entry=entry
    )

@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    data = [e for e in load_data() if e['id'] != entry_id]
    save_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)