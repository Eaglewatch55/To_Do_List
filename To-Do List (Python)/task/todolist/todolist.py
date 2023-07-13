from sqlalchemy import create_engine, Column, Integer, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

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
    menu = ["1) Today's tasks",
            "2) Week's tasks",
            "3) All tasks",
            "4) Missed tasks",
            "5) Add a task",
            "6) Delete a task",
            "0) Exit"]

    for option in menu:
        print(option)


def retrieve_tasks(connection, date_range="today"):
    Session = sessionmaker(bind=connection)
    session = Session()

    if date_range == "today":
        query = session.query(Task).filter(Task.deadline == today).all()

    elif date_range == "week":
        query = session.query(Task).\
            filter(today <= Task.deadline,
                   Task.deadline <= today + timedelta(days=6)).\
            order_by(Task.deadline).all()

    elif date_range == "all":
        query = session.query(Task).order_by(Task.deadline).all()

    elif date_range == "missed":
        query = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()

    session.close()
    return query


def add_task(temp_task, d_line, connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    to_add = Task(task=temp_task, deadline=datetime.strptime(d_line, "%Y-%m-%d"))
    session.add(to_add)
    session.commit()
    session.close()


def print_tasks(task_list, dates=False, empty_message="Nothing to do!", end=True):

    f = True

    if len(task_list) == 0:
        print(empty_message)
        f = False

    else:
        if dates:
            for i, t in enumerate(tasks):
                print(f"{i + 1}. {t}. {t.deadline.strftime('%d %b')}")

        else:
            for i, t in enumerate(task_list):
                print(f"{i + 1}. {t}")

    if end:
        print()

    return f


def delete_task(d_task: Task, connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    session.delete(d_task)
    session.commit()
    session.close()

engine = startup()
today = datetime.today().date()
while True:
    print_menu()
    selection = int(input())
    print()

    if selection == 0:
        print("Bye!")
        exit()

    elif selection == 1:
        tasks = retrieve_tasks(engine)
        print(f"Today {today.strftime('%d %b')}:")
        print_tasks(tasks)

    elif selection == 2:
        week_tasks = retrieve_tasks(engine, "week")
        task_dict = {(today + timedelta(days=d)): [] for d in range(7)}

        for t in week_tasks:
            task_dict[t.deadline].append(t)

        for d in task_dict.keys():
            print(d.strftime('%A %d %b'), end=":\n")
            print_tasks(task_dict[d])

    elif selection == 3:
        tasks = retrieve_tasks(engine, "all")
        print(f"All tasks:")
        print_tasks(tasks, dates=True)

    elif selection == 4:
        tasks = retrieve_tasks(engine, "missed")
        print(f"Missed tasks:")
        print_tasks(tasks, dates=True, empty_message="All tasks have been completed!")

    elif selection == 5:
        print("Enter a task")
        task = input()
        print("Enter a deadline")
        deadline = input()
        add_task(task, deadline, engine)
        print("The task has been added!")

    elif selection == 6:
        tasks = retrieve_tasks(engine, "all")
        if len(tasks) > 0:
            print("Choose the number of the task you want to delete:")

        flag = print_tasks(tasks, dates=True, empty_message="Nothing to delete", end=False)

        if flag:
            to_delete = int(input()) - 1
            delete_task(tasks[to_delete], engine)
            print("The task has been deleted!")

    else:
        raise NotImplementedError

    print()
