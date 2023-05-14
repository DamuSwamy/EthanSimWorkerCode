from st2common.runners.base_action import Action
import requests
from zipfile import ZipFile

class GetPriceListAction(Action):
    def run(self, auth_token, market, price_view, file_path):
        self.base_uri = 'https://api.partner.microsoft.com/v1.0/sales/pricesheets'
        endpoint = "{}(Market=\'{}\',PricesheetView=\'{}\')/$value?timeline=current".format(self.base_uri, market, price_view)
        headers= {
            'Content-Type': 'application/*',
            'Content-Disposition': 'attachment; filename=/tmp/price_list.csv.zip',
            'Content-Transfer-Encoding': 'application/binary',
            'Authorization': 'Bearer {}'.format(auth_token)
        }
        response = requests.request('get', endpoint, headers=headers, data={})
        print(endpoint)
        if response.status_code > 299 and response.status_code < 599:
            print("status_code: " + str(response.status_code))
            return False
        print("Downloading the file....")
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("Download completed")

        with ZipFile(file_path, 'r') as zObject:
            zObject.extract("sheets.csv", path="/home/amujawar")
        zObject.close()
        print("Zip extracted")
        return True
