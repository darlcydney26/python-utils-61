class InputValidationError(Exception):
    pass

class Processor:
    def __init__(self):
        self.processed_items = []

    def validate_input(self, item):
        if not isinstance(item, dict):
            raise InputValidationError('Input should be a dictionary')
        if 'value' not in item:
            raise InputValidationError('Missing required key: value')
        if not isinstance(item['value'], (int, float)):
            raise InputValidationError('Value must be a number')

    def process_items(self, items):
        for item in items:
            try:
                self.validate_input(item)
                self.processed_items.append(item['value'] * 2)  
            except InputValidationError as e:
                print(f'Error processing item {item}: {e}')  

    def get_results(self):
        return self.processed_items

if __name__ == '__main__':
    processor = Processor()
    test_items = [{'value': 1}, {'value': 2}, {'invalid_key': 3}, 'not_a_dict']
    processor.process_items(test_items)
    print(processor.get_results())