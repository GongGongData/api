FROM mysql:latest

# MySQL 설정
ENV MYSQL_ROOT_PASSWORD=secret
ENV MYSQL_DATABASE=gonggong
#ENV MYSQL_USER=root
#ENV MYSQL_PASSWORD=mypassword

# 포트 설정 (기본 MySQL 포트는 3306)
EXPOSE 3306
