import tarantool

from async_task_processor.primitives.base_task import BaseTask


class TarantoolTask(BaseTask):
    conn_max_retries = None
    conn_retries = None
    conn_retry_countdown = None
    ack = True  # Using to prevent tarantool ack task
    connection = None
    data = None
    queue_name = None
    _task = None
    _tube = None

    def __init__(self, loop, connection, tube, foo, args, bind, timeout, max_retries, retry_countdown,
                 conn_max_retries, conn_retry_countdown, name):
        """

        :type connection: asynctnt.Connection
        :type tube: asynctnt_queue.tube.Tube
        """
        self.conn_max_retries = conn_max_retries or 0
        self.conn_retry_countdown = conn_retry_countdown or 1
        self.conn_retries = 0
        self.queue_name = tube.name
        self.connection = connection
        self._tube = tube
        super().__init__(loop, type(self).__name__, foo, args, bind, timeout, max_retries, retry_countdown, name)

    def set_tube(self, task):
        """

        :type task: asynctnt_queue.Task
        :return:
        """
        self._task = task
        self.data = task.data

    def reset(self):
        self._task, self.data = None, None

    def __call__(self, *args, **kwargs):
        """Sync tarantool command execute. You may use self(<tarantool_command>) in task function

        :param args:
        :param kwargs:
        :return:
        """
        t = tarantool.connect(self.connection.host, self.connection.port, self.connection.username,
                              self.connection.password, self.connection.encoding)
        r = t.call(*args, **kwargs)
        t.close()
        return r

    @property
    def tube(self):
        return self._tube

    @property
    def task(self):
        return self._task
