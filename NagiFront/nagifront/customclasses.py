# Custom classes used in Nagifront.

class WidgetSetting(object):
    pos = [0,0]             # Widget position of upper left corner in [x,y] format
    widget_type = ""        # Widget type in string
    additional_data = {}    # Dict for storing additional data needed for widgets of specific type.

    def __init__(self, pos, widget_type, **additional_data):
        self.pos = pos
        self.widget_type = widget_type
        self.additional_data = additional_data


class DashboardSetting(object):
    widget_list = []        # List for storing WidgetSettings of widgets which should be displayed on dashboard.

    def __init__(widget_list=None):
        if widget_list is not None:
            self.widget_list += widget_list
