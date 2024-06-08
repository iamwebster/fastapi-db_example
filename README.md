## Небольшой гайд на sqlalchemy и alembic

### models.py
Создаем модели таблиц  
```py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass 


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    posts = relationship('Post', back_populates='user')
    

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='posts')
```
### Запускаем базу в докере 
```yml
version: '3.8'

services:
  db:
    container_name: postgresql
    image: postgres
    restart: always
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASS}
      - POSTGRES_DB=${DB_NAME}
    env_file:
      - .env
    ports:
      - "5432:5432"
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
```

### Выполнение миграций
Первое что необходимо сделать, так это инициализировать алембик
```bash
alembic init alembic
```
Создается файл alembic.ini, в котором нам необходимо прописать путь к нашей БД.
Делать мы это будем с помощью переменных окружения.
```ini
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s/%(DB_NAME)s
```

Далее создаем файл config.py чтобы забрать переменные окружения
```py
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
```
Далее заходим в файл env.py, который находится в директории migrations, который создал алембик. Здесь нам необходимо указать наши переменные окружения, чтобы они могли быть использованы в alembic.ini
```py
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.models import Base

config = context.config

config.set_main_option('DB_HOST', DB_HOST)
config.set_main_option('DB_NAME', DB_NAME)
config.set_main_option('DB_PASS', DB_PASS)
config.set_main_option('DB_PORT', DB_PORT)
config.set_main_option('DB_USER', DB_USER)
```
Также меняем target_metadata 
```py
target_metadata = Base.metadata
```
Теперь нам необходимо создать некую ревизию, подготовить наши данные для миграции 
```bash
alembic revision --autogenerate -m "database creation"
```
Теперь чтобы применить миграции нам нужно выполнить их, вставя вторым аргументов хэш миграции, который есть в папке migrations/versions
```bash
alembic upgrade 04ad56cccdee
```
Чтобы обновить до последней ревизии:
```bash
alembic upgrade head
```