import http.client
from .luis_sdk import LUISClient as SDKClient
from .luis_sdk.luis_response import LUISResponse


class LUISClient(SDKClient):

    _TrainMask = '/luis/api/v2.0/apps/%s/versions/%s/train?subscription-key=%s'

    def __init__(self, app_id, app_key, verbose=True, staging=False):
        super(LUISClient, self).__init__(
            app_id=app_id, app_key=app_key, verbose=verbose)
        self.staging = staging

    def _predict_url_gen(self, text):
        return ''.join([
            super(LUISClient, self)._predict_url_gen(text), 
            '&staging=%s' % str(self.staging).lower()
        ])

    def _train_url_gen(self, version_id):
        return self._TrainMask % (self._app_id, version_id, self._app_key)

    def train(self, version_id):
        if version_id is None:
            raise TypeError('NULL text to predict')
        version_id = version_id.strip()
        return self.train_sync(version_id)

    def train_sync(self, version_id):
        try:
            conn = http.client.HTTPSConnection(self._LUISURL)
            conn.request('POST', self._train_url_gen(version_id))
            res = conn.getresponse()
            # [note] the LUIS train api returns HTTPResponse object, not JSONReponse object
            #        which seems inconsistent with app query API
            # [FIXME] make it consistent with other luis SDK ?
            #return LUISResponse(res.read().decode('UTF-8'))
            return res
        except Exception:
            raise
        