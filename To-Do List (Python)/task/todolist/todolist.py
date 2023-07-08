from sqlalchemy import create_engine, Column, Integer, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.now())

    def __repr__(self):
        return self.task


def startup():
    connection = create_engine('sqlite:///todo.db?check_same_thread=False')  # Create/Connect to db
    Base.metadata.create_all(connection)    # Create table
    return connection


def update():
    raise NotImplementedError


def print_menu():
    menu = ["1) Today's tasks", "2) Add a task", "0) Exit"]
    for option in menu:
        print(option)


def retrieve_tasks(connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    return session.query(Task).all()


def add_task(task, connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    to_add = Task(task=task)
    session.add(to_add)
    session.commit()


engine = startup()
while True:
    print_menu()
    selection = int(input())
    print()

    if selection == 0:
        print("Bye!")
        exit()

    elif selection == 1:
        tasks = retrieve_tasks(engine)
        print("Today:")

        if len(tasks) == 0:
            print("Nothing to do!")
            print()
            continue

        for i, t in enumerate(tasks):
            print(f"{i + 1}. {t}")

    elif selection == 2:
        print("Enter a task")
        add_task(input(), engine)
        print("The task has been added!")

    else:
        raise NotImplementedError

    print()
