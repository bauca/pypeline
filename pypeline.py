from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Record:
    name: str
    col: int
    row: int


class Middleware:    
    def __init__(self, context):
        if(context is None):
            raise TypeError("context can't be None")

        self.pipeline = context

    def should_run(self, record):
        return True

    def process(self, record):
        if record is None:
            print("No record provided for {self.__class__}")

        print(f"I'm {self.__class__} Processing record {record.name} for {self.pipeline.name}")


class MultiplyBySevenUnits(Middleware):
    def __init__(self, context):
        super().__init__(context)

    def should_run(self, record: Record):
        return record.col == 1
            
    def process(self, record: Record):
        super().process(record)
        record.col = record.col * 7
        self.pipeline.data["NextMiddlewareData"] = "Something"

class SumFiveUnits(Middleware):
    def __init__(self, context):
        super().__init__(context)

    def process(self, record: Record):
        super().process(record)
        record.row = record.row + 5
        print(f'Previous middleware gave me: {self.pipeline.data["NextMiddlewareData"]}')
        
class Pipeline:
    
    def __init__(self, name=__name__):
        self.middlewares = []
        self.name = name
        self.data = {}

    def register(self, middleware: Middleware):
        self.middlewares.append(middleware(self))
        return self    
    
    def run(self, record: Record):
        if(record is None):
            print("Record can't be None")
        
        total_middlewares = len(self.middlewares)
        for index in range(total_middlewares):
            middleware = self.middlewares[index]
            if(middleware.should_run(record)):
                middleware.process(record)      
        
        return record

if __name__ == "__main__":
    input = Record("Record1", col=1, row=2)
    
    pipeline = Pipeline("FirstPipeline")
    pipeline.register(MultiplyBySevenUnits)
    pipeline.register(SumFiveUnits)

    pipeline.run(input)

    print(input)
    assert input.col == 1*7
    assert input.row == 2+5
