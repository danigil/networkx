import csv
import logging
import os

import networkx as nx
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

            flash(f'Calculated, top_nodes: {top_nodes}!', 'success')
            logging.log(level=logging.DEBUG, msg=f"calculating matching")

            ret_edges = calc_response(type, edges, top_nodes)
            now = datetime.now()
            file_name = f'{now.strftime("%d-%m-%Y-%H-%M-%S")}.csv'

            logging.log(level=logging.DEBUG, msg=f"writing to file_name: {file_name}")

            with open(f'website_code/static/outputs/{file_name}', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(ret_edges)

            logging.log(level=logging.DEBUG, msg=f"redirecting to download page")
            return redirect(url_for(".download_output_page", name=file_name))
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

    matching_edges = list(
        map(lambda tup: (str(tup[0]), str(tup[1])), filter(lambda tup: matching_ret[tup[0]] == tup[1], edges)))
    print("ret: ", matching_edges)

    return matching_edges
