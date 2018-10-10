from flask import Flask, request, jsonify
import math
import pandas as pd

app = Flask(__name__)

FILE = "../banggo_database.csv"
file_df = pd.read_csv(FILE)

def query(sku_id):
    query_result = file_df.loc[file_df['a_sku_id'] == sku_id].values.tolist()
    if len(query_result) > 0:
        return query_result[0][2:] 
    else:
        return []

@app.route('/')
def price_query():
    pathname = request.args.get("pathname", None)
    if pathname == None:
        return jsonify({"price", []})
    print(pathname)
    sku_id = int(pathname.split('/')[2].split('.')[0])
    price_list = query(sku_id)

    for i in range(len(price_list)):
        if math.isnan(price_list[i]):
            price_list[i] = -1
    return jsonify({"sku_id": sku_id, "price_list": price_list})


if __name__ == "__main__":
    app.run()
    
