class ContextService:
    variables: dict = {}

    @staticmethod
    def get_item(key: str):
        return ContextService.variables[key]
    
    @staticmethod
    def set_item(key: str, value):
        ContextService.variables[key] = value