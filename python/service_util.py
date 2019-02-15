import win32serviceutil
import time
import codecs
import locale


UNKNOWN = 0
STOPPED = 1
START_PENDING = 2
STOP_PENDING = 3
RUNNING = 4

status_code = {
    0: "UNKNOWN",
    1: "STOPPED",
    2: "START_PENDING",
    3: "STOP_PENDING",
    4: "RUNNING"
}

def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


class WinService:

    def is_iterable(self, source):
        if source is not None:
            try:
                iter(source)
            except TypeError:
                return False
            return True
        else:
            raise RuntimeError("argument cannot be None")

    def get_service_status(self, service_name):
        try:
            result = win32serviceutil.QueryServiceStatus(service_name)[1]
            if result == START_PENDING:
                print("service %s is %s, please wait" % (service_name, status_code[result]))
                time.sleep(2)
                return RUNNING
            elif result == STOP_PENDING:
                print("service %s is %s, please wait" % (service_name, status_code[result]))
                time.sleep(2)
                return STOPPED
            else:
                return result if result is not None else 0
        except Exception as e:
            if e.message:
                raise RuntimeError(e.message)
            elif e.args:
                # print e.args
                args = list()
                for arg in e.args:
                    if self.is_iterable(arg):
                        args.append(eval(repr(arg)), 'gbk')
                    else:
                        args.append(arg)
                print("Error:", args[-1], tuple(args))
                raise RuntimeError
            else:
                raise RuntimeError("Uncaught exception, maybe it is a 'Access Denied'")  # will not reach here

        pass

    def start(self, name):
        status = self.get_service_status(name)
        if status == STOPPED:
            pass
        elif status == RUNNING:
            print("service %s already started" % name)
            return status

        try:
            print("starting %s" % name)
            win32serviceutil.StartService(name)
        except Exception as e:
            if e.message:
                raise RuntimeError(e.message)
            elif e.args:
                # print e.args
                args = list()
                for arg in e.args:
                    if self.is_iterable(arg):
                        args.append(eval(repr(arg), 'gbk'))
                    else:
                        args.append(arg)
                print("Error:", args[-1], tuple(args))
                raise RuntimeError
            else:
                raise RuntimeError("Uncaught exception, maybe it is a 'Access Denied'")  # will not reach here
        return self.get_service_status(name)
        pass

    def stop(self, name):
        status = self.get_service_status(name)
        if status == STOPPED:
            print("service %s already stopped" % name)
            return status
        elif status == RUNNING:
            pass
        else:
            return status
        try:
            print("stopping %s" % name)
            win32serviceutil.StopService(name)
        except Exception as e:
            if e.message:
                print(e.message)
            elif e.args:
                # print e.args
                args = list()
                for arg in e.args:
                    if self.is_iterable(arg):
                        args.append(eval(repr(arg)), 'gbk')
                    else:
                        args.append(arg)
                print("Error:", args[-1], tuple(args))
                raise RuntimeError
            else:
                raise RuntimeError("Uncaught exception, maybe it is a 'Access Denied'")  # will not reach here
        return self.get_service_status(name)
        pass

    def restart(self, name):
        pass


if __name__ == "__main__":
    print(WinService().start("AUService"))