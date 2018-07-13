class ApplitoolsMixin(object):

    def start_visual_test(self, test_name):
        if not self.eyes:
            raise Exception('An applitools eyes instance is required')
        self.eyes.open(self.driver, app_name=self.app_name, test_name=test_name)

    def stop_visual_test(self):
        self.eyes.close()

    def check_window(self):
        self.eyes.check_window(self.__class__.__name__)
