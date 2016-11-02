class Status:
    nothing = 'nothing'
    matched = 'matched'
    reboot = 'reboot'
    done = 'done'

    @staticmethod
    def is_status_valid(status):
        result = True
        if status != Status.nothing and \
            status != Status.matched and \
                status != Status.done and \
                status != Status.reboot:
            result = False
        return result
