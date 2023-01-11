import csv

import networkx as nx
from . import app
from .forms import EnvyFreeMatchingCSVAndTextForm
from .algorithms.envy_free_matching import envy_free_matching, minimum_weight_envy_free_matching
from flask import render_template, redirect, url_for, request, flash, json
from pandas import read_csv
from datetime import datetime


@app.route('/')
def home_page():
    return render_template('home.html', title='Envy Free Bipartite Matching')


@app.route('/article')
def article_page():
    return render_template('article.html', title='Envy Free Bipartite Matching Article')


@app.route("/algo", methods=['GET', 'POST'])
def algo_page():
    form = EnvyFreeMatchingCSVAndTextForm()
    if not form.validate_on_submit():
        type = request.args["type"]
        if not type:
            type = "non_weighted"
        return render_template('algo.html', title=f'{type}_algo', form=form, type=type)

    else:
        input_file = form.file.data
        input_text = form.top_nodes.data

        if input_file and input_text:
            top_nodes = [int(num) for num in input_text.split(',')]

            edges = read_csv(input_file, header=None)
            edges = [tup for tup in edges.itertuples(index=False, name=None)]
            # if not is_valid_input_csv("non_weighted", edges):
            #     flash(f'ERROR edge csv file is malformed', category="error")
            #     return render_template('algo.html', title='Algo1', form=form)
            # else:
            # flash(f'Calculating, top_nodes: {top_nodes}!', 'success')

            ret_edges = calc_response("non_weighted", edges, top_nodes)
            now = datetime.now()
            file_name = f'{now.strftime("%d-%m-%Y-%H-%M-%S")}.csv'
            with open(f'website_code/static/outputs/{file_name}', 'w', newline='') as f:

                writer = csv.writer(f)
                writer.writerows(ret_edges)

            return redirect(url_for(".download_output_page", name=file_name))
        else:
            flash(f'ERROR missing input', category="error")


@app.route("/download")
def download_output_page():
    name = request.args['name']
    return render_template('download.html', name=name)


valid_input_csv_functions = {
    "non_weighted": lambda df: df.applymap(lambda x: type(x) == int and x > 0).all().all()
}


def is_valid_input_csv(type, df):
    return valid_input_csv_functions[type](df)


algorithms = {
    "non_weighted": envy_free_matching,
    "weighted": minimum_weight_envy_free_matching
}


def calc_response(type, edges, top_nodes):
    G = nx.Graph(edges)

    current_algo = algorithms[type]

    matching_ret = current_algo(G, top_nodes=top_nodes)
    matching_edges = list(
        map(lambda tup: (str(tup[0]), str(tup[1])), filter(lambda tup: matching_ret[tup[0]] == tup[1], edges)))
    print("ret: ", matching_edges)

    return matching_edges
