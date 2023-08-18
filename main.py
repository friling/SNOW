from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_folder='static')  # Add 'static_folder' to serve the CSS file

@app.route('/export', methods=['POST'])
def export():
    selected_manager = request.form['selected_manager']
    df = pd.read_excel('uploaded_file.xlsx')  # Replace 'uploaded_file.xlsx' with the actual name of the uploaded file
    filtered_df = df[(df['Requestor1'] == selected_manager) | (df['Requestor2'] == selected_manager) | (df['Requestor3'] == selected_manager) | (df['Requestor4'] == selected_manager)]
    output_file = 'exported_data.xlsx'
    filtered_df.to_excel(output_file, index=False)
    return send_file(output_file, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        df = pd.read_excel(file)
        # Get unique values from the last 3 columns (Manager1, Manager2, Manager3)
        managers = sorted(pd.unique(df.iloc[:, -4:].values.ravel()))
        return render_template('show_data.html', data=df.to_dict('records'), managers=managers)
    else:
        return "Invalid file format"


if __name__ == '__main__':
    app.run(debug=True)
