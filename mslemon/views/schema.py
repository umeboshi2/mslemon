import colander
import deform

from trumpet.resources import MemoryTmpStore

from trumpet.views.schema import deferred_choices, make_select_widget
from trumpet.views.schema import AddUserSchema
from trumpet.views.schema import NameSelectSchema
from trumpet.views.schema import UploadFileSchema


tmpstore = MemoryTmpStore()


