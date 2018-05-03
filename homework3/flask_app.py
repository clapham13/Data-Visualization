from flask import Flask, Response
from analysis import loadData, showViz
data = loadData()
app = Flask(__name__, static_url_path='', static_folder='.')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

@app.route('/vis/<platform>/<int:rating>')
def visualize(zip_code):
    '''
    Returns a flask visualization by filtering the data by zip-code
    '''
    df = data
    zip_filtered = df[['cuisine','perZip.' + str(zip_code)]]
    zip_filtered.rename(columns={'perZip.' + str(zip_code): 'total'}, inplace=True)
    zip_filtered = zip_filtered.dropna(axis=0, how='any') # Remove n/a values
    
    # Top 25
    zip_filtered = zip_filtered.sort_values(by=['total'], ascending=False)[:25][['cuisine', 'total']]
    response = '' # In case of errors return blank
    if zip_filtered is not None:
        response = showViz(zip_filtered, zip_code).to_json()

    return Response(response,
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

if __name__ == '__main__':
    app.run(port=8000)
