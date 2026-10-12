from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_function():
    TestingSessionLocal().close()


def test_health_check():
    setup_function()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    teardown_function()


def test_create_and_list_transaction():
    setup_function()

    payload = {
        "description": "Monthly salary",
        "amount": 50000,
        "category": "Salary",
        "transaction_type": "income",
	"transaction_date": "2026-10-12"
    }

    response = client.post("/transactions", json=payload)
    assert response.status_code == 200

    response = client.get("/transactions")
    assert response.status_code == 200
    assert len(response.json()) == 1

    teardown_function()


def test_summary_calculates_balance():
    setup_function()

    client.post(
        "/transactions",
        json={
            "description": "Monthly salary",
            "amount": 50000,
            "category": "Salary",
            "transaction_type": "income",
	    "transaction_date": "2026-10-12",
        },
    )

    client.post(
        "/transactions",
        json={
            "description": "Groceries",
            "amount": 4500,
            "category": "Food",
            "transaction_type": "expense",
	    "transaction_date": "2026-10-12",
        },
    )

    response = client.get("/summary")
    assert response.status_code == 200

    data = response.json()
    assert data["total_income"] == 50000
    assert data["total_expenses"] == 4500
    assert data["balance"] == 45500

    teardown_function()


def test_invalid_transaction_type():
    setup_function()

    response = client.post(
        "/transactions",
        json={
            "description": "Invalid transaction",
            "amount": 100,
            "category": "Other",
            "transaction_type": "invalid",
	    "transaction_date": "2026-10-12",
        },
    )

    assert response.status_code == 400
    teardown_function()
