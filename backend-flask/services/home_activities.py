from datetime import datetime, timedelta, timezone
from opentelemetry import trace

from lib.db import pool

tracer = trace.get_tracer("home.activities")


class HomeActivities:
  def run(cognito_user_id=None):
    # logger.info("HomeActivities") # to run this add argument "logger" in run method. 
    with tracer.start_as_current_span("home-activities-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())
      span.set_attribute("user.id", str(cognito_user_id))

      sql = """
      SELECT * FROM actifities
      """
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchall()
    return json[0]
    return results