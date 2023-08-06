#!/usr/bin/python


from Crypto.Util import asn1
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_OAEP
from clint.textui import progress

import requests
import base64
from itertools import chain

from . import googleplay_pb2, config, utils

ssl_verify = True


class LoginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RequestError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GooglePlayAPI(object):
    """Google Play Unofficial API Class

    Usual APIs methods are login(), search(), details(), bulkDetails(),
    download(), browse(), reviews() and list()."""

    BASE = "https://android.clients.google.com/"
    FDFE = BASE + "fdfe/"
    UPLOADURL = FDFE + "uploadDeviceConfig"
    SEARCHURL = FDFE + "search"
    CHECKINURL = BASE + "checkin"
    AUTHURL = BASE + "auth"

    def __init__(self, debug=False, device_codename='bacon'):
        self.authSubToken = None
        self.gsfId = None
        self.debug = debug
        self.deviceBuilder = config.DeviceBuilder(device_codename)

    def encrypt_password(self, login, passwd):
        """Encrypt the password using the google publickey, using
        the RSA encryption algorithm"""

        binaryKey = base64.b64decode(config.GOOGLE_PUBKEY)
        i = utils.readInt(binaryKey, 0)
        modulus = utils.toBigInt(binaryKey[4:][0:i])
        j = utils.readInt(binaryKey, i+4)
        exponent = utils.toBigInt(binaryKey[i+8:][0:j])

        seq = asn1.DerSequence()
        seq.append(modulus)
        seq.append(exponent)

        publicKey = RSA.importKey(seq.encode())
        cipher = PKCS1_OAEP.new(publicKey)
        combined = login.encode() + b'\x00' + passwd.encode()
        encrypted = cipher.encrypt(combined)
        h = b'\x00' + SHA.new(binaryKey).digest()[0:4]
        return base64.urlsafe_b64encode(h + encrypted)

    def setAuthSubToken(self, authSubToken):
        self.authSubToken = authSubToken

        # put your auth token in config.py to avoid multiple login requests
        if self.debug:
            print("authSubToken: " + authSubToken)

    def getDefaultHeaders(self):
        """Return the default set of request headers, which
        can later be updated, based on the request type"""

        headers = {
            "Accept-Language": self.deviceBuilder.locale.replace('_', '-'),
            "X-DFE-Encoded-Targets": config.DFE_TARGETS,
            "User-Agent": self.deviceBuilder.getUserAgent()
        }
        if self.gsfId is not None:
            headers["X-DFE-Device-Id"] = "{0:x}".format(self.gsfId)
        if self.authSubToken is not None:
            headers["Authorization"] = "GoogleLogin auth=%s" % self.authSubToken
        return headers

    def checkin(self, email, ac2dmToken):
        headers = self.getDefaultHeaders()
        headers["Content-Type"] = "application/x-protobuffer"

        request = self.deviceBuilder.getAndroidCheckinRequest()

        stringRequest = request.SerializeToString()
        res = requests.post(self.CHECKINURL, data=stringRequest,
                            headers=headers, verify=ssl_verify)
        response = googleplay_pb2.AndroidCheckinResponse()
        response.ParseFromString(res.content)

        # checkin again to upload gfsid
        request2 = googleplay_pb2.AndroidCheckinRequest()
        request2.CopyFrom(request)
        request2.id = response.androidId
        request2.securityToken = response.securityToken
        request2.accountCookie.append("[" + email + "]")
        request2.accountCookie.append(ac2dmToken)
        stringRequest = request2.SerializeToString()
        requests.post(self.CHECKINURL, data=stringRequest,
                      headers=headers, verify=ssl_verify)

        return response.androidId

    def uploadDeviceConfig(self):
        """Upload the device configuration defined in the file
        *device.properties* to the google account. Default device is a Google Nexus 6P"""

        upload = googleplay_pb2.UploadDeviceConfigRequest()
        upload.deviceConfiguration.CopyFrom(self.deviceBuilder.getDeviceConfig())
        headers = self.getDefaultHeaders()
        headers["X-DFE-Enabled-Experiments"] = "cl:billing.select_add_instrument_by_default"
        headers["X-DFE-Unsupported-Experiments"] = "nocache:billing.use_charging_poller,market_emails,buyer_currency,prod_baseline,checkin.set_asset_paid_app_field,shekel_test,content_ratings,buyer_currency_in_app,nocache:encrypted_apk,recent_changes"
        headers["X-DFE-Client-Id"] = "am-android-google"
        headers["X-DFE-SmallestScreenWidthDp"] = "320"
        headers["X-DFE-Filter-Level"] = "3"
        stringRequest = upload.SerializeToString()
        res = requests.post(self.UPLOADURL, data=stringRequest,
                            headers=headers, verify=ssl_verify)
        googleplay_pb2.ResponseWrapper.FromString(res.content)

    def login(self, email=None, password=None, gsfId=None, authSubToken=None):
        """Login to your Google Account.
        For first time login you should provide:
            * email
            * password
        For the following logins you need to provide:
            * gsfId
            * authSubToken"""
        if email is not None and password is not None:
            # First time setup, where we obtain an ac2dm token and
            # upload device information

            encryptedPass = self.encrypt_password(email, password).decode('utf-8')
            # AC2DM token
            params = self.deviceBuilder.getLoginParams(email, encryptedPass)
            response = requests.post(self.AUTHURL, data=params, verify=ssl_verify)
            data = response.text.split()
            params = {}
            for d in data:
                if "=" not in d:
                    continue
                k, v = d.split("=")[0:2]
                params[k.strip().lower()] = v.strip()
            if "auth" in params:
                ac2dmToken = params["auth"]
            elif "error" in params:
                if "NeedsBrowser" in params["error"]:
                    raise LoginError("Security check is needed, try to visit "
                                     "https://accounts.google.com/b/0/DisplayUnlockCaptcha "
                                     "to unlock, or setup an app-specific password")
                raise LoginError("server says: " + params["error"])
            else:
                raise LoginError("Auth token not found.")

            self.gsfId = self.checkin(email, ac2dmToken)
            if self.debug:
                print("Google Services Framework Id: %s" % "{0:x}".format(self.gsfId))
            self.getAuthSubToken(email, encryptedPass)
            if self.debug:
                print("Uploading device configuration")
            self.uploadDeviceConfig()
        elif gsfId is not None and authSubToken is not None:
            # no need to initialize API
            self.gsfId = gsfId
            self.setAuthSubToken(authSubToken)
            # check if token is valid with a simple search
            self.search('firefox', 1, None)
        else:
            raise LoginError('Either (email,pass) or (gsfId, authSubToken) is needed')

    def getAuthSubToken(self, email, passwd):
        params = self.deviceBuilder.getAuthParams(email, passwd)
        response = requests.post(self.AUTHURL, data=params, verify=ssl_verify)
        data = response.text.split()
        params = {}
        for d in data:
            if "=" not in d:
                continue
            k, v = d.split("=")[0:2]
            params[k.strip().lower()] = v.strip()
        if "auth" in params:
            self.setAuthSubToken(params["auth"])
        elif "error" in params:
            raise LoginError("server says: " + params["error"])
        else:
            raise LoginError("Auth token not found.")

    def _check_response_integrity(self, apps):
        if any([a['docId'] == '' for a in apps]):
            raise LoginError('Unexpected behaviour, probably expired '
                             'token')

    def executeRequestApi2(self, path, datapost=None,
                           post_content_type="application/x-www-form-urlencoded; charset=UTF-8"):
        if self.authSubToken is None:
            raise Exception("You need to login before executing any request")
        headers = self.getDefaultHeaders()

        if datapost is not None:
            headers["Content-Type"] = post_content_type

        url = self.FDFE + path
        if datapost is not None:
            response = requests.post(url, data=str(datapost),
                                     headers=headers, verify=ssl_verify,
                                     timeout=60)
        else:
            response = requests.get(url, headers=headers,
                                    verify=ssl_verify,
                                    timeout=60)

        message = googleplay_pb2.ResponseWrapper.FromString(response.content)
        if message.commands.displayErrorMessage != "":
            raise RequestError(message.commands.displayErrorMessage)

        return message

    def search(self, query, nb_result, offset=None):
        """ Search the play store for an app.

        nb_result is the maximum number of result to be returned.

        offset is used to take result starting from an index.
        """
        if self.authSubToken is None:
            raise Exception("You need to login before executing any request")

        remaining = nb_result
        output = []

        nextPath = "search?c=3&q=%s" % requests.utils.quote(query)
        if (offset is not None):
            nextPath += "&o=%d" % int(offset)
        while remaining > 0 and nextPath is not None:
            currentPath = nextPath
            data = self.executeRequestApi2(currentPath)
            if len(data.preFetch) > 0:
                response = data.preFetch[0].response
            else:
                response = data
            if response.payload.HasField('searchResponse'):
                # we still need to fetch the first page, so go to
                # next loop iteration without decrementing counter
                nextPath = response.payload.searchResponse.nextPageUrl
                continue

            if len(response.payload.listResponse.cluster) == 0:
                # strange behaviour, probably due to
                # expired token
                raise LoginError('Unexpected behaviour, probably expired '
                                 'token')
            cluster = response.payload.listResponse.cluster[0]
            if cluster.doc[0].containerMetadata.nextPageUrl != "":
                nextPath = cluster.doc[0].containerMetadata.nextPageUrl
            else:
                nextPath = None
            apps = list(chain.from_iterable([doc.child for doc in cluster.doc]))
            output += list(map(utils.fromDocToDictionary, apps))
            remaining -= len(apps)

        if len(output) > nb_result:
            output = output[:nb_result]

        return output

    def details(self, packageName):
        """Get app details from a package name.

        packageName is the app unique ID (usually starting with 'com.')."""
        path = "details?doc=%s" % requests.utils.quote(packageName)
        data = self.executeRequestApi2(path)
        app = utils.fromDocToDictionary(data.payload.detailsResponse.docV2)
        self._check_response_integrity([app])
        return app

    def bulkDetails(self, packageNames):
        """Get several apps details from a list of package names.

        This is much more efficient than calling N times details() since it
        requires only one request.

        packageNames is a list of app ID (usually starting with 'com.')."""

        path = "bulkDetails"
        req = googleplay_pb2.BulkDetailsRequest()
        req.docid.extend(packageNames)
        data = req.SerializeToString()
        message = self.executeRequestApi2(path,
                                          data.decode("utf-8"),
                                          "application/x-protobuf")
        response = message.payload.bulkDetailsResponse
        detailsList = [entry.doc for entry in response.entry]
        result = list(map(utils.fromDocToDictionary, detailsList))
        self._check_response_integrity(result)
        return result

    def browse(self, cat=None, subCat=None):
        """Browse categories. If neither cat nor subcat are specified,
        return a list of categories, otherwise it return a list of apps
        using cat (category ID) and subCat (subcategory ID) as filters."""
        path = "browse?c=3"
        if cat is not None:
            path += "&cat=%s" % requests.utils.quote(cat)
        if subCat is not None:
            path += "&ctr=%s" % requests.utils.quote(subCat)
        data = self.executeRequestApi2(path)
        output = []

        if cat is None and subCat is None:
            # result contains all categories available
            for cat in data.payload.browseResponse.category:
                elem = {'name': cat.name,
                        'dataUrl': cat.dataUrl,
                        'catId': cat.unknownCategoryContainer.categoryIdContainer.categoryId}
                output.append(elem)
        else:
            # result contains apps of a specific category
            # organized by sections
            for pf in data.preFetch:
                for cluster in pf.response.payload.listResponse.cluster:
                    for doc in cluster.doc:
                        apps = [a for a in doc.child]
                        apps = list(map(utils.fromDocToDictionary,
                                        apps))
                        section = {'title': doc.title,
                                   'docid': doc.docid,
                                   'apps': apps}
                        output.append(section)
        return output

    def list(self, cat, ctr=None, nb_results=None, offset=None):
        """List apps for a specfic category *cat*.

        If ctr (subcategory ID) is None, returns a list of valid subcategories.

        If ctr is provided, list apps within this subcategory."""
        path = "list?c=3&cat=%s" % requests.utils.quote(cat)
        if ctr is not None:
            path += "&ctr=%s" % requests.utils.quote(ctr)
        if nb_results is not None:
            path += "&n=%s" % requests.utils.quote(nb_results)
        if offset is not None:
            path += "&o=%s" % requests.utils.quote(offset)
        data = self.executeRequestApi2(path)
        output = []
        if ctr is None:
            # list subcategories
            for pf in data.preFetch:
                for cluster in pf.response.payload.listResponse.cluster:
                    for doc in cluster.doc:
                        output.append(doc.docid)
        else:
            # list apps for specific subcat
            for cluster in data.payload.listResponse.cluster:
                for doc in cluster.doc:
                    apps = [a for a in doc.child]
                    apps = list(map(utils.fromDocToDictionary,
                                    apps))
                    output += apps
        return output

    def reviews(self, packageName, filterByDevice=False, sort=2,
                nb_results=None, offset=None):
        """Browse reviews for an application

        Args:
            packageName (str): app unique ID.
            filterByDevice (bool): filter results for current device
            sort (int): sorting criteria (values are unknown)
            nb_results (int): max number of reviews to return
            offset (int): return reviews starting from an offset value

        Returns:
            dict object containing all the protobuf data returned from
            the api
        """
        path = "rev?doc=%s&sort=%d" % (requests.utils.quote(packageName), sort)
        if (nb_results is not None):
            path += "&n=%d" % int(nb_results)
        if (offset is not None):
            path += "&o=%d" % int(offset)
        if(filterByDevice):
            path += "&dfil=1"
        data = self.executeRequestApi2(path)
        output = []
        for rev in data.payload.reviewResponse.getResponse.review:
            author = {'personIdString': rev.author2.personIdString,
                      'personId': rev.author2.personId,
                      'name': rev.author2.name,
                      'profilePicUrl': rev.author2.urls.url,
                      'googlePlusUrl': rev.author2.googlePlusUrl}
            review = {'documentVersion': rev.documentVersion,
                      'timestampMsec': rev.timestampMsec,
                      'starRating': rev.starRating,
                      'comment': rev.comment,
                      'commentId': rev.commentId,
                      'author': author}
            output.append(review)
        return output

    def _deliver_data(self, url, cookies, progress_bar):
        headers = self.getDefaultHeaders()
        if not progress_bar:
                return requests.get(url, headers=headers,
                                    cookies=cookies, verify=ssl_verify,
                                    timeout=60).content
        response_content = bytes()
        response = requests.get(url, headers=headers,
                                cookies=cookies, verify=ssl_verify,
                                stream=True, timeout=60)
        total_length = int(response.headers.get('content-length'))
        chunk_size = 32 * (1 << 10)  # 32 KB
        bar = progress.Bar(expected_size=(total_length >> 10))
        for index, chunk in enumerate(response.iter_content(chunk_size=chunk_size)):
            response_content += chunk
            bar.show(index * chunk_size >> 10)
        bar.done()
        return response_content

    def delivery(self, packageName, versionCode, offerType=1,
                 downloadToken=None, progress_bar=False, expansion_files=False):
        """Download an already purchased app.

        Args:
            packageName (str): app unique ID (usually starting with 'com.')
            versionCode (int): version to download
            offerType (int): different type of downloads (mostly unused for apks)
            downloadToken (str): download token returned by 'purchase' API
            progress_bar (bool): wether or not to print a progress bar to stdout

        Returns:
            Dictionary containing apk data and a list of expansion files. As stated
            in android documentation, there can be at most 2 expansion files, one with
            main content, and one for patching the main content. Their names should
            follow this format:

            [main|patch].<expansion-version>.<package-name>.obb

            Data to build this name string is provided in the dict object. For more
            info check https://developer.android.com/google/play/expansion-files.html
        """
        path = "delivery"
        params = {'ot': str(offerType),
                  'doc': packageName,
                  'vc': str(versionCode)}
        headers = self.getDefaultHeaders()
        if downloadToken is not None:
            params['dtok'] = downloadToken
        url = "https://android.clients.google.com/fdfe/%s" % path
        response = requests.get(url, headers=headers,
                                params=params, verify=ssl_verify,
                                timeout=60)
        resObj = googleplay_pb2.ResponseWrapper.FromString(response.content)
        if resObj.commands.displayErrorMessage != "":
            raise RequestError(resObj.commands.displayErrorMessage)
        elif resObj.payload.deliveryResponse.appDeliveryData.downloadUrl == "":
            raise RequestError('App not purchased')
        else:
            result = {}
            result['docId'] = packageName
            result['additionalData'] = []
            downloadUrl = resObj.payload.deliveryResponse.appDeliveryData.downloadUrl
            cookie = resObj.payload.deliveryResponse.appDeliveryData.downloadAuthCookie[0]
            cookies = {
                str(cookie.name): str(cookie.value)
            }
            result['data'] = self._deliver_data(downloadUrl, cookies, progress_bar)
            if not expansion_files:
                return result
            for obb in resObj.payload.deliveryResponse.appDeliveryData.additionalFile:
                a = {}
                # fileType == 0 -> main
                # fileType == 1 -> patch
                if obb.fileType == 0:
                    obbType = 'main'
                else:
                    obbType = 'patch'
                a['type'] = obbType
                a['versionCode'] = obb.versionCode
                a['data'] = self._deliver_data(obb.downloadUrl, None, progress_bar)
                result['additionalData'].append(a)
            return result

    def download(self, packageName, versionCode, offerType=1,
                 progress_bar=False, expansion_files=False):
        """Download an app and return its raw data (APK file). Free apps need
        to be "purchased" first, in order to retrieve the download cookie.
        If you want to download an already purchased app, use *delivery* method.

        Args:
            packageName (str): app unique ID (usually starting with 'com.')
            versionCode (int): version to download
            offerType (int): different type of downloads (mostly unused for apks)
            downloadToken (str): download token returned by 'purchase' API
            progress_bar (bool): wether or not to print a progress bar to stdout

        Returns
            Dictionary containing apk data and optional expansion files
            (see *delivery*)
        """

        if self.authSubToken is None:
            raise Exception("You need to login before executing any request")

        path = "purchase"
        headers = self.getDefaultHeaders()
        params = {
            'ot': str(offerType),
            'doc': packageName,
            'vc': str(versionCode)
        }
        url = self.FDFE + path
        response = requests.post(url, headers=headers,
                                 params=params, verify=ssl_verify,
                                 timeout=60)

        resObj = googleplay_pb2.ResponseWrapper.FromString(response.content)
        if resObj.commands.displayErrorMessage != "":
            raise RequestError(resObj.commands.displayErrorMessage)
        else:
            dlToken = resObj.payload.buyResponse.downloadToken
            return self.delivery(packageName, versionCode, offerType, dlToken,
                                 progress_bar=progress_bar, expansion_files=expansion_files)

    def changeDevice(self, device_codename):
        self.deviceBuilder = config.DeviceBuilder(device_codename)

    # Helpers

    def getLocale(self):
        return self.deviceBuilder.locale

    def setLocale(self, locale):
        self.deviceBuilder.locale = locale

    def getTimeZone(self):
        return self.deviceBuilder.timezone

    def setTimeZone(self, timezone):
        self.deviceBuilder.timezone = timezone

    @staticmethod
    def getDevicesCodenames():
        return config.getDevicesCodenames()

    @staticmethod
    def getDevicesReadableNames():
        return config.getDevicesReadableNames()
