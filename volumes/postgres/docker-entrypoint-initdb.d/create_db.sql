/* ユーザ作成 */
CREATE ROLE catalogtool WITH LOGIN PASSWORD 'catalogtool';
ALTER ROLE catalogtool SUPERUSER CREATEDB;

/* データベース削除(データベースが存在しない場合はなにもしない) */
DROP DATABASE IF EXISTS catalogtool;

/* データベース作成 */
CREATE DATABASE catalogtool WITH OWNER catalogtool ENCODING UTF8;

/* データベース接続 */
\c catalogtool

/* テーブル作成 */
-- DROP TABLE IF EXISTS Id_Mapping;
CREATE TABLE Id_Mapping
(
  CaddeId varchar(256) NOT NULL UNIQUE,
  Username varchar(256) NOT NULL,
  Password varchar(256) NOT NULL
);
