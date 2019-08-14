class Update:

    def __init__(self):
        self.update = {
            "ok": True
        }
        self.result = []
        self.first_update = True

        try:
            with open(".last_update.id", "r") as f:
                self.last_update_id = int(f.read())
        except:
            with open(".last_update.id", "w+") as f:
                self.last_update_id = 141384202
                f.write(str(141384202))

    def sendUpdate(self):
        self.update['result'] = self.result
        return self.update

    def appendMessageToResult(self, message):
        self.result.append({
            "update_id": self.last_update_id,
            "message": message
        })

        self.last_update_id += 1
        with open(".last_update.id", "w+") as f:
            f.write(str(self.last_update_id))


    def appendQueryCallbackToResult(self, message):
        self.result.append({
            "update_id": self.last_update_id,
            "callback_query": message
        })

        self.last_update_id += 1
        with open(".last_update.id", "w+") as f:
            f.write(str(self.last_update_id))

    def flushResult(self):
        self.update['result'].clear()

    def popResults(self):
        if len(self.update['result']) > 0:
            self.update['result'].pop()