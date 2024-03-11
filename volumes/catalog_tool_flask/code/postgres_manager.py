import traceback

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.orm import sessionmaker

from catalogtool_exception import CatalogToolException


class postgres_NotFound(Exception):
    """ 指定したCADDEユーザIDのCKANログイン情報がないエラー"""
    pass


class Postgres:

    def __init__(self, app, postgres):
        self.__app = app

        # DBエンジン作成
        posgresql_url = postgres['dialect'] + postgres['driver'] + '://' + postgres['username'] + ':' + \
            postgres['password'] + '@' + postgres['host'] + ':' + \
            postgres['port'] + '/' + postgres['database']
        engine = create_engine(posgresql_url)

        # セッション作成
        SessionClass = sessionmaker(engine)
        self.__SESSION = SessionClass()

    def get_cadde_user_id(self, ckan_username):
        self.__app.logger.warning('=== postgres_manger.py get_record ===')
        res = {
            'status': 'error',
            'message': '',
            'cadde_id_list': []
        }

        try:
            # テーブル定義
            Base = declarative_base()

            class User(Base):
                __tablename__ = 'id_mapping'
                caddeid = Column(String(256), primary_key=True)
                username = Column(String(256))
                password = Column(String(256))

            # 指定したレコードの取得
            users = self.__SESSION.query(User).filter(
                User.username == ckan_username).all()
            res['cadde_id_list'] = [r.caddeid for r in users]
            res['status'] = 'success'

        except exc.SQLAlchemyError:
            self.__app.logger.error('get_cadde_user_id sqlalchemr_Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'get_cadde_user_id_postgres_SQLAlchemyError', 500)

        except Exception:
            self.__app.logger.error('get_cadde_user_id Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'get_cadde_user_id_postgres_Exception', 500)

        finally:
            self.__SESSION.close()

        return res

    def get_ckan_user_info(self, cadde_user_id):
        self.__app.logger.warning('=== postgres_manger.py add_new_record ===')
        res = {
            'status': 'error',
            'message': '',
            'ckan_username': '',
            'ckan_user_password': ''
        }

        try:
            # テーブル定義
            Base = declarative_base()

            class User(Base):
                __tablename__ = 'id_mapping'
                caddeid = Column(String(256), primary_key=True)
                username = Column(String(256))
                password = Column(String(256))

            # ユーザレコード追加
            users = self.__SESSION.query(User).filter(
                User.caddeid == cadde_user_id).all()
            if not users or not users[0].username or not users[0].password:
                raise postgres_NotFound('エラー')

            res['ckan_username'] = users[0].username
            res['ckan_user_password'] = users[0].password
            res['status'] = 'success'

        except postgres_NotFound:
            self.__app.logger.error('get_ckan_user_info postgres_NotFound')
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException(
                'get_ckan_user_info_postgres_NotFound', 404)

        except exc.SQLAlchemyError:
            self.__app.logger.error('get_ckan_user_info sqlalchemr_Exception')
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException(
                'get_ckan_user_info_postgres_SQLAlchemyError', 500)

        except Exception:
            self.__app.logger.error('get_ckan_user_info Exception')
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException(
                'get_ckan_user_info_postgres_Exception', 500)

        finally:
            self.__SESSION.close()

        return res

    def add_new_record(self, ckan_username, ckan_password, cadde_user_id_list):
        self.__app.logger.warning('=== postgres_manger.py add_new_record ===')
        res = {
            'status': 'error',
            'message': ''
        }

        try:
            # テーブル定義
            Base = declarative_base()

            class User(Base):
                __tablename__ = 'id_mapping'
                caddeid = Column(String(256), primary_key=True)
                username = Column(String(256))
                password = Column(String(256))

            # ユーザレコード追加
            for cadde_user_id in cadde_user_id_list:
                user_info = User(username=ckan_username,
                                 password=ckan_password, caddeid=cadde_user_id)
                self.__SESSION.add(user_info)
            self.__SESSION.commit()
            res['status'] = 'success'

        except exc.IntegrityError:
            self.__app.logger.error('add_new_record duplicate_cadde_user_id')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'add_new_record_postgres_IntegrityError', 400)

        except exc.SQLAlchemyError:
            self.__app.logger.error('add_new_record sqlalchemr_Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'add_new_record_postgres_SQLAlchemyError', 500)

        except Exception:
            self.__app.logger.error('add_new_record Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'add_new_record_postgres_Exception', 500)

        finally:
            self.__SESSION.close()

        return res

    def update_record(self, ckan_username, ckan_password, cadde_user_id_list):
        self.__app.logger.warning('=== postgres_manger.py update_record ===')
        res = {
            'status': 'error',
            'message': ''
        }

        try:
            # テーブル定義
            Base = declarative_base()

            class User(Base):
                __tablename__ = 'id_mapping'
                caddeid = Column(String(256), primary_key=True)
                username = Column(String(256))
                password = Column(String(256))

            # CKANユーザ名をキーにユーザ情報を取得
            users_record = self.__SESSION.query(User).filter(
                User.username == ckan_username).all()
            db_cadde_id_list = [r.caddeid for r in users_record]

            # リクエストにないCADDEユーザIDのレコードを削除
            for __db_cadde_user_id in db_cadde_id_list:
                if __db_cadde_user_id not in cadde_user_id_list:
                    self.__SESSION.query(User).filter(
                        User.caddeid == __db_cadde_user_id).delete()

            # DBにないCADDEユーザIDのレコードを追加
            for __update_cadde_user_id in cadde_user_id_list:
                if __update_cadde_user_id not in db_cadde_id_list:
                    __update_user_info = User(
                        username=ckan_username, password=ckan_password, caddeid=__update_cadde_user_id)
                    self.__SESSION.add(__update_user_info)

            self.__SESSION.commit()
            res['status'] = 'success'

        except exc.IntegrityError:
            self.__app.logger.error('update_record duplicate_cadde_user_id')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'update_record_postgres_IntegrityError', 400)

        except exc.SQLAlchemyError:
            self.__app.logger.error('update_record sqlalchemr_Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'update_record_postgres_SQLAlchemyError', 500)

        except Exception:
            self.__app.logger.error('update_record Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException('update_record_postgres_Exception', 500)

        finally:
            self.__SESSION.close()

        return res

    def update_password(self, ckan_username, ckan_user_password):
        self.__app.logger.warning('=== postgres_manger.py update_password ===')
        res = {
            'status': 'error',
            'message': ''
        }

        try:
            # テーブル定義
            Base = declarative_base()

            class User(Base):
                __tablename__ = 'id_mapping'
                caddeid = Column(String(256), primary_key=True)
                username = Column(String(256))
                password = Column(String(256))

            # CKANユーザ名をキーに取得したレコードのパスワード更新
            update_users_records = self.__SESSION.query(
                User).filter(User.username == ckan_username).all()
            for r in update_users_records:
                r.password = ckan_user_password

            self.__SESSION.commit()
            res['status'] = 'success'

        except exc.SQLAlchemyError:
            self.__app.logger.error('update_record sqlalchemr_Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'update_password_postgres_SQLAlchemyError', 500)

        except Exception:
            self.__app.logger.error('update_record Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException(
                'update_password_postgres_Exception', 500)

        return res

    def delete_record(self, ckan_username):
        self.__app.logger.warning('=== postgres_manger.py delete_record ===')
        res = {
            'status': 'error',
            'message': ''
        }

        try:
            # テーブル定義
            Base = declarative_base()

            class User(Base):
                __tablename__ = 'id_mapping'
                caddeid = Column(String(256), primary_key=True)
                username = Column(String(256))
                password = Column(String(256))

            # ユーザレコード削除
            self.__SESSION.query(User).filter(
                User.username == ckan_username).delete()
            self.__SESSION.commit()
            res['status'] = 'success'

        except exc.SQLAlchemyError:
            self.__app.logger.error('delete_record sqlalchemr_Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException('delete_postgres_SQLAlchemyError', 500)

        except Exception:
            self.__app.logger.error('delete_record Exception')
            self.__app.logger.error(traceback.format_exc())
            self.__SESSION.rollback()
            raise CatalogToolException('delete_postgres_Exception', 500)

        finally:
            self.__SESSION.close()

        return res
