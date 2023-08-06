import csv
import io
import logging
import os
import re
from base64 import b64encode

import networkx as nx
import networkx.algorithms.bipartite
from . import app
from .forms import EnvyFreeMatchingCSVAndTextForm, EnvyFreeMatchingListAndTextForm
from .algorithms.envy_free_matching import envy_free_matching, minimum_weight_envy_free_matching, _EFM_partition
from flask import render_template, session, redirect, url_for, request, flash, json
from pandas import read_csv
from datetime import datetime
import json
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from networkx.readwrite import json_graph


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
    logging.log(level=logging.DEBUG, msg=f"type: {type}")
    form = EnvyFreeMatchingListAndTextForm()

    if not form.validate_on_submit():
        logging.log(level=logging.DEBUG, msg=f"rendering algo page")
        return render_template('algo.html', title=f'{type}_algo', form=form, type=type)
    else:
        input_text = form.top_nodes.data
        input_list = form.edges.data
        if input_list:
            if type == "non_weighted":
                m = re.findall('(\\d+,\\d+)', input_list)
            else:
                m = re.findall('(\\d+,\\d+,\\d+.\\d+)', input_list)
            if len(m) == 0:
                logging.log(level=logging.DEBUG, msg=f'ERROR edges input is malformed')

                flash(f'ERROR edges input is malformed', category="error")
                return render_template('algo.html', title='Algo', form=form, type=type)

            if type == 'non_weighted':
                edges = [(int(from_node), int(to_node)) for from_node, to_node in map(lambda s: s.split(','), m)]
            else:
                edges = [(int(from_node), int(to_node), float(weight)) for from_node, to_node, weight in
                         map(lambda s: s.split(','), m)]

            X = set([tup[0] for tup in edges])
            Y = set([tup[1] for tup in edges])

            inter = X.intersection(Y)
            if len(inter) != 0:
                logging.log(level=logging.DEBUG, msg=f'ERROR bipartite sets intersect')
                flash(f'ERROR bipartite sets intersect', category="error")
                return render_template('algo.html', title='Algo', form=form, type=type)

            if input_text == '':
                top_nodes = [tup[0] for tup in edges]
            else:
                top_nodes = [int(num) for num in input_text.split(',')]

            top_nodes = list(set(top_nodes))

            logging.log(level=logging.DEBUG, msg=f"edges: {edges}")
            logging.log(level=logging.DEBUG, msg=f"top_nodes: {top_nodes}")

            if not is_valid_input_csv(type, edges):
                logging.log(level=logging.DEBUG, msg=f'ERROR edges input is malformed')
                flash(f'ERROR edges input is malformed', category="error")
                return render_template('algo.html', title='Algo', form=form, type=type)

            input_checkbox = form.checkbox.data

            logging.log(level=logging.DEBUG, msg=f"redirecting to result page")
            session["type"] = type
            session["edges"] = edges
            session["top_nodes"] = top_nodes
            if input_checkbox:
                session["stage"] = "1"
            else:
                session["stage"] = "-1"
            session.modified = True

            return redirect(url_for('result_page'))
        else:
            flash(f'ERROR missing input', category="error")
            return render_template('algo.html', title='Algo', form=form, type=type)


matching_color = 'limegreen'
good_color = 'blue'
bad_color = 'red'


@app.route("/result", methods=['GET', 'POST'])
def result_page():
    if request.method == 'POST':
        data = json.loads(request.form["payload"])
        stage = data.get("stage", "1")
    else:
        stage = session.get("stage", "-1")

    args = []
    kwargs = {}

    if stage in ("-1", "1"):
        type = session["type"]
        edges = session["edges"]
        top_nodes = session["top_nodes"]
        args = [type, edges, top_nodes]

    elif stage in ("2", "3"):
        G = nx.node_link_graph(data["G"])
        M_str_keys = data["M"]
        M = {int(k): v for k, v in M_str_keys.items()}
        top_nodes = data["top_nodes"]
        type = data["type"]

        args = [G, M, top_nodes]
        kwargs = {"type": type}
    if stage == "3":
        EFM = data["X_L"], data["X_S"], data["Y_L"], data["Y_S"]
        args.append(EFM)

    payload, img = calc(stage, *args, **kwargs)
    return render_template(
        'result.html',
        result_img=img,
        payload=json.dumps(payload),
        stage=stage,
        good_color=good_color,
        bad_color=bad_color,
        matching_color=matching_color,
    )


# stage_dict = {
#     "1": "Stage 1/3: Maximum Matching",
#     "2": "Stage 2/3: EFM Partition",
#     "3": "Stage 3/3: X_L, Y_L"
# }

valid_input_csv_functions = {
    "non_weighted": lambda list_of_tup: all(
        len(tup) == 2 and type(tup[0]) == int and type(tup[1]) == int for tup in list_of_tup),
    "weighted": lambda list_of_tup: all(
        len(tup) == 3 and type(tup[0]) == int and type(tup[1]) == int and type(tup[2]) == float for tup in list_of_tup),
}


def is_valid_input_csv(type, edges):
    return valid_input_csv_functions[type](edges)


def is_valid_input_list(list, type="non_weighted"):
    if type == "non_weighted":
        return re.fullmatch('(\\d+,\\d+)+', list)
    else:
        return re.fullmatch('(\\d+,\\d+,\\d+.\\d+)+', list)


algorithms = {
    "non_weighted": envy_free_matching,
    "weighted": minimum_weight_envy_free_matching
}


def ret_graph_fig(G, M, top_nodes, type="non_weighted", stage=1, EFM=None, M_envy_free=None):
    def draw_matching(M, color='red'):
        G_matching = nx.Graph()
        for key in M:
            for tup in G.edges:
                if key in tup:
                    if type == "non_weighted":
                        G_matching.add_edge(key, M[key])
                    else:
                        G_matching.add_edge(key, M[key], weight=G[key][M[key]]["weight"])

        nx.draw_networkx_edges(
            G_matching,
            pos=pos,
            edge_color=color,
            ax=ax
        )

    fig, ax = plt.subplots()

    X, Y = networkx.algorithms.bipartite.sets(G, top_nodes)
    pos = nx.drawing.layout.bipartite_layout(G, X)
    nx.draw_networkx(
        G,
        pos=pos,
        ax=ax
    )
    if stage==-1:
        draw_matching(M, color=good_color)
    else:
        draw_matching(M, color=matching_color)

    if stage >= 2:
        color_map = []
        for node in G:
            if node in EFM[0] or node in EFM[2]:
                color_map.append(good_color)
            else:
                color_map.append(bad_color)

        nx.draw_networkx_nodes(
            G,
            pos=pos,
            ax=ax,
            node_color=color_map
        )

    if stage >= 3:
        draw_matching(M_envy_free, good_color)

    return fig, ax, pos


def ret_img(fig):
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    file_object = io.BytesIO()
    img = Image.fromarray(data.astype('uint8'))
    img.save(file_object, 'PNG')
    base64img = "data:image/png;base64," + b64encode(file_object.getvalue()).decode('ascii')

    return base64img


def calc(stage: str, *args, **kwargs):
    assert stage in ("-1", "1", "2", "3")

    def calc_max_matching(type, edges, top_nodes):
        if type == 'non_weighted':
            logging.log(level=logging.DEBUG, msg=f"calc_response: non_weighted")

            G = nx.Graph(edges)
        else:
            logging.log(level=logging.DEBUG, msg=f"calc_response: weighted")

            G = nx.Graph()
            G.add_weighted_edges_from(edges)

        M = nx.bipartite.maximum_matching(G, top_nodes=top_nodes)
        fig, ax, pos = ret_graph_fig(G, M, top_nodes, type=type, stage=1)
        img = ret_img(fig)
        payload = {
            "G": nx.node_link_data(G),
            "M": M,
            "top_nodes": top_nodes,
            "type": type
        }

        return payload, img

    def calc_efm_partition(G, M, top_nodes, type="non_weighted"):
        X_L, X_S, Y_L, Y_S = _EFM_partition(G, M, top_nodes)
        fig, ax, pos = ret_graph_fig(G, M, top_nodes, type=type, stage=2, EFM=(X_L, X_S, Y_L, Y_S))

        img = ret_img(fig)
        payload = {
            "G": nx.node_link_data(G),
            "M": M,
            "top_nodes": top_nodes,
            "type": type,
            "X_L": list(X_L),
            "X_S": list(X_S),
            "Y_L": list(Y_L),
            "Y_S": list(Y_S)
        }
        return payload, img

    def calc_envy_free_matching(G, M, top_nodes, EFM, type="non_weighted"):
        if type == "non_weighted":
            xs_ys = EFM[1] + EFM[3]
            M_envy_free = {node: M[node] for node in M if node not in xs_ys and M[node] not in xs_ys}
        else:
            xl_yl = set(EFM[0] + EFM[2])
            M_envy_free = nx.bipartite.minimum_weight_full_matching(G.subgraph(xl_yl), top_nodes)
        fig, ax, pos = ret_graph_fig(G, M, top_nodes, type=type, stage=3, EFM=EFM, M_envy_free=M_envy_free)

        img = ret_img(fig)
        return {}, img

    action = {
        "-1": calc_response,
        "1": calc_max_matching,
        "2": calc_efm_partition,
        "3": calc_envy_free_matching
    }

    payload, img = action[stage](*args, **kwargs)
    payload["stage"] = str(int(stage) + 1)

    return payload, img

def calc_response(type, edges, top_nodes):
    if type == 'non_weighted':
        logging.log(level=logging.DEBUG, msg=f"calc_response: non_weighted")

        G = nx.Graph(edges)
    else:
        logging.log(level=logging.DEBUG, msg=f"calc_response: weighted")

        G = nx.Graph()
        G.add_weighted_edges_from(edges)

    current_algo = algorithms[type]

    M = current_algo(G, top_nodes=top_nodes)
    fig, ax, pos = ret_graph_fig(G, M, top_nodes, type=type, stage=-1)
    img = ret_img(fig)

    return {}, img
