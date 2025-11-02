class SetProxy:
    def __init__(self, client, namespace, set):
        self.client = client
        self.namespace = namespace
        self.set = set

    def __repr__(self):
        return (f"SetProxy(client={self.client!r}; namespace={self.namespace!r},"
                f"set={self.set!r})")

    def get(self, key):
        db_key = (self.namespace, self.set, key)
        (_, _, record) =  self.client.get(db_key)
        return record

    def query(self):
        return self.client.query(self.namespace, self.set)
