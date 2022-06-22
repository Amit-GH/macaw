
class NlpPipeline:
    def __init__(self, modules: dict):
        self.modules = dict()
        self.modules.update(modules)
        self.context = dict()

    def run(self, state_manager):
        for model_name, model in self.modules.items():
            # TODO: pass in required input to every model.
            conv = None  # get from state_manager
            model_output = model.run(conv)

            # TODO: Save output in state_manager.
            pass
