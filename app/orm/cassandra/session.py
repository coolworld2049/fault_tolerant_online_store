from cassandra.cluster import Cluster, Session


def create_cassandra_session(
    contact_points: list[str],
) -> Session:
    cluster = Cluster(contact_points=contact_points)
    session = cluster.connect()
    return session
