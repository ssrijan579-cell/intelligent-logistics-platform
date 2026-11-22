
"""
SQLite database layer for Customer Experience & Feedback Intelligence.
"""

import os
import sqlite3

from pathlib import Path


# ==========================================================
# Database Configuration
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DB_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "feedback"
    / "customer_feedback.db"
)

# Allows a different database location in production.
DB_PATH = Path(
    os.getenv("FEEDBACK_DB_PATH", str(DEFAULT_DB_PATH))
).expanduser()


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DB_PATH,
        timeout=10,
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# Database Initialization
# ==========================================================

def initialize_database():

    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customer_feedback (

                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,

                shipment_id TEXT NOT NULL UNIQUE,

                overall_rating INTEGER NOT NULL
                    CHECK(overall_rating BETWEEN 1 AND 5),

                delivery_rating INTEGER NOT NULL
                    CHECK(delivery_rating BETWEEN 1 AND 5),

                agent_rating INTEGER NOT NULL
                    CHECK(agent_rating BETWEEN 1 AND 5),

                packaging_rating INTEGER NOT NULL
                    CHECK(packaging_rating BETWEEN 1 AND 5),

                comments TEXT NOT NULL,

                sentiment TEXT DEFAULT 'Pending',

                complaint_category TEXT DEFAULT 'Unclassified',

                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_feedback_shipment
            ON customer_feedback(shipment_id)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_feedback_sentiment
            ON customer_feedback(sentiment)
            """
        )

        connection.commit()


# ==========================================================
# Insert Feedback
# ==========================================================

def create_feedback(feedback_data):

    initialize_database()

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO customer_feedback (

                shipment_id,
                overall_rating,
                delivery_rating,
                agent_rating,
                packaging_rating,
                comments

            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,

            (
                feedback_data["shipment_id"],
                feedback_data["overall_rating"],
                feedback_data["delivery_rating"],
                feedback_data["agent_rating"],
                feedback_data["packaging_rating"],
                feedback_data["comments"],
            ),
        )

        feedback_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT *
            FROM customer_feedback
            WHERE feedback_id = ?
            """,
            (feedback_id,),
        ).fetchone()

        connection.commit()

        return dict(row)


# ==========================================================
# Retrieve Feedback
# ==========================================================

def get_all_feedback(limit=100, offset=0):

    initialize_database()

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM customer_feedback
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()

        return [dict(row) for row in rows]


# ==========================================================
# Update NLP Results
# ==========================================================

def update_feedback_analysis(
    feedback_id,
    sentiment,
    complaint_category,
):

    initialize_database()

    with get_connection() as connection:

        cursor = connection.execute(
            """
            UPDATE customer_feedback

            SET
                sentiment = ?,
                complaint_category = ?

            WHERE feedback_id = ?
            """,

            (
                sentiment,
                complaint_category,
                feedback_id,
            ),
        )

        connection.commit()

        return cursor.rowcount > 0


# ==========================================================
# Feedback Analytics
# ==========================================================

def get_feedback_summary():

    initialize_database()

    with get_connection() as connection:

        summary = connection.execute(
            """
            SELECT

                COUNT(*) AS total_feedback,

                ROUND(AVG(overall_rating), 2)
                    AS average_rating,

                SUM(
                    CASE
                        WHEN overall_rating >= 4
                        THEN 1 ELSE 0
                    END
                ) AS positive_ratings,

                SUM(
                    CASE
                        WHEN overall_rating = 3
                        THEN 1 ELSE 0
                    END
                ) AS neutral_ratings,

                SUM(
                    CASE
                        WHEN overall_rating <= 2
                        THEN 1 ELSE 0
                    END
                ) AS negative_ratings

            FROM customer_feedback
            """
        ).fetchone()

        return dict(summary)
