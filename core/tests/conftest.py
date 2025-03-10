import pytest
from starlette.testclient import TestClient
from faker import Faker

from main import app
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from core.database import Base, get_db

from core.database import SessionLocal
from users.models import UserModel
from tasks.models import TaskModel

faker = Faker()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="session", autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def anon_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="package", autouse=True)
def generate_mock_data(db_session):
    user = UserModel(username='user_test')
    user.set_password("12345678")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"user created Username: {user.username} #{user.id}")

    tasks_list = []
    for _ in range(10):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=faker.sentence(nb_words=6),
                description=faker.text(),
                is_completed=faker.boolean()
            )
        )
    db_session.add_all(tasks_list)
    db_session.commit()
    print(f"task created for {user.username}")
