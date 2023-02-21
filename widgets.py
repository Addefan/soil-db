from django.forms import SelectDateWidget


class OptionalSelectDateWidget(SelectDateWidget):
    def get_context(self, name, value, attrs):
        self.is_required = False
        return super(OptionalSelectDateWidget, self).get_context(name, value, attrs)
