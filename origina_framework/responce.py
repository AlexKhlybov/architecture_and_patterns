class Status:
    @staticmethod
    def HTTP_200_OK():
        return "200 OK"

    @staticmethod
    def HTTP_404_NOT_FOUND():
        return "404 WHAT"

    @staticmethod
    def HTTP_200_OK_FAKE():
        return "200 OK", "Hello from Fake"
