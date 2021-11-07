from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Record:
    name: str
    col: int
    row: int


class Middleware:
    def process(self, record):
        if record is None:
            logger.debug("No record provided for {self.__name__}")

        print(f"I'm {self.__name__} Processing record {record.name}")


class MyColMiddleware(Middleware):
    def __init__(self):
        pass
    
    def process(self, record: Record):
        record.col = record.col * 7

class MyRowMiddleware(Middleware):
    def __init__(self):
        pass

    def process(self, record: Record):
        record.row = record.col * 5

        
class Pipeline:

    def __init__(self):
        self.middlewares = []

    def register(self, type: Middleware):
        self.middlewares.append(type)
        return self    
    
    def run(self, record: Record):
        if(record is None):
            logger.debug("Record can't be None")
        for i in range(len(self.middlewares)):
            middleware = self.middlewares[i]
            middleware.process(middleware, record=record)

        return record   

if __name__ == "__main__":
    input = Record("Record1", 1, 2)
    
    pipeline = Pipeline()
    pipeline.register(MyColMiddleware)
    pipeline.register(MyRowMiddleware)

    output = pipeline.run(input)

    print(input)
    print(output)