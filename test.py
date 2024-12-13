from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Создание базы данных и сессии
engine = create_engine('sqlite:///:memory:')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Определение моделей
class Parent(Base):
    __tablename__ = 'parent'
    id1 = Column(Integer, primary_key=True)
    id2 = Column(Integer, primary_key=True)

class Child(Base):
    __tablename__ = 'child'
    parent_id1 = Column(Integer, ForeignKey('parent.id1'), primary_key=True)
    parent_id2 = Column(Integer, ForeignKey('parent.id2'), primary_key=True)

# Создание всех таблиц
Base.metadata.create_all(engine)

# Добавление данных в таблицу parent
parent_record = Parent(id1=1, id2=2)
session.add(parent_record)
session.commit()

# Добавление данных в таблицу child
child_record = Child(parent_id1=1, parent_id2=2)
session.add(child_record)  # Добавляем объект child в сессию
session.commit()  # Сохраняем изменения в базе данных

# Проверка добавленных данных
added_child = session.query(Child).filter_by(parent_id1=1, parent_id2=2).first()
print(f"Added Child: {added_child.parent_id1}, {added_child.parent_id2}")