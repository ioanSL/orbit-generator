import os
import requests
from pathlib import Path


API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDc4MzZFQTgwNWVGMkE4NDdGZkNkM2ZlMTU4OTRBNj" \
          "E1OUNkMzg4MDciLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTYzNTc3MzcyMjMwNywibmFtZSI6IlRlc3RpbmcgU29sdXRpb24if" \
          "Q.sqVUUQiuWh6wF7w10kdy1dTI1QehC2HJMLlr8XATxRY"


class NFTStorage(object):
    def __init__(self, api_key):
        self._url = "https://api.nft.storage"
        self.api_key = api_key
        self.files = []

    def post_files(self, path):
        """
        Sends all files to your NFT.Storage account
        """
        header = {"Content-Type": "image/*",
                  "Authorization": "Bearer {}".format(self.api_key)}
        artifacts = {"media": 0}
        for dirpath, _, files in os.walk(path):
            for file in files:
                if "png" in file:
                    with Path(os.path.abspath(os.path.join(dirpath, file))).open("rb") as fp:
                        image_binary = fp.read()
                        response = requests.post(url="{}/upload".format(self._url), headers=header,
                                                 files={"file": (file, image_binary)})

        print(">>>", response.text)

        # response = requests.get(url="{}/".format(self._url), headers=header, files=artifacts)
        # return requests.post(url=self._url, headers=header)

    def check_file(self, cid):
        """
        Check if given cid is being stored and linked to any stored item on NFT.Storage

        :param cid: unique identifier of your file
        :return: boolean check
        """
        pass

    def get_all(self):
        """
        Request all files stored under your NFT.Storage account
        """
        pass


if __name__ == "__main__":
    NFT = NFTStorage(api_key=API_KEY)
    NFT.post_files("/home/dexter/workspace/3D-Earth-Like-Planet-Procedural-Generator/test")
