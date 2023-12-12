import os
import re

from flask import Flask, request, Response
from typing import Any, Iterator, List

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(cmd: str, val: str, file_list: Iterator) -> List[Any]:
    if cmd == 'filter':
        return list(filter(lambda x: val in x, file_list))

    if cmd == 'map':
        val = int(val)
        return list(map(lambda x: x.split()[val], file_list))

    if cmd == 'unique':
        return list(set(file_list))

    if cmd == 'sort':
        reverse = val == 'desc'  # если val == 'desc' reverse вернёт True
        return sorted(file_list, reverse=reverse)

    if cmd == 'limit':
        val = int(val)
        return list(file_list)[:val]

    if cmd == 'regex':
        regex = re.compile(val)
        return list(filter(lambda x: regex.search(x), file_list))
        # /perform_query?cmd1=regex&val1=images\/\w*\.png&file_name=apache_logs.txt
    return []


@app.route("/perform_query", methods=["POST", "GET"])  # /perform_query?cmd1=filter&val1=POST&file_name=apache_logs.txt
def perform_query() -> Response:  # содержит всю информацию ответа сервера на HTTP-запрос
    cmd1 = request.args.get('cmd1')
    val1 = request.args.get('val1')
    cmd2 = request.args.get('cmd2')
    val2 = request.args.get('val2')
    file_name = request.args.get('file_name')

    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    if not (cmd1 and val1 and file_name):
        return app.response_class("Missing query parameter or file name", status=400)

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return app.response_class("File not found", status=400)

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    with open(file_path) as file:
        res = build_query(cmd1, val1, file)
        if cmd2 and val2:
            res = build_query(cmd2, val2, res)

    return app.response_class('\n'.join(res), content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=False)
