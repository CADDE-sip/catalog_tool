#!/usr/bin/env python3

import connexion
import logging

from swagger_server import encoder

__LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s :%(message)s'
logging.basicConfig(format=__LOG_FORMAT, level=logging.INFO)

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.config['JSON_AS_ASCII'] = False
    app.add_api('swagger.yaml', arguments={'title': 'カタログ作成支援ツール　OAuth2認証拡張コンテナI/F'}, pythonic_params=True)
    app.run(port=28080)


if __name__ == '__main__':
    main()
