import csv
import io
import logging
import os
from base64 import b64encode

import networkx as nx
import networkx.algorithms.bipartite
from . import app
from .forms import EnvyFreeMatchingCSVAndTextForm
from .algorithms.envy_free_matching import envy_free_matching, minimum_weight_envy_free_matching
from flask import render_template, redirect, url_for, request, flash, json
from pandas import read_csv
from datetime import datetime


@app.route('/')
def home_page():
    if "name" in request.args:
        os.remove(f'website_code/static/outputs/{request.args["name"]}')

    return render_template('home.html', title='Envy Free Bipartite Matching')


@app.route('/article')
def article_page():
    return render_template('article.html', title='Envy Free Bipartite Matching Article')


@app.route("/algo", methods=['GET', 'POST'])
def algo_page():
    type = request.args["type"]
    if not type:
        type = "non_weighted"
    logging.log(level=logging.DEBUG,msg=f"type: {type}")
    form = EnvyFreeMatchingCSVAndTextForm()

    if not form.validate_on_submit():
        logging.log(level=logging.DEBUG, msg=f"rendering algo page")
        return render_template('algo.html', title=f'{type}_algo', form=form, type=type)
    else:
        input_file = form.file.data
        input_text = form.top_nodes.data
        logging.log(level=logging.DEBUG, msg=f"got form:\n\tinput_file: {input_file}\n\tinput_text: {input_text}")

        if input_file and input_text:
            top_nodes = [int(num) for num in input_text.split(',')]

            edges = read_csv(input_file, header=None)
            edges = [tup for tup in edges.itertuples(index=False, name=None)]

            logging.log(level=logging.DEBUG, msg=f"edges: {edges}")
            logging.log(level=logging.DEBUG, msg=f"top_nodes: {top_nodes}")


            if not is_valid_input_csv(type, edges):
                logging.log(level=logging.DEBUG, msg=f"edge csv file is malformed, EXITING")

                flash(f'ERROR edge csv file is malformed', category="error")
                return render_template('algo.html', title='Algo', form=form)

            logging.log(level=logging.DEBUG, msg=f"calculating matching")

            matching_edges, originalimg = calc_response(type, edges, top_nodes)

            from PIL import Image

            file_object = io.BytesIO()
            img = Image.fromarray(originalimg.astype('uint8'))
            img.save(file_object, 'PNG')
            base64img = "data:image/png;base64," + b64encode(file_object.getvalue()).decode('ascii')

            logging.log(level=logging.DEBUG, msg=f"redirecting to result page")
            return render_template('result.html', result=base64img, matching_size=int(len(matching_edges)/2))
        else:
            flash(f'ERROR missing input', category="error")


@app.route("/download")
def download_output_page():
    name = request.args['name']
    return render_template('download.html', name=name)


valid_input_csv_functions = {
    "non_weighted": lambda list_of_tup:all(len(tup) == 2 and type(tup[0])==int and type(tup[1])==int for tup in list_of_tup),
    "weighted": lambda list_of_tup:all(len(tup) == 3 and type(tup[0])==int and type(tup[1])==int and type(tup[2])==float for tup in list_of_tup),
}


def is_valid_input_csv(type, edges):
    return valid_input_csv_functions[type](edges)


algorithms = {
    "non_weighted": envy_free_matching,
    "weighted": minimum_weight_envy_free_matching
}


def calc_response(type, edges, top_nodes):
    if type =='non_weighted':
        logging.log(level=logging.DEBUG, msg=f"calc_response: non_weighted")

        G = nx.Graph(edges)
    else:
        logging.log(level=logging.DEBUG, msg=f"calc_response: weighted")

        G = nx.Graph()
        G.add_weighted_edges_from(edges)


    current_algo = algorithms[type]

    matching_ret = current_algo(G, top_nodes=top_nodes)
    logging.log(level=logging.DEBUG, msg=f"calc_response: return: {matching_ret}")

    import matplotlib
    matplotlib.use('agg')
    import matplotlib.pyplot as plt

    fig = plt.figure()
    fig.add_subplot(111)

    X, Y = networkx.algorithms.bipartite.sets(G, top_nodes)
    pos = nx.drawing.layout.bipartite_layout(G, X)
    nx.draw_networkx(
        G,
        pos=pos,
    )

    if type == 'non_weighted':
        G_matching = nx.Graph(matching_ret.items())
    else:
        G_matching = nx.Graph()
        for key in matching_ret:
            for tup in edges:
                if key in tup:
                    G_matching.add_edge(key, matching_ret[key], weight=tup[2])

    nx.draw_networkx_edges(
        G_matching,
        pos=pos,
        edge_color='red'
    )

    fig.canvas.draw()

    import numpy as np

    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return matching_ret, data
