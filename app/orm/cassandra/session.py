from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session


def create_cassandra_session(
    contact_points: str,
    keyspace: str,
    username: str,
    password: str,
) -> Session:
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster(
        contact_points=contact_points.split(","), auth_provider=auth_provider
    )
    session = cluster.connect(keyspace)
    return session
