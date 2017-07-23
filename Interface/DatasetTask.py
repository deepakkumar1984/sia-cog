from pandas import read_csv
import os

def peekData(folder, filename, request):
    result = []
    count = 5
    if 'peekcount' in request:
        count = request['peekcount']

    filepath = folder + "/" + filename
    if not os.path.exists(filepath):
        return result;

    data = read_csv(filepath)
    result = data.head(count)
    return result.to_json()
