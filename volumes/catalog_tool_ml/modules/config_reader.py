# Configファイルの読み込み

import configparser


class ConfigInit():
    def __init__(self, config_filename):
        config_ini = configparser.ConfigParser()

        # コンフィグファイル確認
        if not config_filename:
            print('ERROR: Couldn\'t load ConfigFile')

        try:
            config_ini.read(config_filename, encoding='utf-8')

            # 設定の初期化
            section_name = 'gRPC'
            self.ML_PORT = config_ini.get(section_name, 'ML_PORT')

            section_name = 'ANALYSIS'
            self.CLF_MODEL_THEME = config_ini.get(section_name, 'CLF_MODEL_THEME')
            self.CLF_MODEL_KEYWORDS = config_ini.get(section_name, 'CLF_MODEL_KEYWORDS')
            self.MLB_MODEL_KEYWORDS = config_ini.get(section_name, 'MLB_MODEL_KEYWORDS')
            
            section_name = 'DIR_RECIEVE'
            self.DIR_RECIEVE = config_ini.get(section_name, 'DIR_RECIEVE')

        except Exception as e:
            # Error処理
            print('ERROR: config init Error.')
            print('log: ', e)


def main():
    config_file = '../config.ini'
    conf = ConfigInit(config_file)

    print('読み込み結果')
    print(conf.ML_PORT)


if __name__ == '__main__':
    main()

