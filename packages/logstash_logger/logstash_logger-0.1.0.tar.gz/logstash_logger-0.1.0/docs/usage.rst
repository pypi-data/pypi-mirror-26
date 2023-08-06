=====
Usage
=====

This logger must be used with ELK (ElasticSearch, LogStash, Kibana) stack ::
You can find docker stack image to build the entire stack https://github.com/rcourivaud/docker-elk

To use Logstash Logger in a project::

    from logstash_logger import LogstashLogger

You just have to inherit from LogstashLogger Class::

    class MyClass(LogstashLogger):
        def __init__(self):
            super().__init__(logger_name,
                 file_name=None,
                 host="localhost",
                 port=5000,
                 extra=None,
                 **kwargs)
            self.info("Initialize {}".format(self.__class__)

You can define extra parameters which will be passed over all logging functions ::

    class MyClass(LogstashLogger):
        def __init__(self):
            super().__init__(logger_name,
                 extra={"class":self.__class__})
            self.info("Initializing method ", extra={"comment":")
