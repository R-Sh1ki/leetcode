import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from leetcode import LeetCode
    from pathlib import Path

    lc = LeetCode(notebook=Path(__file__))
    return (lc,)


@app.cell(disabled=True)
def _(lc):
    catalog = lc.sync_catalog()
    return


@app.cell
def _(lc):
    catalog_db = lc.catalog.connection
    return (catalog_db,)


@app.cell
def _(catalog_db, mo):
    _df = mo.sql(
        f"""
        SELECT
            topics.slug,
            COALESCE(topics.translated_name, topics.name) AS topic,
            COUNT(*) AS total,
            SUM(problems.remote_status = 'SOLVED') AS remote_solved,
            SUM(problems.archived = 1) AS archived
        FROM topics
        JOIN problem_topics
            ON problem_topics.topic_slug = topics.slug
        JOIN problems
            ON problems.id = problem_topics.problem_id
        GROUP BY topics.slug
        ORDER BY topics.slug;
        """,
        engine=catalog_db
    )
    return


@app.cell
def _(catalog_db, mo):
    _df = mo.sql(
        f"""
        SELECT
            problems.id,
            problems.title,
            problems.slug,
            problems.difficulty,
            problems.remote_status
        FROM problems
        JOIN problem_topics
            ON problem_topics.problem_id = problems.id
        JOIN topics
            ON topics.slug = problem_topics.topic_slug
        WHERE problems.archived = 0
            AND problems.paid_only = 0
            AND topics.slug = 'articulation-point'
        ORDER BY CAST(problems.id AS INTEGER);
        """,
        engine=catalog_db
    )
    return


if __name__ == "__main__":
    app.run()
