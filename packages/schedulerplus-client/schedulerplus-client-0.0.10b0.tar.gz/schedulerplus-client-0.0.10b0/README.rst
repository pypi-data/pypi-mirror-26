example:

1.`export serverIp = xxx export serverPort = xxx`

2.schedulerplus_client.conf
```
[schedulerplus_client]
zk_url = localhost:2181
schedulerplus_url = localhost:8888
job_group = demogroup

```

3.demo_executor.py
```python
from schedulerplus.client.job_executor import JobExecutor
from schedulerplus.client.job_code_messages import *


class DemoExecutor(JobExecutor):

    def execute(self, external_data):
        print external_data
        return SUCCESS_CODE, SUCCESS_MESSAGE
```


4.web_main.py
```python
import cherrypy
from schedulerplus.client.config import Config
Config.instance().load("xxx")

from schedulerplus.client.job_dispatcher import JobDispatcher
from schedulerplus.client.job_register import JobRegister

from demo.demo_executor import DemoExecutor


class JobDispatchController(object):
    job_dispatcher = JobDispatcher()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def dispatch(self):
        form = cherrypy.request.json
        self.job_dispatcher.dispatch(form)


if __name__ == "__main__":
    JobRegister.instance().register("demo", DemoExecutor())
    cherrypy.quickstart(JobDispatchController())
```